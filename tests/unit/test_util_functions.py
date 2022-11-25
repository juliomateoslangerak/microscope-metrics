from microscopemetrics.utilities import utilities
import pytest
from tests.test_utilities import get_file
import numpy as np



@pytest.fixture
def is_saturated_b():
   data = np.zeros((100,100),'uint8')
   data[10,10]=255
   return utilities.is_saturated(data)

def test_run_is_saturated():
    assert not(is_saturated_b())
