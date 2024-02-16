import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from microscopemetrics.samples import psf_beads
from microscopemetrics.strategies import strategies as st_mm


@pytest.mark.instantiation
@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_psf_beads_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], psf_beads.PSFBeadsAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@pytest.mark.run
@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=100000)
def test_psf_beads_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output


@pytest.mark.analysis
@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            c_image_shape=st.just(3),
            nr_valid_beads=st.integers(min_value=0, max_value=10),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_nr_valid_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["valid_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_analyzed:
        assert measured == expected


@pytest.mark.analysis
@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.integers(min_value=0, max_value=10),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_nr_lateral_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["edge_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_discarded_lateral_edge:
        assert measured == expected


@pytest.mark.analysis
@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.integers(min_value=0, max_value=10),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_nr_axial_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["out_of_focus_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_axial_edge:
        assert measured == expected


@pytest.mark.analysis
@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(10),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.integers(min_value=0, max_value=2),
        )
    )
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_nr_intensity_outliers_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["clustering_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_intensity_outlier:
        assert measured == expected


# from tests.test_utilities import get_file
#
# from microscopemetrics.samples import psf_beads
# import numpy as np
#
#
# @pytest.fixture()
# def psf_beads_analysis():
#     file_path = get_file(
#         "https://dev.mri.cnrs.fr/attachments/download/3072/psf_beads_EM-488_MAG-40.npy"
#     )
#     data = np.load(file_path)
#
#     analysis = psf_beads.PSFBeadsAnalysis()
#     analysis.set_data("beads_image", data)
#     analysis.set_metadata("theoretical_fwhm_lateral_res", 0.300)
#     analysis.set_metadata("theoretical_fwhm_axial_res", 0.800)
#     analysis.set_metadata("pixel_size", (0.35, 0.06, 0.06))
#
#     return analysis
#
#
# def test_run_psf_beads(psf_beads_analysis):
#     assert psf_beads_analysis.run()
#     assert psf_beads_analysis.output
