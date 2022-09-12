import pytest
from os import path
from tests.constants import *

from microscopemetrics.samples import argolight
import numpy as np


@pytest.fixture
def argolight_b():
    temp_dir = path.abspath(TEST_DATA_DIR)
    file_name = '201702_RI510_Argolight-1-1_010_SIR_ALX.npy'
    file_url = 'http://dev.mri.cnrs.fr/attachments/download/2290/201702_RI510_Argolight-1-1_010_SIR_ALX.npy'
    try:
        data = np.load(path.join(temp_dir, file_name))
    except FileNotFoundError as e:
        repos = np.DataSource(temp_dir)
        file_obj = repos.open(file_url)
        data = np.load(file_obj.name)

    analysis = argolight.ArgolightBAnalysis()
    analysis.input.data = {'argolight_b': data}
    analysis.set_metadata('spots_distance', 5)
    analysis.set_metadata('pixel_size', (.125, .39, .39))

    return analysis


@pytest.fixture
def argolight_e_horizontal():
    temp_dir = path.abspath(TEST_DATA_DIR)
    file_name = '201702_RI510_Argolight-1-1_005_SIR_ALX.npy'
    file_url = 'http://dev.mri.cnrs.fr/attachments/download/2292/201702_RI510_Argolight-1-1_005_SIR_ALX.npy'
    try:
        data = np.load(path.join(temp_dir, file_name))
    except FileNotFoundError as e:
        repos = np.DataSource(temp_dir)
        repos.open(file_url)
        raise Exception from e

    analysis = argolight.ArgolightEAnalysis()
    analysis.input.data = {'argolight_e': data}
    analysis.set_metadata('pixel_size', (.125, .39, .39))
    analysis.set_metadata('axis', 2)

    return analysis


@pytest.fixture
def argolight_e_vertical():
    temp_dir = path.abspath(TEST_DATA_DIR)
    file_name = '201702_RI510_Argolight-1-1_004_SIR_ALX.npy'
    file_url = 'http://dev.mri.cnrs.fr/attachments/download/2291/201702_RI510_Argolight-1-1_004_SIR_ALX.npy'
    try:
        data = np.load(path.join(temp_dir, file_name))
    except FileNotFoundError as e:
        repos = np.DataSource(temp_dir)
        repos.open(file_url)
        raise Exception from e

    analysis = argolight.ArgolightEAnalysis()
    analysis.input.data = {'argolight_e': data}
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
