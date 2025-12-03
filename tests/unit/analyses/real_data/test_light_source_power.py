from dataclasses import asdict

import pytest
from microscopemetrics_schema.datamodel import (
    LightSourcePowerDataset,
    LightSourcePowerInputData,
    LightSourcePowerInputParameters,
    LightSourcePowerKeyMeasurement,
    LightSourcePowerOutput,
)

from microscopemetrics.analyses.light_source_power import analyse_light_source_power
from tests.helper_functions import (
    assert_key_measurements_equality,
    filter_dict,
    remove_np_pd_data,
)
from tests.unit.analyses.real_data.conftest import (
    build_dataset_from_dir,
    get_test_subdirectories,
)


def pytest_generate_tests(metafunc):
    if "dataset_dir" in metafunc.fixturenames:
        test_dirs = get_test_subdirectories("light_source_power_datasets")
        metafunc.parametrize("dataset_dir", test_dirs)


@pytest.mark.parametrize(
    "data_gen_args",
    [
        {
            "dataset_target_class": LightSourcePowerDataset,
            "input_parameters_target_class": LightSourcePowerInputParameters,
            "input_data_target_class": LightSourcePowerInputData,
            "output_target_class": LightSourcePowerOutput,
            "key_measurements_target_class": LightSourcePowerKeyMeasurement,
            "input_non_images_field": "power_measurements",
            "do_generate_missing_key_measurements": True,
            # "do_generate_missing_input_parameters": True,
        }
    ],
)
def test_light_source_power(data_gen_args, dataset_dir):
    dataset_tested = build_dataset_from_dir(
        dataset_dir=dataset_dir,
        **data_gen_args,
    )
    expected_output = asdict(dataset_tested.output)
    dataset_tested.output = None
    assert analyse_light_source_power(dataset_tested)
    assert dataset_tested.processed

    analyzed_output = asdict(dataset_tested.output)

    analyzed_output = filter_dict(
        expected=expected_output,
        analyzed=analyzed_output,
    )
    expected_output = remove_np_pd_data(expected_output)
    analyzed_output = remove_np_pd_data(analyzed_output)

    assert assert_key_measurements_equality(
        expected=expected_output["key_measurements"], actual=analyzed_output["key_measurements"]
    ), "Key measurements do not match"
