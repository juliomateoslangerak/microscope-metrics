from datetime import datetime

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from debugpy.launcher import channel
from scipy.signal import correlate
from skimage.registration import phase_cross_correlation

import microscopemetrics as mm
from microscopemetrics.analyses import analysis_tools as mm_analysis_tools
from microscopemetrics.analyses import schema_tools as mm_schema_tools


def _compute_relative_positions(
    channel: np.ndarray,
    reference_frame: int,
    voxel_size_micron,
):
    relative_positions = {
        "relative_position_pixel_z": [],
        "relative_position_pixel_y": [],
        "relative_position_pixel_x": [],
        "relative_position_micron_z": [],
        "relative_position_micron_y": [],
        "relative_position_micron_x": [],
        "relative_position_micron_3d": [],
    }
    rel_pos_arr = np.ndarray(
        [
            phase_cross_correlation(
                channel[reference_frame],
                t_point_array,
                upsample_factor=4,
            )
            for t_point_array in channel
        ]
    )
    # relative_positions["relative_position_pixel_z"].append(t_point_shift[0])
    # relative_positions["relative_position_pixel_y"].append(t_point_shift[1])
    # relative_positions["relative_position_pixel_x"].append(t_point_shift[2])
    # relative_positions["relative_position_micron_z"].append(
    #     np.nan if voxel_size_micron[0] is None else
    #     t_point_shift[0] * voxel_size_micron[0]
    # )
    # relative_positions["relative_position_micron_y"].append(
    #     np.nan if voxel_size_micron[1] is None else
    #     t_point_shift[1] * voxel_size_micron[1]
    # )
    # relative_positions["relative_position_micron_x"].append(
    #     np.nan if voxel_size_micron[2] is None else
    #     t_point_shift[2] * voxel_size_micron[2]
    # )

    return relative_positions


def _compute_displacements(relative_positions, voxel_size_micron):
    all_micron_sizes = all(voxel_size_micron)
    displacements = {
        "displacement_pixel_z": [0.0],
        "displacement_pixel_y": [0.0],
        "displacement_pixel_x": [0.0],
        "displacement_micron_z": [0.0 if voxel_size_micron[0] else np.nan],
        "displacement_micron_y": [0.0 if voxel_size_micron[1] else np.nan],
        "displacement_micron_x": [0.0 if voxel_size_micron[2] else np.nan],
        "displacement_micron_3d": [0.0 if all_micron_sizes else np.nan],
    }

    for frame_nr in range(1, len(relative_positions["relative_position_micron_x"])):
        displacements["displacement_pixel_z"].append(
            relative_positions["relative_position_pixel_z"][frame_nr]
            - relative_positions["relative_position_pixel_z"][frame_nr - 1]
        )
        displacements["displacement_pixel_y"].append(
            relative_positions["relative_position_pixel_y"][frame_nr]
            - relative_positions["relative_position_pixel_y"][frame_nr - 1]
        )
        displacements["displacement_pixel_x"].append(
            relative_positions["relative_position_pixel_x"][frame_nr]
            - relative_positions["relative_position_pixel_x"][frame_nr - 1]
        )
        displacements["displacement_micron_z"].append(
            relative_positions["relative_position_micron_z"][frame_nr]
            - relative_positions["relative_position_micron_z"][frame_nr - 1]
        )
        displacements["displacement_micron_y"].append(
            relative_positions["relative_position_micron_y"][frame_nr]
            - relative_positions["relative_position_micron_y"][frame_nr - 1]
        )
        displacements["displacement_micron_x"].append(
            relative_positions["relative_position_micron_x"][frame_nr]
            - relative_positions["relative_position_micron_x"][frame_nr - 1]
        )
        displacements["displacement_micron_3d"].append(
            np.sqrt(
                np.sum(
                    [
                        d**2
                        for d in [
                            displacements["displacement_micron_z"][-1],
                            displacements["displacement_micron_y"][-1],
                            displacements["displacement_micron_x"][-1],
                        ]
                    ]
                )
                if all_micron_sizes
                else np.nan
            )
        )

    return displacements


def _compute_velocities(
    displacements,
    time_intervals,
):
    temp_output = [np.nan for _ in displacements["displacement_pixel_z"]]
    velocities = {
        "velocity_pixel_z": temp_output,
        "velocity_pixel_y": temp_output,
        "velocity_pixel_x": temp_output,
        "velocity_micron_z": temp_output,
        "velocity_micron_y": temp_output,
        "velocity_micron_x": temp_output,
        "velocity_micron_3d": temp_output,
    }

    return velocities


def _process_image(
    image: mm_schema.Image,
    channel_nr: int,
    reference_frame_nr: int,
    snr_threshold: float,
):
    image_id = mm_schema_tools.get_object_id(image) or image.name
    mm.logger.info(f"Processing image {image_id}...")

    voxel_size_micron = (
        image.voxel_size_z_micron,
        image.voxel_size_y_micron,
        image.voxel_size_x_micron,
    )

    image_rows = {"image_id": image_id}

    relative_positions = _compute_relative_positions(
        channel=image.array_data[..., channel_nr],
        reference_frame=reference_frame_nr,
        voxel_size_micron=voxel_size_micron,
    )

    displacements = _compute_displacements(relative_positions, voxel_size_micron)

    velocities = _compute_velocities(
        displacements,
        time_intervals=None,
    )

    msd

    return image_rows


def analyse_stage_drift(dataset: mm_schema.StageDriftDataset) -> bool:
    mm_schema_tools.validate_images_requirements(
        images_list=dataset.input_data.beads_images,
        axis_to_check_shape=[0, 1, 2, 3, 4],
        saturation_threshold=dataset.input_parameters.saturation_threshold,
        bit_depth=dataset.input_parameters.bit_depth,
    )

    # Containers for input data and input parameters
    snr_threshold = dataset.input_parameters.snr_threshold
    channel_nr = dataset.input_parameters.channel_nr
    reference_frame_nr = dataset.input_parameters.reference_frame_nr

    image_properties = []

    for image in dataset.input_data.beads_images:
        # TODO: implement here the use ot the analysis_roi
        image_rows = _process_image(
            image=image,
            channel_nr=channel_nr,
            reference_frame_nr=reference_frame_nr,
            snr_threshold=snr_threshold,
        )

    dataset.processed = True

    return True
