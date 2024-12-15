from datetime import datetime

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

import microscopemetrics as mm


def _get_intensity_profiles(
    dataset: mm_schema.UserExperimentDataset,
) -> mm_schema.Table:
    pass


def _get_orthogonal_images(
    dataset: mm_schema.UserExperimentDataset,
) -> list[mm_schema.OrthogonalImage]:
    pass


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
