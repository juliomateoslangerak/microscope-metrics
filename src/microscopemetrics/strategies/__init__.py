import random

import numpy as np
from scipy.ndimage import rotate, shift
from skimage.exposure import rescale_intensity as skimage_rescale_intensity
from skimage.filters import gaussian as skimage_gaussian

try:
    from hypothesis import assume
    from hypothesis import strategies as st
except ImportError as e:
    raise ImportError(
        "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
    ) from e


def _apply_co_registration_transformations(
    image, translations_z, translations_y, translations_x, rotations_z
):
    transformed_image = np.zeros_like(image)
    for ch in range(image.shape[-1]):
        transformed_image[..., ch] = shift(
            input=image[..., ch],
            shift=[0.0, translations_z[ch], translations_y[ch], translations_x[ch]],
            mode="nearest",
        )
        transformed_image[..., ch] = rotate(
            input=transformed_image[..., ch],
            angle=rotations_z[ch],
            axes=(2, 3),
            reshape=False,
            mode="nearest",
        )

    return transformed_image


def _apply_drift_transformations(image, drift_z, drift_y, drift_x):
    transformed_image = np.zeros_like(image)
    transformed_image[0] = image[0]
    for t in range(1, image.shape[0]):
        transformed_image[t] = shift(
            input=image[t],
            shift=[
                0 if drift_z is None else np.random.uniform(-drift_z, drift_z),
                0 if drift_y is None else np.random.uniform(-drift_y, drift_y),
                0 if drift_x is None else np.random.uniform(-drift_x, drift_x),
                0,  # No shift between channels
            ],
            mode="nearest",
        )

    return transformed_image


def gen_psf_beads_channel():
    pass


