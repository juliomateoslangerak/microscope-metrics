import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema
import numpy as np
import pandas as pd
import pytest
from hypothesis import given, reproduce_failure, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema
from scipy import ndimage
from skimage.exposure import rescale_intensity
from skimage.filters import gaussian

from microscopemetrics import AnalysisError, DataFormatError
from microscopemetrics.analyses import stage_drift
from microscopemetrics.strategies import st_beads_test_data
from microscopemetrics.strategies.stage_drift import st_stage_drift_dataset


@given(st_stage_drift_dataset())
@settings(max_examples=1)
def test_stage_drift_analysis_instantiation(stage_drift_dataset):
    stage_drift_dataset = stage_drift_dataset["unprocessed_dataset"]
    assert isinstance(stage_drift_dataset, mm_schema.StageDriftDataset)
    assert stage_drift_dataset.name
    assert stage_drift_dataset.description
    assert stage_drift_dataset.microscope
    assert stage_drift_dataset.input_parameters
