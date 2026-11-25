"""Chromatic shift analysis (Chromagnon) on synthetic images.

Channel 1 of a synthetic 2-channel bead volume is channel 0 shifted by a known
(dz, dy, dx). The tests check that the analysis recovers the shift, that the
correction file it saves can be applied to another image, and that images that
do not match a correction are rejected.

Chromagnon and Priithon are optional dependencies; the tests are skipped when
they are not installed.
"""

import os

import numpy as np
import pytest
from microscopemetrics_schema import datamodel as mm_schema
from scipy import ndimage

pytest.importorskip("Chromagnon")
pytest.importorskip("Priithon")

from microscopemetrics.analyses import chromagnon_apply, chromatic_shift  # noqa: E402
from microscopemetrics.analyses.schema_tools import numpy_to_mm_image  # noqa: E402

TRUE_SHIFT = (1.0, 3.0, 2.0)  # dz, dy, dx (pixels) of channel 1
WAVES = [500.0, 600.0]


def _make_image(seed, ny=128, nx=128, nt=1, waves=WAVES, name="synthetic"):
    rng = np.random.default_rng(seed)
    nz = 16
    frames = []
    for _ in range(nt):
        vol = np.zeros((nz, ny, nx), np.float32)
        for _ in range(20):
            vol[
                int(rng.integers(4, nz - 4)),
                int(rng.integers(16, ny - 16)),
                int(rng.integers(16, nx - 16)),
            ] = 1000.0
        vol = ndimage.gaussian_filter(vol, sigma=(1.2, 1.5, 1.5))
        vol += rng.normal(0.0, 1.0, vol.shape).astype(np.float32)
        vol = np.clip(vol, 0, None)
        moving = ndimage.shift(vol, shift=TRUE_SHIFT, order=1, mode="nearest")
        frames.append(np.stack([vol, moving], axis=-1))
    arr = np.stack(frames, axis=0).astype(np.uint16)  # TZYXC

    image = numpy_to_mm_image(
        array=arr,
        name=f"{name}.dv",
        channel_names=["ref", "moving"],
        emission_wavelengths_nm=waves,
    )
    image.voxel_size_z_micron = 0.20
    image.voxel_size_y_micron = 0.10
    image.voxel_size_x_micron = 0.10
    image.data_reference = mm_schema.DataReference(
        omero_object_id=1, omero_object_type="IMAGE"
    )
    return image


def _make_dataset(local, images=None, average=True):
    return mm_schema.ChromaticShiftDataset(
        name="reference_slide",
        microscope=mm_schema.Microscope(name="test_scope"),
        processed=False,
        input_data=mm_schema.ChromaticShiftInputData(
            chromatic_shift_images=images or [_make_image(seed=0, name="reference")]
        ),
        input_parameters=mm_schema.ChromaticShiftInputParameters(
            reference_channel_index=0,
            do_local_alignment=local,
            max_shift_micron=10.0,
            average_references=average,
        ),
    )


def _residual_shift(arr_tzyxc):
    from skimage.registration import phase_cross_correlation

    ref = arr_tzyxc[0, ..., 0].astype(float)
    mov = arr_tzyxc[0, ..., 1].astype(float)
    shift, _, _ = phase_cross_correlation(ref, mov, upsample_factor=10)
    return np.asarray(shift)


@pytest.fixture(scope="module")
def global_dataset():
    dataset = _make_dataset(local=False)
    chromatic_shift.analyse_chromatic_shift(dataset)
    return dataset


@pytest.fixture(scope="module")
def local_dataset():
    dataset = _make_dataset(local=True)
    chromatic_shift.analyse_chromatic_shift(dataset)
    return dataset


def _correction_path(dataset, tmp_path):
    path = os.path.join(tmp_path, dataset.output.correction_filename)
    with open(path, "wb") as fh:
        fh.write(dataset.output.correction_file)
    return path


def test_global_shift_recovered(global_dataset):
    assert global_dataset.processed
    kms = {km.channel_nr: km for km in global_dataset.output.key_measurements}
    assert set(kms) == {0, 1}
    ref, mov = kms[0], kms[1]

    # The reported shift is the displacement of the channel relative to the
    # reference, so it has the sign of the shift applied to the synthetic image.
    measured = (mov.shift_z_pixel, mov.shift_y_pixel, mov.shift_x_pixel)
    for meas, true in zip(measured, TRUE_SHIFT):
        assert abs(meas - true) <= 0.5
    assert ref.total_deviation_micron == 0.0
    assert abs(mov.magnification_x - 1.0) < 0.02
    assert abs(mov.rotation_degrees) < 1.0
    # The largest displacement includes rotation and magnification, so it is at
    # least the length of the translation.
    translation = np.linalg.norm(
        [mov.shift_z_micron, mov.shift_y_micron, mov.shift_x_micron]
    )
    assert mov.total_deviation_micron >= translation - 1e-6

    assert len(global_dataset.output.corrected_images) == 1
    assert global_dataset.output.correction_filename.endswith(".chromagnon.csv")


def test_local_outputs(local_dataset):
    output = local_dataset.output
    assert output.correction_filename.endswith(".chromagnon.tif")
    assert output.local_distortion_maps
    assert output.local_distortion_vectors


def test_total_deviation_matches_translation_without_rotation():
    # No rotation or magnification: the deviation is the translation length.
    parms = [0.8, 1.5, -2.0, 0.0, 1.0, 1.0, 1.0]
    voxel = (0.2, 0.1, 0.1)
    expected = np.linalg.norm(np.array(parms[:3]) * voxel)
    assert chromatic_shift._total_deviation_micron(
        parms, (16, 128, 160), voxel
    ) == pytest.approx(expected)


