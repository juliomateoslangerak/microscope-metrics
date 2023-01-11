import numpy as np

from microscopemetrics.utilities import utilities


def test_is_saturated():
    unsaturated_data = np.zeros((10, 10), "uint8")
    unsaturated_data[0:5, ...] = 100
    saturated_data = np.zeros((10, 10), "uint8")
    saturated_data[0:5, ...] = 255  # 50% of the image is saturated
    assert not utilities.is_saturated(unsaturated_data)
    assert not utilities.is_saturated(unsaturated_data, thresh=0.4)
    assert utilities.is_saturated(saturated_data)
    assert not utilities.is_saturated(saturated_data, thresh=0.6)
