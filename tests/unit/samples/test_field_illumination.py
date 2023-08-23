import numpy as np
import pytest
from linkml_runtime.dumpers import YAMLDumper

from microscopemetrics.data_schema import core_schema
from microscopemetrics.samples import field_illumination
from tests.test_utilities import get_file


@pytest.fixture
def field_illumination_analysis():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/2926/chroma.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)
    analysis = field_illumination.FieldIlluminationAnalysis(
        name="an analysis",
        description="a description",
        input={
            "field_illumination_image": {
                "data": data,
                "name": "image_name",
                "image_url": image_url,
            }
        },
        output={},
    )

    return analysis


def test_run_field_illumination(field_illumination_analysis):
    assert field_illumination_analysis.run()
    assert field_illumination_analysis.processed
