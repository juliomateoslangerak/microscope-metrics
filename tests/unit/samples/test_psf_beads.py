import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics import SaturationError
from microscopemetrics.samples import psf_beads
from microscopemetrics.strategies import strategies as st_mm


@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=1)
def test_psf_beads_analysis_instantiation(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert isinstance(dataset, mm_schema.PSFBeadsDataset)
    assert dataset.name
    assert dataset.description
    assert dataset.microscope
    assert dataset.input


@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=1)
def test_psf_beads_analysis_run(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert not dataset.processed
    assert psf_beads.analyse_psf_beads(dataset)
    assert dataset.processed


@given(
    st_mm.st_psf_beads_dataset(
        test_data=st_mm.st_psf_beads_test_data(
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
def test_psf_beads_analysis_nr_valid_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im["valid_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_analyzed:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        test_data=st_mm.st_psf_beads_test_data(
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
def test_psf_beads_analysis_nr_lateral_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im["edge_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_discarded_lateral_edge:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        test_data=st_mm.st_psf_beads_test_data(
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
def test_psf_beads_analysis_nr_axial_edge_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(im["out_of_focus_bead_positions"]) for im in expected_output.values())

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_axial_edge:
        assert measured == expected


@given(
    st_mm.st_psf_beads_dataset(
        test_data=st_mm.st_psf_beads_test_data(
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
    psf_beads_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    psf_beads.analyse_psf_beads(psf_beads_dataset)

    expected = sum(len(img_cp) for img_cp in expected_output["clustering_bead_positions"])

    for measured in psf_beads_dataset.output.key_values.nr_of_beads_considered_intensity_outlier:
        assert measured == expected
