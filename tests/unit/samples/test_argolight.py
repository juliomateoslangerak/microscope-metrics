import numpy as np
import pytest

from microscopemetrics.samples import argolight
from tests.test_utilities import get_file


@pytest.fixture
def argolight_b():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/2290/201702_RI510_Argolight-1-1_010_SIR_ALX.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)

    analysis = argolight.ArgolightBAnalysis(
        name="an analysis",
        description="a description",
        input={
            "argolight_b_image": {"data": data, "name": "image_name", "url": image_url},
            "spots_distance": 40,
        },
        output={},
    )

    return analysis


@pytest.fixture
def argolight_e_horizontal():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/2292/201702_RI510_Argolight-1-1_004_SIR_ALX.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)

    analysis = argolight.ArgolightEAnalysis(
        name="an analysis",
        description="a description",
        input={
            "argolight_e_image": {"data": data, "name": "image_name", "url": image_url},
            "axis": 2,
        },
        output={},
    )
    return analysis


@pytest.fixture
def argolight_e_vertical():
    image_url = "https://dev.mri.cnrs.fr/attachments/download/2291/201702_RI510_Argolight-1-1_005_SIR_ALX.npy"
    file_path = get_file(image_url)
    data = np.load(file_path)

    analysis = argolight.ArgolightEAnalysis(
        name="an analysis",
        description="a description",
        input={
            "argolight_e_image": {"data": data, "name": "image_name", "url": image_url},
            "axis": 1,
        },
        output={},
    )

    return analysis


def test_run_argolight_b(argolight_b):
    assert argolight_b.run()
    assert argolight_b.processed


def test_run_argolight_e_horizontal(argolight_e_horizontal):
    assert argolight_e_horizontal.run()
    assert argolight_e_horizontal.processed


def test_run_argolight_e_vertical(argolight_e_vertical):
    assert argolight_e_vertical.run()
    assert argolight_e_vertical.processed
