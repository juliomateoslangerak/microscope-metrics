import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema
import numpy as np
import pandas as pd
import pytest
from hypothesis import given, reproduce_failure, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema
from scipy import ndimage
from skimage.exposure import rescale_intensity
from skimage.filters import gaussian

from microscopemetrics import AnalysisError, DataFormatError
from microscopemetrics.analyses import psf_beads
from microscopemetrics.analyses.tools import fit_gaussian
from microscopemetrics.strategies.psf_beads import (
    st_psf_beads_dataset,
    st_psf_beads_test_data,
)


@given(
    shifts=st.lists(
        st.tuples(
            st.floats(min_value=0.1, max_value=0.49),
            st.floats(min_value=0.1, max_value=0.49),
            st.floats(min_value=0.1, max_value=0.49),
        ),
        min_size=3,
        max_size=10,
    ),
    signal=st.integers(min_value=2000, max_value=10000),
    background=st.integers(min_value=40, max_value=400),
    sigma_axial=st.floats(min_value=1.0, max_value=3.0),
    sigma_lateral=st.floats(min_value=1.0, max_value=2.0),
)
def test_average_beads(shifts, signal, background, sigma_axial, sigma_lateral):
    beads = []
    ref_beads = []

    for shift in shifts:
        # Reproducing acquisition flow:
        # - bead real position shifted
        # - bead is blurred by microscope PSF (gaussian?)
        # - bead is noised by Poisson noise in the camera
        # a replica is caught as reference before shifting
        bead = np.zeros((61, 21, 21), dtype=np.uint16)
        bead[30, 10, 10] = 1
        bead = gaussian(
            bead, sigma=(sigma_axial, sigma_lateral, sigma_lateral), preserve_range=False
        )
        bead = np.astype(rescale_intensity(bead, out_range=(background, signal)), np.uint16)
        ref_bead = bead.copy()
        bead = ndimage.shift(bead, shift, mode="nearest", order=1)
        bead = np.random.poisson(bead)
        ref_bead = np.random.poisson(ref_bead)
        beads.append(bead)
        ref_beads.append(ref_bead)

    averaged_bead = psf_beads._average_beads_group(
        pd.DataFrame({"beads": beads, "considered_valid": True}),
        voxel_size_micron=(None, None, None),
    ).values[0]
    ref_bead = np.mean(ref_beads, axis=0)

    averaged_sigma_z = fit_gaussian(np.squeeze(averaged_bead[:, 10, 10]))[3][3]
    averaged_sigma_y = fit_gaussian(np.squeeze(averaged_bead[30, :, 10]))[3][3]
    averaged_sigma_x = fit_gaussian(np.squeeze(averaged_bead[30, 10, :]))[3][3]

    ref_sigma_z = fit_gaussian(np.squeeze(ref_bead[:, 10, 10]))[3][3]
    ref_sigma_y = fit_gaussian(np.squeeze(ref_bead[30, :, 10]))[3][3]
    ref_sigma_x = fit_gaussian(np.squeeze(ref_bead[30, 10, :]))[3][3]

    assert averaged_sigma_z == pytest.approx(ref_sigma_z, abs=0.3)
    assert averaged_sigma_y == pytest.approx(ref_sigma_y, abs=0.3)
    assert averaged_sigma_x == pytest.approx(ref_sigma_x, abs=0.3)


