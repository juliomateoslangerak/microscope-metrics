import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from microscopemetrics.samples import psf_beads
from microscopemetrics.strategies import strategies as st_mm


@pytest.mark.instantiation
@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_psf_beads_analysis_instantiation(dataset):
    assert isinstance(dataset["unprocessed_analysis"], psf_beads.PSFBeadsAnalysis)
    assert dataset["unprocessed_analysis"].name
    assert dataset["unprocessed_analysis"].description
    assert dataset["unprocessed_analysis"].microscope
    assert dataset["unprocessed_analysis"].input


@pytest.mark.run
@given(st_mm.st_psf_beads_dataset())
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_run(dataset):
    assert not dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].run()
    assert dataset["unprocessed_analysis"].processed
    assert dataset["unprocessed_analysis"].output


@pytest.mark.analysis
@given(
    st_mm.st_psf_beads_dataset(
        psf_beads_test_data=st_mm.st_psf_beads_test_data(
            nr_edge_beads=st.just(0),
            nr_out_of_focus_beads=st.just(0),
            nr_clustering_beads=st.just(0),
        )
    )
)
@settings(max_examples=1, suppress_health_check=[HealthCheck.too_slow], deadline=20000)
def test_psf_beads_analysis_valid_beads(dataset):
    psf_beads_dataset = dataset["unprocessed_analysis"]
    expected_output = dataset["expected_output"]
    psf_beads_dataset.run()

    assert psf_beads_dataset.processed

    assert len(psf_beads_dataset.output.analyzed_bead_centroids) == len(
        psf_beads_dataset.input.psf_beads_images
    )


"""
        "valid_bead_positions": valid_bead_positions,
        "edge_bead_positions": edge_beads_positions,
        "out_of_focus_bead_positions": out_of_focus_beads_positions,
        "clustering_bead_positions": clustering_beads_positions,
        "applied_sigmas": applied_sigmas,
        "signal": signal,
        "do_noise": do_noise,
"""


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
