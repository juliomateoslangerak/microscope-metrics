import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from microscopemetrics import SaturationError
from microscopemetrics.samples import field_illumination, numpy_to_image_byref
from tests import strategies as mm_st
from tests.test_utilities import get_file


@given(mm_st.st_field_illumination_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_field_illumination_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], field_illumination.FieldIlluminationAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@given(mm_st.st_field_illumination_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def test_field_illumination_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output


@given(
    mm_st.st_field_illumination_dataset(
        expected_output=mm_st.st_field_illumination_test_data(
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
