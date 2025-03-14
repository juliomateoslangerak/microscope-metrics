from dataclasses import asdict

import pytest
from microscopemetrics_schema.datamodel import (
    PSFBeads,
    PSFBeadsDataset,
    PSFBeadsInputData,
    PSFBeadsInputParameters,
    PSFBeadsKeyMeasurements,
    PSFBeadsOutput,
)

from microscopemetrics.analyses.psf_beads import analyse_psf_beads
from tests.helper_functions import filter_dict, remove_np_pd_data


@pytest.mark.parametrize(
    "images_dataset_generator",
    [
        {
            "dataset_path": "psf_beads_datasets",
            "dataset_target_class": PSFBeadsDataset,
            "sample_target_class": PSFBeads,
            "input_parameters_target_class": PSFBeadsInputParameters,
            "input_data_target_class": PSFBeadsInputData,
            "input_images_field": "psf_beads_images",
            "output_target_class": PSFBeadsOutput,
            "key_measurements_target_class": PSFBeadsKeyMeasurements,
            "do_generate_missing_key_measurements": True,
            "do_generate_missing_input_parameters": True,
        }
    ],
    indirect=True,
)
def test_psf_beads(images_dataset_generator):
    expected_output = asdict(images_dataset_generator.output)
    images_dataset_generator.output = None
    assert analyse_psf_beads(images_dataset_generator)
    assert images_dataset_generator.processed

    analyzed_output = asdict(images_dataset_generator.output)

    analyzed_output = filter_dict(
        expected=expected_output,
        analyzed=analyzed_output,
    )
    expected_output = remove_np_pd_data(expected_output)
    analyzed_output = remove_np_pd_data(analyzed_output)

    assert analyzed_output["key_measurements"] == expected_output["key_measurements"]
