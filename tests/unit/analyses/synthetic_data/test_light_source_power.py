import tempfile

import pytest
from hypothesis import given, note, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics.analyses import (
    csv_power_measurements_parser,
    extract_power_measurements_csv,
    light_source_power,
)
from microscopemetrics.strategies.light_source_power import (
    st_light_source_power_dataset,
    st_light_source_power_test_data,
)


@given(st_light_source_power_dataset())
@settings(max_examples=1)
def test_light_source_power_analysis_instantiation(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert isinstance(dataset, mm_schema.LightSourcePowerDataset)
    assert dataset.name
    assert dataset.description
    assert dataset.microscope
    assert dataset.input_parameters


@given(st_light_source_power_dataset())
@settings(max_examples=1)
def test_light_source_power_analysis_run(dataset):
    dataset = dataset["unprocessed_dataset"]
    assert not dataset.processed
    assert light_source_power.analyse_light_source_power(dataset)
    assert dataset.processed


@given(st_light_source_power_dataset())
@settings(max_examples=1)
def test_light_source_power_input_data_to_csv(light_source_power_dataset):
    light_source_power_dataset = light_source_power_dataset["unprocessed_dataset"]
    assert not light_source_power_dataset.processed
    with tempfile.TemporaryDirectory() as tmp_dir:
        extract_power_measurements_csv(
            light_source_power_dataset, output_path=tmp_dir + "/test.csv"
        )
        read_data = csv_power_measurements_parser(tmp_dir + "/test.csv")

    assert read_data
    assert isinstance(read_data, list)
    assert all(isinstance(item, mm_schema.PowerMeasurement) for item in read_data)
