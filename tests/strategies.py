import dataclasses

import numpy as np
from hypothesis import assume
from hypothesis import strategies as st
from microscopemetrics_schema import strategies as st_mm_schema
from skimage.filters import gaussian as skimage_gaussian
from skimage.util import random_noise as skimage_random_noise

from microscopemetrics import samples as mm_samples
from microscopemetrics.samples import field_illumination


@st.composite
def st_field_illumination_test_data(
    draw,
    x_image_shape=st.integers(min_value=256, max_value=2048),
    y_image_shape=st.integers(min_value=256, max_value=2048),
    c_image_shape=st.integers(min_value=1, max_value=5),
    dtype=st.sampled_from([np.uint8, np.uint16, np.float32]),
    do_noise=st.just(True),
    target_min_intensity=st.floats(min_value=0.1, max_value=0.49),
    target_max_intensity=st.floats(min_value=0.5, max_value=0.9),
    x_center_rel_offset=st.floats(min_value=-0.8, max_value=0.8),
    y_center_rel_offset=st.floats(min_value=-0.8, max_value=0.8),
    dispersion=st.floats(min_value=0.5, max_value=1.0),
):
    """Generate a field illumination image."""
    x_image_shape = draw(x_image_shape)
    y_image_shape = draw(y_image_shape)
    c_image_shape = draw(c_image_shape)
    # We do not want images that are too elongated
    assume(0.5 < (x_image_shape / y_image_shape) < 2)

    dtype = draw(dtype)
    if np.issubdtype(dtype, np.integer):
        max_value = np.iinfo(dtype).max
    elif np.issubdtype(dtype, np.floating):
        max_value = np.finfo(dtype).max
    else:
        raise ValueError("Unsupported datatype")

    # Generate the image as float64
    image = np.zeros(shape=(y_image_shape, x_image_shape, c_image_shape), dtype="float64")

    image_target_min_intensities = []
    image_target_max_intensities = []
    image_y_center_rel_offsets = []
    image_x_center_rel_offsets = []
    image_dispersions = []

    for ch in range(c_image_shape):
        ch_target_min_intensity = draw(target_min_intensity)
        ch_target_max_intensity = draw(target_max_intensity)
        image_target_min_intensities.append(ch_target_min_intensity)
        image_target_max_intensities.append(ch_target_max_intensity)

        ch_y_center_rel_offset = draw(y_center_rel_offset)
        ch_x_center_rel_offset = draw(x_center_rel_offset)
        image_y_center_rel_offsets.append(ch_y_center_rel_offset)
        image_x_center_rel_offsets.append(ch_x_center_rel_offset)

        ch_dispersion = draw(dispersion)
        image_dispersions.append(ch_dispersion)

        # Generate the channel as float64
        channel = np.zeros(shape=(y_image_shape, x_image_shape), dtype="float64")
        y_center = int(channel.shape[0] * (0.5 + ch_y_center_rel_offset / 2))
        x_center = int(channel.shape[1] * (0.5 + ch_x_center_rel_offset / 2))

        # Add a gaussian field at the center of the channel
        channel[y_center, x_center] = 1.0
        channel = skimage_gaussian(
            channel, sigma=max(channel.shape) * ch_dispersion, preserve_range=True
        )

        # Normalize channel intensity to be between ch_target_min_intensity and ch_target_max_intensity
        # Saturation point is at 1.0 when we rescale later to the target dtype
        channel = channel - np.min(channel)
        channel = channel / np.max(channel)
        channel = (
            channel * (ch_target_max_intensity - ch_target_min_intensity) + ch_target_min_intensity
        )

        # Add noise
        if do_noise:
            channel = skimage_random_noise(channel, mode="poisson", clip=False)

        image[:, :, ch] = channel

    # Rescale to the target dtype
    image = np.clip(image, None, 1)
    image = image * max_value
    image = image.astype(dtype)
    image = np.expand_dims(image, (0, 1))

    return {
        "image": image,
        "y_center_rel_offsets": image_y_center_rel_offsets,
        "x_center_rel_offsets": image_x_center_rel_offsets,
        "target_min_intensities": image_target_min_intensities,
        "target_max_intensities": image_target_max_intensities,
        "dispersions": image_dispersions,
        "do_noise": do_noise,
    }


@st.composite
def st_field_illumination_dataset(
    draw,
    unprocessed_dataset=st_mm_schema.st_mm_field_illumination_unprocessed_dataset(),
    field_illumination_test_data=st_field_illumination_test_data(),
):
    unprocessed_dataset = draw(unprocessed_dataset)
    field_illumination_test_data = draw(field_illumination_test_data)
    unprocessed_dataset.input.field_illumination_image = draw(
        st_mm_schema.st_mm_image_as_numpy(
            shape=st.just(field_illumination_test_data["image"].shape),
            data=field_illumination_test_data["image"],
        )
    )
    unprocessed_analysis = field_illumination.FieldIlluminationAnalysis(
        **dataclasses.asdict(unprocessed_dataset)
    )

    return {"unprocessed_analysis": unprocessed_analysis, "expected_output": unprocessed_dataset}
