from datetime import datetime
from typing import Optional, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from scipy import ndimage

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools

MAX_NR_PEAKS = 100


def _add_column_name_level(df: pd.DataFrame, level_name: str, level_value: str):
    if isinstance(df.columns, pd.MultiIndex):
        new_columns = pd.MultiIndex.from_tuples(
            [(level_value, *col) for col in df.columns],
            names=[level_name] + list(df.columns.names),
        )
    else:
        new_columns = pd.MultiIndex.from_tuples(
            [(level_value, col) for col in df.columns],
            names=[level_name, df.columns.name],
        )
    df.columns = new_columns


def _add_row_index_level(df: pd.DataFrame, level_name: str, level_value: str):
    if isinstance(df.index, pd.MultiIndex):
        new_index = pd.MultiIndex.from_tuples(
            [(level_value, *row) for row in df.index],
            names=[level_name] + list(df.index.names),
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


def _average_beads_group(
    group: pd.DataFrame,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
    min_axial_distance_px: float,
) -> pd.Series:
    """
    Averages the beads in a group by first aligning them to the center of the image and then averaging them.
    Then calculates measurements on the averaged bead.
    """
    dtype = {bead.dtype for bead in group.beads}
    if len(dtype) > 1:
        raise ValueError("All beads must have the same dtype.")
    # TODO: consider using a higher threshold to do averaging
    if group.considered_valid.sum() < 2:
        mm.logger.warning("Less than 2 valid beads to average.")
        return pd.Series({"average_bead": np.nan})
    aligned_beads = [
        ndimage.shift(row.beads, (row.shift_z, row.shift_y, row.shift_x), mode="nearest", order=1)
        for row in group.itertuples()
        if row.considered_valid
    ]
    mm.logger.info(f"Averaging {len(aligned_beads)} beads")

    average_bead = np.mean(aligned_beads, axis=0).astype(dtype.pop())

    # Process the average bead to get measurements
    measurements = _process_bead(average_bead, voxel_size_micron, min_axial_distance_px)

    # Add the average bead array to the measurements
    result = pd.Series({"average_bead": average_bead})
    result = pd.concat([result, pd.Series(measurements)])

    return result


def _average_beads(
    bead_properties: pd.DataFrame,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
    min_axial_distance_px: float,
    bead_profiles_z: pd.DataFrame,
    bead_profiles_y: pd.DataFrame,
    bead_profiles_x: pd.DataFrame,
    source_images: list,
) -> Tuple[
    Optional[pd.DataFrame],
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    Optional[mm_schema.Image],
]:
    """
    Averages beads across all images, calculates measurements on the averaged beads,
    extracts profiles, and creates the average bead images.

    Returns a tuple of:
    - average_beads_properties: DataFrame with averaged bead properties or None
    - bead_profiles_z: DataFrame with z profiles (including average if computed)
    - bead_profiles_y: DataFrame with y profiles (including average if computed)
    - bead_profiles_x: DataFrame with x profiles (including average if computed)
    - average_bead_image: mm_schema.Image or None
    """
    # Do the actual averaging grouped by image and channel
    average_beads_properties = pd.DataFrame(
        {
            keys: _average_beads_group(
                group,
                voxel_size_micron=voxel_size_micron,
                min_axial_distance_px=min_axial_distance_px,
            )
            for keys, group in bead_properties.groupby(
                [
                    "channel_nr",
                    "channel_name",
                    "excitation_wavelength_nm",
                    "emission_wavelength_nm",
                ],
                dropna=False,  # often wavelengths are NaN
            )
        }
    ).T
    average_beads_properties.index.names = [
        "channel_nr",
        "channel_name",
        "excitation_wavelength_nm",
        "emission_wavelength_nm",
    ]

    # If after dropping image-channels without beads we keep nothing, we return
    if average_beads_properties.dropna(subset=["average_bead"]).empty:
        mm.logger.warning("No average beads were computed")
        return None, bead_profiles_z, bead_profiles_y, bead_profiles_x, None

    # If a channel does not have any beads, the average bead is NaN, and
    # it has to be replaced by a zeroed array
    zero_bead = np.zeros_like(average_beads_properties["average_bead"].dropna().iloc[0])
    average_beads_properties["average_bead"] = average_beads_properties["average_bead"].apply(
        lambda x: zero_bead.copy() if isinstance(x, float) and np.isnan(x) else x
    )

    # it is the _process_bead function that decides if a bead is
    # considered axial edge or not. For the average bead, this is not
    # relevant, so we drop this column.
    average_beads_properties.drop(columns=["considered_axial_edge"], inplace=True)

    # Crop average bead z profiles to match individual bead crops (±4x median FWHM per channel)
    median_fwhm_by_channel = (
        bead_properties[bead_properties["considered_valid"]]
        .groupby(level="channel_nr")["fwhm_pixel_z"]
        .median()
        .dropna()
    )
    channel_nr_level = average_beads_properties.index.names.index("channel_nr")
    for idx, row in average_beads_properties.iterrows():
        channel_nr = idx[channel_nr_level] if isinstance(idx, tuple) else idx
        if channel_nr not in median_fwhm_by_channel.index:
            continue
        half_window = int(min_axial_distance_px)
        for col in ["z_raw", "z_fitted_airy", "z_fitted_gaussian"]:
            profile = row[col]
            if isinstance(profile, np.ndarray):
                center_z = profile.shape[0] // 2  # average bead is centered by construction
                crop_start = max(0, center_z - half_window)
                crop_end = min(len(profile), center_z + half_window)
                average_beads_properties.at[idx, col] = profile[crop_start:crop_end]

    # Extract profiles from average beads and join with existing profiles
    bead_profiles_z = bead_profiles_z.join(_extract_profiles(average_beads_properties, "z"))
    bead_profiles_y = bead_profiles_y.join(_extract_profiles(average_beads_properties, "y"))
    bead_profiles_x = bead_profiles_x.join(_extract_profiles(average_beads_properties, "x"))

    # Create the average bead image
    average_bead_image = None
    # TODO: get more metadata from the source images
    if len(average_beads_properties["average_bead"]):
        average_bead_image = mm.analyses.numpy_to_mm_image(
            array=np.expand_dims(
                np.stack(
                    [c for c in average_beads_properties["average_bead"]],
                    axis=-1,
                ),
                axis=0,
            ),
            name="average_bead",
            description="Average bead image extracted from all the beads considered valid in the dataset.",
            source_images=source_images,
            channel_names=[
                i[average_beads_properties.index.names.index("channel_name")]
                for i in average_beads_properties.index
            ],
            excitation_wavelengths_nm=[
                i[average_beads_properties.index.names.index("excitation_wavelength_nm")]
                for i in average_beads_properties.index
            ],
            emission_wavelengths_nm=[
                i[average_beads_properties.index.names.index("emission_wavelength_nm")]
                for i in average_beads_properties.index
            ],
        )

        # We don't need the average bead arrays anymore
        average_beads_properties.drop("average_bead", axis=1, inplace=True)

        average_beads_properties = average_beads_properties.add_prefix("average_bead_")

    return (
        average_beads_properties,
        bead_profiles_z,
        bead_profiles_y,
        bead_profiles_x,
        average_bead_image,
    )


def _generate_key_measurements(bead_properties, average_bead_properties):
    measurement_aggregation_columns = [
        "channel_name",
        "channel_nr",
        "excitation_wavelength_nm",
        "emission_wavelength_nm",
        "intensity_max",
        "intensity_min",
        "intensity_std",
        "fit_airy_r2_z",
        "fit_airy_r2_y",
        "fit_airy_r2_x",
        "fit_gaussian_r2_z",
        "fit_gaussian_r2_y",
        "fit_gaussian_r2_x",
        "fwhm_pixel_z",
        "fwhm_pixel_y",
        "fwhm_pixel_x",
        "fwhm_lateral_asymmetry_ratio",
        "fwhm_micron_z",
        "fwhm_micron_y",
        "fwhm_micron_x",
    ]
    count_aggregation_columns = [
        "channel_name",
        "channel_nr",
        "excitation_wavelength_nm",
        "emission_wavelength_nm",
        "total_bead",
        "considered_valid",
        "considered_self_proximity",
        "considered_lateral_edge",
        "considered_axial_edge",
        "considered_intensity_std_outlier",
        "considered_bad_fit_airy_z",
        "considered_bad_fit_airy_y",
        "considered_bad_fit_airy_x",
        "considered_bad_fit_gaussian_z",
        "considered_bad_fit_gaussian_y",
        "considered_bad_fit_gaussian_x",
    ]

    reindex_bead_properties_df = bead_properties.reset_index()

    # Add an all True column to count the total number of beads
    reindex_bead_properties_df["total_bead"] = True

    # We aggregate counts for each channel on beads according to their status
    channel_counts = (
        reindex_bead_properties_df[count_aggregation_columns]
        .groupby(
            ["channel_nr", "channel_name", "excitation_wavelength_nm", "emission_wavelength_nm"],
            dropna=False,  # often wavelengths are not present
        )
        .agg(["sum"])
    )
    channel_counts.columns = [
        "_".join((col[0], "count")).strip() for col in channel_counts.columns.values
    ]

    # We aggregate measurements for each channel only on beads considered valid
    valid_bead_properties_df = reindex_bead_properties_df[
        reindex_bead_properties_df.considered_valid
    ]
    channel_measurements = (
        valid_bead_properties_df[measurement_aggregation_columns]
        .groupby(
            ["channel_nr", "channel_name", "excitation_wavelength_nm", "emission_wavelength_nm"],
            dropna=False,  # often wavelengths are not present
        )
        .agg(["mean", "median", "std"])
    )
    channel_measurements.columns = [
        "_".join(col).strip() for col in channel_measurements.columns.values
    ]

    if average_bead_properties is not None:
        key_measurements = pd.concat(
            [channel_counts, channel_measurements, average_bead_properties], axis=1
        )
    else:
        key_measurements = pd.concat([channel_counts, channel_measurements], axis=1)

    key_measurements.reset_index(inplace=True)
    key_measurements = [
        mm_schema.PSFBeadsKeyMeasurement(**km) for km in key_measurements.to_dict(orient="records")
    ]

    return key_measurements


def _process_bead(
    bead: np.ndarray,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
    min_axial_distance_px: float,
    calculate_shifts: bool = False,
):
    if not isinstance(bead, np.ndarray) and np.isnan(bead):
        result = {
            "z_raw": np.nan,
            "z_fitted_airy": np.nan,
            "z_fitted_gaussian": np.nan,
            "y_raw": np.nan,
            "y_fitted_airy": np.nan,
            "y_fitted_gaussian": np.nan,
            "x_raw": np.nan,
            "x_fitted_airy": np.nan,
            "x_fitted_gaussian": np.nan,
            "fit_airy_r2_z": np.nan,
            "fit_airy_r2_y": np.nan,
            "fit_airy_r2_x": np.nan,
            "fit_gaussian_r2_z": np.nan,
            "fit_gaussian_r2_y": np.nan,
            "fit_gaussian_r2_x": np.nan,
            "fwhm_pixel_z": np.nan,
            "fwhm_pixel_y": np.nan,
            "fwhm_pixel_x": np.nan,
            "fwhm_micron_z": np.nan,
            "fwhm_micron_y": np.nan,
            "fwhm_micron_x": np.nan,
            "fwhm_lateral_asymmetry_ratio": np.nan,
            "considered_axial_edge": np.nan,
            "intensity_integrated": np.nan,
            "intensity_max": np.nan,
            "intensity_min": np.nan,
            "intensity_std": np.nan,
        }
        if calculate_shifts:
            result.update({"shift_z": np.nan, "shift_y": np.nan, "shift_x": np.nan})
        return result

    intensity_max = bead.max()
    intensity_min = bead.min()
    intensity_std = bead.std()
    intensity_integrated = (bead - intensity_min).sum()

    # Find the strongest sections to generate profiles
    z_focus = np.argmax(np.max(bead, axis=(1, 2)))
    y_focus = np.argmax(np.max(bead, axis=(0, 2)))
    x_focus = np.argmax(np.max(bead, axis=(0, 1)))

    # Generate profiles
    profile_z_raw = np.squeeze(bead[:, y_focus, x_focus])
    profile_y_raw = np.squeeze(bead[z_focus, :, x_focus])
    profile_x_raw = np.squeeze(bead[z_focus, y_focus, :])

    # Normalize the profiles and subtract the background
    profile_z_raw = (profile_z_raw - profile_z_raw.min()) / (
        profile_z_raw.max() - profile_z_raw.min()
    )
    profile_y_raw = (profile_y_raw - profile_y_raw.min()) / (
        profile_y_raw.max() - profile_y_raw.min()
    )
    profile_x_raw = (profile_x_raw - profile_x_raw.min()) / (
        profile_x_raw.max() - profile_x_raw.min()
    )

    # Fitting the profiles
    try:
        # Airy profiles
        profile_z_fitted_airy, airy_r2_z, airy_fwhm_z, (airy_center_pos_z, _) = mm_tools.fit_airy(
            profile_z_raw
        )
        profile_y_fitted_airy, airy_r2_y, airy_fwhm_y, (airy_center_pos_y, _) = mm_tools.fit_airy(
            profile_y_raw
        )
        profile_x_fitted_airy, airy_r2_x, airy_fwhm_x, (airy_center_pos_x, _) = mm_tools.fit_airy(
            profile_x_raw
        )

        # Gaussian profiles
        profile_z_fitted_gauss, gauss_r2_z, gauss_fwhm_z, (_, _, gauss_center_pos_z, _) = (
            mm_tools.fit_gaussian(profile_z_raw)
        )
        profile_y_fitted_gauss, gauss_r2_y, gauss_fwhm_y, (_, _, gauss_center_pos_y, _) = (
            mm_tools.fit_gaussian(profile_y_raw)
        )
        profile_x_fitted_gauss, gauss_r2_x, gauss_fwhm_x, (_, _, gauss_center_pos_x, _) = (
            mm_tools.fit_gaussian(profile_x_raw)
        )
    except RuntimeError as e:
        mm.logger.error(f"Error while fitting the profiles for bead: {e}")
        result = {
            "z_raw": np.nan,
            "z_fitted_airy": np.nan,
            "z_fitted_gaussian": np.nan,
            "y_raw": np.nan,
            "y_fitted_airy": np.nan,
            "y_fitted_gaussian": np.nan,
            "x_raw": np.nan,
            "x_fitted_airy": np.nan,
            "x_fitted_gaussian": np.nan,
            "fit_airy_r2_z": np.nan,
            "fit_airy_r2_y": np.nan,
            "fit_airy_r2_x": np.nan,
            "fit_gaussian_r2_z": np.nan,
            "fit_gaussian_r2_y": np.nan,
            "fit_gaussian_r2_x": np.nan,
            "fwhm_pixel_z": np.nan,
            "fwhm_pixel_y": np.nan,
            "fwhm_pixel_x": np.nan,
            "fwhm_micron_z": np.nan,
            "fwhm_micron_y": np.nan,
            "fwhm_micron_x": np.nan,
            "fwhm_lateral_asymmetry_ratio": np.nan,
            "considered_axial_edge": False,
            "intensity_integrated": intensity_integrated,
            "intensity_max": intensity_max,
            "intensity_min": intensity_min,
            "intensity_std": intensity_std,
        }
        if calculate_shifts:
            result.update({"shift_z": np.nan, "shift_y": np.nan, "shift_x": np.nan})

        return result

    airy_fwhm_lateral_asymmetry_ratio = max(airy_fwhm_y, airy_fwhm_x) / min(
        airy_fwhm_y, airy_fwhm_x
    )
    gauss_fwhm_lateral_asymmetry_ratio = max(gauss_fwhm_y, gauss_fwhm_x) / min(
        gauss_fwhm_y, gauss_fwhm_x
    )

    if all(voxel_size_micron):
        airy_fwhm_micron_z = airy_fwhm_z * voxel_size_micron[0]
        airy_fwhm_micron_y = airy_fwhm_y * voxel_size_micron[1]
        airy_fwhm_micron_x = airy_fwhm_x * voxel_size_micron[2]
        gauss_fwhm_micron_z = gauss_fwhm_z * voxel_size_micron[0]
        gauss_fwhm_micron_y = gauss_fwhm_y * voxel_size_micron[1]
        gauss_fwhm_micron_x = gauss_fwhm_x * voxel_size_micron[2]
    else:
        airy_fwhm_micron_z = np.nan
        airy_fwhm_micron_y = np.nan
        airy_fwhm_micron_x = np.nan
        gauss_fwhm_micron_z = np.nan
        gauss_fwhm_micron_y = np.nan
        gauss_fwhm_micron_x = np.nan

    considered_axial_edge = (
        gauss_center_pos_z < min_axial_distance_px
        or profile_z_raw.shape[0] - gauss_center_pos_z < min_axial_distance_px
    )

    result = {
        "z_raw": profile_z_raw,
        "z_fitted_airy": profile_z_fitted_airy,
        "z_fitted_gaussian": profile_z_fitted_gauss,
        "y_raw": profile_y_raw,
        "y_fitted_airy": profile_y_fitted_airy,
        "y_fitted_gaussian": profile_y_fitted_gauss,
        "x_raw": profile_x_raw,
        "x_fitted_airy": profile_x_fitted_airy,
        "x_fitted_gaussian": profile_x_fitted_gauss,
        "fit_airy_r2_z": airy_r2_z,
        "fit_airy_r2_y": airy_r2_y,
        "fit_airy_r2_x": airy_r2_x,
        "fit_gaussian_r2_z": gauss_r2_z,
        "fit_gaussian_r2_y": gauss_r2_y,
        "fit_gaussian_r2_x": gauss_r2_x,
        # We are choosing the Gaussian fit for the FWHM
        "fwhm_pixel_z": gauss_fwhm_z,
        "fwhm_pixel_y": gauss_fwhm_y,
        "fwhm_pixel_x": gauss_fwhm_x,
        "fwhm_micron_z": gauss_fwhm_micron_z,
        "fwhm_micron_y": gauss_fwhm_micron_y,
        "fwhm_micron_x": gauss_fwhm_micron_x,
        "fwhm_lateral_asymmetry_ratio": gauss_fwhm_lateral_asymmetry_ratio,
        "considered_axial_edge": considered_axial_edge,
        "intensity_integrated": intensity_integrated,
        "intensity_max": intensity_max,
        "intensity_min": intensity_min,
        "intensity_std": intensity_std,
    }
    if calculate_shifts:
        result.update(
            {
                "shift_z": (profile_z_raw.shape[0] // 2) - gauss_center_pos_z,
                "shift_y": (profile_y_raw.shape[0] // 2) - gauss_center_pos_y,
                "shift_x": (profile_x_raw.shape[0] // 2) - gauss_center_pos_x,
            }
        )
    return result


def _process_channel(
    channel: np.ndarray,
    sigma_min: float,
    sigma_max: float,
    min_lateral_distance_px: float,
    min_axial_distance_px: float,
    snr_threshold: float,
    fitting_airy_r2_threshold: float,
    fitting_gaussian_r2_threshold: float,
    intensity_robust_z_score_threshold: float,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
) -> pd.DataFrame:
    bead_properties = mm_tools.find_beads(
        channel=channel,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        min_lateral_distance_px=min_lateral_distance_px,
        snr_threshold=snr_threshold,
        max_num_peaks=MAX_NR_PEAKS,
    )

    if len(bead_properties) == 0:
        mm.logger.warning("No beads found in channel")
        return pd.DataFrame()

    bead_properties = bead_properties.assign(
        considered_intensity_std_outlier=pd.Series(dtype=bool),
    )

    bead_properties = bead_properties.join(
        bead_properties["beads"].apply(
            lambda x: pd.Series(
                _process_bead(x, voxel_size_micron, min_axial_distance_px, calculate_shifts=True)
            )
        )
    )
    bead_properties["considered_bad_fit_airy_z"] = (
        bead_properties["fit_airy_r2_z"] < fitting_airy_r2_threshold
    )
    bead_properties["considered_bad_fit_airy_y"] = (
        bead_properties["fit_airy_r2_y"] < fitting_airy_r2_threshold
    )
    bead_properties["considered_bad_fit_airy_x"] = (
        bead_properties["fit_airy_r2_x"] < fitting_airy_r2_threshold
    )
    bead_properties["considered_bad_fit_gaussian_z"] = (
        bead_properties["fit_gaussian_r2_z"] < fitting_gaussian_r2_threshold
    )
    bead_properties["considered_bad_fit_gaussian_y"] = (
        bead_properties["fit_gaussian_r2_y"] < fitting_gaussian_r2_threshold
    )
    bead_properties["considered_bad_fit_gaussian_x"] = (
        bead_properties["fit_gaussian_r2_x"] < fitting_gaussian_r2_threshold
    )

    mm_tools.calculate_bead_outliers(
        bead_properties=bead_properties,
        robust_z_score_threshold=intensity_robust_z_score_threshold,
        measurements=["intensity_std"],
    )

    # We need to invalidate all the bad fits and outliers
    bead_properties["considered_valid"] = [
        not any([prox, l_edge, a_edge, bfa_z, bfa_y, bfa_x, bfg_z, bfg_y, bfg_x, i_out])
        for prox, l_edge, a_edge, bfa_z, bfa_y, bfa_x, bfg_z, bfg_y, bfg_x, i_out in zip(
            bead_properties["considered_self_proximity"],
            bead_properties["considered_lateral_edge"],
            bead_properties["considered_axial_edge"],
            bead_properties["considered_bad_fit_airy_z"],
            bead_properties["considered_bad_fit_airy_y"],
            bead_properties["considered_bad_fit_airy_x"],
            bead_properties["considered_bad_fit_gaussian_z"],
            bead_properties["considered_bad_fit_gaussian_y"],
            bead_properties["considered_bad_fit_gaussian_x"],
            bead_properties["considered_intensity_std_outlier"],
        )
    ]

    return bead_properties


def _process_image(
    image: mm_schema.Image,
    sigma_min: float,
    sigma_max: float,
    min_lateral_distance_px: float,
    min_axial_distance_px: float,
    snr_threshold: float,
    fitting_airy_r2_threshold: float,
    fitting_gaussian_r2_threshold: float,
    intensity_robust_z_score_threshold: float,
) -> tuple:
    channel_names = [c.name for c in image.channel_series.channels]
    excitation_wavelengths_nm = [c.excitation_wavelength_nm for c in image.channel_series.channels]
    emission_wavelengths_nm = [c.emission_wavelength_nm for c in image.channel_series.channels]
    voxel_size_micron = (
        image.voxel_size_z_micron,
        image.voxel_size_y_micron,
        image.voxel_size_x_micron,
    )

    # Get image data and remove the time dimension
    image = image.array_data[0, ...]

    # Some images (e.g. OMX-3D-SIM) may contain negative values.
    image = np.clip(image, a_min=0, a_max=None)

    nr_channels = image.shape[-1]

    bead_properties = []

    for ch in range(nr_channels):
        ch_bead_positions = _process_channel(
            channel=image[..., ch],
            sigma_min=sigma_min,
            sigma_max=sigma_max,
            min_lateral_distance_px=min_lateral_distance_px,
            min_axial_distance_px=min_axial_distance_px,
            snr_threshold=snr_threshold,
            fitting_airy_r2_threshold=fitting_airy_r2_threshold,
            fitting_gaussian_r2_threshold=fitting_gaussian_r2_threshold,
            intensity_robust_z_score_threshold=intensity_robust_z_score_threshold,
            voxel_size_micron=voxel_size_micron,
        )

        _add_row_index_level(
            ch_bead_positions, "emission_wavelength_nm", emission_wavelengths_nm[ch]
        )
        _add_row_index_level(
            ch_bead_positions, "excitation_wavelength_nm", excitation_wavelengths_nm[ch]
        )
        _add_row_index_level(ch_bead_positions, "channel_nr", ch)
        _add_row_index_level(ch_bead_positions, "channel_name", channel_names[ch])
        bead_properties.append(ch_bead_positions)

    return pd.concat(bead_properties)


def _generate_center_roi(
    dataset: mm_schema.PSFBeadsDataset,
    positions,
    root_name,
    color,
    stroke_width=1,
):
    rois = []

    for image in dataset.input_data.psf_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        if positions.empty or image_id not in positions.index.get_level_values("image_id"):
            continue
        points = []
        for index, row in positions.xs(image_id, level="image_id").iterrows():
            points.append(
                mm_schema.Point(
                    name=index[positions.index.names[1:].index("bead_id")],
                    z=row["center_z"],
                    y=row["center_y"] + 0.5,  # Rois are centered on the voxel
                    x=row["center_x"] + 0.5,
                    c=index[positions.index.names[1:].index("channel_nr")],
                    stroke_color=mm_schema.Color(
                        r=color[0], g=color[1], b=color[2], alpha=color[3]
                    ),
                    stroke_width=stroke_width,
                )
            )

        if points:
            rois.append(
                mm_schema.Roi(
                    name=f"{root_name}_{image_id}",
                    description=f"{root_name} in image {image_id}",
                    linked_references=image.data_reference,
                    points=points,
                )
            )

    return rois


def _crop_z_profiles(bead_properties: pd.DataFrame, min_axial_distance_px: int) -> None:
    """Crop z profiles in-place to min_axial_distance around center_z, per channel.

    The median FWHM is computed from valid beads only, giving a total window of 8x the
    median FWHM. Profiles that extend beyond the array bounds are clamped (e.g. axial-edge
    beads will produce shorter profiles).
    """
    profile_cols = ["z_raw", "z_fitted_airy", "z_fitted_gaussian"]
    for idx, row in bead_properties.iterrows():
        center_z = int(row["center_z"])
        z_top = int(row.center_z) - min_axial_distance_px
        z_bottom = int(row.center_z) + min_axial_distance_px
        for col in profile_cols:
            profile = row[col]
            if isinstance(profile, np.ndarray):
                # Cuts the relevant section
                profile = profile[max(0, z_top) : min(profile.shape[0], z_bottom)]
                # Pads with "empty" data to get constant length
                profile = np.pad(
                    profile,
                    (
                        (
                            abs(z_top) if z_top < 0 else 0,
                            abs(z_bottom - profile.shape[0]) if z_bottom > profile.shape[0] else 0,
                        )
                    ),
                )

                bead_properties.at[idx, col] = profile


def _extract_profiles(bead_properties, axis: str) -> pd.DataFrame:
    profile_col_names = [
        f"{axis}_raw",
        f"{axis}_fitted_airy",
        f"{axis}_fitted_gaussian",
    ]
    column_indexes = [
        i
        for i in bead_properties.index.names
        if i not in ["channel_name", "excitation_wavelength_nm", "emission_wavelength_nm"]
    ]

    profiles = {}
    for index, row in bead_properties.iterrows():
        if isinstance(index, (list, tuple)):
            index = [index[bead_properties.index.names.index(col_i)] for col_i in column_indexes]

            index_str = "_".join([str(i) for i in index])
        else:
            index_str = str(index)
        for profile_name in profile_col_names:
            profiles[f"{index_str}_{profile_name}"] = pd.Series(row[profile_name])

    bead_properties.drop(columns=profile_col_names, inplace=True)

    return pd.DataFrame(profiles)


def _make_suggestion(bead_properties, input_parameters):
    return "Exemple suggestion"


def analyse_psf_beads(dataset: mm_schema.PSFBeadsDataset) -> bool:

    mm.analyses.validate_images_requirements(
        images_list=dataset.input_data.psf_beads_images,
        axis_to_check_shape=[1, 2, 3, 4],
        saturation_threshold=dataset.input_parameters.saturation_threshold,
        bit_depth=dataset.input_parameters.bit_depth,
    )
    # TODO: Implement Nyquist validation??

    # Containers for input data and input parameters
    min_lateral_distance_px = dataset.input_parameters.min_lateral_distance_px
    min_axial_diatance_px = dataset.input_parameters.min_axial_distance_px
    snr_threshold = dataset.input_parameters.snr_threshold
    fitting_airy_r2_threshold = dataset.input_parameters.fitting_airy_r2_threshold
    fitting_gaussian_r2_threshold = dataset.input_parameters.fitting_gaussian_r2_threshold

    # Containers for output data
    bead_properties = []

    # Second loop main image analysis
    for image in dataset.input_data.psf_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        mm.logger.info(f"Processing image {image_id}...")

        if image.array_data.shape[0] != 1:
            mm.logger.warning(
                f"Image {image_id} must be in TZYXC order and single time-point. Using first time-point."
            )

        voxel_size_micron = (
            image.voxel_size_z_micron,
            image.voxel_size_y_micron,
            image.voxel_size_x_micron,
        )

        image_bead_properties = _process_image(
            image=image,
            sigma_min=dataset.input_parameters.sigma_min,
            sigma_max=dataset.input_parameters.sigma_max,
            min_lateral_distance_px=min_lateral_distance_px,
            min_axial_distance_px=min_axial_diatance_px,
            snr_threshold=snr_threshold,
            fitting_airy_r2_threshold=fitting_airy_r2_threshold,
            fitting_gaussian_r2_threshold=fitting_gaussian_r2_threshold,
            intensity_robust_z_score_threshold=dataset.input_parameters.intensity_robust_z_score_threshold,
        )

        if len(image_bead_properties) == 0:
            mm.logger.warning(f"No beads found in image {image.name}")
            continue

        mm.logger.info(
            f"Image {image_id} processed."
            f"    {image_bead_properties.considered_valid.sum()} beads considered valid."
            f"    {image_bead_properties.considered_lateral_edge.sum()} beads considered lateral edge."
            f"    {image_bead_properties.considered_self_proximity.sum()} beads considered self proximity."
            f"    {image_bead_properties.considered_axial_edge.sum()} beads considered axial edge."
            f"    {image_bead_properties.considered_intensity_std_outlier.sum()} beads considered intensity std outlier."
            f"    {image_bead_properties.considered_bad_fit_airy_z.sum()} beads considered bad Airy fit in z."
            f"    {image_bead_properties.considered_bad_fit_airy_y.sum()} beads considered bad Airy fit in y."
            f"    {image_bead_properties.considered_bad_fit_airy_x.sum()} beads considered bad Airy fit in x."
            f"    {image_bead_properties.considered_bad_fit_gaussian_z.sum()} beads considered bad Gaussian fit in z."
            f"    {image_bead_properties.considered_bad_fit_gaussian_y.sum()} beads considered bad Gaussian fit in y."
            f"    {image_bead_properties.considered_bad_fit_gaussian_x.sum()} beads considered bad Gaussian fit in x."
        )

        _add_row_index_level(image_bead_properties, "image_id", image_id)
        bead_properties.append(image_bead_properties)

    if bead_properties:
        bead_properties = pd.concat(bead_properties)
    else:  # No beads found
        mm.logger.error("No valid or invalid beads found in any image")
        raise mm.AnalysisError(
            message="No valid or invalid beads found in any image",
            suggestion=_make_suggestion(bead_properties, dataset.input_parameters),
        )

    # Crop z profiles to a consistent length before extraction
    _crop_z_profiles(bead_properties, int(min_axial_diatance_px))

    # Extract bead profiles first (needed by _average_beads)
    bead_profiles_z = _extract_profiles(bead_properties, "z")
    bead_profiles_y = _extract_profiles(bead_properties, "y")
    bead_profiles_x = _extract_profiles(bead_properties, "x")

    # Calculate average beads, extract their profiles, and create the average bead image
    (
        average_beads_properties,
        bead_profiles_z,
        bead_profiles_y,
        bead_profiles_x,
        average_bead,
    ) = _average_beads(
        bead_properties=bead_properties,
        voxel_size_micron=voxel_size_micron,
        min_axial_distance_px=min_axial_diatance_px,
        bead_profiles_z=bead_profiles_z,
        bead_profiles_y=bead_profiles_y,
        bead_profiles_x=bead_profiles_x,
        source_images=dataset.input_data.psf_beads_images,
    )

    # At this point we need to drop some data that we don't need anymore
    # bead arrays
    bead_properties.drop("beads", axis=1, inplace=True)
    # shifts for average bead calculation
    bead_properties.drop(["shift_z", "shift_y", "shift_x"], axis=1, inplace=True)

    # At this point we know if we found valid beads, and we raise an exception
    # if there are no beads. Depending on the number of invalid beads and their
    # classes
    if bead_properties["considered_valid"].sum() == 0:
        mm.logger.error("No valid beads found in any image")
        raise mm.AnalysisError(
            message="No beads valid found in any image\n"
            f"  - Lateral_edge: {bead_properties['considered_lateral_edge'].sum()}\n"
            f"  - Axial_edge: {bead_properties['considered_axial_edge'].sum()}\n"
            f"  - Bad_airy_fit_x: {bead_properties['considered_bad_fit_airy_x'].sum()}\n"
            f"  - Bad_airy_fit_y: {bead_properties['considered_bad_fit_airy_y'].sum()}\n"
            f"  - Bad_airy_fit_z: {bead_properties['considered_bad_fit_airy_z'].sum()}\n"
            f"  - Bad_gaussian_fit_x: {bead_properties['considered_bad_fit_gaussian_x'].sum()}\n"
            f"  - Bad_gaussian_fit_y: {bead_properties['considered_bad_fit_gaussian_y'].sum()}\n"
            f"  - Bad_gaussian_fit_z: {bead_properties['considered_bad_fit_gaussian_z'].sum()}\n"
            f"  - Intensity_std_outlier: {bead_properties['considered_intensity_std_outlier'].sum()}",
            suggestion=_make_suggestion(bead_properties, dataset.input_parameters),
        )

    key_measurements = _generate_key_measurements(
        bead_properties=bead_properties,
        average_bead_properties=average_beads_properties,
    )

    considered_valid_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_valid],
        root_name="considered_valid_bead_centers",
        color=(0, 255, 0, 100),
        stroke_width=8,
    )
    considered_lateral_edge_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_lateral_edge],
        root_name="considered_lateral_edge_bead_centers",
        color=(255, 0, 0, 100),
        stroke_width=4,
    )
    considered_self_proximity_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_self_proximity],
        root_name="considered_self_proximity_bead_centers",
        color=(255, 0, 0, 100),
        stroke_width=4,
    )
    considered_axial_edge_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_axial_edge],
        root_name="considered_axial_edge_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_outlier_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_intensity_std_outlier],
        root_name="considered_outlier_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_airy_z_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_airy_z],
        root_name="considered_bad_fit_airy_z_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_airy_y_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_airy_y],
        root_name="considered_bad_fit_airy_y_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_airy_x_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_airy_x],
        root_name="considered_bad_fit_airy_x_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_gaussian_z_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_gaussian_z],
        root_name="considered_bad_fit_gaussian_z_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_gaussian_y_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_gaussian_y],
        root_name="considered_bad_fit_gaussian_y_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )
    considered_bad_fit_gaussian_x_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_bad_fit_gaussian_x],
        root_name="considered_bad_fit_gaussian_x_bead_centers",
        color=(0, 0, 255, 100),
        stroke_width=4,
    )

    bead_properties = mm.analyses.df_to_table(bead_properties.reset_index(), "bead_properties")
    bead_profiles_z = mm.analyses.df_to_table(bead_profiles_z, "bead_profiles_z")
    bead_profiles_y = mm.analyses.df_to_table(bead_profiles_y, "bead_profiles_y")
    bead_profiles_x = mm.analyses.df_to_table(bead_profiles_x, "bead_profiles_x")

    dataset.output = mm_schema.PSFBeadsOutput(
        processing_application=mm.__name__,
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        analyzed_bead_centers=considered_valid_bead_centers,
        considered_bead_centers_lateral_edge=considered_lateral_edge_bead_centers,
        considered_bead_centers_self_proximity=considered_self_proximity_bead_centers,
        considered_bead_centers_axial_edge=considered_axial_edge_bead_centers,
        considered_bead_centers_outlier=considered_outlier_bead_centers,
        considered_bead_centers_z_fit_airy_quality=considered_bad_fit_airy_z_bead_centers,
        considered_bead_centers_y_fit_airy_quality=considered_bad_fit_airy_y_bead_centers,
        considered_bead_centers_x_fit_airy_quality=considered_bad_fit_airy_x_bead_centers,
        considered_bead_centers_z_fit_gaussian_quality=considered_bad_fit_gaussian_z_bead_centers,
        considered_bead_centers_y_fit_gaussian_quality=considered_bad_fit_gaussian_y_bead_centers,
        considered_bead_centers_x_fit_gaussian_quality=considered_bad_fit_gaussian_x_bead_centers,
        key_measurements=key_measurements,
        bead_properties=bead_properties,
        bead_profiles_z=bead_profiles_z,
        bead_profiles_y=bead_profiles_y,
        bead_profiles_x=bead_profiles_x,
        average_bead=average_bead,
    )

    dataset.description = (
        "PSF beads dataset\n"
        f"Successfully analyzed on {dataset.output.processing_datetime}.\n"
        "Found beads:\n"
        f"- Valid: {bead_properties.table_data['considered_valid'].sum()}\n"
        f"- Invalid: {len(bead_properties.table_data) - bead_properties.table_data['considered_valid'].sum()}\n"
        f"  - Lateral_edge: {bead_properties.table_data['considered_lateral_edge'].sum()}\n"
        f"  - Axial_edge: {bead_properties.table_data['considered_axial_edge'].sum()}\n"
        f"  - Bad_airy_fit_x: {bead_properties.table_data['considered_bad_fit_airy_x'].sum()}\n"
        f"  - Bad_airy_fit_y: {bead_properties.table_data['considered_bad_fit_airy_y'].sum()}\n"
        f"  - Bad_airy_fit_z: {bead_properties.table_data['considered_bad_fit_airy_z'].sum()}\n"
        f"  - Bad_gaussian_fit_x: {bead_properties.table_data['considered_bad_fit_gaussian_x'].sum()}\n"
        f"  - Bad_gaussian_fit_y: {bead_properties.table_data['considered_bad_fit_gaussian_y'].sum()}\n"
        f"  - Bad_gaussian_fit_z: {bead_properties.table_data['considered_bad_fit_gaussian_z'].sum()}\n"
        f"  - Intensity_std_outlier: {bead_properties.table_data['considered_intensity_std_outlier'].sum()}"
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
