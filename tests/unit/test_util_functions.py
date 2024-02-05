import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from microscopemetrics.utilities import utilities


@given(st.sampled_from([np.uint8, np.uint16, np.float32]))
def test_is_saturated(data_type):
    if np.issubdtype(data_type, np.integer):
        max_value = np.iinfo(data_type).max
    elif np.issubdtype(data_type, np.floating):
        max_value = np.finfo(data_type).max
    else:
        raise ValueError("Unsupported datatype")
    unsaturated_data = np.zeros((10, 10), data_type)
    unsaturated_data[0:5, ...] = max_value / 2  # 50% of the image is saturated
    saturated_data = np.zeros((10, 10), data_type)
    saturated_data[0:5, ...] = max_value  # 50% of the image is saturated
    assert not utilities.is_saturated(unsaturated_data)
    assert not utilities.is_saturated(unsaturated_data, threshold=0.4)
    assert utilities.is_saturated(saturated_data)
    assert not utilities.is_saturated(saturated_data, threshold=0.6)
