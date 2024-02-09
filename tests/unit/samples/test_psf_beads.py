import numpy as np
import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from microscopemetrics import SaturationError
from microscopemetrics.samples import psf_beads, numpy_to_image_byref
from tests import strategies as st_mm
from tests.test_utilities import get_file


@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_psf_beads_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], psf_beads.PSFBeadsAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def test_psf_beads_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output

# from tests.test_utilities import get_file
#
# from microscopemetrics.samples import psf_beads
# import numpy as np
#
#
# @pytest.fixture()
# def psf_beads_analysis():
#     file_path = get_file(
#         "https://dev.mri.cnrs.fr/attachments/download/3072/psf_beads_EM-488_MAG-40.npy"
#     )
#     data = np.load(file_path)
#
#     analysis = psf_beads.PSFBeadsAnalysis()
#     analysis.set_data("beads_image", data)
#     analysis.set_metadata("theoretical_fwhm_lateral_res", 0.300)
#     analysis.set_metadata("theoretical_fwhm_axial_res", 0.800)
#     analysis.set_metadata("pixel_size", (0.35, 0.06, 0.06))
#
#     return analysis
#
#
# def test_run_psf_beads(psf_beads_analysis):
#     assert psf_beads_analysis.run()
#     assert psf_beads_analysis.output
