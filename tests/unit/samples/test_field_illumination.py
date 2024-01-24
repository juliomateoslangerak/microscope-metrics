import numpy as np
import pytest

from microscopemetrics.samples import field_illumination, numpy_to_image_byref
from tests.test_utilities import get_file


@pytest.fixture
def field_illumination_analysis():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/3071/chroma.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)
    analysis = field_illumination.FieldIlluminationAnalysis(
        name="an analysis",
        description="a description",
        microscope="1234",
        input={
            "field_illumination_image": numpy_to_image_byref(
                array=data,
                name="image_name",
                description="image_description",
                image_url=image_url,
                source_image_url=image_url,
            ),
        },
        output={},
    )

    return analysis


def test_run_field_illumination(field_illumination_analysis):
    assert field_illumination_analysis.run()
    assert field_illumination_analysis.processed
