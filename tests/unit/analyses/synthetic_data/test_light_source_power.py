import pytest
from hypothesis import given, note, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema

from microscopemetrics.analyses import light_source_power
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
