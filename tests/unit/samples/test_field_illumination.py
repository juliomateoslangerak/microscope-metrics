import numpy as np
import pytest
from linkml_runtime.dumpers import YAMLDumper

from microscopemetrics.samples import field_illumination
from tests.test_utilities import get_file


@pytest.fixture
def field_illumination_analysis():
    file_path = get_file("https://dev.mri.cnrs.fr/attachments/download/2926/chroma.npy")
    data = np.load(file_path)
    analysis = field_illumination.FieldIlluminationAnalysis(
        name="an analysis",
        description="a description",
        input={"field_illumination_image": {"data": data}},
        output={},
    )

    # analysis = field_illumination.FieldIlluminationAnalysis(image={"data": data})

    return analysis


def test_run_field_illumination(field_illumination_analysis):
    assert field_illumination_analysis.run()
    assert field_illumination_analysis.processed
