"""Chromatic-shift analysis.

Measures (and optionally corrects) the 3D chromatic shift between the channels of
a multi-channel image using the Chromagnon algorithm
(Matsuda et al. 2018, Sci Rep 8:7583 - fiducial-marker-free registration).

Only the *compute core* of Chromagnon is used here. File I/O and the GUI of the
original Chromagnon distribution are intentionally bypassed: images come in as
microscope-metrics ``Image`` objects (TZYXC numpy arrays) and results go out as
microscope-metrics schema objects. OMERO-metrics is responsible for loading the
images and for persisting the results.
"""

import os
from datetime import datetime
from typing import Optional

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

import microscopemetrics as mm
from microscopemetrics.analyses import analysis_tools as mm_analysis_tools
from microscopemetrics.analyses import schema_tools as mm_schema_tools

# The per-(time, wave) alignment parameters produced by Chromagnon, in order.
# Mirror of ``Chromagnon.aligner.ZYXRM_ENTRY``.
ZYXRM_ENTRY = ["tz", "ty", "tx", "r", "mz", "my", "mx"]

# Suffix added to the corrected image name (Chromagnon convention). The original
# file extension is replaced by ALIGNED_EXT, since the corrected image is not saved
# in the original format: e.g. "cs_test.nd2" -> "cs_test_ALN.tif".
ALIGNED_SUFFIX = "_ALN"
ALIGNED_EXT = ".tif"

# Fixed tolerated fraction of saturated pixels before a channel is flagged.
SATURATION_THRESHOLD = 0.01

# Optional progress hook. Chromagnon's aligner reports human-readable progress via
# an "echo" callback (see Chromagnon.aligner.setEchofunc). A caller (e.g.
# OMERO-metrics) can install a sink here to surface that progress live; when unset,
# Chromagnon falls back to printing to stdout. The hook is a module-level global so
# it can be wired in without changing the generic ``analyse_*(dataset)`` signature.
# Sync-worker safe: each analysis runs in its own process, so the global is not
# shared across concurrent runs.
_ECHO_FUNC = None


def set_echo_func(func=None) -> None:
    """Install (or clear, with ``None``) the Chromagnon progress echo sink.

    ``func`` is called by Chromagnon as ``func(msg: str, **kwargs)``.
    """
    global _ECHO_FUNC
    _ECHO_FUNC = func


def aligned_image_name(name: str) -> str:
    """Return the corrected-image name: "<root>_ALN.tif" for "<root>.<ext>"."""
    root = os.path.splitext(name or "image")[0]
    return f"{root}{ALIGNED_SUFFIX}{ALIGNED_EXT}"


def _save_correction_bytes(an):
    """Save the Chromagnon correction (params + optional local map) to bytes.

    Uses Chromagnon's own ``saveParm`` (writes a .chromagnon.csv when there is no
    local map, a .chromagnon.tif when there is), which can be re-loaded later via
    ``loadParm`` to apply the same correction to other images.

    Returns (bytes, filename). The correction file is one of the outputs, so a
    failure raises AnalysisError instead of returning a result without it.
    """
    import shutil
    import tempfile

    outdir = tempfile.mkdtemp(prefix="chromagnon_")
    try:
        an.outdir = outdir
        fn = an.saveParm()
        with open(fn, "rb") as fh:
            return fh.read(), os.path.basename(fn)
    except Exception as e:
        raise mm.AnalysisError(
            message=f"Could not save the Chromagnon correction file: {e}",
            suggestion="Check that tifffile is installed (needed for local alignment).",
        ) from e
    finally:
        shutil.rmtree(outdir, ignore_errors=True)


