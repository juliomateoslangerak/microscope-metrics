import pytest
from hypothesis import given, note, settings
from hypothesis import strategies as st

from microscopemetrics_schema import datamodel as mm_schema
from microscopemetrics import SaturationError
from microscopemetrics.samples import field_illumination
from microscopemetrics.strategies import strategies as st_mm


@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=10)
def test_field_illumination_analysis_instantiation(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert isinstance(dataset, mm_schema.FieldIlluminationDataset)
    assert dataset.name
    assert dataset.description
    assert dataset.microscope
    assert dataset.input


@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=10)
def test_field_illumination_analysis_run(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert not dataset.processed
    assert field_illumination.analise_field_illumination(dataset)
    assert dataset.processed


@given(
    st_mm.st_field_illumination_dataset(
        expected_output=st_mm.st_field_illumination_test_data(
            centroid_y_relative=st.floats(min_value=-0.0, max_value=0.6),
            centroid_x_relative=st.floats(min_value=-0.0, max_value=0.6),
        )
    )
)
def test_field_illumination_analysis_centroids(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analise_field_illumination(field_illumination_dataset)

    measured_centroids = list(
        zip(
            field_illumination_dataset.output.key_values.centroid_y_relative,
            field_illumination_dataset.output.key_values.centroid_x_relative,
        )
    )
    expected_centroids = list(
        zip(
            expected_output["centroid_generated_y_relative"],
            expected_output["centroid_generated_x_relative"],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input.sigma}"
    )

    for measured_c, expected_c in zip(measured_centroids, expected_centroids):
        assert measured_c[0] == pytest.approx(expected_c[0], abs=0.2)
        assert measured_c[1] == pytest.approx(expected_c[1], abs=0.2)


@given(
    st_mm.st_field_illumination_dataset(
        expected_output=st_mm.st_field_illumination_test_data(
            centroid_y_relative=st.floats(min_value=-0.0, max_value=0.6),
            centroid_x_relative=st.floats(min_value=-0.0, max_value=0.6),
        )
    )
)
def test_field_illumination_analysis_centroids_weighted(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analise_field_illumination(field_illumination_dataset)

    measured_centroids_weighted = list(
        zip(
            field_illumination_dataset.output.key_values.centroid_weighted_y_relative,
            field_illumination_dataset.output.key_values.centroid_weighted_x_relative,
        )
    )
    expected_centroids = list(
        zip(
            expected_output["centroid_generated_y_relative"],
            expected_output["centroid_generated_x_relative"],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input.sigma}"
    )

    for measured_c_w, expected_c in zip(measured_centroids_weighted, expected_centroids):
        assert measured_c_w[0] == pytest.approx(expected_c[0], abs=0.2)
        assert measured_c_w[1] == pytest.approx(expected_c[1], abs=0.2)


@given(st_mm.st_field_illumination_dataset())
def test_field_illumination_analysis_max_intensity_positions(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analise_field_illumination(field_illumination_dataset)

    measured_max_intensity_positions = list(
        zip(
            field_illumination_dataset.output.key_values.max_intensity_pos_y_relative,
            field_illumination_dataset.output.key_values.max_intensity_pos_x_relative,
        )
    )
    expected_centroids = list(
        zip(
            expected_output["centroid_generated_y_relative"],
            expected_output["centroid_generated_x_relative"],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input.sigma}"
    )

    for measured_m_i, expected_c in zip(measured_max_intensity_positions, expected_centroids):
        assert measured_m_i[0] == pytest.approx(expected_c[0], abs=0.05)
        assert measured_m_i[1] == pytest.approx(expected_c[1], abs=0.05)


@given(st_mm.st_field_illumination_dataset())
def test_field_illumination_analysis_centroids_fitted(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analise_field_illumination(field_illumination_dataset)

    measured_centroids_fitted = list(
        zip(
            field_illumination_dataset.output.key_values.centroid_fitted_y_relative,
            field_illumination_dataset.output.key_values.centroid_fitted_x_relative,
        )
    )
    expected_centroids = list(
        zip(
            expected_output["centroid_generated_y_relative"],
            expected_output["centroid_generated_x_relative"],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input.sigma}"
    )

    for measured_m_i, expected_c in zip(measured_centroids_fitted, expected_centroids):
        assert measured_m_i[0] == pytest.approx(expected_c[0], abs=0.05)
        assert measured_m_i[1] == pytest.approx(expected_c[1], abs=0.05)


@given(
    st_mm.st_field_illumination_dataset(
        expected_output=st_mm.st_field_illumination_test_data(
            target_min_intensity=st.just(1.5),
        )
    )
)
def test_field_illumination_analysis_raises_saturation_error(dataset):
    with pytest.raises(SaturationError):
        dataset = dataset["unprocessed_dataset"]
        field_illumination.analise_field_illumination(dataset)
