from datetime import datetime
from itertools import combinations, permutations
from typing import Optional, Tuple

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from numpy.random.mtrand import permutation
from scipy.signal import correlate
from skimage.registration import phase_cross_correlation

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


def _cross_correlation_translations(
    array1: np.ndarray, array2: np.ndarray, window_size: int
) -> dict:
    """Cross-correlate two arrays and return the maximum value after a fitting."""
    correlated_array = correlate(array1, array2, mode="valid", method="fft")
    max_index = np.unravel_index(np.argmax(correlated_array), correlated_array.shape)
    # Generate profiles
    profile_z_raw = np.squeeze(correlated_array[:, max_index[1], max_index[2]])
    profile_y_raw = np.squeeze(correlated_array[max_index[0], :, max_index[2]])
    profile_x_raw = np.squeeze(correlated_array[max_index[0], max_index[1], :])

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
        mm.logger.error(f"Error while computing the shifts: {e}")
        return {"translation_z": np.nan, "translation_y": np.nan, "translation_x": np.nan}

    return {
        "translation_z": gauss_center_pos_z,
        "translation_y": gauss_center_pos_y,
        "translation_x": gauss_center_pos_x,
    }


def _compute_bead_intensities(
    bead: np.ndarray,
):
    if not isinstance(bead, np.ndarray) and np.isnan(bead):
        return {
            "intensity_integrated": np.nan,
            "intensity_max": np.nan,
            "intensity_min": np.nan,
            "intensity_std": np.nan,
        }

    return {
        "intensity_integrated": (bead - bead.min()).sum(),
        "intensity_max": bead.max(),
        "intensity_min": bead.min(),
        "intensity_std": bead.std(),
    }


def _locate_beads(
    channel: np.ndarray,
    sigma_min: float,
    sigma_max: float,
    min_lateral_distance_px: int,
    min_axial_distance_px: int,
    snr_threshold: float,
) -> pd.DataFrame:
    bead_properties = mm_tools.find_beads(
        channel=channel,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        min_lateral_distance_px=min_lateral_distance_px,
        min_axial_distance_px=min_axial_distance_px,
        snr_threshold=snr_threshold,
        max_num_peaks=MAX_NR_PEAKS,
        return_bead_images=True,
    )

    if len(bead_properties) == 0:
        mm.logger.warning("No beads found")
        return pd.DataFrame()

    bead_properties = bead_properties.join(
        bead_properties["beads"].apply(lambda x: pd.Series(_compute_bead_intensities(x)))
    )

    return bead_properties


