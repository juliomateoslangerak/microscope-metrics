import pytest
from tests.test_utilities import get_file

from microscopemetrics.samples import argolight
import numpy as np


@pytest.fixture
def argolight_b():
    file_path = get_file('https://dev.mri.cnrs.fr/attachments/download/2290/201702_RI510_Argolight-1-1_010_SIR_ALX.npy')
    data = np.load(file_path)

    analysis = argolight.ArgolightBAnalysis()
    analysis.set_data('argolight_b', data)
    analysis.set_metadata('spots_distance', 5)
    analysis.set_metadata('pixel_size', (.125, .39, .39))

    return analysis


@pytest.fixture
def argolight_e_horizontal():
    file_path = get_file('https://dev.mri.cnrs.fr/attachments/download/2292/201702_RI510_Argolight-1-1_005_SIR_ALX.npy')
    data = np.load(file_path)

    analysis = argolight.ArgolightEAnalysis()
    analysis.set_data('argolight_e', data)
    analysis.set_metadata('pixel_size', (.125, .39, .39))
    analysis.set_metadata('axis', 2)

    return analysis


@pytest.fixture
def argolight_e_vertical():
    file_path = get_file('https://dev.mri.cnrs.fr/attachments/download/2291/201702_RI510_Argolight-1-1_004_SIR_ALX.npy')
    data = np.load(file_path)

    analysis = argolight.ArgolightEAnalysis()
    analysis.set_data('argolight_e', data)
    analysis.set_metadata('pixel_size', (.125, .39, .39))
    analysis.set_metadata('axis', 1)

    return analysis


def test_run_argolight_b(argolight_b):
    assert argolight_b.run()
    assert argolight_b.output


def test_run_argolight_e_horizontal(argolight_e_horizontal):
    assert argolight_e_horizontal.run()
    assert argolight_e_horizontal.output


def test_run_argolight_e_vertical(argolight_e_vertical):
    assert argolight_e_vertical.run()
    assert argolight_e_vertical.output
