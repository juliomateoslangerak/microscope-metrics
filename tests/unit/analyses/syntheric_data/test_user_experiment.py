import numpy as np
import pandas as pd
import pytest
from hypothesis import given, reproduce_failure, settings
from hypothesis import strategies as st
from microscopemetrics_schema import datamodel as mm_schema
from microscopemetrics_schema import strategies as st_mm_schema
from scipy import ndimage
from skimage.filters import gaussian
from skimage.util import random_noise as skimage_random_noise

from microscopemetrics.analyses import psf_beads

# from microscopemetrics.strategies.user_experiment import (
#     st_user_experiment_dataset,
#     st_user_experiment_test_data,
# )
#
# @pytest.skip
# @given(st_user_experiment_dataset())
# @settings(max_examples=1)
# def test_user_experiment_analysis_instantiation(dataset):
#     dataset = dataset["unprocessed_dataset"]
#     assert isinstance(dataset, mm_schema.UserExperimentDataset)
#     assert dataset.name
#     assert dataset.description
#     assert dataset.microscope
#     assert dataset.input_parameters
