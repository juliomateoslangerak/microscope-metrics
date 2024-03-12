import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from microscopemetrics.samples import psf_beads
from microscopemetrics.strategies import strategies as st_mm


@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10)
def test_psf_beads_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], psf_beads.PSFBeadsAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
        )
    )
)
@settings(max_examples=10)
def test_psf_beads_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output


@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.integers(min_value=0, max_value=10),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(deadline=200000)
def test_psf_beads_analysis_nr_valid_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["valid_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_analyzed:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.integers(min_value=0, max_value=10),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(deadline=200000)
def test_psf_beads_analysis_nr_lateral_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["edge_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_discarded_lateral_edge:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(71),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(0),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.integers(min_value=0, max_value=10),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(deadline=200000)
def test_psf_beads_analysis_nr_axial_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["out_of_focus_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_axial_edge:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            z_image_shape=st.just(61),
            y_image_shape=st.just(512),
            x_image_shape=st.just(512),
            c_image_shape=st.just(3),
            nr_valid_beads=st.just(10),
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.integers(min_value=0, max_value=2),
            # To find the outliers we need to ensure that all images have the same intensity related parameters
            dtype=st.just(np.uint16),
            do_noise=st.just(True),
            signal=st.just(100.0),
            target_min_intensity=st.just(0.1),
            target_max_intensity=st.just(0.5),
            sigma_z=st.just(2),
            sigma_y=st.just(1.5),
            sigma_x=st.just(1.5),
        )
    )
)
@settings(deadline=200000)
def test_psf_beads_analysis_nr_intensity_outliers_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()
    assert psf_beads_dataset.processed

    expected = sum(len(im["clustering_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_intensity_outlier:
        assert measured == expected
