"""Apply a saved Chromagnon correction to other images (Phase 2).

The chromatic-shift analysis (``chromatic_shift.py``) measures the chromatic
shift of a reference sample and saves it as a Chromagnon correction file:
``.chromagnon.csv`` for a global (affine) correction, ``.chromagnon.tif`` when a
local (non-linear) distortion map is included. Files made by the desktop
Chromagnon have the same format.

This module re-applies such a file to other images. It does not depend on OMERO:
images are microscope-metrics ``Image`` objects (TZYXC ``array_data``) and the
correction is a file on disk.

Chromagnon matches the channels of the correction and of the target image by
their wavelength (rounded to an integer). Images without usable emission
wavelengths use the channel numbers 0, 1, 2, ... (see
``chromatic_shift._channel_waves``). When the channels do not match, Chromagnon
would open a GUI message box, which cannot work on a server, so the
compatibility is checked here first (:func:`check_compatibility`) and an image
that does not match is not corrected.
"""

import numpy as np
from microscopemetrics_schema import datamodel as mm_schema

import microscopemetrics as mm
from microscopemetrics.analyses import chromatic_shift

# File-name endings of Chromagnon correction files.
CORRECTION_SUFFIXES = (".chromagnon.csv", ".chromagnon.tif")


def is_correction_filename(name: str) -> bool:
    """Whether ``name`` looks like a Chromagnon correction file."""
    return bool(name) and name.lower().endswith(CORRECTION_SUFFIXES)


def read_correction_info(path: str) -> dict:
    """Read the header of a Chromagnon correction file.

    Returns a dict with:
    - ``local``: True for a .chromagnon.tif with a local distortion map
    - ``nt``, ``nw``: number of time points and channels
    - ``waves``: channel wavelengths (int, nm, or channel numbers)
    - ``reference_wave``: wavelength of the reference channel
    - ``pixel_size_zyx``: pixel size (micron) of the measured image
    - ``ny``, ``nx``: YX size of the distortion map (local only, else None)
    """
    _, imgio = chromatic_shift._import_chromagnon()
    from Chromagnon import chromformat

    reader = chromformat.ChromagnonReader(path)
    try:
        local = not reader.text
        return {
            "local": local,
            "nt": int(reader.nt),
            "nw": int(reader.nw),
            "waves": [int(round(float(w))) for w in list(reader.wave)[: reader.nw]],
            "reference_wave": int(round(float(reader.refwave))),
            "pixel_size_zyx": [float(p) for p in reader.pxlsiz],
            "ny": int(reader.ny) if local else None,
            "nx": int(reader.nx) if local else None,
        }
    finally:
        reader.close()


def image_waves(image: mm_schema.Image) -> list:
    """Channel wavelengths of ``image`` as Chromagnon will see them (int)."""
    return [int(round(w)) for w in chromatic_shift._channel_waves(image)]


def check_compatibility(info: dict, image: mm_schema.Image) -> list:
    """Return the reasons why the correction cannot be applied to ``image``.

    An empty list means the correction can be applied. ``image`` needs its
    shape and channels, not its pixel data.
    """
    reasons = []

    waves = image_waves(image)
    if len(waves) != info["nw"] or sorted(waves) != sorted(info["waves"]):
        reasons.append(
            f"Channel wavelengths do not match: correction {info['waves']}, "
            f"image {waves}."
        )

    nt = image.shape_t or 1
    if info["nt"] not in (1, nt):
        reasons.append(
            f"Number of time points does not match: correction {info['nt']}, "
            f"image {nt}."
        )

    if info["local"] and (info["ny"], info["nx"]) != (image.shape_y, image.shape_x):
        reasons.append(
            "Image size does not match the local distortion map: correction "
            f"{info['ny']}x{info['nx']} (YX), image {image.shape_y}x{image.shape_x}."
        )

    return reasons


def apply_correction(image: mm_schema.Image, correction_path: str) -> np.ndarray:
    """Apply a Chromagnon correction file to ``image``.

    ``image.array_data`` must be loaded (TZYXC). Returns the corrected TZYXC
    array with the same shape and dtype as the input. Raises
    ``mm.AnalysisError`` when the correction does not fit the image.
    """
    info = read_correction_info(correction_path)
    reasons = check_compatibility(info, image)
    if reasons:
        raise mm.AnalysisError(
            message=f"The correction cannot be applied to {image.name}.",
            suggestion=" ".join(reasons),
        )

    ch_aligner, imgio = chromatic_shift._import_chromagnon()
    reader = chromatic_shift._build_reader(image, imgio)

    an = ch_aligner.Chromagnon(reader)
    try:
        corrected = _apply_loaded(an, reader, info, correction_path)
    finally:
        an.close()

    # Same as the analysis: Chromagnon returns floats, keep the input pixel type.
    input_dtype = image.array_data.dtype
    if np.issubdtype(input_dtype, np.integer):
        info_dtype = np.iinfo(input_dtype)
        corrected = np.clip(np.rint(corrected), info_dtype.min, info_dtype.max)
    return corrected.astype(input_dtype, copy=False)


