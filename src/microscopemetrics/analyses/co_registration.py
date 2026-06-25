from datetime import datetime
from typing import Optional, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

import microscopemetrics as mm
from microscopemetrics.analyses import tools as mm_tools

MAX_NR_PEAKS = 100
# We establish an arbitrary value that defines:
# - the tolerance for a bead to be considered too close to the axial edge
# - the size of the window (times fwhm) for the z profiles
Z_PROFILE_FWHM_HALF_WINDOW = 4


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


def _compute_bead_intensities(
    bead: np.ndarray,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
):
    if not isinstance(bead, np.ndarray) and np.isnan(bead):
        return {
            "intensity_integrated": np.nan,
            "intensity_max": np.nan,
            "intensity_min": np.nan,
            "intensity_std": np.nan,
        }

    return {
        "intensity_integrated": (bead - intensity_min).sum(),
        "intensity_max": bead.max(),
        "intensity_min": bead.min(),
        "intensity_std": bead.std(),
    }


def _locate_beads(
    channels_merge: np.ndarray,
    sigma_min: float,
    sigma_max: float,
    min_distance_px: float,
    snr_threshold: float,
    voxel_size_micron: tuple[float | None, float | None, float | None] | None,
) -> pd.DataFrame:
    bead_properties = mm_tools.find_beads(
        channel=channels_merge,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        min_distance_px=min_distance_px,
        snr_threshold=snr_threshold,
        max_num_peaks=MAX_NR_PEAKS,
    )

    if len(bead_properties) == 0:
        mm.logger.warning("No beads found")
        return pd.DataFrame()

    bead_properties = bead_properties.join(
        bead_properties["beads"].apply(
            lambda x: pd.Series(_compute_bead_intensities(x, voxel_size_micron))
        )
    )

    return bead_properties


def _process_image(
    image: mm_schema.Image,
    sigma_min: float,
    sigma_max: float,
    min_distance_px: float,
    snr_threshold: float,
) -> tuple:
    channel_names = [c.name for c in image.channel_series.channels]
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
        ch_bead_positions = _locate_beads(
            channels_merge=image[..., ch],
            sigma_min=sigma_min,
            sigma_max=sigma_max,
            min_distance_px=min_distance_px,
            snr_threshold=snr_threshold,
            voxel_size_micron=voxel_size_micron,
        )

        _add_row_index_level(ch_bead_positions, "channel_nr", ch)
        _add_row_index_level(ch_bead_positions, "channel_name", channel_names[ch])
        bead_properties.append(ch_bead_positions)

    return pd.concat(bead_properties)


def _estimate_min_bead_distance(dataset: mm_schema.PSFBeadsDataset) -> float:
    # TODO: get the resolution somewhere or pass it as a metadata and remove it from the schema
    # Assuming we are imaging using nyquist criterium,
    # the min distance factor should be roughly twice the min_lateral_distance_factor
    return dataset.input_parameters.min_lateral_distance_factor * 2


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


def _crop_z_profiles(bead_properties: pd.DataFrame) -> None:
    """Crop z profiles in-place to ±4x median FWHM around center_z, per channel.

    The median FWHM is computed from valid beads only, giving a total window of 8x the
    median FWHM. Profiles that extend beyond the array bounds are clamped (e.g. axial-edge
    beads will produce shorter profiles).
    """
    profile_cols = ["z_raw", "z_fitted_airy", "z_fitted_gaussian"]
    median_fwhm_by_channel = (
        bead_properties[bead_properties["considered_valid"]]
        .groupby(level="channel_nr")["fwhm_pixel_z"]
        .median()
    )
    channel_nr_level = bead_properties.index.names.index("channel_nr")
    for idx, row in bead_properties.iterrows():
        channel_nr = idx[channel_nr_level]
        if channel_nr not in median_fwhm_by_channel.index:
            continue
        half_window = int(Z_PROFILE_FWHM_HALF_WINDOW * median_fwhm_by_channel[channel_nr])
        center_z = int(row["center_z"])
        crop_start = max(0, center_z - half_window)
        for col in profile_cols:
            profile = row[col]
            if isinstance(profile, np.ndarray):
                crop_end = min(len(profile), center_z + half_window)
                bead_properties.at[idx, col] = profile[crop_start:crop_end]


