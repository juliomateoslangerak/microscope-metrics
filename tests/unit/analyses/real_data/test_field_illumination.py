from dataclasses import asdict

import pytest
from microscopemetrics_schema.datamodel import (
    FieldIlluminationDataset,
    FieldIlluminationInputData,
    FieldIlluminationInputParameters,
    FieldIlluminationKeyMeasurements,
    FieldIlluminationOutput,
    HomogeneousField,
)

from microscopemetrics.analyses.field_illumination import analyse_field_illumination
from tests.helper_functions import filter_dict, remove_np_pd_data


@pytest.mark.parametrize(
    "images_dataset_generator",
    [
        {
            "dataset_path": "field_illumination_datasets",
            "dataset_target_class": FieldIlluminationDataset,
            "sample_target_class": HomogeneousField,
            "input_parameters_target_class": FieldIlluminationInputParameters,
            "input_data_target_class": FieldIlluminationInputData,
            "input_images_field": "field_illumination_image",
            "output_target_class": FieldIlluminationOutput,
            "key_measurements_target_class": FieldIlluminationKeyMeasurements,
            "do_generate_missing_key_measurements": False,
            "do_generate_missing_input_parameters": False,
        }
    ],
    indirect=True,
)
def test_field_illumination(images_dataset_generator):
    expected_output = asdict(images_dataset_generator.output)
    images_dataset_generator.output = None
    assert analyse_field_illumination(images_dataset_generator)
    assert images_dataset_generator.processed

    analyzed_output = asdict(images_dataset_generator.output)

    analyzed_output = filter_dict(
        expected=expected_output,
        analyzed=analyzed_output,
    )
    expected_output = remove_np_pd_data(expected_output)
    analyzed_output = remove_np_pd_data(analyzed_output)

    assert analyzed_output["key_measurements"] == expected_output["key_measurements"]