def _process_image(
    image: mm_schema.Image,
    sigma_min: float,
    sigma_max: float,
    min_lateral_distance_px: int,
    min_axial_distance_px: int,
    snr_threshold: float,
    reference_channel_nr: int,
):
    channel_names = [c.name for c in image.channel_series.channels]
    excitation_wavelengths_nm = [c.excitation_wavelength_nm for c in image.channel_series.channels]
    emission_wavelengths_nm = [c.emission_wavelength_nm for c in image.channel_series.channels]
    moving_channel_nbs = [ch for ch in range(len(channel_names)) if ch != reference_channel_nr]
    voxel_size_micron = (
        image.voxel_size_z_micron,
        image.voxel_size_y_micron,
        image.voxel_size_x_micron,
    )

    # Get image data and remove the time dimension
    image_data = image.array_data[0, ...]

    # Some images (e.g. OMX-3D-SIM) may contain negative values.
    image_data = np.clip(image_data, a_min=0, a_max=None)

    bead_properties = _locate_beads(
        channel=image_data[..., reference_channel_nr],
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        min_lateral_distance_px=min_lateral_distance_px,
        min_axial_distance_px=min_axial_distance_px,
        snr_threshold=snr_threshold,
    )

    # Image level properties
    image_rows = []
    bead_rows = []
    half_lateral_distance = min_lateral_distance_px // 2
    half_axial_distance = min_axial_distance_px // 2
    for moving_channel_nb in moving_channel_nbs:
        image_shift, image_error, image_phasediff = phase_cross_correlation(
            image_data[..., reference_channel_nr],
            image_data[..., moving_channel_nb],
            upsample_factor=10,
        )
        image_translations = {
            "image_id": mm.analyses.get_object_id(image) or image.name,
            "reference_channel_nr": reference_channel_nr,
            "reference_channel_name": channel_names[reference_channel_nr],
            "channel_nr": moving_channel_nb,
            "channel_name": channel_names[moving_channel_nb],
            "excitation_wavelength_nm": excitation_wavelengths_nm[moving_channel_nb],
            "emission_wavelength_nm": emission_wavelengths_nm[moving_channel_nb],
            "translation_z": image_shift[0],
            "translation_y": image_shift[1],
            "translation_x": image_shift[2],
            "translation_error": image_error,
            "phase_diff": image_phasediff,
        }

        for index, row in bead_properties.iterrows():
            if row.considered_valid:
                bead_shift, bead_error, bead_phase_diff = phase_cross_correlation(
                    image_data[
                        int(row.center_z - half_axial_distance) : int(
                            row.center_z + half_axial_distance
                        ),
                        int(row.center_y - half_lateral_distance) : int(
                            row.center_y + half_lateral_distance
                        ),
                        int(row.center_x - half_lateral_distance) : int(
                            row.center_x + half_lateral_distance
                        ),
                        reference_channel_nr,
                    ],
                    image_data[
                        int(row.center_z - half_axial_distance) : int(
                            row.center_z + half_axial_distance
                        ),
                        int(row.center_y - half_lateral_distance) : int(
                            row.center_y + half_lateral_distance
                        ),
                        int(row.center_x - half_lateral_distance) : int(
                            row.center_x + half_lateral_distance
                        ),
                        moving_channel_nb,
                    ],
                    upsample_factor=10,
                    disambiguate=True,
                )
                if all(voxel_size_micron):
                    bead_shift_micron = (
                        bead_shift[0] * voxel_size_micron[0],
                        bead_shift[1] * voxel_size_micron[1],
                        bead_shift[2] * voxel_size_micron[2],
                    )
                    distance_lateral_micron = np.sqrt(
                        np.sum(
                            [
                                bead_shift_micron[1] ** 2,
                                bead_shift_micron[2] ** 2,
                            ]
                        )
                    )
                    distance_3d_micron = np.sqrt(np.sum([s**2 for s in bead_shift_micron]))
                else:
                    bead_shift_micron = (np.nan, np.nan, np.nan)
                    distance_lateral_micron = np.nan
                    distance_3d_micron = np.nan
                bead_translations = {
                    "image_id": mm.analyses.get_object_id(image) or image.name,
                    "bead_id": index,
                    "reference_channel_nr": reference_channel_nr,
                    "reference_channel_name": channel_names[reference_channel_nr],
                    "channel_nr": moving_channel_nb,
                    "channel_name": channel_names[moving_channel_nb],
                    "excitation_wavelength_nm": excitation_wavelengths_nm[moving_channel_nb],
                    "emission_wavelength_nm": emission_wavelengths_nm[moving_channel_nb],
                    "sigma_LoG": row.sigma_LoG,
                    "center_z": row.center_z,
                    "center_y": row.center_y,
                    "center_x": row.center_x,
                    "considered_self_proximity": row.considered_self_proximity,
                    "considered_lateral_edge": row.considered_lateral_edge,
                    "considered_axial_edge": row.considered_axial_edge,
                    "considered_valid": row.considered_valid,
                    "translation_z_px": bead_shift[0],
                    "translation_y_px": bead_shift[1],
                    "translation_x_px": bead_shift[2],
                    "translation_error_px": bead_error,
                    "translation_z_micron": bead_shift_micron[0],
                    "translation_y_micron": bead_shift_micron[1],
                    "translation_x_micron": bead_shift_micron[2],
                    "distance_lateral_micron": distance_lateral_micron,
                    "distance_3d_micron": distance_3d_micron,
                    "phase_diff": bead_phase_diff,
                }

            else:
                bead_translations = {
                    "image_id": mm.analyses.get_object_id(image) or image.name,
                    "bead_id": index,
                    "reference_channel_nr": reference_channel_nr,
                    "reference_channel_name": channel_names[reference_channel_nr],
                    "channel_nr": moving_channel_nb,
                    "channel_name": channel_names[moving_channel_nb],
                    "excitation_wavelength_nm": excitation_wavelengths_nm[moving_channel_nb],
                    "emission_wavelength_nm": emission_wavelengths_nm[moving_channel_nb],
                    "sigma_LoG": row.sigma_LoG,
                    "center_z": row.center_z,
                    "center_y": row.center_y,
                    "center_x": row.center_x,
                    "considered_self_proximity": row.considered_self_proximity,
                    "considered_lateral_edge": row.considered_lateral_edge,
                    "considered_axial_edge": row.considered_axial_edge,
                    "considered_valid": row.considered_valid,
                }

            bead_rows.append(bead_translations)

        image_rows.append(image_translations)

    return image_rows, bead_rows


