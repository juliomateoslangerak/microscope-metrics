import pytest
from hypothesis import given, note, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics import SaturationError
from microscopemetrics.samples import field_illumination
from microscopemetrics.strategies import strategies as st_mm


@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=1)
def test_field_illumination_analysis_instantiation(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert isinstance(dataset, mm_schema.FieldIlluminationDataset)
    assert dataset.name
    assert dataset.description
    assert dataset.microscope
    assert dataset.input_parameters


@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=1)
def test_field_illumination_analysis_run(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert not dataset.processed
    assert field_illumination.analyse_field_illumination(dataset)
    assert dataset.processed


@given(
    st_mm.st_field_illumination_dataset(
        test_data=st_mm.st_field_illumination_test_data(
            center_y_relative=st.floats(min_value=-0.0, max_value=0.6),
            center_x_relative=st.floats(min_value=-0.0, max_value=0.6),
        )
    )
)
def test_field_illumination_analysis_centers_geometric(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analyse_field_illumination(field_illumination_dataset)

    measured_centers = list(
        zip(
            field_illumination_dataset.output.key_measurements.center_geometric_y_relative,
            field_illumination_dataset.output.key_measurements.center_geometric_x_relative,
        )
    )
    expected_centers = list(
        zip(
            [e_c for im in expected_output["centers_generated_y_relative"] for e_c in im],
            [e_c for im in expected_output["centers_generated_x_relative"] for e_c in im],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input_parameters.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input_parameters.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input_parameters.sigma}"
    )

    for measured_c, expected_c in zip(measured_centers, expected_centers):
        assert measured_c[0] == pytest.approx(expected_c[0], abs=0.2)
        assert measured_c[1] == pytest.approx(expected_c[1], abs=0.2)


@given(
    st_mm.st_field_illumination_dataset(
        test_data=st_mm.st_field_illumination_test_data(
            center_y_relative=st.floats(min_value=-0.0, max_value=0.6),
            center_x_relative=st.floats(min_value=-0.0, max_value=0.6),
        )
    )
)
def test_field_illumination_analysis_centers_of_mass(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analyse_field_illumination(field_illumination_dataset)

    measured_centers_weighted = list(
        zip(
            field_illumination_dataset.output.key_measurements.center_of_mass_y_relative,
            field_illumination_dataset.output.key_measurements.center_of_mass_x_relative,
        )
    )
    expected_centers = list(
        zip(
            [e_c for im in expected_output["centers_generated_y_relative"] for e_c in im],
            [e_c for im in expected_output["centers_generated_x_relative"] for e_c in im],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input_parameters.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input_parameters.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input_parameters.sigma}"
    )

    for measured_c_w, expected_c in zip(measured_centers_weighted, expected_centers):
        assert measured_c_w[0] == pytest.approx(expected_c[0], abs=0.2)
        assert measured_c_w[1] == pytest.approx(expected_c[1], abs=0.2)


@given(st_mm.st_field_illumination_dataset())
def test_field_illumination_analysis_max_intensity_positions(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analyse_field_illumination(field_illumination_dataset)

    measured_max_intensity_positions = list(
        zip(
            field_illumination_dataset.output.key_measurements.max_intensity_pos_y_relative,
            field_illumination_dataset.output.key_measurements.max_intensity_pos_x_relative,
        )
    )
    expected_centers = list(
        zip(
            [e_c for im in expected_output["centers_generated_y_relative"] for e_c in im],
            [e_c for im in expected_output["centers_generated_x_relative"] for e_c in im],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input_parameters.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input_parameters.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input_parameters.sigma}"
    )

    for measured_m_i, expected_c in zip(measured_max_intensity_positions, expected_centers):
        assert measured_m_i[0] == pytest.approx(expected_c[0], abs=0.05)
        assert measured_m_i[1] == pytest.approx(expected_c[1], abs=0.05)


@given(st_mm.st_field_illumination_dataset())
def test_field_illumination_analysis_centers_fitted(dataset):
    field_illumination_dataset = dataset["unprocessed_dataset"]
    expected_output = dataset["expected_output"]
    field_illumination.analyse_field_illumination(field_illumination_dataset)

    measured_centers_fitted = list(
        zip(
            field_illumination_dataset.output.key_measurements.center_fitted_y_relative,
            field_illumination_dataset.output.key_measurements.center_fitted_x_relative,
        )
    )
    expected_centers = list(
        zip(
            [e_c for im in expected_output["centers_generated_y_relative"] for e_c in im],
            [e_c for im in expected_output["centers_generated_x_relative"] for e_c in im],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_dataset.input_parameters.bit_depth}"
        f"saturation_threshold: {field_illumination_dataset.input_parameters.saturation_threshold}"
        f"sigma: {field_illumination_dataset.input_parameters.sigma}"
    )

    for measured_m_i, expected_c in zip(measured_centers_fitted, expected_centers):
        assert measured_m_i[0] == pytest.approx(expected_c[0], abs=0.05)
        assert measured_m_i[1] == pytest.approx(expected_c[1], abs=0.05)


@given(
    st_mm.st_field_illumination_dataset(
        test_data=st_mm.st_field_illumination_test_data(
            target_min_intensity=st.just(1.5),
        )
    )
)
def test_field_illumination_analysis_raises_saturation_error(dataset):
    with pytest.raises(SaturationError):
        dataset = dataset["unprocessed_dataset"]
        field_illumination.analyse_field_illumination(dataset)
