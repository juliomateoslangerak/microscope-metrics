# import pytest
# from tests.test_utilities import get_file
#
# from microscopemetrics.samples import psf_beads
# import numpy as np
#
#
# @pytest.fixture()
# def psf_beads_analysis():
#     file_path = get_file(
#         "https://dev.mri.cnrs.fr/attachments/download/2295/psf_beads_EM-488_MAG-40.npy"
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
