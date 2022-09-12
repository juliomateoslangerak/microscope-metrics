import pytest
from os import path
from tests.constants import *

from microscopemetrics.samples import psf_beads
import numpy as np


@pytest.fixture()
def psf_beads_analysis():
    temp_dir = path.abspath(TEST_DATA_DIR)
    file_name = '20191206_100xOil_A647_Cy3_FITC_DAPI_ri-1.512_na-1.4_100nm_561_002_SIR.npy'
    file_url = 'http://dev.mri.cnrs.fr/attachments/download/2295/psf_beads_EM-488_MAG-40.npy'
    try:
        data = np.load(path.join(temp_dir, file_name))
    except FileNotFoundError as e:
        repos = np.DataSource(temp_dir)
        file_obj = repos.open(file_url)
        data = np.load(file_obj.name)

    analysis = psf_beads.PSFBeadsAnalysis()
    analysis.input.data = {'beads_image': data}
    analysis.set_metadata('theoretical_fwhm_lateral_res', 0.300)
    analysis.set_metadata('theoretical_fwhm_axial_res', 0.800)
    analysis.set_metadata('pixel_size', (.35, .06, .06))

    return analysis


def test_run_psf_beads(psf_beads_analysis):
    assert psf_beads_analysis.run()
    assert psf_beads_analysis.output
