import contextlib
import random

import numpy as np
import pandas as pd

try:
    from hypothesis import assume
    from hypothesis import strategies as st
except ImportError as e:
    raise ImportError(
        "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
    ) from e
import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema
from skimage.exposure import rescale_intensity as skimage_rescale_intensity
from skimage.filters import gaussian as skimage_gaussian
from skimage.util import random_noise as skimage_random_noise

from microscopemetrics.analyses import numpy_to_mm_image
from microscopemetrics.strategies import st_beads_test_data


# Strategies for PSF beads
@st.composite
def st_psf_beads_dataset(
    draw,
    unprocessed_dataset=st_mm_analyses_schema.st_mm_psf_beads_unprocessed_dataset(),
    test_data=st_beads_test_data(),
):
    test_data = draw(test_data)
    psf_beads_unprocessed_dataset = draw(unprocessed_dataset)
    excitation_wavelengths_nm = [405.0, 488.0, 561.0, 642.0, 705.0]
    emission_wavelengths_nm = [435.0, 525.0, 605.0, 692.0, 750.0]

    psf_beads_unprocessed_dataset.input_data.psf_beads_images = [
        numpy_to_mm_image(
            array=image,
            name=f"PSF_image_{i}",
            channel_names=[f"Channel_{c}" for c in range(image.shape[-1])],
            excitation_wavelengths_nm=[
                excitation_wavelengths_nm[c] for c in range(image.shape[-1])
            ],
            emission_wavelengths_nm=[emission_wavelengths_nm[c] for c in range(image.shape[-1])],
        )
        for i, image in enumerate(test_data.pop("images"))
    ]
    # Setting min_distance
    psf_beads_unprocessed_dataset.input_parameters.min_lateral_distance_factor = test_data[
        "min_lateral_distance_factor"
    ][0]
    # Setting the sigmas if available
    with contextlib.suppress(ValueError):
        psf_beads_unprocessed_dataset.input_parameters.sigma_min = (
            min(sigma for image in test_data["applied_sigmas"] for dim in image for sigma in dim)
            - 0.5
        )
        psf_beads_unprocessed_dataset.input_parameters.sigma_max = (
            max(sigma for image in test_data["applied_sigmas"] for dim in image for sigma in dim)
            + 2.0
        )
    # Setting the bit depth to the data type of the image
    image_dtype = {
        a.array_data.dtype for a in psf_beads_unprocessed_dataset.input_data.psf_beads_images
    }
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        psf_beads_unprocessed_dataset.input_parameters.bit_depth = np.iinfo(image_dtype).bits
    elif np.issubdtype(image_dtype, np.floating):
        psf_beads_unprocessed_dataset.input_parameters.bit_depth = np.finfo(image_dtype).bits
    else:
        psf_beads_unprocessed_dataset.input_parameters.bit_depth = None

    return {
        "unprocessed_dataset": psf_beads_unprocessed_dataset,
        "expected_output": test_data,
    }
