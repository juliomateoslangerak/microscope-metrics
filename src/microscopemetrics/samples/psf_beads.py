from datetime import datetime

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from scipy import ndimage, signal
from skimage.feature import peak_local_max
from skimage.filters import gaussian

from microscopemetrics import FittingError, SaturationError
from microscopemetrics.samples import (
    df_to_table,
    dict_to_table,
    logger,
    validate_requirements,
)
from microscopemetrics.utilities.utilities import fit_airy, is_saturated


def _add_column_name_level(df: pd.DataFrame, level_name: str, level_value: str):
    # Check if the DataFrame has a MultiIndex or a single-level index
    if isinstance(df.columns, pd.MultiIndex):
        new_columns = pd.MultiIndex.from_tuples(
            [(level_value, *col) for col in df.columns], names=[level_name] + list(df.columns.names)
        )
    else:
        new_columns = pd.MultiIndex.from_tuples(
            [(level_value, col) for col in df.columns], names=[level_name, df.columns.name]
        )
    df.columns = new_columns


def _add_row_index_level(df: pd.DataFrame, level_name: str, level_value: str):
    # Check if the DataFrame has a MultiIndex or a single-level index
    if isinstance(df.index, pd.MultiIndex):
        new_index = pd.MultiIndex.from_tuples(
            [(level_value, *row) for row in df.index], names=[level_name] + list(df.index.names)
        )
    else:
        new_index = pd.MultiIndex.from_tuples(
            [(level_value, row) for row in df.index], names=[level_name, df.index.name]
        )
    df.index = new_index


def _concatenate_index_levels(index_names, index_values, pattern="{level_name}-{level_value}_"):
    concatenated_str = "".join(
        pattern.format(level_name=level_name, level_value=level_value)
        for level_name, level_value in zip(index_names, index_values)
    )

    return concatenated_str.rstrip("_")