def _apply_loaded(an, reader, info: dict, correction_path: str) -> np.ndarray:
    """Load ``correction_path`` into ``an`` and return the corrected TZYXC floats."""
    an.setEchofunc(chromatic_shift._ECHO_FUNC)
    an.loadParm(correction_path)

    nt = reader.nt
    has_local = an.mapyx is not None
    if has_local and info["nt"] == 1 and nt > 1:
        # Chromagnon expands the affine parameters of a single time point to all
        # time points (setAlignParam), but fills the distortion map only for the
        # time points present in the file. Use the same map for every time point.
        an.mapyx[1:] = an.mapyx[0]

    frames = []
    for t in range(nt):
        channels = []
        for w in range(reader.nw):
            if has_local:
                arr = an.get3DArrayRemapped(w=w, t=t)
            else:
                arr = an.get3DArrayAligned(w=w, t=t)
            channels.append(np.asarray(arr))
        frames.append(np.stack(channels, axis=-1))  # ZYXC
    return np.stack(frames, axis=0)  # TZYXC


def _section_aligner(image: mm_schema.Image, planes_cyx: np.ndarray, correction_path: str):
    """Chromagnon object for one section (1 Z plane per channel) with the
    correction loaded. ``image`` gives the channels and pixel size."""
    ch_aligner, imgio = chromatic_shift._import_chromagnon()
    arr = np.asarray(planes_cyx, dtype=np.float32)[None, :, None]  # (t, w, z, y, x)
    reader = imgio.Reader(np.ascontiguousarray(arr))
    reader.setPixelSize(
        pz=image.voxel_size_z_micron or 1.0,
        py=image.voxel_size_y_micron or 1.0,
        px=image.voxel_size_x_micron or 1.0,
    )
    reader.wave = chromatic_shift._channel_waves(image)
    an = ch_aligner.Chromagnon(reader)
    an.setEchofunc(chromatic_shift._ECHO_FUNC)
    an.loadParm(correction_path)
    return an


def section_sources(image: mm_schema.Image, correction_path: str, z: int) -> list:
    """For each channel, the input Z plane that the correction moves to plane ``z``.

    Chromagnon corrects Z by resampling along Z (translation tz and
    magnification mz about the stack centre, see Priithon
    ``imgResample.trans3D_affine``). For display, the nearest input plane is used
    instead of interpolating. tz and mz are read from the file (a Chromagnon
    object built on a single section drops the Z terms); tz is rescaled to the
    image's Z pixel size like Chromagnon does (``dratio``).
    """
    _, imgio = chromatic_shift._import_chromagnon()
    from Chromagnon import chromformat

    reader = chromformat.ChromagnonReader(correction_path)
    try:
        parms = np.asarray(reader.alignParms[0], dtype=float)  # (nw, 7)
        file_waves = [int(round(float(w))) for w in list(reader.wave)[: reader.nw]]
        file_pz = float(reader.pxlsiz[0])
    finally:
        reader.close()
    image_pz = image.voxel_size_z_micron or file_pz
    dratio_z = file_pz / image_pz if image_pz else 1.0

    nz = int(image.shape_z or 1)
    cz = nz / 2.0 - 0.5
    sources = []
    for wave in image_waves(image):
        if wave in file_waves:
            tz, mz = parms[file_waves.index(wave), 0], parms[file_waves.index(wave), 4]
        else:
            tz, mz = 0.0, 1.0
        z_in = (z - cz) / (mz or 1.0) + cz - tz * dratio_z
        sources.append(int(np.clip(round(z_in), 0, nz - 1)))
    return sources


def correct_section(
    image: mm_schema.Image, planes_cyx: np.ndarray, correction_path: str
) -> np.ndarray:
    """Apply the in-plane (YX) part of a correction to one section.

    ``planes_cyx`` holds one plane per channel (e.g. a Z projection, or the
    planes given by :func:`section_sources`). The YX translation, rotation and
    magnification, and the local distortion map if the file has one, are
    applied; the Z terms are dropped (already handled by the choice of planes).
    Only a 2D resampling per channel, so it is fast enough for interactive
    display. Returns float32 (c, y, x).
    """
    info = read_correction_info(correction_path)
    reasons = check_compatibility(info, image)
    if reasons:
        raise mm.AnalysisError(
            message=f"The correction cannot be applied to {image.name}.",
            suggestion=" ".join(reasons),
        )
    an = _section_aligner(image, planes_cyx, correction_path)
    try:
        an.alignParms[..., 0] = 0.0  # tz
        an.alignParms[..., 4] = 1.0  # mz
        has_local = an.mapyx is not None
        out = []
        for w in range(len(planes_cyx)):
            arr = (
                an.get3DArrayRemapped(w=w, t=0)
                if has_local
                else an.get3DArrayAligned(w=w, t=0)
            )
            out.append(np.asarray(arr, dtype=np.float32).reshape(arr.shape[-2:]))
        return np.stack(out)
    finally:
        an.close()


def correction_label(info: dict) -> str:
    """Short human-readable summary of a correction file header."""
    kind = "local + global" if info["local"] else "global"
    text = (
        f"{kind}; {info['nw']} channels {info['waves']} "
        f"(reference {info['reference_wave']}); "
        f"pixel size ZYX {', '.join(f'{p:g}' for p in info['pixel_size_zyx'])} um"
    )
    if info["nt"] > 1:
        text += f"; {info['nt']} time points"
    if info["local"]:
        text += f"; map {info['ny']}x{info['nx']} (YX)"
    return text


__all__ = [
    "CORRECTION_SUFFIXES",
    "is_correction_filename",
    "read_correction_info",
    "image_waves",
    "check_compatibility",
    "apply_correction",
    "section_sources",
    "correct_section",
    "correction_label",
]
