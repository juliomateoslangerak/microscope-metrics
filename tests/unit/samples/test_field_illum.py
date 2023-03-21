import pytest
from tests.test_utilities import get_file

from microscopemetrics.samples import field_illum
import numpy as np

@pytest.fixture
def field_illum_analysis():
    file_path = get_file('https://amubox.univ-amu.fr/s/to2aJbpBZKeiTJj/download/chroma.npy')
    data = np.load(file_path)

    analysis = field_illum.FieldHomogeneityAnalysis()
    analysis.set_data('image', data)

    return analysis


def test_run_field_illum(field_illum_analysis):
    assert field_illum_analysis.run()
    assert field_illum_analysis.output
