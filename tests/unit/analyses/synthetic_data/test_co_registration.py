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
from microscopemetrics.analyses import co_registration
from microscopemetrics.strategies import st_beads_test_data
from microscopemetrics.strategies.co_registration import st_co_registration_dataset


@given(
    st_co_registration_dataset(
        test_data=st_beads_test_data(
            c_image_shape=st.just(2),
        )
    )
)
@settings(max_examples=1)
def test_co_registration_analysis_instantiation(co_registration_dataset):
    co_registration_dataset = co_registration_dataset["unprocessed_dataset"]
    assert isinstance(co_registration_dataset, mm_schema.CoRegistrationDataset)
    assert co_registration_dataset.name
    assert co_registration_dataset.description
    assert co_registration_dataset.microscope
    assert co_registration_dataset.input_parameters


@given(
    st_co_registration_dataset(
        unprocessed_dataset=st_mm_analyses_schema.st_mm_co_registration_unprocessed_dataset(
            input_parameters=st_mm_analyses_schema.st_mm_co_registration_input_parameters(
                sigma_min=st.just(0.7),
            )
        ),
    )
)
@settings(max_examples=1)
def test_co_registration_analysis_run(co_registration_dataset):
    co_registration_dataset = co_registration_dataset["unprocessed_dataset"]
    assert not co_registration_dataset.processed
    assert co_registration.analyse_co_registration(co_registration_dataset)
    assert co_registration_dataset.processed


@given(
    st_co_registration_dataset(
        test_data=st_beads_test_data(
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        ),
    )
)
@settings(max_examples=5)
def test_co_registration_analysis_no_beads(dataset):
    co_registration_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    co_registration_dataset.input_parameters.min_lateral_distance_factor = expected_output[
        "min_lateral_distance_factor"
    ][0]

    with pytest.raises(AnalysisError):
        co_registration.analyse_co_registration(co_registration_dataset)


@given(
    st_co_registration_dataset(
        test_data=st_beads_test_data(
            nr_images=st.just(2),
        ),
    )
)
@settings(max_examples=1)
def test_co_registration_analysis_different_lateral_shapes(dataset):
    co_registration_dataset = dataset["unprocessed_dataset"]
    co_registration_dataset.input_data.multiwavelength_beads_images[0].shape_x = (
        co_registration_dataset.input_data.multiwavelength_beads_images[0].shape_x - 1
    )
    co_registration_dataset.input_data.multiwavelength_beads_images[0].array_data = (
        co_registration_dataset.input_data.multiwavelength_beads_images[0].array_data[
            :, :, :, 1:, :
        ]
    )

    with pytest.raises(DataFormatError):
        co_registration.analyse_co_registration(co_registration_dataset)


@given(
    st_co_registration_dataset(
        test_data=st_beads_test_data(
            nr_images=st.just(2),
        ),
    )
)
@settings(max_examples=1)
def test_co_registration_analysis_different_pixel_size(dataset):
    co_registration_dataset = dataset["unprocessed_dataset"]
    co_registration_dataset.input_data.multiwavelength_beads_images[0].voxel_size_x_micron = 0.2
    co_registration_dataset.input_data.multiwavelength_beads_images[0].voxel_size_y_micron = 0.2
    co_registration_dataset.input_data.multiwavelength_beads_images[0].voxel_size_z_micron = 0.6
    co_registration_dataset.input_data.multiwavelength_beads_images[1].voxel_size_x_micron = 0.3
    co_registration_dataset.input_data.multiwavelength_beads_images[1].voxel_size_y_micron = 0.3
    co_registration_dataset.input_data.multiwavelength_beads_images[1].voxel_size_z_micron = 0.6

    with pytest.raises(DataFormatError):
        co_registration.analyse_co_registration(co_registration_dataset)


# @given(
#     st_psf_beads_dataset(
#         test_data=st_psf_beads_test_data(
#             z_image_shape=st.just(61),
#             y_image_shape=st.just(512),
#             x_image_shape=st.just(512),
#             c_image_shape=st.just(3),
#             nr_valid_beads=st.integers(min_value=3, max_value=20),
#             nr_edge_beads=st.just(0),
#             nr_out_of_focus_beads=st.just(0),
#             nr_clustering_beads=st.just(0),
#             # We create very noisy images.
#             dtype=st.just(np.uint16),
#             do_noise=st.just(True),
#             signal=st.just(0.003),
#             background=st.just(0.001),
#             sigma_z=st.just(2),
#             sigma_y=st.just(1.5),
#             sigma_x=st.just(1.5),
#         ),
#         unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(
#             input_parameters=st_mm_analyses_schema.st_mm_psf_beads_input_parameters(
#                 # We want to be very permissive with the fitting or otherwise
#                 # clustering beads will be thrown away.
#                 fitting_airy_r2_threshold=st.just(0.1),
#                 # intensity_robust_z_score_threshold=st.just(4.0),
#                 # We want to limit the sigma range to avoid finding noise as beads.
#                 sigma_min=st.just(1.1),
#                 snr_threshold=st.just(5.0),
#             )
#         ),
#     )
# )
# @settings(deadline=20000)
# def test_psf_beads_analysis_noisy_beads(dataset):
#     psf_beads_dataset = dataset["unprocessed_dataset"]
#     expected_output = dataset["expected_output"]
#     psf_beads.analyse_psf_beads(psf_beads_dataset)
#
#     expected = sum(len(im_vbp) for im_vbp in expected_output["valid_bead_positions"])
#
#     for measured_km in psf_beads_dataset.output.key_measurements:
#         # We just have to hope not to detect too many
#         assert measured_km["considered_valid_count"] <= expected
