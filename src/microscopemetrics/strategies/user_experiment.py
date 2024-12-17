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
from microscopemetrics_schema import strategies as st_mm_schema
from skimage.exposure import rescale_intensity as skimage_rescale_intensity
from skimage.filters import gaussian as skimage_gaussian
from skimage.util import random_noise as skimage_random_noise

from microscopemetrics.analyses import numpy_to_mm_image


# Strategies for user experiment
def _gen_user_experiment_channel(
    z_shape: int,
    y_shape: int,
    x_shape: int,
    t_shape: int,
    lines_nr: int,
    sigma: float,
    target_min_intensity: float,
    target_max_intensity: float,
    do_noise: bool,
    signal: int,
):
    # Generate the channel as float64
    channel = np.zeros(shape=(t_shape, z_shape, y_shape, x_shape), dtype="float64")

    # draw lines_nr lines through the center of the image in z across the y and x dimensions
    for i in range(lines_nr):
        channel[
            :,  # Time
            int(channel.shape[0] * 0.5),  # Z
            :,  # Y
            int(channel.shape[2] * i / lines_nr),  # X
        ] = 1.0
        channel[
            :,
            int(channel.shape[0] * 0.5),
            int(channel.shape[1] * i / lines_nr),
            :,
        ] = 1.0
        channel[
            :,
            :,
            int(channel.shape[1] * i / lines_nr),
            int(channel.shape[1] * i / lines_nr),
        ] = 1.0

    channel = skimage_gaussian(
        channel,
        sigma=sigma,
        mode="constant",
        preserve_range=True,
    )

    # Normalize channel intensity to be between target_min_intensity and target_max_intensity
    # Saturation point is at 1.0 when we rescale later to the target dtype
    channel = skimage_rescale_intensity(
        channel, out_range=(target_min_intensity, target_max_intensity)
    )

    if do_noise:
        # The noise on a 1.0 intensity image is too strong, so we rescale the image to
        # the defined signal and then rescale it back to the target intensity
        channel = channel * signal
        channel = skimage_random_noise(channel, mode="poisson", clip=False)
        channel = channel / signal

    return channel


def _gen_user_experiment_image(
    z_shape: int,
    y_shape: int,
    x_shape: int,
    c_shape: int,
    lines_nr: list[int],
    sigma: list[float],
    target_min_intensity: list[float],
    target_max_intensity: list[float],
    do_noise: bool,
    signal: list[int],
    dtype: np.dtype,
    t_shape: int = 1,  # Added the time dimension here. Not used in the function yet
):
    # Generate the image as float64
    image = np.zeros(shape=(t_shape, z_shape, y_shape, x_shape, c_shape), dtype="float64")

    for ch in range(c_shape):
        image[..., ch] = _gen_user_experiment_channel(
            z_shape=z_shape,
            y_shape=y_shape,
            x_shape=x_shape,
            t_shape=t_shape,
            lines_nr=lines_nr[ch],
            sigma=sigma[ch],
            target_min_intensity=target_min_intensity[ch],
            target_max_intensity=target_max_intensity[ch],
            do_noise=do_noise,
            signal=signal[ch],
        )

    # Rescale to the target dtype
    image = np.clip(image, None, 1)
    image = skimage_rescale_intensity(image, in_range=(0.0, 1.0), out_range=dtype)

    return image


@st.composite
def st_user_experiment_test_data(
    draw,
    nr_images=st.integers(min_value=1, max_value=3),
    z_image_shape=st.integers(min_value=2, max_value=50),
    y_image_shape=st.integers(min_value=512, max_value=1024),
    x_image_shape=st.integers(min_value=512, max_value=1024),
    c_image_shape=st.integers(min_value=1, max_value=3),
    dtype=st.sampled_from([np.uint8, np.uint16, np.float32]),
    do_noise=st.just(True),
    signal=st.floats(min_value=20.0, max_value=1000.0),
    target_min_intensity=st.floats(min_value=0.001, max_value=0.1),
    target_max_intensity=st.floats(min_value=0.5, max_value=0.9),
    sigma=st.floats(min_value=2.0, max_value=10.0),
    nr_orthogonal_rois=st.integers(min_value=0, max_value=3),
    nr_profile_rois=st.integers(min_value=0, max_value=3),
):
    pass


@st.composite
def st_user_experiment_dataset(
    draw,
    unprocessed_dataset=st_mm_schema.st_mm_user_experiment_unprocessed_dataset(),
    test_data=st_user_experiment_test_data(),
):
    pass