def _combine_images(images: list) -> mm_schema.Image:
    """Combine several images into one high-SNR image for a shared correction.

    Per-pixel maximum across the dataset images (Chromagnon's "average references").
    All images must share the same shape. The outputs of the combined image are
    linked to the first image so they attach to a real OMERO object.
    """
    arrays = [img.array_data for img in images]
    shapes = {a.shape for a in arrays}
    if len(shapes) != 1:
        raise mm.DataFormatError(
            "average_references requires all images to have the same shape; "
            f"got {sorted(shapes)}."
        )
    # The images are combined pixel by pixel, so their channels and pixel sizes
    # must match too (as when Chromagnon averages reference files).
    first = images[0]
    for img in images[1:]:
        if _channel_waves(img) != _channel_waves(first):
            raise mm.DataFormatError(
                "average_references requires the same channels (emission "
                f"wavelengths) in all images; {img.name} differs from {first.name}."
            )
        for axis in ("z", "y", "x"):
            a = getattr(img, f"voxel_size_{axis}_micron")
            b = getattr(first, f"voxel_size_{axis}_micron")
            if a and b and not np.isclose(a, b, rtol=1e-3):
                raise mm.DataFormatError(
                    "average_references requires the same pixel size in all "
                    f"images; {img.name} differs from {first.name} in {axis}."
                )
    # Per-pixel maximum, as Chromagnon does (alignfuncs.averageImage): the beads
    # of all images end up in one image without being dimmed by the others.
    combined = np.maximum.reduce(arrays)
    # Strip the extension first, so that the name does not end in a pseudo
    # extension (".dv_combined_reference") that aligned_image_name would drop.
    root = os.path.splitext(first.name or "image")[0]
    combined_image = mm_schema_tools.numpy_to_mm_image(
        array=combined,
        name=f"{root}_combined_reference",
        description="Per-pixel maximum across the dataset images (averaged references).",
        source_images=images,
        channel_names=[c.name for c in first.channel_series.channels],
    )
    # Attach the combined image's outputs (ROIs, corrected image) to the first
    # real OMERO image so they can be dumped.
    combined_image.data_reference = first.data_reference
    combined_image.voxel_size_z_micron = first.voxel_size_z_micron
    combined_image.voxel_size_y_micron = first.voxel_size_y_micron
    combined_image.voxel_size_x_micron = first.voxel_size_x_micron
    # Keep the channel wavelengths: Chromagnon identifies the channels by them and
    # writes them to the correction file. Without them _channel_waves falls back
    # to synthetic values (500, 520, ...), and the saved correction would not match
    # the wavelengths of the images it is later applied to.
    for c_comb, c_first in zip(
        combined_image.channel_series.channels, first.channel_series.channels
    ):
        c_comb.excitation_wavelength_nm = c_first.excitation_wavelength_nm
        c_comb.emission_wavelength_nm = c_first.emission_wavelength_nm
    return combined_image


def _import_chromagnon():
    """Lazily import the Chromagnon compute core and the imgio array reader.

    These are optional, heavy dependencies, so we import them only when the
    analysis is actually run and raise a helpful error otherwise.
    """
    try:
        from Chromagnon import aligner as ch_aligner
        from Priithon import imgio  # imgio lives inside Priithon since 2026-11
    except ImportError as e:
        raise mm.AnalysisError(
            message=(
                "The Chromagnon compute core could not be imported. "
                "Make sure that the 'Chromagnon' and 'Priithon' packages are "
                "installed (pip) or that their 'src' folders are on the PYTHONPATH."
            ),
            suggestion=str(e),
        ) from e
    return ch_aligner, imgio


def _channel_waves(image: mm_schema.Image) -> list:
    """Return a list of distinct 'wavelengths' for the channels of an image.

    Chromagnon identifies channels by wavelength and refuses to run if two
    channels share the same wavelength. We use the emission wavelengths when they
    are all present and distinct. Otherwise we follow the Chromagnon/Priithon
    convention for files without wavelengths in the header and use the channel
    numbers 0, 1, 2, ... (Priithon.imgio.generalIO.makeWaves, WAVE_START=0,
    WAVE_STEP=1). Reader.getWaveIdx also accepts a channel index in place of a
    wavelength, so a correction saved this way can be applied by channel number.
    """
    channels = image.channel_series.channels
    emissions = [c.emission_wavelength_nm for c in channels]

    if all(e is not None for e in emissions) and len(set(emissions)) == len(emissions):
            return [float(e) for e in emissions]

    # Fallback: channel numbers, as Chromagnon does when the header has no wavelengths.
    return [float(i) for i in range(len(channels))]


