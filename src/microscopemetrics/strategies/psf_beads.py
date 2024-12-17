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


# Strategies for PSF beads
def _gen_psf_beads_channel():
    pass


def _gen_psf_beads_image(
    z_image_shape: int,
    y_image_shape: int,
    x_image_shape: int,
    c_image_shape: int,
    nr_valid_beads: int,
    nr_edge_beads: int,
    nr_out_of_focus_beads: int,
    nr_clustering_beads: int,
    min_distance_z: int,
    min_distance_y: int,
    min_distance_x: int,
    sigma_z: float,
    sigma_y: float,
    sigma_x: float,
    target_min_intensity: float,
    target_max_intensity: float,
    do_noise: bool,
    signal: int,
    dtype: np.dtype,
):
    # Generate the image as float64
    image = np.zeros(
        shape=(z_image_shape, y_image_shape, x_image_shape, c_image_shape),
        dtype="float32",
    )

    applied_sigmas = []
    non_edge_bead_positions = []
    edge_bead_positions = []
    valid_bead_positions = []
    out_of_focus_bead_positions = []
    clustering_bead_positions = []

    # The strategy is as follows:
    # 1. Generate the valid beads in the center of the image.
    # Those equal to valid_beads + out_of_focus_beads + clustering_beads
    # 2. Generate the edge beads in the edge of the image making sure that they are not too close to the valid beads
    # 3. Gradually remove out_of_focus_beads and clustering_beads from those not in the edge
    while len(non_edge_bead_positions) < (
        nr_valid_beads + nr_out_of_focus_beads + nr_clustering_beads
    ):
        z_pos = z_image_shape // 2
        y_pos = random.randint(min_distance_y + 2, y_image_shape - min_distance_y - 2)
        x_pos = random.randint(min_distance_x + 2, x_image_shape - min_distance_x - 2)
        if not non_edge_bead_positions:
            non_edge_bead_positions.append((z_pos, y_pos, x_pos))
        for pos in non_edge_bead_positions:
            if abs(pos[1] - y_pos) <= min_distance_y and abs(pos[2] - x_pos) <= min_distance_x:
                break
            else:
                continue
        else:
            non_edge_bead_positions.append((z_pos, y_pos, x_pos))

    while len(edge_bead_positions) < nr_edge_beads:
        z_pos = z_image_shape // 2
        y_pos = random.choice(
            [
                random.randint(5, min_distance_y // 2 - 2),
                random.randint(y_image_shape - min_distance_y // 2 + 2, y_image_shape - 5),
            ]
        )
        x_pos = random.choice(
            [
                random.randint(5, min_distance_x // 2 - 2),
                random.randint(x_image_shape - min_distance_x // 2 + 2, x_image_shape - 5),
            ]
        )
        if not edge_bead_positions:
            edge_bead_positions.append((z_pos, y_pos, x_pos))
        for pos in edge_bead_positions:
            if abs(pos[1] - y_pos) <= min_distance_y and abs(pos[2] - x_pos) <= min_distance_x:
                break
            else:
                continue
        else:
            edge_bead_positions.append((z_pos, y_pos, x_pos))

    for _ in range(nr_out_of_focus_beads):
        pos = non_edge_bead_positions.pop()
        pos = (
            random.choice(
                [
                    random.randint(3, min_distance_z - 2),
                    random.randint(z_image_shape - min_distance_z + 2, z_image_shape - 4),
                ]
            ),
            pos[1],
            pos[2],
        )
        out_of_focus_bead_positions.append(pos)

    for _ in range(nr_clustering_beads):
        pos_1 = non_edge_bead_positions.pop()
        pos_2 = (
            pos_1[0],
            pos_1[1] + random.choice([-1, 1]),
            pos_1[2] + random.choice([-1, 1]),
        )
        image[pos_1[0], pos_1[1], pos_1[2], :] = np.random.normal(signal * 1.5, signal / 10)
        image[pos_2[0], pos_2[1], pos_2[2], :] = np.random.normal(signal * 1.5, signal / 10)
        clustering_bead_positions.append(
            (pos_1[0], (pos_1[1] + pos_2[1]) // 2, (pos_1[2] + pos_2[2]) // 2)
        )

    for pos in edge_bead_positions:
        image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
    for pos in non_edge_bead_positions:
        image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
        valid_bead_positions.append(pos)
    for pos in out_of_focus_bead_positions:
        image[pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)

    # Apply a gaussian filter to the image
    for ch in range(c_image_shape):
        sigma_correction = 1 + ch * 0.1
        applied_sigmas.append(
            (
                sigma_z * sigma_correction,
                sigma_y * sigma_correction,
                sigma_x * sigma_correction,
            )
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

    return (
        image,
        applied_sigmas,
        non_edge_bead_positions,
        edge_bead_positions,
        valid_bead_positions,
        out_of_focus_bead_positions,
        clustering_bead_positions,
    )


@st.composite
def st_psf_beads_test_data(
    draw,
    nr_images=st.integers(min_value=1, max_value=3),
    # We want an odd number of slices, so we can have a center slice
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
    min_distance=st.just(20),
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

    min_distance_z = draw(min_distance) // 2
    min_distance_y = draw(min_distance)
    min_distance_x = draw(min_distance)

    for _ in range(draw(nr_images)):
        _nr_valid_beads = draw(nr_valid_beads)
        _nr_edge_beads = draw(nr_edge_beads)
        _nr_out_of_focus_beads = draw(nr_out_of_focus_beads)
        _nr_clustering_beads = draw(nr_clustering_beads)
        # We want at least one bead and not too many beads
        assume(
            20
            > (_nr_valid_beads + _nr_edge_beads + _nr_out_of_focus_beads + _nr_clustering_beads)
            > 0
        )

        _signal = draw(signal)
        _target_min_intensity = draw(target_min_intensity)
        _target_max_intensity = draw(target_max_intensity)

        _sigma_z = draw(sigma_z)
        _sigma_y = draw(sigma_y)
        _sigma_x = draw(sigma_x)

        # We do not want images that are too elongated
        assume(0.5 < (x_image_shape / y_image_shape) < 2)

        (
            image,
            applied_sigmas,
            non_edge_bead_positions,
            edge_bead_positions,
            valid_bead_positions,
            out_of_focus_bead_positions,
            clustering_bead_positions,
        ) = _gen_psf_beads_image(
            z_image_shape=z_image_shape,
            y_image_shape=y_image_shape,
            x_image_shape=x_image_shape,
            c_image_shape=c_image_shape,
            nr_valid_beads=_nr_valid_beads,
            nr_edge_beads=_nr_edge_beads,
            nr_out_of_focus_beads=_nr_out_of_focus_beads,
            nr_clustering_beads=_nr_clustering_beads,
            min_distance_z=min_distance_z,
            min_distance_y=min_distance_y,
            min_distance_x=min_distance_x,
            sigma_z=_sigma_z,
            sigma_y=_sigma_y,
            sigma_x=_sigma_x,
            target_min_intensity=_target_min_intensity,
            target_max_intensity=_target_max_intensity,
            do_noise=do_noise,
            signal=_signal,
            dtype=dtype,
        )

        output["images"].append(image)
        output["valid_bead_positions"].append(valid_bead_positions)
        output["edge_bead_positions"].append(edge_bead_positions)
        output["out_of_focus_bead_positions"].append(out_of_focus_bead_positions)
        output["clustering_bead_positions"].append(clustering_bead_positions)
        output["applied_sigmas"].append(applied_sigmas)
        output["min_distance_z"].append(min_distance_z)
        output["min_distance_y"].append(min_distance_y)
        output["min_distance_x"].append(min_distance_x)
        output["signal"].append(_signal)
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

    psf_beads_unprocessed_dataset.input_data.psf_beads_images = [
        numpy_to_mm_image(
            array=image,
            name=f"PSF_image_{i}",
            channel_names=[f"Channel_{c}" for c in range(image.shape[-1])],
        )
        for i, image in enumerate(test_data.pop("images"))
    ]

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