def _extract_profiles(bead_properties, axis: str) -> pd.DataFrame:
    profile_col_names = [
        f"{axis}_raw",
        f"{axis}_fitted_airy",
        f"{axis}_fitted_gaussian",
    ]
    column_indexes = [i for i in bead_properties.index.names if i != "channel_name"]

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


def analyse_psf_beads(dataset: mm_schema.CoRegistrationDataset) -> bool:
    mm.analyses.validate_requirements()
    # TODO: Implement Nyquist validation??

    # Containers for input data and input parameters
    images = {}
    images_shape = None
    voxel_size_micron = None
    min_distance_px = _estimate_min_bead_distance(dataset)
    snr_threshold = dataset.input_parameters.snr_threshold
    fitting_airy_r2_threshold = dataset.input_parameters.fitting_airy_r2_threshold
    fitting_gaussian_r2_threshold = dataset.input_parameters.fitting_gaussian_r2_threshold

    # Containers for output data
    saturated_channels = {}
    bead_properties = []

    # First loop to prepare data and do checks
    for image in dataset.input_data.psf_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        images[image_id] = image.array_data[0, ...]

        saturated_channels[image_id] = []

        # Check image shape
        mm.logger.info(f"Checking image {image_id} shape...")
        if len(image.array_data.shape) != 5:
            mm.logger.error(f"Image {image_id} must be 5D")
            raise mm.DataFormatError(
                f"Image {image_id} must be 5D (TZYXC). {len(image.array_data.shape)}D was provided. "
            )

        if image.array_data.shape[0] != 1:
            mm.logger.warning(
                f"Image {image_id} must be in TZYXC order and single time-point. Using first time-point."
            )

        # Check all shapes equal
        if images_shape is None:
            images_shape = image.array_data.shape
        elif images_shape != image.array_data.shape:
            mm.logger.error("Not all images have the same dimensions")
            raise mm.DataFormatError(
                "Not all images have the same sizes. Please make sure that"
                "all dimensions (TZYXC) are consistent.",
                "In a future version, only ZYX will be required to be equal.",
            )

        # Check all pixel sizes equal
        if voxel_size_micron is None:
            voxel_size_micron = (
                image.voxel_size_z_micron,
                image.voxel_size_y_micron,
                image.voxel_size_x_micron,
            )
        elif voxel_size_micron != (
            image.voxel_size_z_micron,
            image.voxel_size_y_micron,
            image.voxel_size_x_micron,
        ):
            mm.logger.error("Not all images have the same voxel sizes")
            raise mm.DataFormatError(
                "Not all images have the same voxel sizes. "
                "Please make sure that all input data have the same voxel sizes.",
            )

        # Check image saturation
        mm.logger.info(f"Checking image {image_id} saturation...")
        for c in range(image.array_data.shape[-1]):
            if mm_tools.is_saturated(
                channel=image.array_data[..., c],
                threshold=dataset.input_parameters.saturation_threshold,
                detector_bit_depth=dataset.input_parameters.bit_depth,
            ):
                mm.logger.error(f"Image {image_id}: channel {c} is saturated")
                saturated_channels[image_id].append(c)

    if any(len(saturated_channels[name]) for name in saturated_channels):
        mm.logger.error(f"Channels {saturated_channels} are saturated")
        raise mm.SaturationError(f"Channels {saturated_channels} are saturated")

    # Second loop main image analysis
    for image in dataset.input_data.psf_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        mm.logger.info(f"Processing image {image_id}...")

        image_bead_properties = _process_image(
            image=image,
            sigma_min=dataset.input_parameters.sigma_min,
            sigma_max=dataset.input_parameters.sigma_max,
            min_distance_px=min_distance_px,
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
            f"    {image_bead_properties.considered_intensity_outlier.sum()} beads considered intensity outlier."
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

    # Crop z profiles to a consistent length (±4x median FWHM per channel) before extraction
    _crop_z_profiles(bead_properties)

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
            message="No beads valid found in any image",
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
    considered_intensity_outlier_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_intensity_outlier],
        root_name="considered_intensity_outlier_bead_centers",
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
        considered_bead_centers_intensity_outlier=considered_intensity_outlier_bead_centers,
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
        f"  - Intensity_outlier: {bead_properties.table_data['considered_intensity_outlier'].sum()}"
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
