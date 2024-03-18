import dataclasses

import numpy as np
import pandas as pd

try:
    from hypothesis import assume
    from hypothesis import strategies as st
except ImportError:
    raise ImportError(
        "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
    )
from microscopemetrics_schema import datamodel as mm_schema
from microscopemetrics_schema import strategies as st_mm_schema
from skimage.exposure import rescale_intensity as skimage_rescale_intensity
from skimage.filters import gaussian as skimage_gaussian
from skimage.util import random_noise as skimage_random_noise

from microscopemetrics import samples as mm_samples
from microscopemetrics.samples import (
    argolight,
    field_illumination,
    numpy_to_mm_image,
    psf_beads,
)


# Strategies for Field Illumination
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

    for image_nr in range(draw(nr_images)):
        # We want a different number of channels for each image
        c_shape = draw(c_image_shape)
        # Generate the image as float64
        image = np.zeros(shape=(y_image_shape, x_image_shape, c_shape), dtype="float64")

        image_target_min_intensities = []
        image_target_max_intensities = []
        centers_generated_y_relative = []
        centers_generated_x_relative = []
        image_dispersions = []
        image_signals = []

        for ch in range(c_shape):
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

            # Generate the channel as float64
            channel = np.zeros(shape=(y_image_shape, x_image_shape), dtype="float64")
            channel[
                int(channel.shape[0] * (0.5 + ch_y_center_rel_offset / 2)),
                int(channel.shape[1] * (0.5 + ch_x_center_rel_offset / 2)),
            ] = 1.0

            channel = skimage_gaussian(
                channel,
                sigma=max(channel.shape) * ch_dispersion,
                mode="constant",
                cval=0.0,
                preserve_range=True,
            )

            # Normalize channel intensity to be between ch_target_min_intensity and ch_target_max_intensity
            # Saturation point is at 1.0 when we rescale later to the target dtype
            channel = skimage_rescale_intensity(
                channel, out_range=(ch_target_min_intensity, ch_target_max_intensity)
            )

            if do_noise:
                # The noise on a 1.0 intensity image is too strong so we rescale the image to
                # the defined signal and then rescale it back to the target intensity
                ch_signal = draw(signal)
                channel = channel * ch_signal
                channel = skimage_random_noise(channel, mode="poisson", clip=False)
                channel = channel / ch_signal
                image_signals.append(ch_signal)

            image[:, :, ch] = channel

        # Rescale to the target dtype
        image = np.clip(image, None, 1)
        image = skimage_rescale_intensity(image, in_range=(0.0, 1.0), out_range=dtype)
        image = np.expand_dims(image, (0, 1))

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
    unprocessed_dataset=st_mm_schema.st_mm_field_illumination_unprocessed_dataset(),
    test_data=st_field_illumination_test_data(),
):
    test_data = draw(test_data)
    field_illumination_unprocessed_dataset = draw(unprocessed_dataset)

    field_illumination_unprocessed_dataset.input.field_illumination_image = [
        numpy_to_mm_image(image, name=f"FI_image_{i}")
        for i, image in enumerate(test_data.pop("images"))
    ]

    # Setting the bit depth to the data type of the image
    image_dtype = {
        a.array_data.dtype
        for a in field_illumination_unprocessed_dataset.input.field_illumination_image
    }
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        field_illumination_unprocessed_dataset.input.bit_depth = np.iinfo(image_dtype).bits
    elif np.issubdtype(image_dtype, np.floating):
        field_illumination_unprocessed_dataset.input.bit_depth = np.finfo(image_dtype).bits
    else:
        field_illumination_unprocessed_dataset.input.bit_depth = None

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
            key_values = {}
            for col in columns:
                key_values[col] = getattr(dataset.output.key_values, col)
        else:
            continue
        table.append(key_values)

    table = [pd.DataFrame(d) for d in table]

    return pd.concat(table, ignore_index=True)


# Strategies for Argolight
# Strategies for Argolight B

# Strategies for Argolight E