def _minmax_normalize(arr: np.ndarray) -> np.ndarray:
    """Min-max normalise an array to [0, 1]. Returns zeros for a flat array."""
    arr = np.asarray(arr, dtype=float)
    a_min = arr.min()
    a_max = arr.max()
    if a_max - a_min == 0:
        return np.zeros_like(arr)
    return (arr - a_min) / (a_max - a_min)


def _registration_rmse(
    corrected_channels: list[np.ndarray], reference_channel_index: int
) -> list[float]:
    """RMSE of each aligned channel against the reference channel.

    Both arrays are min-max normalised to [0, 1] first so that the RMSE reflects
    residual mis-registration rather than the difference in absolute intensity
    between fluorophores. The reference channel gets 0 by definition.
    """
    ref_norm = _minmax_normalize(corrected_channels[reference_channel_index])
    rmse = []
    for ch in corrected_channels:
        ch_norm = _minmax_normalize(ch)
        rmse.append(float(np.sqrt(np.mean(np.square(ch_norm - ref_norm)))))
    return rmse


def _channel_field_2d(mapyx_w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the (dy, dx) 2D displacement field for one channel.

    ``mapyx_w`` is either (2, ny, nx) for a 2D alignment or (nz, 2, ny, nx) for a 3D
    one; in the 3D case the field is averaged over Z to give a single 2D field.
    """
    mapyx_w = np.asarray(mapyx_w, dtype=float)
    if mapyx_w.ndim == 4:  # (nz, 2, ny, nx) -> average over Z
        mapyx_w = mapyx_w.mean(axis=0)
    # `mapyx` is the local correction field (moving -> reference). Return the
    # physical local displacement of the channel, i.e. its negative, so the quiver
    # arrows point the same way as the reported (sign-flipped) global shift.
    dy = -mapyx_w[0]
    dx = -mapyx_w[1]
    return dy, dx


def _magnitude_color(fraction: float) -> mm_schema.Color:
    """Map a 0..1 magnitude fraction to a blue(low) -> red(high) colour."""
    fraction = float(np.clip(fraction, 0.0, 1.0))
    r = int(round(255 * fraction))
    b = int(round(255 * (1.0 - fraction)))
    return mm_schema.Color(r=r, g=0, b=b, alpha=200)


def _build_distortion_outputs(
    image: mm_schema.Image,
    image_id: str,
    mapyx: np.ndarray,
    reference_channel_index: int,
    sampling: int,
) -> tuple[list[mm_schema.Image], list[mm_schema.Roi]]:
    """Build the per-channel magnitude heatmaps and quiver ROIs from ``mapyx``.

    Returns (magnitude_images, vector_rois) for every non-reference channel.
    """
    channels = image.channel_series.channels
    n_channels = len(channels)
    z_center = (image.shape_z or 1) // 2

    magnitude_images = []
    vector_rois = []

    for w in range(n_channels):
        if w == reference_channel_index:
            continue  # reference channel has a null distortion field

        dy, dx = _channel_field_2d(mapyx[w])
        magnitude = np.hypot(dy, dx)
        ny, nx = magnitude.shape

        # --- Magnitude heatmap image (full YX resolution) ---
        magnitude_image = mm_schema_tools.numpy_to_mm_image(
            array=magnitude.astype(np.float32),
            name=f"{os.path.splitext(image.name or 'image')[0]}_local_distortion_magnitude_ch{w}",
            description=(
                "Local (non-linear) distortion magnitude in pixels for channel "
                f"{channels[w].name} relative to channel {reference_channel_index}."
            ),
            channel_names=[channels[w].name],
        )
        # The magnitude is a float quantity in pixels. Give it no source image so
        # that OMERO creates it as a float image (rather than inheriting the uint16
        # source pixel type, which would truncate the sub-pixel values / fail to
        # upload). An empty list keeps the dumper from erroring on a None source.
        magnitude_image.source_images = []
        magnitude_images.append(magnitude_image)

        # --- Quiver (arrow) ROI on a down-sampled grid ---
        step = max(1, int(round(max(ny, nx) / max(2, sampling))))
        # Auto-scale so that the largest arrows are roughly one grid cell long.
        grid_mag = magnitude[step // 2 :: step, step // 2 :: step]
        max_mag = float(np.percentile(grid_mag, 95)) if grid_mag.size else 0.0
        scale = (step / max_mag) if max_mag > 0 else 1.0

        lines = []
        for gy in range(step // 2, ny, step):
            for gx in range(step // 2, nx, step):
                vy = float(dy[gy, gx])
                vx = float(dx[gy, gx])
                mag = float(np.hypot(vy, vx))
                color_fraction = (mag / max_mag) if max_mag > 0 else 0.0
                lines.append(
                    mm_schema.Line(
                        name=f"({gx},{gy})",
                        x1=float(gx),
                        y1=float(gy),
                        x2=float(gx + vx * scale),
                        y2=float(gy + vy * scale),
                        z=z_center,
                        c=w,
                        stroke_color=_magnitude_color(color_fraction),
                        stroke_width=2,
                    )
                )

        vector_rois.append(
            mm_schema.Roi(
                name=f"local_distortion_vectors_{image_id}_ch{w}",
                description=(
                    "Local distortion quiver for channel "
                    f"{channels[w].name} vs channel {reference_channel_index}. "
                    f"Arrow display scale: {scale:.1f}x (1 pixel of displacement is "
                    f"drawn as {scale:.1f} pixels). Colour: blue=small, red=large."
                ),
                linked_references=image.data_reference,
                lines=lines,
            )
        )

    return magnitude_images, vector_rois


def _build_reader(image: mm_schema.Image, imgio):
    """Wrap a microscope-metrics ``Image`` into an in-memory imgio reader.

    ``Image.array_data`` is ordered TZYXC while the imgio ``ArrayReader`` expects
    (t, w, z, y, x) == TWZYX, so the channel axis is moved next to time.
    Pixel size and channel wavelengths are set on the reader *before* it is handed
    to ``Chromagnon`` because ``Chromagnon.__init__`` reads them immediately.
    """
    # TZYXC -> TWZYX
    arr_twzyx = np.ascontiguousarray(np.transpose(image.array_data, (0, 4, 1, 2, 3)))

    reader = imgio.Reader(arr_twzyx)  # returns Priithon.imgio.arrayIO.Reader

    pz = image.voxel_size_z_micron or 1.0
    py = image.voxel_size_y_micron or 1.0
    px = image.voxel_size_x_micron or 1.0
    reader.setPixelSize(pz=pz, py=py, px=px)
    reader.wave = _channel_waves(image)

    return reader


def _run_chromagnon(
    image: mm_schema.Image,
    reference_channel_index: int,
    do_local_alignment: bool,
    max_shift_micron: float,
    phase_contrast: bool,
    ch_aligner,
    imgio,
):
    """Run Chromagnon on a single image.

    ``reference_channel_index`` < 0 means auto-select the reference channel.
    The Z alignment is always enabled for 3D data (and is a no-op for 2D).

    Returns a tuple of:
    - align_parms: numpy array of shape (n_channels, 7) with entries ZYXRM_ENTRY
    - corrected_array: TZYXC numpy array of the aligned image (all channels)
    - registration_rmse: list of per-channel RMSE against the reference channel
    - mapyx: local distortion field for t=0, or None. Shape (nw, 2, ny, nx) for a 2D
      alignment or (nw, nz, 2, ny, nx) for a 3D one.
    - reference_channel: the channel index actually used as the reference.
    """
    reader = _build_reader(image, imgio)

    # 3D data -> align in Z as well; for a single-plane image this is a no-op.
    do_z = reader.nz > 1

    an = ch_aligner.Chromagnon(reader)
    try:
        return _align_and_correct(
            an, image, reader, reference_channel_index, do_local_alignment,
            max_shift_micron, phase_contrast, do_z,
        )
    finally:
        an.close()


def _align_and_correct(
    an, image, reader, reference_channel_index, do_local_alignment,
    max_shift_micron, phase_contrast, do_z,
):
    """Body of :func:`_run_chromagnon` (``an`` is closed by the caller)."""
    # Surface Chromagnon's progress messages through the installed sink (if any).
    an.setEchofunc(_ECHO_FUNC)
    if reference_channel_index is not None and reference_channel_index >= 0:
        an.setReferenceWave(reference_channel_index)
    an.setDoZ(do_z)
    an.setphaseContrast(bool(phase_contrast))
    an.setMaxShift(max_shift_micron)

    # findBestChannel keeps an explicitly set reference wave, or auto-selects one
    # (based on wavelength/intensity) when it was left unset (auto mode).
    an.findBestChannel()
    reference_channel = int(an.refwave)

    # Establish the reference channel image and estimate the global affine
    # alignment (translation, rotation, magnification) for every channel.
    an.setRefImg()
    an.findAlignParamWave()

    has_local = False
    if do_local_alignment:
        # Always use the 2D (projection-based) local alignment, even for 3D data.
        # findNonLinear3D is section-wise and far slower. findNonLinear2D yields a
        # 2D displacement field that get3DArrayRemapped applies across Z. The 3D
        # global Z shift is still handled by setDoZ()/findAlignParamWave above.
        an.findNonLinear2D()
        has_local = True

    # (n_channels, 7) in ZYXRM_ENTRY order
    align_parms = np.array(an.alignParms[0], dtype=float)

    # The alignment is measured on the first time point. Apply it to every time
    # point, as a saved correction is (chromagnon_apply.apply_correction).
    if reader.nt > 1:
        an.alignParms[1:] = an.alignParms[0]
        if has_local and an.mapyx is not None:
            an.mapyx[1:] = an.mapyx[0]

    # Build the corrected image (all channels). an.setRegionCutOut() is not
    # called, but Chromagnon may still crop the borders.
    frames = []
    for t in range(reader.nt):
        channels = []
        for w in range(reader.nw):
            if has_local:
                aligned_zyx = an.get3DArrayRemapped(w=w, t=t)
            else:
                aligned_zyx = an.get3DArrayAligned(w=w, t=t)
            channels.append(np.asarray(aligned_zyx))
        frames.append(channels)

    # Residual mis-registration on the first time point: RMSE of each aligned
    # channel vs the reference channel actually used (also when it was chosen
    # automatically).
    registration_rmse = _registration_rmse(frames[0], reference_channel)

    # [t][c] of (z, y, x) -> TZYXC
    corrected_array = np.stack([np.stack(f, axis=-1) for f in frames], axis=0)

    # Chromagnon's remapping returns floats; cast the corrected image back to the
    # input pixel type. OMERO creates the dumped image with the source (input)
    # image's pixel type, so a float array on a uint16 source would fail to upload.
    input_dtype = image.array_data.dtype
    if np.issubdtype(input_dtype, np.integer):
        info = np.iinfo(input_dtype)
        corrected_array = np.clip(np.rint(corrected_array), info.min, info.max).astype(
            input_dtype
        )
    else:
        corrected_array = corrected_array.astype(input_dtype, copy=False)

    # Local distortion field (t=0) for the quiver / magnitude outputs.
    mapyx = np.asarray(an.mapyx[0], dtype=float) if has_local and an.mapyx is not None else None

    # Re-applicable Chromagnon correction file (params + optional local map).
    correction_bytes, correction_name = _save_correction_bytes(an)

    return (
        align_parms,
        corrected_array,
        registration_rmse,
        mapyx,
        reference_channel,
        correction_bytes,
        correction_name,
    )


def _total_deviation_micron(parms, shape_zyx, voxel_zyx) -> float:
    """Largest displacement (micron) caused by the global alignment parameters.

    ``parms`` are Chromagnon's alignParms of one channel ``[tz, ty, tx, r, mz,
    my, mx]``. The displacement is evaluated with the same coordinate transform
    that Chromagnon applies to the image (Priithon ``imgResample``: Z first,
    then YX, about the image centre). It is an affine function of the position,
    so its length is largest at one of the corners of the volume; the corners
    are checked. A single section (nz == 1) is not moved in Z
    (``alignfuncs.applyShift``).
    """
    from Priithon import imgResample

    tz, ty, tx, r, mz, my, mx = (float(p) for p in parms)
    nz, ny, nx = (int(n) for n in shape_zyx)
    if any(not v for v in voxel_zyx[1:]) or (int(shape_zyx[0]) > 1 and not voxel_zyx[0]):
        # Without the pixel size the displacement cannot be given in microns.
        return float("nan")
    voxel = np.array([v if v else np.nan for v in voxel_zyx], dtype=float)
    start = (-0.5, -0.5)  # trans3D_affine: dzyx - 0.5 (dzyx = 0)

    # YX: scipy affine_transform maps an output index o to the input index
    # invmat @ o + offset.
    inv_yx = imgResample.transformMatrix(r, np.array([my, mx]))
    off_yx = imgResample.getOffset((ny, nx), inv_yx, ty, tx, start)
    # Z: done the same way on (y, z) sections with mag (1, mz), shift (0, tz).
    inv_z = imgResample.transformMatrix(0, np.array([1.0, mz]))
    off_z = imgResample.getOffset((ny, nz), inv_z, 0, tz, start)

    largest = 0.0
    for z in (0, nz - 1):
        for y in (0, ny - 1):
            for x in (0, nx - 1):
                iy, ix = inv_yx @ np.array([y, x], dtype=float) + off_yx
                dz = 0.0
                if nz > 1:
                    dz = (inv_z @ np.array([y, z], dtype=float) + off_z)[1] - z
                d = np.array([dz, iy - y, ix - x]) * voxel
                largest = max(largest, float(np.sqrt(np.nansum(np.square(d)))))
    return largest


def _records_for_image(
    image: mm_schema.Image,
    image_id: str,
    align_parms: np.ndarray,
    registration_rmse: list[float],
    reference_channel_index: int,
) -> list[dict]:
    """Turn the raw Chromagnon parameters of one image into per-channel records."""
    channels = image.channel_series.channels
    channel_names = [c.name for c in channels]
    voxel = (
        image.voxel_size_z_micron or np.nan,
        image.voxel_size_y_micron or np.nan,
        image.voxel_size_x_micron or np.nan,
    )

    shape_zyx = (image.shape_z or 1, image.shape_y, image.shape_x)

    records = []
    for ch_nr, parms in enumerate(align_parms):
        total_deviation_micron = _total_deviation_micron(parms, shape_zyx, voxel)
        tz, ty, tx, r, mz, my, mx = parms
        # Chromagnon's alignParms describe the CORRECTION that maps the moving
        # channel onto the reference. We report the physical chromatic displacement
        # of the channel relative to the reference, i.e. the negative of the
        # correction for the (signed) translation and rotation. The magnifications
        # (mz/my/mx) are ratios about 1 and are reported as the raw correction
        # factors.
        tz, ty, tx, r = -tz, -ty, -tx, -r
        shift_z_micron = tz * voxel[0]
        shift_y_micron = ty * voxel[1]
        shift_x_micron = tx * voxel[2]

        records.append(
            {
                "image_id": image_id,
                "channel_nr": ch_nr,
                "channel_name": channel_names[ch_nr],
                "excitation_wavelength_nm": channels[ch_nr].excitation_wavelength_nm,
                "emission_wavelength_nm": channels[ch_nr].emission_wavelength_nm,
                "reference_channel_nr": reference_channel_index,
                "shift_z_pixel": float(tz),
                "shift_y_pixel": float(ty),
                "shift_x_pixel": float(tx),
                "shift_z_micron": float(shift_z_micron),
                "shift_y_micron": float(shift_y_micron),
                "shift_x_micron": float(shift_x_micron),
                "total_deviation_micron": total_deviation_micron,
                "rotation_degrees": float(r),
                "magnification_z": float(mz),
                "magnification_y": float(my),
                "magnification_x": float(mx),
                "registration_rmse": float(registration_rmse[ch_nr]),
            }
        )

    return records


def _generate_key_measurements(
    records_df: pd.DataFrame,
) -> list[mm_schema.ChromaticShiftKeyMeasurement]:
    """Aggregate per-(image, channel) records into one KeyMeasurement per channel.

    When several images are analysed together the shifts are averaged per channel.
    The full, non-aggregated values remain available in the properties table.
    """
    measurement_columns = [
        "reference_channel_nr",
        "shift_z_pixel",
        "shift_y_pixel",
        "shift_x_pixel",
        "shift_z_micron",
        "shift_y_micron",
        "shift_x_micron",
        "total_deviation_micron",
        "rotation_degrees",
        "magnification_z",
        "magnification_y",
        "magnification_x",
        "registration_rmse",
    ]

    aggregated = (
        records_df.groupby(["channel_nr", "channel_name"])[measurement_columns]
        .mean()
        .reset_index()
    )
    # reference_channel_nr is a constant per dataset; keep it integer.
    aggregated["reference_channel_nr"] = aggregated["reference_channel_nr"].round().astype(int)
    # Per-channel values that are not averaged: the wavelengths (taken from the
    # first image) and the name of the reference channel.
    first = records_df.drop_duplicates("channel_nr").set_index("channel_nr")
    names = first["channel_name"].to_dict()
    for column in ("excitation_wavelength_nm", "emission_wavelength_nm"):
        aggregated[column] = [
            None if pd.isna(v) else float(v)
            for v in aggregated["channel_nr"].map(first[column])
        ]
    aggregated["reference_channel_name"] = aggregated["reference_channel_nr"].map(names)

    return [
        mm_schema.ChromaticShiftKeyMeasurement(**km)
        for km in aggregated.to_dict(orient="records")
    ]


def analyse_chromatic_shift(dataset: mm_schema.ChromaticShiftDataset) -> bool:
    # A re-run must not leave the previous result marked as processed if it fails.
    dataset.processed = False
    dataset.output = None

    ch_aligner, imgio = _import_chromagnon()

    params = dataset.input_parameters
    reference_channel_index = params.reference_channel_index

    records = []
    corrected_images = []
    local_distortion_maps = []
    local_distortion_vectors = []
    correction_file = None
    correction_filename = None

    # "Average references": combine the dataset images into one high-SNR image and
    # compute a single shared correction from it.
    input_images = list(dataset.input_data.chromatic_shift_images)
    if params.average_references and len(input_images) > 1:
        images_to_process = [_combine_images(input_images)]
    else:
        images_to_process = input_images

    # In auto mode the reference is chosen on the first image and then used for
    # the others, so that the shifts of all images (averaged per channel in the
    # key measurements) are measured against the same channel.
    locked_reference = reference_channel_index

    for image in images_to_process:
        image_id = mm_schema_tools.get_object_id(image) or image.name
        mm.logger.info(f"Processing image {image_id}...")

        # Check image shape
        if len(image.array_data.shape) != 5:
            mm.logger.error(f"Image {image_id} must be 5D")
            raise mm.DataFormatError(
                f"Image {image_id} must be 5D (TZYXC). "
                f"{len(image.array_data.shape)}D was provided."
            )

        n_channels = image.array_data.shape[-1]
        if n_channels < 2:
            mm.logger.error(f"Image {image_id} must have at least 2 channels")
            raise mm.DataFormatError(
                f"Image {image_id} must have at least 2 channels to measure a "
                "chromatic shift."
            )
        # A negative reference_channel_index means "auto-select".
        if reference_channel_index >= n_channels:
            raise mm.DataFormatError(
                f"reference_channel_index {reference_channel_index} is out of range "
                f"for image {image_id} with {n_channels} channels."
            )

        # Check image saturation. The bit depth is inferred from the pixel dtype
        # (detector_bit_depth=None) and the saturation tolerance is fixed.
        for c in range(n_channels):
            if mm_analysis_tools.is_saturated(
                channel=image.array_data[..., c],
                threshold=SATURATION_THRESHOLD,
                detector_bit_depth=None,
            ):
                mm.logger.warning(f"Image {image_id}: channel {c} is saturated")

        (
            align_parms,
            corrected_array,
            registration_rmse,
            mapyx,
            reference_channel,
            image_correction_file,
            image_correction_filename,
        ) = _run_chromagnon(
            image=image,
            reference_channel_index=locked_reference,
            do_local_alignment=params.do_local_alignment,
            max_shift_micron=params.max_shift_micron,
            phase_contrast=params.phase_contrast,
            ch_aligner=ch_aligner,
            imgio=imgio,
        )

        if locked_reference is None or locked_reference < 0:
            locked_reference = reference_channel

        # Keep the first available correction as the dataset-level correction file.
        if correction_file is None and image_correction_file is not None:
            correction_file = image_correction_file
            base = os.path.splitext(dataset.name or image.name or "chromatic_shift")[0]
            ext = image_correction_filename.split(".", 1)[1] if (
                image_correction_filename and "." in image_correction_filename
            ) else "chromagnon.csv"
            correction_filename = f"{base}.{ext}"

        records.extend(
            _records_for_image(
                image=image,
                image_id=image_id,
                align_parms=align_parms,
                registration_rmse=registration_rmse,
                reference_channel_index=reference_channel,
            )
        )

        corrected_images.append(
            mm_schema_tools.numpy_to_mm_image(
                array=corrected_array,
                name=aligned_image_name(image.name),
                description=(
                    "Chromatic-shift corrected image. All channels aligned onto "
                    f"channel {reference_channel}."
                ),
                voxel_size_micron_z=image.voxel_size_z_micron,
                voxel_size_micron_y=image.voxel_size_y_micron,
                voxel_size_micron_x=image.voxel_size_x_micron,
                source_images=[image],
                channel_names=[c.name for c in image.channel_series.channels],
                excitation_wavelengths_nm=[
                    c.excitation_wavelength_nm for c in image.channel_series.channels
                ],
                emission_wavelengths_nm=[
                    c.emission_wavelength_nm for c in image.channel_series.channels
                ],
            )
        )

        # Local distortion outputs (magnitude heatmaps + quiver ROIs) when a local
        # (non-linear) alignment was computed.
        if mapyx is not None:
            magnitude_images, vector_rois = _build_distortion_outputs(
                image=image,
                image_id=image_id,
                mapyx=mapyx,
                reference_channel_index=reference_channel,
                sampling=params.distortion_vector_sampling,
            )
            local_distortion_maps.extend(magnitude_images)
            local_distortion_vectors.extend(vector_rois)

    if not records:
        raise mm.AnalysisError(
            message="No images were processed for chromatic shift.",
            suggestion="Provide at least one multi-channel image.",
        )

    records_df = pd.DataFrame(records)

    key_measurements = _generate_key_measurements(records_df)

    channel_shift_properties = mm_schema_tools.df_to_table(
        records_df, "channel_shift_properties"
    )

    dataset.output = mm_schema.ChromaticShiftOutput(
        processing_application=mm.__name__,
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        key_measurements=key_measurements,
        corrected_images=corrected_images,
        local_distortion_maps=local_distortion_maps,
        local_distortion_vectors=local_distortion_vectors,
        channel_shift_properties=channel_shift_properties,
        correction_file=correction_file,
        correction_filename=correction_filename,
    )

    ref_note = "auto" if reference_channel_index < 0 else "requested"
    dataset.description = (
        "Chromatic shift dataset\n"
        f"Successfully analyzed on {dataset.output.processing_datetime}.\n"
        f"Reference channel: {reference_channel} ({ref_note})\n"
        f"Images analyzed: {records_df['image_id'].nunique()}\n"
        f"Channels per image: {records_df['channel_nr'].nunique()}"
    )

    dataset.processed = True

    return True