def _average_beads(beads: list[np.ndarray]) -> np.ndarray:
    """
    This function takes a list of 3D point spread function bead arrays and averages them to generate a single psf bead.
    It does so by:
    1. Normalizing the intensities into a float32 0-1 range
    2. Increasing the resolution of the beads through interpolation by a factor of 4
    3. Aligning the beads into a common reference frame. It does so using cross correlation
    4. Averaging the beads
    """
    # We first create an fake psf image to align the beads to
    centre_psf = np.zeros(beads[0].shape, dtype=np.float32)
    centre_psf[tuple(dim // 2 for dim in centre_psf.shape)] = 1
    centre_psf = gaussian(centre_psf, sigma=1, preserve_range=True)

    # Normalize the intensities
    beads = [(bead.astype(np.float32) - bead.min()) / bead.max() for bead in beads]

    # Align the beads
    correlations = [signal.correlate(centre_psf, bead, mode="same") for bead in beads]
    shifts = [
        np.unravel_index(np.argmax(correlation), correlation.shape) for correlation in correlations
    ]

    # Increase the resolution of the beads
    hr_beads = [ndimage.zoom(bead, 4, order=1) for bead in beads]


import numpy as np
from scipy.optimize import least_squares


def gaussian_3d(x, y, z, xo, yo, zo, sigma_x, sigma_y, sigma_z, offset):
    """Returns the 3D Gaussian function with a fixed amplitude of 1.0."""
    amplitude = 1.0
    g = offset + amplitude * np.exp(
        -(
            ((x - xo) ** 2) / (2 * sigma_x**2)
            + ((y - yo) ** 2) / (2 * sigma_y**2)
            + ((z - zo) ** 2) / (2 * sigma_z**2)
        )
    )
    return g.ravel()


def fit_gaussian_3d(data):
    """Fits a 3D Gaussian to the data and returns the fit parameters."""
    # Generate the x, y, z coordinate arrays
    x = np.arange(data.shape[0])
    y = np.arange(data.shape[1])
    z = np.arange(data.shape[2])
    x, y, z = np.meshgrid(x, y, z, indexing="ij")

    # Initial guess for the parameters
    xo, yo, zo = np.array(data.shape) / 2
    sigma_x = sigma_y = sigma_z = np.std(data)
    offset = np.min(data)
    initial_guess = (xo, yo, zo, sigma_x, sigma_y, sigma_z, offset)

    # Fit the 3D Gaussian
    def error_function(params):
        return gaussian_3d(x, y, z, *params) - data.ravel()

    result = least_squares(error_function, initial_guess)

    return result.x


def calculate_shift(data):
    """Calculates the shift of the 3D Gaussian from the center."""
    params = fit_gaussian_3d(data)
    xo, yo, zo, sigma_x, sigma_y, sigma_z, offset = params

    # The shift from the center
    center = np.array(data.shape) / 2
    shift = np.array([xo, yo, zo]) - center

    return shift


# Example usage:
# Replace 'data' with your actual 3D numpy array
data = np.random.rand(10, 10, 10)  # Example data
shift = calculate_shift(data)
print("Shift of the Gaussian:", shift)


def _calculate_bead_intensity_outliers(
    bead_positions: pd.DataFrame, robust_z_score_threshold: float
) -> None:
    bead_positions["max_intensity_robust_z_score"] = pd.Series(dtype="float")
    bead_positions["considered_intensity_outlier"] = pd.Series(dtype="bool")

    median = bead_positions[bead_positions.considered_valid]["intensity_max"].median()
    mad = bead_positions[bead_positions.considered_valid]["intensity_max"].mad()

    if len(bead_positions[bead_positions.considered_valid]) == 1:
        bead_positions["max_intensity_robust_z_score"] = 0
        bead_positions["considered_intensity_outlier"] = False
    elif 1 < len(bead_positions[bead_positions.considered_valid]) < 6:
        bead_positions["max_intensity_robust_z_score"] = (
            0.6745 * (bead_positions["intensity_max"] - median) / mad
        )
        bead_positions["considered_intensity_outlier"] = False
    else:
        bead_positions["max_intensity_robust_z_score"] = (
            0.6745 * (bead_positions["intensity_max"] - median) / mad
        )
        bead_positions["considered_intensity_outlier"] = (
            abs(bead_positions["max_intensity_robust_z_score"]) > robust_z_score_threshold
        )

    bead_positions["considered_intensity_outlier"] = bead_positions[
        "considered_intensity_outlier"
    ].astype(bool)


def _generate_key_measurements(
    bead_properties_df,
):
    measurement_aggregation_columns = [
        "channel_nr",
        "intensity_max",
        "intensity_min",
        "intensity_std",
        "fit_r2_z",
        "fit_r2_y",
        "fit_r2_x",
        "fwhm_pixel_z",
        "fwhm_pixel_y",
        "fwhm_pixel_x",
        "fwhm_lateral_asymmetry_ratio",
        "fwhm_micron_z",
        "fwhm_micron_y",
        "fwhm_micron_x",
    ]
    count_aggregation_columns = [
        "channel_nr",
        "considered_valid",
        "considered_self_proximity",
        "considered_lateral_edge",
        "considered_axial_edge",
        "considered_intensity_outlier",
        "considered_bad_fit_z",
        "considered_bad_fit_y",
        "considered_bad_fit_x",
    ]
    # We aggregate counts for each channel on beads according to their status
    channel_counts = (
        bead_properties_df[count_aggregation_columns].groupby("channel_nr").agg(["sum"])
    )
    channel_counts.columns = [
        "_".join((col[0], "count")).strip() for col in channel_counts.columns.values
    ]

    # We aggregate measurements for each channel only on beads considered valid
    valid_bead_properties_df = bead_properties_df[bead_properties_df.considered_valid]
    channel_measurements = (
        valid_bead_properties_df[measurement_aggregation_columns]
        .groupby("channel_nr")
        .agg(["mean", "median", "std"])
    )
    channel_measurements.columns = [
        "_".join(col).strip() for col in channel_measurements.columns.values
    ]

    return pd.merge(channel_counts, channel_measurements, on=["channel_nr"]).reset_index()


def _process_bead(bead: np.ndarray, voxel_size_micron: Tuple[float, float, float]):
    # Find the strongest sections to generate profiles
    z_max = np.max(bead, axis=(1, 2))
    z_focus = np.argmax(z_max)
    y_max = np.max(bead, axis=(0, 2))
    y_focus = np.argmax(y_max)
    x_max = np.max(bead, axis=(0, 1))
    x_focus = np.argmax(x_max)

    # Generate profiles
    z_profile = np.squeeze(bead[:, y_focus, x_focus])
    y_profile = np.squeeze(bead[z_focus, :, x_focus])
    x_profile = np.squeeze(bead[z_focus, y_focus, :])

    # Normalize the profiles and subtract the background
    z_profile = (z_profile - z_profile.min()) / (z_profile.max() - z_profile.min())
    y_profile = (y_profile - y_profile.min()) / (y_profile.max() - y_profile.min())
    x_profile = (x_profile - x_profile.min()) / (x_profile.max() - x_profile.min())

    # Fitting the profiles
    z_fitted_profile, z_r2, z_fwhm, z_center_pos = fit_airy(z_profile)
    y_fitted_profile, y_r2, y_fwhm, y_center_pos = fit_airy(y_profile)
    x_fitted_profile, x_r2, x_fwhm, x_center_pos = fit_airy(x_profile)

    if all(voxel_size_micron):
        z_fwhm_micron = z_fwhm * voxel_size_micron[0]
        y_fwhm_micron = y_fwhm * voxel_size_micron[1]
        x_fwhm_micron = x_fwhm * voxel_size_micron[2]
    else:
        z_fwhm_micron = None
        y_fwhm_micron = None
        x_fwhm_micron = None

    considered_axial_edge = (
        z_center_pos < z_fwhm * 4 or z_profile.shape[0] - z_center_pos < z_fwhm * 4
    )

    intensity_max = bead.max()
    intensity_min = bead.min()
    intensity_std = bead.std()

    return (
        (z_profile, y_profile, x_profile),
        (z_fitted_profile, y_fitted_profile, x_fitted_profile),
        (z_r2, y_r2, x_r2),
        (z_fwhm, y_fwhm, x_fwhm),
        (z_fwhm_micron, y_fwhm_micron, x_fwhm_micron),
        considered_axial_edge,
        intensity_max,
        intensity_min,
        intensity_std,
    )


def _find_beads(channel: np.ndarray, sigma: Tuple[float, float, float], min_distance: float):
    logger.debug(f"Finding beads in channel of shape {channel.shape}")

    if all(sigma):
        logger.debug(f"Applying Gaussian filter with sigma {sigma}")
        channel_gauss = gaussian(image=channel, sigma=sigma)
    else:
        logger.debug("No Gaussian filter applied")
        channel_gauss = channel

    # We find the beads in the MIP for performance and to avoid anisotropy issues in the axial direction
    channel_gauss_mip = np.max(channel_gauss, axis=0)

    # Find bead centers
    positions_all = peak_local_max(image=channel_gauss_mip, threshold_rel=0.2)

    # Find beads min distance filtered
    # We need to remove the beads that are close to each other before the
    # ones that are close to the edge in order to avoid keeping beads that
    # are close to each other but far from the edge. If an edge bead is
    # removed, the other bead that was close to it will be kept.
    positions_proximity_filtered = peak_local_max(
        image=channel_gauss_mip, threshold_rel=0.2, min_distance=int(min_distance), p_norm=2
    )
    positions_proximity_edge_filtered = peak_local_max(
        image=channel_gauss_mip,
        threshold_rel=0.2,
        min_distance=int(min_distance),
        exclude_border=(int(min_distance // 2), int(min_distance // 2)),
        p_norm=2,
    )
    # TODO: lateral considered contain also axial considered
    # Convert arrays to sets for easier comparison
    positions_all_set = set(map(tuple, positions_all))
    positions_proximity_filtered_set = set(map(tuple, positions_proximity_filtered))
    positions_proximity_edge_filtered_set = set(map(tuple, positions_proximity_edge_filtered))
    positions_edge_filtered_set = (
        positions_proximity_filtered_set & positions_proximity_edge_filtered_set
    )

    considered_valid_positions_set = positions_proximity_edge_filtered_set
    considered_positions_proximity_set = positions_all_set - positions_proximity_filtered_set
    considered_positions_edge_set = positions_all_set - positions_edge_filtered_set
    considered_positions_set = positions_all_set - positions_proximity_edge_filtered_set

    logger.debug(f"Beads found: {len(positions_all)}")
    logger.debug(f"Beads kept for analysis: {len(considered_valid_positions_set)}")
    logger.debug(f"Beads considered: {len(considered_positions_set)}")
    logger.debug(
        f"Beads considered for being to close to the edge: {len(considered_positions_edge_set)}"
    )
    logger.debug(
        f"Beads considered for being to close to each other: {len(considered_positions_proximity_set)}"
    )

    # Convert pandas dataframes adding the z dimension
    considered_valid_positions = pd.DataFrame(
        [
            [int(channel_gauss[:, y, x].argmax()), y, x, True, False, False]
            for y, x in considered_valid_positions_set
        ],
        columns=[
            "z_centroid",
            "y_centroid",
            "x_centroid",
            "considered_valid",
            "considered_self_proximity",
            "considered_lateral_edge",
        ],
    )
    considered_positions_proximity = pd.DataFrame(
        [
            [int(channel_gauss[:, y, x].argmax()), y, x, False, True, False]
            for y, x in considered_positions_proximity_set
        ],
        columns=[
            "z_centroid",
            "y_centroid",
            "x_centroid",
            "considered_valid",
            "considered_self_proximity",
            "considered_lateral_edge",
        ],
    )
    considered_positions_edge = pd.DataFrame(
        [
            [int(channel_gauss[:, y, x].argmax()), y, x, False, False, True]
            for y, x in considered_positions_edge_set
        ],
        columns=[
            "z_centroid",
            "y_centroid",
            "x_centroid",
            "considered_valid",
            "considered_self_proximity",
            "considered_lateral_edge",
        ],
    )
    positions = pd.concat(
        [considered_valid_positions, considered_positions_proximity, considered_positions_edge],
        ignore_index=True,
    )
    # We need to convert those considered_x columns to boolean types
    positions["considered_valid"] = positions["considered_valid"].astype(bool)
    positions["considered_self_proximity"] = positions["considered_self_proximity"].astype(bool)
    positions["considered_lateral_edge"] = positions["considered_lateral_edge"].astype(bool)
    positions.insert(loc=0, column="bead_id", value=positions.index)

    bead_images = [
        channel[
            :,
            (pos["y_centroid"] - int(min_distance // 2)) : (
                pos["y_centroid"] + int(min_distance // 2) + 1
            ),
            (pos["x_centroid"] - int(min_distance // 2)) : (
                pos["x_centroid"] + int(min_distance // 2) + 1
            ),
        ]
        for _, pos in positions.iterrows()
    ]

    return (bead_images, positions)


def _process_channel(
    channel: np.ndarray,
    sigma: Tuple[float, float, float],
    min_bead_distance: float,
    snr_threshold: float,
    fitting_r2_threshold: float,
    intensity_robust_z_score_threshold: float,
    voxel_size_micron: Tuple[float, float, float],
) -> Tuple:
    (
        beads,
        bead_positions,
    ) = _find_beads(
        channel=channel,
        sigma=sigma,
        min_distance=min_bead_distance,
    )

    # TODO: activate this when average beads are working
    #  average_bead = _average_beads(beads)

    bead_profiles = []
    bead_fitted_profiles = []
    bead_positions = bead_positions.assign(
        considered_axial_edge=pd.Series(dtype=bool),
        considered_intensity_outlier=pd.Series(dtype=bool),
        considered_bad_fit_z=pd.Series(dtype=bool),
        considered_bad_fit_y=pd.Series(dtype=bool),
        considered_bad_fit_x=pd.Series(dtype=bool),
        intensity_max=pd.Series(dtype=float),
        intensity_min=pd.Series(dtype=float),
        intensity_std=pd.Series(dtype=float),
        fit_r2_z=pd.Series(dtype=float),
        fit_r2_y=pd.Series(dtype=float),
        fit_r2_x=pd.Series(dtype=float),
        fwhm_pixel_z=pd.Series(dtype=float),
        fwhm_pixel_y=pd.Series(dtype=float),
        fwhm_pixel_x=pd.Series(dtype=float),
        fwhm_lateral_asymmetry_ratio=pd.Series(dtype=float),
        fwhm_micron_z=pd.Series(dtype=float),
        fwhm_micron_y=pd.Series(dtype=float),
        fwhm_micron_x=pd.Series(dtype=float),
    )

    for i, bead in enumerate(beads):
        try:
            (
                bpr,
                fpr,
                r2,
                fwhm,
                fwhm_micron,
                ax_edge,
                intensity_max,
                intensity_min,
                intensity_std,
            ) = _process_bead(bead=bead, voxel_size_micron=voxel_size_micron)
            bead_profiles.append(bpr)
            bead_fitted_profiles.append(fpr)
            bead_positions.at[i, "intensity_max"] = intensity_max
            bead_positions.at[i, "intensity_min"] = intensity_min
            bead_positions.at[i, "intensity_std"] = intensity_std
            bead_positions.at[i, "fit_r2_z"] = r2[0]
            bead_positions.at[i, "fit_r2_y"] = r2[1]
            bead_positions.at[i, "fit_r2_x"] = r2[2]
            bead_positions.at[i, "considered_bad_fit_z"] = r2[0] < fitting_r2_threshold
            bead_positions.at[i, "considered_bad_fit_y"] = r2[1] < fitting_r2_threshold
            bead_positions.at[i, "considered_bad_fit_x"] = r2[2] < fitting_r2_threshold
            bead_positions.at[i, "fwhm_pixel_z"] = fwhm[0]
            bead_positions.at[i, "fwhm_pixel_y"] = fwhm[1]
            bead_positions.at[i, "fwhm_pixel_x"] = fwhm[2]
            bead_positions.at[i, "fwhm_lateral_asymmetry_ratio"] = max(fwhm[1], fwhm[2]) / min(
                fwhm[1], fwhm[2]
            )
            bead_positions.at[i, "fwhm_micron_z"] = fwhm_micron[0]
            bead_positions.at[i, "fwhm_micron_y"] = fwhm_micron[1]
            bead_positions.at[i, "fwhm_micron_x"] = fwhm_micron[2]
            bead_positions.at[i, "considered_axial_edge"] = bool(ax_edge)
        except FittingError as e:
            logger.error(
                f"Could not fit bead at position: x:{bead_positions.at[i, 'x_centroid']}, y:{bead_positions.at[i, 'y_centroid']}: {e}"
            )
            raise e

    bead_positions["considered_bad_fit_z"] = bead_positions["considered_bad_fit_z"].astype(bool)
    bead_positions["considered_bad_fit_y"] = bead_positions["considered_bad_fit_y"].astype(bool)
    bead_positions["considered_bad_fit_x"] = bead_positions["considered_bad_fit_x"].astype(bool)

    _calculate_bead_intensity_outliers(
        bead_positions, robust_z_score_threshold=intensity_robust_z_score_threshold
    )

    return (
        beads,
        bead_positions,
        bead_profiles,
        bead_fitted_profiles,
    )


def _process_image(
    image: np.ndarray,
    sigma: Tuple[float, float, float],
    min_bead_distance: float,
    snr_threshold: float,
    fitting_r2_threshold: float,
    intensity_robust_z_score_threshold: float,
    voxel_size_micron: Tuple[float, float, float],
) -> tuple:
    # Remove the time dimension
    image = image[0, ...]

    # Some images (e.g. OMX-3D-SIM) may contain negative values.
    image = np.clip(image, a_min=0, a_max=None)

    nr_channels = image.shape[-1]

    bead_images = []
    bead_positions = []
    bead_profiles = []
    bead_fitted_profiles = []

    for ch in range(nr_channels):
        (
            ch_bead_images,
            ch_bead_positions,
            ch_bead_profiles,
            ch_bead_fitted_profiles,
        ) = _process_channel(
            channel=image[..., ch],
            sigma=sigma,
            min_bead_distance=min_bead_distance,
            snr_threshold=snr_threshold,
            fitting_r2_threshold=fitting_r2_threshold,
            intensity_robust_z_score_threshold=intensity_robust_z_score_threshold,
            voxel_size_micron=voxel_size_micron,
        )

        ch_bead_positions.insert(loc=0, column="channel_nr", value=ch)

        bead_images.append(ch_bead_images)
        bead_positions.append(ch_bead_positions)
        bead_profiles.append(ch_bead_profiles)
        bead_fitted_profiles.append(ch_bead_fitted_profiles)

    bead_positions = pd.concat(bead_positions, ignore_index=True)

    return bead_images, bead_positions, bead_profiles, bead_fitted_profiles


def _estimate_min_bead_distance(dataset: mm_schema.PSFBeadsDataset) -> float:
    # TODO: get the resolution somewhere or pass it as a metadata
    return dataset.input.min_lateral_distance_factor


def _generate_center_roi(
    dataset: mm_schema.PSFBeadsDataset,
    positions,
    root_name,
    color,
    stroke_width=1,
):
    rois = []

    for image in dataset.input.psf_beads_images:
        points = []
        for _, row in positions[positions["image_name"] == image.name].iterrows():
            points.append(
                mm_schema.Point(
                    name=f"ch{row['channel_nr']:02d}_b{row['bead_id']:02d}",
                    z=row["z_centroid"],
                    y=row["y_centroid"] + 0.5,  # Rois are centered on the voxel
                    x=row["x_centroid"] + 0.5,
                    c=row["channel_nr"],
                    stroke_color=mm_schema.Color(
                        r=color[0], g=color[1], b=color[2], alpha=color[3]
                    ),
                    stroke_width=stroke_width,
                )
            )

        if points:
            rois.append(
                mm_schema.Roi(
                    name=f"{root_name}_{image.name}",
                    description=f"{root_name} in image {image.name}",
                    linked_references=image.data_reference,
                    points=points,
                )
            )

    return rois


def _generate_profiles_table(
    dataset: mm_schema.PSFBeadsDataset, axis, raw_profiles, fitted_profiles
):
    axis_names = ["z", "y", "x"]
    if len(raw_profiles) != len(fitted_profiles):
        raise ValueError(
            f"Raw and fitted profiles for axis {axis_names[axis]} must have the same image length"
        )

    if any(
        len(raw_profiles[image_name]) != len(fitted_profiles[image_name])
        for image_name in raw_profiles
    ):
        raise ValueError(
            f"Raw and fitted profiles for axis {axis_names[axis]} must have the same number of profiles."
        )

    if all(not any(raw_profiles[image_name]) for image_name in raw_profiles):
        logger.warning(f"No profiles for axis {axis_names[axis]} available. No table generated.")
        return None

    max_length = max(
        len(bead[axis]) for image in raw_profiles.values() for channel in image for bead in channel
    )
    fill_value = None

    profiles = {}
    descriptions = {}
    for image in dataset.input.psf_beads_images:
        for ch in range(image.array_data.shape[-1]):
            for i, (raw, fitted) in enumerate(
                zip(raw_profiles[image.name][ch], fitted_profiles[image.name][ch])
            ):
                if len(raw[axis]) < max_length:
                    raw[axis] += [fill_value] * (max_length - len(raw))
                    fitted[axis] += [fill_value] * (max_length - len(fitted))
                profiles[f"{image.name}_ch_{ch:02d}_bead_{i:02d}_raw"] = raw[axis].tolist()
                descriptions[f"{image.name}_ch_{ch:02d}_bead_{i:02d}_raw"] = (
                    f"Bead {i:02d} in channel {ch} of image {image.name} raw profile in {axis_names[axis]} axis"
                )

                profiles[f"{image.name}_ch_{ch:02d}_bead_{i:02d}_fitted"] = fitted[axis].tolist()
                descriptions[f"{image.name}_ch_{ch:02d}_bead_{i:02d}_fitted"] = (
                    f"Bead {i:02d} in channel {ch} of image {image.name} fitted profile in {axis_names[axis]} axis"
                )

    return dict_to_table(
        name=f"bead_profiles_{axis_names[axis]}",
        dictionary=profiles,
        description=f"Bead profiles in {axis_names[axis]} axis",
        column_descriptions=descriptions,
    )


def analyse_psf_beads(dataset: mm_schema.PSFBeadsDataset) -> bool:
    validate_requirements()
    # TODO: Implement Nyquist validation??

    # Containers for input data and input parameters
    images = {}
    voxel_sizes_micron = {}
    min_bead_distance = _estimate_min_bead_distance(dataset)
    snr_threshold = dataset.input.snr_threshold
    fitting_r2_threshold = dataset.input.fitting_r2_threshold

    # Containers for output data
    saturated_channels = {}
    bead_crops = {}
    bead_properties = []
    bead_profiles = {}
    bead_fitted_profiles = {}

    # First loop to prepare data
    for image in dataset.input.psf_beads_images:
        images[image.name] = image.array_data[0, ...]

        voxel_sizes_micron[image.name] = (
            image.voxel_size_z_micron,
            image.voxel_size_y_micron,
            image.voxel_size_x_micron,
        )
        saturated_channels[image.name] = []

        # Check image shape
        logger.info(f"Checking image {image.name} shape...")
        if len(image.array_data.shape) != 5:
            logger.error(f"Image {image.name} must be 5D")
            return False
        if image.array_data.shape[0] != 1:
            logger.warning(
                f"Image {image.name} must be in TZYXC order and single time-point. Using first time-point."
            )

        # Check image saturation
        logger.info(f"Checking image {image.name} saturation...")
        for c in range(image.array_data.shape[-1]):
            if is_saturated(
                channel=image.array_data[..., c],
                threshold=dataset.input.saturation_threshold,
                detector_bit_depth=dataset.input.bit_depth,
            ):
                logger.error(f"Image {image.name}: channel {c} is saturated")
                saturated_channels[image.name].append(c)

    if any(len(saturated_channels[name]) for name in saturated_channels):
        logger.error(f"Channels {saturated_channels} are saturated")
        raise SaturationError(f"Channels {saturated_channels} are saturated")

    # Second loop main image analysis
    for image in dataset.input.psf_beads_images:
        logger.info(f"Processing image {image.name}...")
        _, image_bead_properties, image_bead_profiles, image_bead_fitted_profiles = _process_image(
            image=image.array_data,
            sigma=(dataset.input.sigma_z, dataset.input.sigma_y, dataset.input.sigma_x),
            min_bead_distance=min_bead_distance,
            snr_threshold=snr_threshold,
            fitting_r2_threshold=fitting_r2_threshold,
            intensity_robust_z_score_threshold=dataset.input.intensity_robust_z_score_threshold,
            voxel_size_micron=voxel_sizes_micron[image.name],
        )
        logger.info(
            f"Image {image.name} processed:"
            f"    {len(image_bead_properties)} beads found"
            f"    {len(image_bead_properties[image_bead_properties['considered_self_proximity']])} beads considered for being to close to each other"
            f"    {len(image_bead_properties[image_bead_properties['considered_lateral_edge']])} beads considered for being to close to the edge"
            f"    {len(image_bead_properties[image_bead_properties['considered_axial_edge']])} beads considered as to close to the top or bottom of the image"
        )

        image_bead_properties.insert(loc=0, column="image_name", value=image.name)
        bead_properties.append(image_bead_properties)
        bead_profiles[image.name] = image_bead_profiles
        bead_fitted_profiles[image.name] = image_bead_fitted_profiles

    bead_properties = pd.concat(bead_properties, ignore_index=True)

    analyzed_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_valid],
        root_name="analyzed_bead_centroids",
        color=(0, 255, 0, 100),
        stroke_width=8,
    )
    considered_bead_centers_lateral_edge = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_lateral_edge],
        root_name="considered_bead_centroids_lateral_edge",
        color=(255, 0, 0, 100),
        stroke_width=4,
    )
    considered_bead_centers_self_proximity = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_self_proximity],
        root_name="considered_bead_centroids_self_proximity",
        color=(255, 0, 0, 100),
        stroke_width=4,
    )
    considered_bead_centers_axial_edge = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_axial_edge],
        root_name="considered_bead_centroids_axial_edge",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bead_centers_intensity_outlier = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_intensity_outlier],
        root_name="considered_bead_centroids_intensity_outlier",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bead_centers_z_fit_quality = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_z],
        root_name="considered_bead_centroids_z_fit_quality",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bead_centers_y_fit_quality = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_y],
        root_name="considered_bead_centroids_y_fit_quality",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bead_centers_x_fit_quality = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_x],
        root_name="considered_bead_centroids_x_fit_quality",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    key_measurements = mm_schema.PSFBeadsKeyMeasurements(
        name="psf_bead_key_measurements",
        description="Averaged key measurements for all beads considered valid in the dataset.",
        **_generate_key_measurements(
            bead_properties_df=bead_properties,
        ).to_dict("list"),
    )
    bead_properties = df_to_table(bead_properties, "bead_properties")
    bead_z_profiles = _generate_profiles_table(
        dataset=dataset,
        axis=0,
        raw_profiles=bead_profiles,
        fitted_profiles=bead_fitted_profiles,
    )
    bead_y_profiles = _generate_profiles_table(
        dataset=dataset,
        axis=1,
        raw_profiles=bead_profiles,
        fitted_profiles=bead_fitted_profiles,
    )
    bead_x_profiles = _generate_profiles_table(
        dataset=dataset,
        axis=2,
        raw_profiles=bead_profiles,
        fitted_profiles=bead_fitted_profiles,
    )

    dataset.output = mm_schema.PSFBeadsOutput(
        processing_application="microscopemetrics",
        processing_version="0.1.0",
        processing_datetime=datetime.now(),
        analyzed_bead_centers=analyzed_bead_centers,
        considered_bead_centers_lateral_edge=considered_bead_centers_lateral_edge,
        considered_bead_centers_self_proximity=considered_bead_centers_self_proximity,
        considered_bead_centers_axial_edge=considered_bead_centers_axial_edge,
        considered_bead_centers_intensity_outlier=considered_bead_centers_intensity_outlier,
        considered_bead_centers_z_fit_quality=considered_bead_centers_z_fit_quality,
        considered_bead_centers_y_fit_quality=considered_bead_centers_y_fit_quality,
        considered_bead_centers_x_fit_quality=considered_bead_centers_x_fit_quality,
        key_measurements=key_measurements,
        bead_properties=bead_properties,
        bead_z_profiles=bead_z_profiles,
        bead_y_profiles=bead_y_profiles,
        bead_x_profiles=bead_x_profiles,
    )

    dataset.processed = True

    return True


# Calculate 2D FFT
# slice_2d = raw_img[17, ...].reshape([1, n_channels, x_size, y_size])
# fft_2D = fft_2d(slice_2d)

# Calculate 3D FFT
# fft_3D = fft_3d(spots_image)
#
# plt.imshow(np.log(fft_3D[2, :, :, 1]))  # , cmap='hot')
# # plt.imshow(np.log(fft_3D[2, 23, :, :]))  # , cmap='hot')
# plt.show()
#