# Strategies for PSF beads
@st.composite
def st_psf_beads_test_data(
    draw,
    nr_images=st.integers(min_value=1, max_value=3),
    # We want an odd number of slices so we can have a center slice
    z_image_shape=st.integers(min_value=51, max_value=71).filter(lambda x: x % 2 != 0),
    y_image_shape=st.integers(min_value=512, max_value=1024),
    x_image_shape=st.integers(min_value=512, max_value=1024),
    c_image_shape=st.integers(min_value=1, max_value=3),
    dtype=st.sampled_from([np.uint8, np.uint16, np.float32]),
    do_noise=st.just(True),
    signal=st.floats(min_value=20.0, max_value=1000.0),
    target_min_intensity=st.floats(min_value=0.001, max_value=0.1),
    target_max_intensity=st.floats(min_value=0.5, max_value=0.9),
    sigma_z=st.floats(min_value=0.9, max_value=1.5),
    sigma_x=st.floats(min_value=0.9, max_value=1.5),
    sigma_y=st.floats(min_value=0.9, max_value=1.5),
    min_distance=st.just(25),
    nr_valid_beads=st.integers(min_value=1, max_value=10),
    nr_edge_beads=st.integers(min_value=0, max_value=3),
    nr_out_of_focus_beads=st.integers(min_value=0, max_value=3),
    nr_clustering_beads=st.integers(min_value=0, max_value=3),
):
    output = {
        "images": [],
        "valid_bead_positions": [],
        "edge_bead_positions": [],
        "out_of_focus_bead_positions": [],
        "clustering_bead_positions": [],
        "applied_sigmas": [],
        "min_distance_z": [],
        "min_distance_y": [],
        "min_distance_x": [],
        "signal": [],
        "do_noise": [],
    }

    z_image_shape = draw(z_image_shape)
    y_image_shape = draw(y_image_shape)
    x_image_shape = draw(x_image_shape)
    c_image_shape = draw(c_image_shape)

    do_noise = draw(do_noise)

    dtype = draw(dtype)

    for image_nr in range(draw(nr_images)):
        nr_valid_beads = draw(nr_valid_beads)
        nr_edge_beads = draw(nr_edge_beads)
        nr_out_of_focus_beads = draw(nr_out_of_focus_beads)
        nr_clustering_beads = draw(nr_clustering_beads)
        # We want at least one bead and not too many beads
        assume(
            20 > (nr_valid_beads + nr_edge_beads + nr_out_of_focus_beads + nr_clustering_beads) > 0
        )

        signal = draw(signal)
        target_min_intensity = draw(target_min_intensity)
        target_max_intensity = draw(target_max_intensity)

        sigma_z = draw(sigma_z)
        sigma_y = draw(sigma_y)
        sigma_x = draw(sigma_x)
        applied_sigmas = []

        min_distance_z = draw(min_distance) // 4
        min_distance_y = draw(min_distance)
        min_distance_x = draw(min_distance)

        # We do not want images that are too elongated
        assume(0.5 < (x_image_shape / y_image_shape) < 2)

        # Generate the image as float64
        image = np.zeros(
            shape=(z_image_shape, y_image_shape, x_image_shape, c_image_shape), dtype="float32"
        )

        non_edge_beads_positions = []
        edge_beads_positions = []
        valid_bead_positions = []
        out_of_focus_beads_positions = []
        clustering_beads_positions = []

        # The strategy is as follows:
        # 1. Generate the valid beads in the center of the image.
        # Those equal to valid_beads + out_of_focus_beads + clustering_beads
        # 2. Generate the edge beads in the edge of the image making sure that they are not too close to the valid beads
        # 3. Gradually remove out_of_focus_beads and clustering_beads from those not in the edge
        while len(non_edge_beads_positions) < (
            nr_valid_beads + nr_out_of_focus_beads + nr_clustering_beads
        ):
            z_pos = z_image_shape // 2
            y_pos = draw(
                st.integers(
                    min_value=min_distance_y + 2, max_value=y_image_shape - min_distance_y - 2
                )
            )
            x_pos = draw(
                st.integers(
                    min_value=min_distance_x + 2, max_value=x_image_shape - min_distance_x - 2
                )
            )
            if not non_edge_beads_positions:
                non_edge_beads_positions.append((z_pos, y_pos, x_pos))
            for pos in non_edge_beads_positions:
                if abs(pos[1] - y_pos) <= min_distance_y and abs(pos[2] - x_pos) <= min_distance_x:
                    break
                else:
                    continue
            else:
                non_edge_beads_positions.append((z_pos, y_pos, x_pos))

        while len(edge_beads_positions) < nr_edge_beads:
            z_pos = z_image_shape // 2
            y_pos = draw(
                st.one_of(
                    st.integers(min_value=5, max_value=int(min_distance_y / 2) - 2),
                    st.integers(
                        min_value=y_image_shape - int(min_distance_y / 2) + 2,
                        max_value=y_image_shape - 5,
                    ),
                )
            )
            x_pos = draw(
                st.one_of(
                    st.integers(min_value=5, max_value=int(min_distance_x / 2) - 2),
                    st.integers(
                        min_value=x_image_shape - int(min_distance_x / 2) + 2,
                        max_value=x_image_shape - 5,
                    ),
                )
            )
            if not edge_beads_positions:
                edge_beads_positions.append((z_pos, y_pos, x_pos))
            for pos in edge_beads_positions:
                if abs(pos[1] - y_pos) <= min_distance_y and abs(pos[2] - x_pos) <= min_distance_x:
                    break
                else:
                    continue
            else:
                edge_beads_positions.append((z_pos, y_pos, x_pos))

        for _ in range(nr_out_of_focus_beads):
            pos = non_edge_beads_positions.pop()
            pos = (
                draw(
                    st.one_of(
                        st.integers(min_value=3, max_value=min_distance_z - 2),
                        st.integers(
                            min_value=z_image_shape - min_distance_z + 2,
                            max_value=z_image_shape - 4,
                        ),
                    )
                ),
                pos[1],
                pos[2],
            )
            out_of_focus_beads_positions.append(pos)

        for _ in range(nr_clustering_beads):
            pos_1 = non_edge_beads_positions.pop()
            pos_2 = (
                pos_1[0],
                pos_1[1] + draw(st.sampled_from([-1, 1])),
                pos_1[2] + draw(st.sampled_from([-1, 1])),
            )
            image[pos_1[0], pos_1[1], pos_1[2], :] = np.random.normal(signal * 1.5, signal / 10)
            image[pos_2[0], pos_2[1], pos_2[2], :] = np.random.normal(signal * 1.5, signal / 10)
            clustering_beads_positions.append(
                (pos_1[0], (pos_1[1] + pos_2[1]) // 2, (pos_1[2] + pos_2[2]) // 2)
            )

        for pos in edge_beads_positions:
            image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
        for pos in non_edge_beads_positions:
            image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
            valid_bead_positions = non_edge_beads_positions
        for pos in out_of_focus_beads_positions:
            image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)

        # Apply a gaussian filter to the image
        for ch in range(c_image_shape):
            sigma_correction = 1 + ch * 0.1
            applied_sigmas.append(
                (sigma_z * sigma_correction, sigma_y * sigma_correction, sigma_x * sigma_correction)
            )
            image[:, :, :, ch] = skimage_gaussian(
                image[:, :, :, ch], sigma=applied_sigmas[-1], preserve_range=True
            )

        # Add noise
        if do_noise:
            image = skimage_random_noise(image, mode="poisson", clip=False)

        image = skimage_rescale_intensity(
            image,
            in_range=(0.0, signal / 20),
            out_range=(target_min_intensity, target_max_intensity),
        )

        image = skimage_rescale_intensity(image, in_range=(0.0, 1.0), out_range=dtype)

        image = np.expand_dims(image, 0)

        output["image"].append(image)
        output["valid_bead_positions"].append(valid_bead_positions)
        output["edge_bead_positions"].append(edge_beads_positions)
        output["out_of_focus_bead_positions"].append(out_of_focus_beads_positions)
        output["clustering_bead_positions"].append(clustering_beads_positions)
        output["applied_sigmas"].append(applied_sigmas)
        output["min_distance_z"].append(min_distance_z)
        output["min_distance_y"].append(min_distance_y)
        output["min_distance_x"].append(min_distance_x)
        output["signal"].append(signal)
        output["do_noise"].append(do_noise)

    return output


