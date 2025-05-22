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


# Strategies for Field Illumination
def _gen_field_illumination_channel(
    y_shape: int,
    x_shape: int,
    y_center_rel_offset: float,
    x_center_rel_offset: float,
    dispersion: float,
    target_min_intensity: float,
    target_max_intensity: float,
    do_noise: bool,
    signal: int,
):
    # Generate the channel as float64
    channel = np.zeros(shape=(y_shape, x_shape), dtype="float64")
    channel[
        int(channel.shape[0] * (0.5 + y_center_rel_offset / 2)),
        int(channel.shape[1] * (0.5 + x_center_rel_offset / 2)),
    ] = 1.0

    channel = skimage_gaussian(
        channel,
        sigma=max(channel.shape) * dispersion,
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


def _gen_field_illumination_image(
    y_shape: int,
    x_shape: int,
    c_shape: int,
    y_center_rel_offset: list[float],
    x_center_rel_offset: list[float],
    dispersion: list[float],
    target_min_intensity: list[float],
    target_max_intensity: list[float],
    do_noise: bool,
    signal: list[int],
    dtype: np.dtype,
):
    # Generate the image as float64
    image = np.zeros(shape=(y_shape, x_shape, c_shape), dtype="float64")

    for ch in range(c_shape):
        image[:, :, ch] = _gen_field_illumination_channel(
            y_shape=y_shape,
            x_shape=x_shape,
            y_center_rel_offset=y_center_rel_offset[ch],
            x_center_rel_offset=x_center_rel_offset[ch],
            dispersion=dispersion[ch],
            target_min_intensity=target_min_intensity[ch],
            target_max_intensity=target_max_intensity[ch],
            do_noise=do_noise,
            signal=signal[ch],
        )

    # Rescale to the target dtype
    image = np.clip(image, None, 1)
    image = skimage_rescale_intensity(image, in_range=(0.0, 1.0), out_range=dtype)
    image = np.expand_dims(image, (0, 1))

    return image


@st.composite
def st_field_illumination_test_data(
    draw,
    nr_images=st.integers(min_value=1, max_value=3),
    y_image_shape=st.integers(min_value=512, max_value=1024),
    x_image_shape=st.integers(min_value=512, max_value=1024),
    c_image_shape=st.integers(min_value=1, max_value=3),
    dtype=st.sampled_from([np.uint8, np.uint16]),
    signal=st.integers(min_value=100, max_value=1000),
    do_noise=st.just(True),
    target_min_intensity=st.floats(min_value=0.1, max_value=0.45),
    target_max_intensity=st.floats(min_value=0.5, max_value=0.9),
    center_y_relative=st.floats(min_value=-0.8, max_value=0.8),
    center_x_relative=st.floats(min_value=-0.8, max_value=0.8),
    dispersion=st.floats(min_value=0.5, max_value=1.0),
):
    output = {
        "images": [],
        "centers_generated_y_relative": [],
        "centers_generated_x_relative": [],
        "target_min_intensities": [],
        "target_max_intensities": [],
        "dispersions": [],
        "do_noise": [],
        "signals": [],
    }

    y_image_shape = draw(y_image_shape)
    x_image_shape = draw(x_image_shape)

    do_noise = draw(do_noise)

    dtype = draw(dtype)

    for _ in range(draw(nr_images)):
        # We want a different number of channels for each image
        _c_image_shape = draw(c_image_shape)

        image_target_min_intensities = []
        image_target_max_intensities = []
        centers_generated_y_relative = []
        centers_generated_x_relative = []
        image_dispersions = []
        image_signals = []

        for _ in range(_c_image_shape):
            ch_target_min_intensity = draw(target_min_intensity)
            ch_target_max_intensity = draw(target_max_intensity)
            # if the dtype is uint8, the difference between the min and max intensity should be less than 0.5
            # otherwise, with only a few intensity levels, the detection will not be accurate. It is anyway a very
            # unlikely scenario in a real world situation
            if dtype == np.uint8:
                assume((ch_target_max_intensity - ch_target_min_intensity) > 0.7)
            image_target_min_intensities.append(ch_target_min_intensity)
            image_target_max_intensities.append(ch_target_max_intensity)

            ch_y_center_rel_offset = draw(center_y_relative)
            ch_x_center_rel_offset = draw(center_x_relative)
            centers_generated_y_relative.append(ch_y_center_rel_offset)
            centers_generated_x_relative.append(ch_x_center_rel_offset)

            ch_dispersion = draw(dispersion)
            image_dispersions.append(ch_dispersion)

            ch_signal = draw(signal)
            image_signals.append(ch_signal)

        image = _gen_field_illumination_image(
            y_shape=y_image_shape,
            x_shape=x_image_shape,
            c_shape=_c_image_shape,
            y_center_rel_offset=centers_generated_y_relative,
            x_center_rel_offset=centers_generated_x_relative,
            dispersion=image_dispersions,
            target_min_intensity=image_target_min_intensities,
            target_max_intensity=image_target_max_intensities,
            do_noise=do_noise,
            signal=image_signals,
            dtype=dtype,
        )

        output["images"].append(image)
        output["centers_generated_y_relative"].append(centers_generated_y_relative)
        output["centers_generated_x_relative"].append(centers_generated_x_relative)
        output["target_min_intensities"].append(image_target_min_intensities)
        output["target_max_intensities"].append(image_target_max_intensities)
        output["dispersions"].append(image_dispersions)
        output["do_noise"].append(do_noise)
        output["signals"].append(image_signals)

    return output


@st.composite
def st_field_illumination_dataset(
    draw,
    unprocessed_dataset=st_mm_analyses_schema.st_mm_field_illumination_unprocessed_dataset(),
    test_data=st_field_illumination_test_data(),
):
    test_data = draw(test_data)
    field_illumination_unprocessed_dataset = draw(unprocessed_dataset)

    field_illumination_unprocessed_dataset.input_data.field_illumination_image = [
        numpy_to_mm_image(
            array=image,
            name=f"FI_image_{i}",
            channel_names=[f"Channel_{i}{j}" for j in range(image.shape[-1])],
        )
        for i, image in enumerate(test_data.pop("images"))
    ]

    # Setting the bit depth to the data type of the image
    image_dtype = {
        a.array_data.dtype
        for a in field_illumination_unprocessed_dataset.input_data.field_illumination_image
    }
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = np.iinfo(
            image_dtype
        ).bits
    elif np.issubdtype(image_dtype, np.floating):
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = np.finfo(
            image_dtype
        ).bits
    else:
        field_illumination_unprocessed_dataset.input_parameters.bit_depth = None

    return {
        "unprocessed_dataset": field_illumination_unprocessed_dataset,
        "expected_output": test_data,
    }


@st.composite
def st_field_illumination_table(
    draw,
    nr_rows=st.integers(min_value=1, max_value=50),
):
    nr_rows = draw(nr_rows)
    columns = [
        "bottom_center_intensity_mean",
        "bottom_center_intensity_ratio",
        "channel_nr",
    ]
    table = []
    for _ in range(nr_rows):
        dataset = draw(st_field_illumination_dataset())["unprocessed_dataset"]
        dataset.run()
        if dataset.processed:
            key_values = {col: getattr(dataset.output.key_values, col) for col in columns}
        else:
            continue
        table.append(key_values)

    table = [pd.DataFrame(d) for d in table]

    return pd.concat(table, ignore_index=True)