@pytest.mark.parametrize("dataset_name", ["global_dataset", "local_dataset"])
def test_apply_correction(dataset_name, request, tmp_path):
    dataset = request.getfixturevalue(dataset_name)
    path = _correction_path(dataset, tmp_path)
    info = chromagnon_apply.read_correction_info(path)
    assert info["waves"] == [500, 600]

    target = _make_image(seed=1, name="target")
    assert chromagnon_apply.check_compatibility(info, target) == []
    before = _residual_shift(target.array_data)
    corrected = chromagnon_apply.apply_correction(target, path)
    assert corrected.shape == target.array_data.shape
    assert corrected.dtype == target.array_data.dtype
    assert np.all(np.abs(before) > 0.5)
    assert np.all(np.abs(_residual_shift(corrected)) < 0.5)

    # A single-time-point correction applies to every time point.
    target_t = _make_image(seed=2, nt=2, name="target_t")
    corrected_t = chromagnon_apply.apply_correction(target_t, path)
    assert np.all(np.abs(_residual_shift(corrected_t[1:])) < 0.5)


@pytest.mark.parametrize("dataset_name", ["global_dataset", "local_dataset"])
def test_correct_section(dataset_name, request, tmp_path):
    dataset = request.getfixturevalue(dataset_name)
    path = _correction_path(dataset, tmp_path)
    target = _make_image(seed=1, name="target")
    full = chromagnon_apply.apply_correction(target, path).astype(float)
    arr = target.array_data[0]

    src = chromagnon_apply.section_sources(target, path, 8)
    assert src[0] == 8 and abs(src[1] - 8) == 1
    for z in (4, 8, 11):
        src = chromagnon_apply.section_sources(target, path, z)
        planes = np.stack([arr[src[c], :, :, c] for c in range(arr.shape[-1])])
        section = chromagnon_apply.correct_section(target, planes, path)
        for c in range(arr.shape[-1]):
            a = full[0, z, 16:-16, 16:-16, c].ravel()
            b = section[c, 16:-16, 16:-16].ravel()
            assert np.corrcoef(a, b)[0, 1] > 0.9


def test_incompatible_images_rejected(global_dataset, local_dataset, tmp_path):
    info_csv = chromagnon_apply.read_correction_info(
        _correction_path(global_dataset, tmp_path)
    )
    info_tif = chromagnon_apply.read_correction_info(
        _correction_path(local_dataset, tmp_path)
    )

    other_waves = _make_image(seed=3, waves=[520.0, 600.0], name="other_waves")
    reasons = chromagnon_apply.check_compatibility(info_csv, other_waves)
    assert reasons and "wavelengths" in reasons[0]

    # Without emission wavelengths the channel numbers are used.
    no_waves = _make_image(seed=3, waves=[None, None], name="no_waves")
    assert chromagnon_apply.image_waves(no_waves) == [0, 1]

    other_size = _make_image(seed=4, ny=96, nx=128, name="other_size")
    assert chromagnon_apply.check_compatibility(info_csv, other_size) == []
    reasons = chromagnon_apply.check_compatibility(info_tif, other_size)
    assert reasons and "size" in reasons[0]

    with pytest.raises(Exception):
        chromagnon_apply.apply_correction(
            other_waves, _correction_path(global_dataset, tmp_path)
        )


def test_key_measurement_channels(global_dataset):
    kms = {km.channel_nr: km for km in global_dataset.output.key_measurements}
    assert [kms[c].emission_wavelength_nm for c in (0, 1)] == WAVES
    assert all(km.reference_channel_nr == 0 for km in kms.values())
    assert all(km.reference_channel_name == "ref" for km in kms.values())


def test_all_time_points_corrected():
    dataset = _make_dataset(
        local=False, images=[_make_image(seed=5, nt=2, name="timelapse")]
    )
    chromatic_shift.analyse_chromatic_shift(dataset)
    corrected = dataset.output.corrected_images[0]
    # Chromagnon may crop the borders, but every time point is kept.
    assert corrected.array_data.shape[0] == 2
    assert np.all(np.abs(_residual_shift(corrected.array_data[1:])) < 0.5)
    # The corrected image keeps the calibration and the channel wavelengths.
    assert corrected.voxel_size_z_micron == pytest.approx(0.20)
    assert [c.emission_wavelength_nm for c in corrected.channel_series.channels] == WAVES


def test_auto_reference():
    dataset = _make_dataset(local=False)
    dataset.input_parameters.reference_channel_index = -1
    chromatic_shift.analyse_chromatic_shift(dataset)
    kms = dataset.output.key_measurements
    reference = {km.reference_channel_nr for km in kms}
    assert len(reference) == 1
    reference = reference.pop()
    # The RMSE is measured against the channel actually chosen as reference.
    assert {km.channel_nr: km for km in kms}[reference].registration_rmse == 0.0


def test_average_references_rejects_different_channels():
    images = [
        _make_image(seed=6, name="a"),
        _make_image(seed=7, waves=[520.0, 600.0], name="b"),
    ]
    dataset = _make_dataset(local=False, images=images, average=True)
    with pytest.raises(Exception, match="same channels"):
        chromatic_shift.analyse_chromatic_shift(dataset)
    assert not dataset.processed


def test_total_deviation_without_pixel_size():
    parms = [0.8, 1.5, -2.0, 0.0, 1.0, 1.0, 1.0]
    assert np.isnan(
        chromatic_shift._total_deviation_micron(parms, (16, 128, 160), (0.2, None, None))
    )