@given(st_psf_beads_dataset())
@settings(max_examples=1)
def test_psf_beads_analysis_instantiation(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert isinstance(dataset, mm_schema.PSFBeadsDataset)
    assert dataset.name
    assert dataset.description
    assert dataset.microscope
    assert dataset.input_parameters


@given(
    st_psf_beads_dataset(
        unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(
            input_parameters=st_mm_analyses_schema.st_mm_psf_beads_input_parameters(
                sigma_min=st.just(0.7),
            )
        ),
    )
)
@settings(max_examples=1)
def test_psf_beads_analysis_run(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert not dataset.processed
    assert psf_beads.analyse_psf_beads(dataset)
    assert dataset.processed


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            min_lateral_distance_factor=st.just(20),
            nr_valid_beads=st.integers(min_value=1, max_value=10),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
        unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(
            input_parameters=st_mm_analyses_schema.st_mm_psf_beads_input_parameters(
                fitting_airy_r2_threshold=st.just(0.7),  # TODO: remove this at some point
                intensity_robust_z_score_threshold=st.just(4.0),
            )
        ),
    )
)
def test_psf_beads_analysis_nr_valid_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.input_parameters.min_lateral_distance_factor = expected_output[
        "min_lateral_distance_factor"
    ][0]

    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im_vbp) for im_vbp in expected_output["valid_bead_positions"])

    for km in psf_beads_dataset.output.key_measurements:
        assert km["considered_valid_count"] == expected


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            dtype=st.just(np.uint16),
            min_lateral_distance_factor=st.just(20),
            signal=st.just(0.01),
            background=st.just(0.005),
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
    )
)
def test_psf_beads_analysis_no_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.input_parameters.min_lateral_distance_factor = expected_output[
        "min_lateral_distance_factor"
    ][0]
    # Should raise AnalysisError
    with pytest.raises(AnalysisError):
        psf_beads.analyse_psf_beads(psf_beads_dataset)


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            nr_images=st.just(2),
            z_image_shape=st.just(31),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(2),
            dtype=st.just(np.uint16),
            min_lateral_distance_factor=st.just(20),
            signal=st.just(0.01),
            background=st.just(0.005),
            nr_valid_beads=st.just(5),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
    )
)
def test_psf_beads_analysis_different_lateral_shapes(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    psf_beads_dataset.input_data.psf_beads_images[0].shape_x = (
        psf_beads_dataset.input_data.psf_beads_images[0].shape_x - 1
    )
    psf_beads_dataset.input_data.psf_beads_images[0].array_data = (
        psf_beads_dataset.input_data.psf_beads_images[0].array_data[:, :, :, 1:, :]
    )

    # Should raise DataFormatError
    with pytest.raises(DataFormatError):
        psf_beads.analyse_psf_beads(psf_beads_dataset)


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            nr_images=st.just(2),
            z_image_shape=st.just(31),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(2),
            dtype=st.just(np.uint16),
            min_lateral_distance_factor=st.just(20),
            signal=st.just(0.01),
            background=st.just(0.005),
            nr_valid_beads=st.just(5),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
    )
)
def test_psf_beads_analysis_different_pixel_size(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    psf_beads_dataset.input_data.psf_beads_images[0].voxel_size_x_micron = 0.2
    psf_beads_dataset.input_data.psf_beads_images[0].voxel_size_y_micron = 0.2
    psf_beads_dataset.input_data.psf_beads_images[0].voxel_size_z_micron = 0.6
    psf_beads_dataset.input_data.psf_beads_images[1].voxel_size_x_micron = 0.3
    psf_beads_dataset.input_data.psf_beads_images[1].voxel_size_y_micron = 0.3
    psf_beads_dataset.input_data.psf_beads_images[1].voxel_size_z_micron = 0.6

    # Should raise DataFormatError
    with pytest.raises(DataFormatError):
        psf_beads.analyse_psf_beads(psf_beads_dataset)


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(3),
            nr_edge_beads=st.integers(min_value=1, max_value=3),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
    )
)
def test_psf_beads_analysis_nr_lateral_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)
    psf_beads_dataset.input_parameters.min_lateral_distance_factor = expected_output[
        "min_lateral_distance_factor"
    ][0]

    expected = sum(len(im_ebp) for im_ebp in expected_output["edge_bead_positions"])

    for measured_km in psf_beads_dataset.output.key_measurements:
        assert measured_km["considered_lateral_edge_count"] == expected


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(71),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(2),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.integers(min_value=1, max_value=5),
            nr_clustering_beads=st.just(0),
        )
    )
)
def test_psf_beads_analysis_nr_axial_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im_ofbp) for im_ofbp in expected_output["out_of_focus_bead_positions"])

    for measured_km in psf_beads_dataset.output.key_measurements:
        assert measured_km["considered_axial_edge_count"] == expected


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(12),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.integers(min_value=1, max_value=2),
            # To find the outliers we need to ensure that all images have the same intensity related parameters
            dtype=st.just(np.uint16),
            do_noise=st.just(True),
            signal=st.just(0.1),
            background=st.just(0.005),
            sigma_z=st.just(2),
            sigma_y=st.just(1.5),
            sigma_x=st.just(1.5),
        ),
        unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(
            input_parameters=st_mm_analyses_schema.st_mm_psf_beads_input_parameters(
                # We want to be very permissive with the fitting or otherwise
                # clustering beads will be thrown away.
                fitting_airy_r2_threshold=st.just(0.2),
            )
        ),
    )
)
@settings(deadline=20000)
def test_psf_beads_analysis_nr_intensity_outliers_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(img_cbp) for img_cbp in expected_output["clustering_bead_positions"])

    for measured_km in psf_beads_dataset.output.key_measurements:
        assert measured_km["considered_intensity_outlier_count"] == expected


@given(
    st_psf_beads_dataset(
        test_data=st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.integers(min_value=3, max_value=20),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
            # We create very noisy images.
            dtype=st.just(np.uint16),
            do_noise=st.just(True),
            signal=st.just(0.003),
            background=st.just(0.001),
            sigma_z=st.just(2),
            sigma_y=st.just(1.5),
            sigma_x=st.just(1.5),
        ),
        unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(
            input_parameters=st_mm_analyses_schema.st_mm_psf_beads_input_parameters(
                # We want to be very permissive with the fitting or otherwise
                # clustering beads will be thrown away.
                fitting_airy_r2_threshold=st.just(0.1),
                # intensity_robust_z_score_threshold=st.just(4.0),
                # We want to limit the sigma range to avoid finding noise as beads.
                sigma_min=st.just(1.1),
                snr_threshold=st.just(5.0),
            )
        ),
    )
)
@settings(deadline=20000)
def test_psf_beads_analysis_noisy_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im_vbp) for im_vbp in expected_output["valid_bead_positions"])

    for measured_km in psf_beads_dataset.output.key_measurements:
        # We just have to hope not to detect too many
        assert measured_km["considered_valid_count"] <= expected