def _generate_center_roi(
    dataset: mm_schema.CoRegistrationDataset,
    positions,
    root_name,
    color,
    stroke_width=1,
):
    rois = []

    for image in dataset.input_data.multiwavelength_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        points = []
        for row in positions[positions.image_id == image_id].itertuples():
            points.append(
                mm_schema.Point(
                    name=row.bead_id,
                    z=row.center_z,
                    y=row.center_y + 0.5,  # Rois are centered on the voxel
                    x=row.center_x + 0.5,
                    c=row.reference_channel_nr,
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


def _make_suggestion(bead_properties, input_parameters):
    return "Exemple suggestion"


def analyse_co_registration(
    dataset: mm_schema.CoRegistrationDataset, total_bead_count=None
) -> bool:
    mm.analyses.validate_images_requirements(
        images_list=dataset.input_data.multiwavelength_beads_images,
        axis_to_check_shape=[1, 2, 3, 4],
        saturation_threshold=dataset.input_parameters.saturation_threshold,
        bit_depth=dataset.input_parameters.bit_depth,
    )

    # Containers for input data and input parameters
    min_lateral_distance_px = int(dataset.input_parameters.min_lateral_distance_px)
    min_axial_distance_px = int(dataset.input_parameters.min_axial_distance_px)
    snr_threshold = dataset.input_parameters.snr_threshold
    reference_channel_nr = dataset.input_parameters.reference_channel_nr

    image_properties = []
    bead_properties = []

    # Second loop main image analysis
    for image in dataset.input_data.multiwavelength_beads_images:
        image_id = mm.analyses.get_object_id(image) or image.name
        mm.logger.info(f"Processing image {image_id}...")

        if image.array_data.shape[0] != 1:
            mm.logger.warning(
                f"Image {image_id} must be in TZYXC order and single time-point. Using first time-point."
            )

        image_rows, bead_rows = _process_image(
            image=image,
            sigma_min=dataset.input_parameters.sigma_min,
            sigma_max=dataset.input_parameters.sigma_max,
            min_lateral_distance_px=min_lateral_distance_px,
            min_axial_distance_px=min_axial_distance_px,
            snr_threshold=snr_threshold,
            reference_channel_nr=reference_channel_nr,
        )
        image_properties.extend(image_rows)
        bead_properties.extend(bead_rows)

        if len(bead_rows) == 0:
            mm.logger.warning(f"No beads found in image {image.name}")
            continue

        mm.logger.info(
            f"Image {image_id} processed."
            f"    {sum([1 for r in bead_properties if r['considered_valid']])} beads considered valid."
            f"    {sum([1 for r in bead_properties if r['considered_lateral_edge']])} beads considered lateral edge."
            f"    {sum([1 for r in bead_properties if r['considered_self_proximity']])} beads considered self proximity."
        )

    image_properties = pd.DataFrame(image_properties)

    if bead_properties:
        bead_properties = pd.DataFrame(bead_properties)
    else:  # No beads found
        mm.logger.error("No valid or invalid beads found in any image")
        raise mm.AnalysisError(
            message="No valid or invalid beads found in any image",
            suggestion=_make_suggestion(bead_properties, dataset.input_parameters),
        )

    if bead_properties["considered_valid"].sum() == 0:
        mm.logger.error("No valid beads found in any image")
        raise mm.AnalysisError(
            message="No beads valid found in any image",
            suggestion=_make_suggestion(bead_properties, dataset.input_parameters),
        )
    if bead_properties["considered_valid"].sum() < 3:
        mm.logger.error(
            f"Only {bead_properties['considered_valid'].sum()} valid beads found in all images combined"
        )
        raise mm.AnalysisError(
            message=f"Only {bead_properties['considered_valid'].sum()} valid beads found in all images combined",
            suggestion=_make_suggestion(bead_properties, dataset.input_parameters),
        )

    mm_tools.calculate_bead_outliers(
        bead_properties=bead_properties,
        robust_z_score_threshold=dataset.input_parameters.robust_z_score_threshold,
        measurements=["distance_3d_micron"],
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
    considered_outlier_bead_centers = _generate_center_roi(
        dataset=dataset,
        positions=bead_properties[bead_properties.considered_distance_3d_micron_outlier],
        root_name="considered_outlier_bead_centers",
        color=(255, 0, 0, 100),
        stroke_width=4,
    )

    key_measurements = []
    for channel_nb in bead_properties.channel_nr.unique():
        key_rowset = bead_properties[bead_properties.channel_nr == channel_nb]
        excitation_wavelength_nm = key_rowset.excitation_wavelength_nm.iloc[0]
        emission_wavelength_nm = key_rowset.emission_wavelength_nm.iloc[0]
        key_measurements.append(
            mm_schema.CoRegistrationKeyMeasurement(
                reference_channel_nr=int(key_rowset.reference_channel_nr.iloc[0]),
                reference_channel_name=key_rowset.reference_channel_name.iloc[0],
                channel_nr=channel_nb,
                channel_name=key_rowset.channel_name.iloc[0],
                excitation_wavelength_nm=(
                    excitation_wavelength_nm.item()
                    if excitation_wavelength_nm is not None
                    else None
                ),
                emission_wavelength_nm=(
                    emission_wavelength_nm.item() if emission_wavelength_nm is not None else None
                ),
                total_bead_count=len(key_rowset),
                considered_valid_count=key_rowset.considered_valid.sum(),
                considered_self_proximity_count=key_rowset.considered_self_proximity.sum(),
                considered_lateral_edge_count=key_rowset.considered_lateral_edge.sum(),
                considered_axial_edge_count=key_rowset.considered_axial_edge.sum(),
                considered_outlier_count=key_rowset.considered_distance_3d_micron_outlier.sum(),
                translation_abs_mean_pixel_x=float(key_rowset.translation_x_px.abs().mean()),
                translation_abs_mean_pixel_y=float(key_rowset.translation_y_px.abs().mean()),
                translation_abs_mean_pixel_z=float(key_rowset.translation_z_px.abs().mean()),
                translation_abs_mean_micron_x=float(key_rowset.translation_x_micron.abs().mean()),
                translation_abs_mean_micron_y=float(key_rowset.translation_y_micron.abs().mean()),
                translation_abs_mean_micron_z=float(key_rowset.translation_z_micron.abs().mean()),
                distance_mean_micron_3d=float(key_rowset.distance_3d_micron.mean()),
                rotation_z_mean=np.nan,  # TODO: rotation is not implemented
            )
        )

    image_properties = mm.analyses.df_to_table(image_properties, "image_properties")
    bead_properties = mm.analyses.df_to_table(bead_properties.reset_index(), "bead_properties")

    dataset.output = mm_schema.CoRegistrationOutput(
        processing_application=mm.__name__,
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        analyzed_bead_centers=considered_valid_bead_centers,
        considered_bead_centers_lateral_edge=considered_lateral_edge_bead_centers,
        considered_bead_centers_self_proximity=considered_self_proximity_bead_centers,
        considered_bead_centers_outlier=considered_outlier_bead_centers,
        key_measurements=key_measurements,
        image_properties=image_properties,
        bead_properties=bead_properties,
    )

    dataset.description = (
        "PSF beads dataset\n"
        f"Successfully analyzed on {dataset.output.processing_datetime}.\n"
        "Found beads:\n"
        f"- Valid: {bead_properties.table_data['considered_valid'].sum()}\n"
        f"- Invalid: {len(bead_properties.table_data) - bead_properties.table_data['considered_valid'].sum()}\n"
        f"  - Lateral_edge: {bead_properties.table_data['considered_lateral_edge'].sum()}\n"
        f"  - Axial_edge: {bead_properties.table_data['considered_axial_edge'].sum()}\n"
        f"  - Self_proximity: {bead_properties.table_data['considered_self_proximity'].sum()}\n"
    )

    dataset.processed = True

    return True