@st.composite
def st_psf_beads_dataset(
    draw,
    unprocessed_dataset=st_mm_schema.st_mm_psf_beads_unprocessed_dataset(),
    test_data=st_psf_beads_test_data(),
):
    test_data = draw(test_data)
    psf_beads_unprocessed_dataset = draw(unprocessed_dataset)

    psf_beads_unprocessed_dataset.input.psf_beads_image = [
        numpy_to_mm_image(image, name=f"PSF_image_{i}")
        for i, image in enumerate(test_data.pop("images"))
    ]

    # Setting the bit depth to the data type of the image
    image_dtype = {a.array_data.dtype for a in psf_beads_unprocessed_dataset.input.psf_beads_image}
    if len(image_dtype) != 1:
        raise ValueError("All images should have the same data type")
    image_dtype = image_dtype.pop()
    if np.issubdtype(image_dtype, np.integer):
        psf_beads_unprocessed_dataset.input.bit_depth = np.iinfo(image_dtype).bits
    elif np.issubdtype(image_dtype, np.floating):
        psf_beads_unprocessed_dataset.input.bit_depth = np.finfo(image_dtype).bits
    else:
        psf_beads_unprocessed_dataset.input.bit_depth = None

    return {
        "unprocessed_dataset": psf_beads_unprocessed_dataset,
        "expected_output": test_data,
    }
