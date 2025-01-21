from datetime import datetime

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd
from scipy.ndimage import zoom
from skimage.measure import profile_line

import microscopemetrics as mm


def _generate_profile(
    image: mm_schema.Image,
    roi: mm_schema.Roi,
) -> mm_schema.Table:
    line = roi.lines[0]

    profile = profile_line(
        image=image.array_data[0, int(line.z), :, :, :],  # T  # Z  # Y  # X  # C
        src=(line.x1, line.y1),
        dst=(line.x2, line.y2),
    )

    columns = [
        mm_schema.Column(
            name="position",
            description="Position along the line",
            data_type="float",
            values=list(range(len(profile))),
        )
    ]
    columns.extend(
        [
            mm_schema.Column(
                name=f"intensity_{c}",
                description=f"Intensity value for channel {c}",
                values=profile[..., c].tolist(),
            )
            for c in range(profile.shape[-1])
        ]
    )

    return mm_schema.Table(
        name=f"{image.name}_{roi.name}_profile",
        description=f"Intensity profile of {roi.name} in {image.name}",
        columns=columns,
    )


def _generate_intensity_profiles(
    dataset: mm_schema.UserExperimentDataset,
) -> list[mm_schema.Table]:
    tables = []

    for roi in dataset.input_data.profile_rois:
        if len(roi.linked_references) != 1:
            raise ValueError("ROI must be linked to exactly one image")

        image = next(
            (
                img
                for img in dataset.input_data.user_experiment_images
                if mm.analyses.get_object_id(roi.linked_references[0])
                == mm.analyses.get_object_id(img)
            ),
            None,
        )
        if image is None:
            raise ValueError("ROI must be linked to an image in the dataset")

        tables.append(
            _generate_profile(
                image=image,
                roi=roi,
            )
        )

    return tables


def _generate_orthogonals(
    image: mm_schema.Image,
    roi: mm_schema.Roi,
) -> tuple[list[mm_schema.OrthogonalImage], list[mm_schema.Roi]]:
    try:
        # We are assuming that the ROI is a single point
        coords = (int(roi.points[0].z), int(roi.points[0].y), int(roi.points[0].x))
    except AttributeError as e:
        raise AttributeError("ROI must have points") from e

    # We are assuming that the voxel size is the same for x and y
    z_ratio = image.voxel_size_z_micron / image.voxel_size_x_micron

    orthogonals = [
        mm_schema.OrthogonalImage(
            name=f"{image.name}_XY_{roi.name}",
            description=f"XY orthogonal view of {image.name} at {coords}",
            channel_series=image.channel_series,
            shape_x=image.shape_x,
            shape_y=image.shape_y,
            shape_z=1,
            source_images=image.data_reference,
            source_roi=roi,
            axis="XY",
            array_data=image.array_data[:, coords[0] : (coords[0] + 1), :, :, :],  # dims TZYXC
        ),
        mm_schema.OrthogonalImage(
            name=f"{image.name}_YZ_{roi.name}",
            description=f"YZ orthogonal view of {image.name} at {coords}",
            channel_series=image.channel_series,
            shape_x=int(np.round(image.shape_z * z_ratio)),
            shape_y=image.shape_y,
            shape_z=1,
            source_images=image.data_reference,
            source_roi=roi,
            axis="YZ",
            array_data=zoom(
                input=np.transpose(
                    image.array_data[:, :, :, coords[1] : (coords[1] + 1), :],  # dims TZYXC
                    axes=(0, 3, 2, 1, 4),  # dims TXYZC
                ),
                zoom=(1, 1, 1, z_ratio, 1),
            ),
        ),
        mm_schema.OrthogonalImage(
            name=f"{image.name}_XZ_{roi.name}",
            description=f"XZ orthogonal view of {image.name} at {coords}",
            channel_series=image.channel_series,
            shape_x=image.shape_x,
            shape_y=int(np.round(image.shape_z * z_ratio)),
            shape_z=1,
            source_images=image.data_reference,
            source_roi=roi,
            axis="XZ",
            array_data=zoom(
                input=np.transpose(
                    image.array_data[:, :, coords[2] : (coords[2] + 1), :, :],  # dims TZYXC
                    axes=(0, 2, 1, 3, 4),  # dims TYZXC
                ),
                zoom=(1, 1, z_ratio, 1, 1),
            ),
        ),
    ]

    section_rois = [
        mm_schema.Roi(
            name=f"{roi.name}_XY",
            description=f"XY position of {roi.name}",
            lines=[
                mm_schema.Line(
                    name=f"section_line_XZ_{roi.name}",
                    x1=0,
                    y1=coords[1],
                    x2=orthogonals[0].shape_x,
                    y2=coords[1],
                ),
                mm_schema.Line(
                    name=f"section_line_YZ_{roi.name}",
                    x1=coords[2],
                    y1=0,
                    x2=coords[2],
                    y2=orthogonals[0].shape_y,
                ),
            ],
        ),
        mm_schema.Roi(
            name=f"{roi.name}_YZ",
            description=f"YZ position of {roi.name}",
            lines=[
                mm_schema.Line(
                    name=f"section_line_XY_{roi.name}",
                    x1=coords[0] * z_ratio,
                    y1=0,
                    x2=coords[0] * z_ratio,
                    y2=orthogonals[1].shape_y,
                ),
                mm_schema.Line(
                    name=f"section_line_XZ_{roi.name}",
                    x1=0,
                    y1=coords[1],
                    x2=orthogonals[1].shape_x,
                    y2=coords[1],
                ),
            ],
        ),
        mm_schema.Roi(
            name=f"{roi.name}_XZ",
            description=f"XZ position of {roi.name}",
            lines=[
                mm_schema.Line(
                    name=f"section_line_XY_{roi.name}",
                    x1=0,
                    y1=coords[0] * z_ratio,
                    x2=orthogonals[2].shape_x,
                    y2=coords[0] * z_ratio,
                ),
                mm_schema.Line(
                    name=f"section_line_YZ_{roi.name}",
                    x1=coords[2],
                    y1=0,
                    x2=coords[2],
                    y2=orthogonals[2].shape_y,
                ),
            ],
        ),
    ]

    return orthogonals, section_rois


def _generate_orthogonal_images(
    dataset: mm_schema.UserExperimentDataset,
) -> list[mm_schema.OrthogonalImage]:
    orthogonals = []
    section_rois = []

    for roi in dataset.input_data.orthogonal_rois:
        if len(roi.linked_references) != 1:
            raise ValueError("ROI must be linked to exactly one image")

        image = next(
            (
                img
                for img in dataset.input_data.user_experiment_images
                if mm.analyses.get_object_id(roi.linked_references[0])
                == mm.analyses.get_object_id(img)
            ),
            None,
        )
        if image is None:
            raise ValueError("ROI must be linked to an image in the dataset")

        o, r = _generate_orthogonals(image=image, roi=roi)
        orthogonals.extend(o)
        section_rois.extend(r)

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

    intensity_profiles = _generate_intensity_profiles(dataset)
    orthogonal_images = _generate_orthogonal_images(dataset)
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
