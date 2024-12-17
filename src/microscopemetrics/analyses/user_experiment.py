from datetime import datetime

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from skimage.measure import profile_line

import microscopemetrics as mm


def _get_intensity_profiles(
    dataset: mm_schema.UserExperimentDataset,
) -> mm_schema.Table:
    pass


def _get_orthogonals(
    image: mm_schema.Image,
    roi: mm_schema.Roi,
) -> list[mm_schema.OrthogonalImage]:
    try:
        coords = [(int(p.z), int(p.y), int(p.x)) for p in roi.points]
    except AttributeError as e:
        raise AttributeError("ROI must have points") from e

    orthogonals = []

    for coord in coords:
        orthogonals.extend(
            (
                mm_schema.OrthogonalImage(
                    shape_x=image.shape_x,
                    shape_y=image.shape_y,
                    shape_z=1,
                    source_image=image,
                    source_roi=roi,
                    axis="XY",
                    array_data=image.array_data[:, coord[0], :, :, :],
                ),
                mm_schema.OrthogonalImage(
                    shape_x=1,
                    shape_y=image.shape_y,
                    shape_z=image.shape_z,
                    source_image=image,
                    source_roi=roi,
                    axis="YZ",
                    array_data=image.array_data[:, :, :, coord[1], :],
                ),
                mm_schema.OrthogonalImage(
                    shape_x=image.shape_x,
                    shape_y=image.shape_z,
                    shape_z=1,
                    source_image=image,
                    source_roi=roi,
                    axis="XZ",
                    array_data=image.array_data[:, :, coord[2], :, :],
                ),
            )
        )
    return orthogonals


def _get_orthogonal_images(
    dataset: mm_schema.UserExperimentDataset,
) -> list[mm_schema.OrthogonalImage]:
    orthogonals = []

    for roi in dataset.input_data.orthogonal_rois:
        if len(roi.linked_references) != 1:
            raise ValueError("ROI must be linked to exactly one image")
        orthogonals.extend(
            _get_orthogonals(
                image=dataset.input_data.user_experiment_images[
                    mm.analyses.get_object_id(roi.linked_references[0])
                ],
                roi=roi,
            )
        )

    return orthogonals


def _get_fft_images(
    dataset: mm_schema.UserExperimentDataset,
) -> list[mm_schema.Image]:
    pass


def _get_key_measurements(
    dataset: mm_schema.UserExperimentDataset,
) -> mm_schema.UserExperimentKeyMeasurements:
    pass


def analyse_user_experiment(dataset: mm_schema.UserExperimentDataset) -> bool:
    mm.analyses.validate_requirements()

    # Containers for output data
    saturated_channels = {}

    # First loop to prepare data
    for image in dataset.input_data.user_experiment_images:
        image_id = mm.analyses.get_object_id(image) or image.name

        saturated_channels[image_id] = []

        # Check image shape
        mm.logger.info(f"Checking image {image_id} shape...")
        if len(image.array_data.shape) != 5:
            mm.logger.error(f"Image {image_id} must be 5D")
            return False

        # Check image saturation
        mm.logger.info(f"Checking image {image_id} saturation...")
        for c in range(image.array_data.shape[-1]):
            if mm.analyses.tools.is_saturated(
                channel=image.array_data[..., c],
                threshold=dataset.input_parameters.saturation_threshold,
                detector_bit_depth=dataset.input_parameters.bit_depth,
            ):
                mm.logger.warning(f"Image {image_id}: channel {c} is saturated")
                saturated_channels[image_id].append(c)

    intensity_profiles = _get_intensity_profiles(dataset)
    orthogonal_images = _get_orthogonal_images(dataset)
    fft_images = _get_fft_images(dataset)

    dataset.output = mm_schema.UserExperimentOutput(
        processing_application="microscopemetrics",
        processing_version=mm.__version__,
        processing_datetime=datetime.now(),
        intensity_profiles=intensity_profiles,
        orthogonal_images=orthogonal_images,
        fft_images=fft_images,
    )

    dataset.processed = True

    return True
