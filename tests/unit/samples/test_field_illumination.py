import pytest
from hypothesis import HealthCheck, given, note, settings
from hypothesis import strategies as st

from microscopemetrics import SaturationError
from microscopemetrics.samples import field_illumination
from microscopemetrics.strategies import strategies as st_mm


@pytest.mark.instantiation
@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_field_illumination_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], field_illumination.FieldIlluminationAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@pytest.mark.run
@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def test_field_illumination_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output


@pytest.mark.analysis
@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow], deadline=100000)
def test_field_illumination_analysis_centroids(dataset):
    field_illumination_analysis = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    field_illumination_analysis.run()

    assert field_illumination_analysis.processed

    image_center = tuple(
        dim / 2
        for dim in field_illumination_analysis.input.field_illumination_image.data.shape[2:4]
    )
    measured_centroids = [
        ((c_y - image_center[0]) / image_center[0], (c_x - image_center[1]) / image_center[1])
        for c_y, c_x in zip(
            field_illumination_analysis.output.key_values.centroid_y,
            field_illumination_analysis.output.key_values.centroid_x,
        )
    ]
    expected_centroids = list(
        zip(
            expected_output["y_center_rel_offsets"],
            expected_output["x_center_rel_offsets"],
        )
    )
    # expected_contrast = [a - b for a, b in zip(expected_output["target_max_intensities"], expected_output["target_min_intensities"])]
    # expected_dispersion = list(expected_output["dispersions"])
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_analysis.input.bit_depth}"
        f"saturation_threshold: {field_illumination_analysis.input.saturation_threshold}"
        f"sigma: {field_illumination_analysis.input.sigma}"
    )

    for measured_c, expected_c in zip(measured_centroids, expected_centroids):
        assert measured_c[0] == pytest.approx(expected_c[0], abs=0.02)
        assert measured_c[1] == pytest.approx(expected_c[1], abs=0.02)


@pytest.mark.analysis
@given(st_mm.st_field_illumination_dataset())
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow], deadline=100000)
def test_field_illumination_analysis_centroids_weighted(dataset):
    field_illumination_analysis = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    field_illumination_analysis.run()

    assert field_illumination_analysis.processed

    image_center = tuple(
        dim / 2
        for dim in field_illumination_analysis.input.field_illumination_image.data.shape[2:4]
    )
    measured_centroids_weighted = [
        ((c_y - image_center[0]) / image_center[0], (c_x - image_center[1]) / image_center[1])
        for c_y, c_x in zip(
            field_illumination_analysis.output.key_values.centroid_weighted_y,
            field_illumination_analysis.output.key_values.centroid_weighted_x,
        )
    ]
    expected_centroids = list(
        zip(
            expected_output["y_center_rel_offsets"],
            expected_output["x_center_rel_offsets"],
        )
    )
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_analysis.input.bit_depth}"
        f"saturation_threshold: {field_illumination_analysis.input.saturation_threshold}"
        f"sigma: {field_illumination_analysis.input.sigma}"
    )

    for measured_c_w, expected_c in zip(measured_centroids_weighted, expected_centroids):
        assert measured_c_w[0] == pytest.approx(expected_c[0], abs=0.02)
        assert measured_c_w[1] == pytest.approx(expected_c[1], abs=0.02)


@pytest.mark.analysis
@given(
    st_mm.st_field_illumination_dataset(
        expected_output=st_mm.st_field_illumination_test_data(
            signal=st.integers(min_value=100, max_value=1000),
            target_min_intensity=st.floats(min_value=0.1, max_value=0.4),
            target_max_intensity=st.floats(min_value=0.6, max_value=0.9),
        )
    )
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def test_field_illumination_analysis_max_intensity_positions(dataset):
    field_illumination_analysis = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    field_illumination_analysis.run()

    assert field_illumination_analysis.processed

    image_center = tuple(
        dim / 2
        for dim in field_illumination_analysis.input.field_illumination_image.data.shape[2:4]
    )
    measured_max_intensity_positions = [
        ((c_y - image_center[0]) / image_center[0], (c_x - image_center[1]) / image_center[1])
        for c_y, c_x in zip(
            field_illumination_analysis.output.key_values.max_intensity_pos_y,
            field_illumination_analysis.output.key_values.max_intensity_pos_x,
        )
    ]
    expected_centroids = list(
        zip(
            expected_output["y_center_rel_offsets"],
            expected_output["x_center_rel_offsets"],
        )
    )
    # expected_contrast = [a - b for a, b in zip(expected_output["target_max_intensities"], expected_output["target_min_intensities"])]
    # expected_dispersion = list(expected_output["dispersions"])
    note(f"Expected output: {expected_output}")
    note(
        f"Input params: "
        f"bit_depth: {field_illumination_analysis.input.bit_depth}"
        f"saturation_threshold: {field_illumination_analysis.input.saturation_threshold}"
        f"sigma: {field_illumination_analysis.input.sigma}"
    )

    for measured_m_i, expected_c in zip(measured_max_intensity_positions, expected_centroids):
        assert measured_m_i[0] == pytest.approx(expected_c[0], abs=0.5)
        assert measured_m_i[1] == pytest.approx(expected_c[1], abs=0.5)


@pytest.mark.errors
@given(
    st_mm.st_field_illumination_dataset(
        expected_output=st_mm.st_field_illumination_test_data(
            target_min_intensity=st.just(1.5),
        )
    )
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_field_illumination_analysis_raises_saturation_error(dataset):
    with pytest.raises(SaturationError):
        assert dataset["unprocessed_analysis"].run()


# @pytest.fixture
# def field_illumination_analysis():
#     image_url = "https://dev.mri.cnrs.fr/attachments/download/3071/chroma.npy"
#     file_path = get_file(image_url)
#     data = np.load(file_path)
#     analysis = field_illumination.FieldIlluminationAnalysis(
#         name="an analysis",
#         description="a description",
#         microscope="1234",
#         input={
#             "field_illumination_image": numpy_to_image_byref(
#                 array=data,
#                 name="image_name",
#                 description="image_description",
#                 image_url=image_url,
#                 source_image_url=image_url,
#             ),
#         },
#         output={},
#     )
#
#     return analysis
#
#
# def test_run_field_illumination(field_illumination_analysis):
#     assert field_illumination_analysis.run()
#     assert field_illumination_analysis.processed