def gen_beads_image(
    z_image_shape: int,
    y_image_shape: int,
    x_image_shape: int,
    c_image_shape: int,
    t_image_shape: int,
    nr_valid_beads: int,
    nr_edge_beads: int,
    nr_out_of_focus_beads: int,
    nr_clustering_beads: int,
    min_distance_z_px: int,
    min_distance_y_px: int,
    min_distance_x_px: int,
    sigma_z: float,
    sigma_y: float,
    sigma_x: float,
    signal: float,
    background: float,
    do_noise: bool,
    dtype: np.dtype,
    # coregistration args
    translations_z: list[float] | None = None,
    translations_y: list[float] | None = None,
    translations_x: list[float] | None = None,
    rotations_z: list[float] | None = None,
    # drift args
    drift_z: float | None = None,
    drift_y: float | None = None,
    drift_x: float | None = None,
):
    # Generate the image as float64
    image = np.zeros(
        shape=(t_image_shape, z_image_shape, y_image_shape, x_image_shape, c_image_shape),
        dtype="float32",
    )

    applied_sigmas = []
    non_edge_bead_positions = []
    edge_bead_positions = []
    valid_bead_positions = []
    out_of_focus_bead_positions = []
    clustering_bead_positions = []

    # The tests might require images with no beads
    if nr_valid_beads + nr_edge_beads + nr_out_of_focus_beads + nr_clustering_beads > 0:

        # The strategy is as follows:
        # 1. Generate the valid beads in the center of the image.
        # Those equal to valid_beads + out_of_focus_beads + clustering_beads
        # 2. Generate the edge beads in the edge of the image making sure that they are not too close to the valid beads
        # 3. Gradually remove out_of_focus_beads and clustering_beads from those not in the edge
        while len(non_edge_bead_positions) < (
            nr_valid_beads + nr_out_of_focus_beads + nr_clustering_beads
        ):
            z_pos = z_image_shape // 2
            y_pos = random.randint(min_distance_y_px + 2, y_image_shape - min_distance_y_px - 2)
            x_pos = random.randint(min_distance_x_px + 2, x_image_shape - min_distance_x_px - 2)
            if not non_edge_bead_positions:
                non_edge_bead_positions.append((z_pos, y_pos, x_pos))
            for pos in non_edge_bead_positions:
                if (
                    abs(pos[1] - y_pos) <= min_distance_y_px
                    and abs(pos[2] - x_pos) <= min_distance_x_px
                ):
                    break
                else:
                    continue
            else:
                non_edge_bead_positions.append((z_pos, y_pos, x_pos))

        while len(edge_bead_positions) < nr_edge_beads:
            z_pos = z_image_shape // 2
            y_pos = random.choice(
                [
                    random.randint(5, min_distance_y_px // 2 - 2),
                    random.randint(y_image_shape - min_distance_y_px // 2 + 2, y_image_shape - 5),
                ]
            )
            x_pos = random.choice(
                [
                    random.randint(5, min_distance_x_px // 2 - 2),
                    random.randint(x_image_shape - min_distance_x_px // 2 + 2, x_image_shape - 5),
                ]
            )
            if not edge_bead_positions:
                edge_bead_positions.append((z_pos, y_pos, x_pos))
            for pos in edge_bead_positions:
                if (
                    abs(pos[1] - y_pos) <= min_distance_y_px
                    and abs(pos[2] - x_pos) <= min_distance_x_px
                ):
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
                        random.randint(3, min_distance_z_px - 2),
                        random.randint(z_image_shape - min_distance_z_px + 2, z_image_shape - 4),
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
            image[:, pos_1[0], pos_1[1], pos_1[2], :] = np.random.normal(signal * 1.5, signal / 10)
            image[:, pos_2[0], pos_2[1], pos_2[2], :] = np.random.normal(signal * 1.5, signal / 10)
            clustering_bead_positions.append(
                (pos_1[0], (pos_1[1] + pos_2[1]) // 2, (pos_1[2] + pos_2[2]) // 2)
            )

        # Fill the image with the beads and adding some normal distributed random intensity
        for pos in edge_bead_positions:
            image[:, pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
        for pos in non_edge_bead_positions:
            image[:, pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)
            valid_bead_positions.append(pos)
        for pos in out_of_focus_bead_positions:
            image[:, pos[0], pos[1], pos[2], :] = np.random.normal(signal, signal / 50)

        # Apply a gaussian filter to the image
        for ch in range(c_image_shape):
            sigma_correction = 1 + ch * 0.1
            applied_sigmas.append(
                (
                    0,  # the sigma for time is 0
                    sigma_z * sigma_correction,
                    sigma_y * sigma_correction,
                    sigma_x * sigma_correction,
                )
            )
            image[:, :, :, :, ch] = skimage_gaussian(
                image[:, :, :, :, ch], sigma=applied_sigmas[-1], preserve_range=True
            )

    # Apply co-registration transformations
    if any([translations_z, translations_y, translations_x, rotations_z]):
        if translations_z is None:
            translations_z = [0.0 for _ in range(c_image_shape)]
        if translations_y is None:
            translations_y = [0.0 for _ in range(c_image_shape)]
        if translations_x is None:
            translations_x = [0.0 for _ in range(c_image_shape)]
        if rotations_z is None:
            rotations_z = [0.0 for _ in range(c_image_shape)]
        image = _apply_co_registration_transformations(
            image, translations_z, translations_y, translations_x, rotations_z
        )

    # Apply drift over time
    if any([drift_z, drift_y, drift_x]):
        image = _apply_drift_transformations(image, drift_z, drift_y, drift_x)

    # Normalize the image to the target range before applying noise
    image_normalized = (
        skimage_rescale_intensity(
            image,
            out_range=(background, signal),
        )
        * np.iinfo(dtype).max
    )

    # Add noise
    if do_noise:
        image_normalized = np.random.poisson(image_normalized)

    image_normalized = np.astype(image_normalized, dtype)

    return (
        image_normalized,
        applied_sigmas,
        non_edge_bead_positions,
        edge_bead_positions,
        valid_bead_positions,
        out_of_focus_bead_positions,
        clustering_bead_positions,
    )


@st.composite
def st_beads_test_data(
    draw,
    nr_images=st.integers(min_value=1, max_value=3),
    # We want an odd number of slices, so we can have a center slice
    z_image_shape=st.just(61),
    y_image_shape=st.just(512),
    x_image_shape=st.just(512),
    c_image_shape=st.integers(min_value=1, max_value=3),
    t_image_shape=st.just(1),
    # testing with uint8 works most of the time, but it produces flaky results
    dtype=st.sampled_from([np.uint16]),
    signal=st.just(0.4),
    background=st.just(0.005),
    do_noise=st.just(True),
    sigma_z=st.floats(min_value=1.4, max_value=1.7),
    sigma_x=st.floats(min_value=1.4, max_value=1.7),
    sigma_y=st.floats(min_value=1.4, max_value=1.7),
    min_lateral_distance_px=st.just(20),
    min_axial_distance_px=st.just(15),
    nr_valid_beads=st.just(5),
    nr_edge_beads=st.just(1),
    nr_out_of_focus_beads=st.just(1),
    nr_clustering_beads=st.just(1),
    translations_z=st.floats(min_value=-1.0, max_value=1.0),
    translations_y=st.floats(min_value=-1.0, max_value=1.0),
    translations_x=st.floats(min_value=-1.0, max_value=1.0),
    rotations_z=st.floats(min_value=-1.0, max_value=1.0),
    drift_z=st.just(None),
    drift_y=st.just(None),
    drift_x=st.just(None),
):
    output = {
        "images": [],
        "valid_bead_positions": [],
        "edge_bead_positions": [],
        "out_of_focus_bead_positions": [],
        "clustering_bead_positions": [],
        "applied_sigmas": [],
        "min_lateral_distance_px": [],
        "min_axial_distance_px": [],
        "signal": [],
        "background": [],
        "do_noise": [],
        "translations_z": [],
        "translations_y": [],
        "translations_x": [],
        "rotations_z": [],
        "drift_z": [],
        "drift_y": [],
        "drift_x": [],
    }

    z_image_shape = draw(z_image_shape)
    y_image_shape = draw(y_image_shape)
    x_image_shape = draw(x_image_shape)
    c_image_shape = draw(c_image_shape)
    t_image_shape = draw(t_image_shape)

    do_noise = draw(do_noise)

    dtype = draw(dtype)

    # Microscope-metrics estimates the min distance as twice the min_distance
    # declared in the input data. Logic being that this distance is declared as
    # times the FWHM and so, if a correct nyquist is used, double the number of pixels.
    # As for the z min distance, we just take the ratio z-fwhm and xy-fwhm of 3
    _min_lateral_distance_px = draw(min_lateral_distance_px)
    _min_axial_distance_px = draw(min_axial_distance_px)

    # Draw co-registration values
    if c_image_shape > 1:
        _translations_z = [draw(translations_z) for _ in range(c_image_shape)]
        _translations_y = [draw(translations_y) for _ in range(c_image_shape)]
        _translations_x = [draw(translations_x) for _ in range(c_image_shape)]
        _rotations_z = [draw(rotations_z) for _ in range(c_image_shape)]
    else:
        _translations_z = None
        _translations_y = None
        _translations_x = None
        _rotations_z = None

    # Draw drift values
    if t_image_shape > 1:
        _drift_z = draw(drift_z)
        _drift_y = draw(drift_y)
        _drift_x = draw(drift_x)
    else:
        _drift_z = None
        _drift_y = None
        _drift_x = None

    for _ in range(draw(nr_images)):
        _nr_valid_beads = draw(nr_valid_beads)
        _nr_edge_beads = draw(nr_edge_beads)
        _nr_out_of_focus_beads = draw(nr_out_of_focus_beads)
        _nr_clustering_beads = draw(nr_clustering_beads)
        # We want at least one bead and not too many beads
        assume(
            20
            > (_nr_valid_beads + _nr_edge_beads + _nr_out_of_focus_beads + _nr_clustering_beads)
            >= 0
        )

        _signal = draw(signal)
        _background = draw(background)

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
        ) = gen_beads_image(
            z_image_shape=z_image_shape,
            y_image_shape=y_image_shape,
            x_image_shape=x_image_shape,
            c_image_shape=c_image_shape,
            t_image_shape=t_image_shape,
            nr_valid_beads=_nr_valid_beads,
            nr_edge_beads=_nr_edge_beads,
            nr_out_of_focus_beads=_nr_out_of_focus_beads,
            nr_clustering_beads=_nr_clustering_beads,
            min_distance_z_px=_min_axial_distance_px,
            min_distance_y_px=_min_lateral_distance_px,
            min_distance_x_px=_min_lateral_distance_px,
            sigma_z=_sigma_z,
            sigma_y=_sigma_y,
            sigma_x=_sigma_x,
            signal=_signal,
            background=_background,
            do_noise=do_noise,
            dtype=dtype,
            translations_z=_translations_z,
            translations_y=_translations_y,
            translations_x=_translations_x,
            rotations_z=_rotations_z,
            drift_z=_drift_z,
            drift_y=_drift_y,
            drift_x=_drift_x,
        )

        output["images"].append(image)
        output["valid_bead_positions"].append(valid_bead_positions)
        output["edge_bead_positions"].append(edge_bead_positions)
        output["out_of_focus_bead_positions"].append(out_of_focus_bead_positions)
        output["clustering_bead_positions"].append(clustering_bead_positions)
        output["applied_sigmas"].append(applied_sigmas)
        output["min_lateral_distance_px"].append(_min_lateral_distance_px)
        output["min_axial_distance_px"].append(_min_axial_distance_px)
        output["signal"].append(_signal)
        output["background"].append(_background)
        output["do_noise"].append(do_noise)
        output["translations_z"].append(_translations_z)
        output["translations_y"].append(_translations_y)
        output["translations_x"].append(_translations_x)
        output["rotations_z"].append(_rotations_z)
        output["drift_z"].append(_drift_z)
        output["drift_y"].append(_drift_y)
        output["drift_x"].append(_drift_x)

    return output
