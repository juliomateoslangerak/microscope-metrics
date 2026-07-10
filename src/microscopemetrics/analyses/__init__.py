# Main analyses module defining the sample superclass
import csv
from datetime import datetime
from typing import Dict, List, Union

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

from microscopemetrics import DataFormatError, SaturationError, logger
from microscopemetrics.analyses.tools import is_saturated


# TODO: This function is getting the id from OMERO. It should be more general
def get_object_id(
    objects: Union[mm_schema.MetricsObject, List[mm_schema.MetricsObject]],
) -> Union[str, List[str]] | None:
    """Get the object id of a metrics object or a list of metrics objects"""
    if isinstance(objects, list):
        return [get_object_id(obj) for obj in objects]
    if not isinstance(objects, mm_schema.MetricsObject):
        raise ValueError("Input should be a metrics object or a list of metrics objects")
    if objects.data_reference:
        try:
            return objects.data_reference.omero_object_id
        except AttributeError:
            logger.warning(f"Object {objects.name} does not have an object id")
            return None


def numpy_to_mm_image(
    array: np.ndarray,
    name: str = None,
    description: str = None,
    source_images: List[mm_schema.Image] = None,
    acquisition_datetime: str = None,
    channel_names: List[str] = None,
    channel_descriptions: List[str] = None,
    excitation_wavelengths_nm: List[float] = None,
    emission_wavelengths_nm: List[float] = None,
) -> mm_schema.Image:
    """Converts a numpy array with dimensions order tzyxc to an image by reference (not inlined)"""
    if array.ndim == 5:
        shape_t, shape_z, shape_y, shape_x, shape_c = array.shape
    elif array.ndim == 2:
        shape_y, shape_x = array.shape
        shape_t, shape_z, shape_c = 1, 1, 1
        array = array.reshape((1, 1, shape_y, shape_x, 1))
    else:
        raise NotImplementedError(
            f"Array of dimension {array.ndim} is not supported by this function. Image has to have either 5 or 2 dimensions"
        )

    if source_images:
        source_images_refs = [
            i.data_reference for i in source_images if i.data_reference is not None
        ]
    else:
        source_images_refs = None

    if acquisition_datetime is None:
        if source_images is not None and len(source_images) == 1:
            acquisition_datetime = source_images[0].acquisition_datetime
        else:
            acquisition_datetime = datetime.now().isoformat()

    if channel_names is not None and len(channel_names) != shape_c:
        raise ValueError(
            "The number of channel names should be equal to the number of channels in the image"
        )
    if channel_descriptions is not None and len(channel_descriptions) != shape_c:
        raise ValueError(
            "The number of channel descriptions should be equal to the number of channels in the image"
        )
    if excitation_wavelengths_nm is not None and len(excitation_wavelengths_nm) != shape_c:
        raise ValueError(
            "The number of excitation wavelengths should be equal to the number of channels in the image"
        )
    if emission_wavelengths_nm is not None and len(emission_wavelengths_nm) != shape_c:
        raise ValueError(
            "The number of emission wavelengths should be equal to the number of channels in the image"
        )

    channels = []
    for i in range(shape_c):
        channel = mm_schema.Channel(
            name=channel_names[i] if channel_names is not None else str(i),
            description=(channel_descriptions[i] if channel_descriptions is not None else None),
            excitation_wavelength_nm=(
                excitation_wavelengths_nm[i] if excitation_wavelengths_nm is not None else None
            ),
            emission_wavelength_nm=(
                emission_wavelengths_nm[i] if emission_wavelengths_nm is not None else None
            ),
        )
        channels.append(channel)

    return mm_schema.Image(
        name=name,
        description=description,
        source_images=source_images_refs,
        array_data=array,
        shape_t=shape_t,
        shape_z=shape_z,
        shape_y=shape_y,
        shape_x=shape_x,
        shape_c=shape_c,
        acquisition_datetime=acquisition_datetime,
        channel_series=mm_schema.ChannelSeries(channels=channels),
    )


def _create_table(
    data: Union[dict[str, list], pd.DataFrame],
    name: str,
    description: str = None,
    column_descriptions: dict[str, str] = None,
) -> mm_schema.Table:
    if len(data) == 0:
        logger.error(f"Table {name} could not created as there is no data")
        return None

    # TODO: Add values to columns
    if isinstance(data, dict):
        columns = [mm_schema.Column(name=n, values=v) for n, v in data.items()]
    elif isinstance(data, pd.DataFrame):
        columns = [mm_schema.Column(name=n, values=data[n].tolist()) for n in data.columns]
    else:
        raise ValueError("Data should be either a dictionary or a pandas dataframe")

    if column_descriptions is not None:
        for column in columns:
            try:
                column.description = column_descriptions[column.name]
            except KeyError:
                logger.warning(f"Column {column.name} does not have a description")

    return mm_schema.Table(
        name=name,
        description=description,
        columns=columns,
        table_data=data,
    )


def dict_to_table(
    dictionary: dict[str, list],
    name: str,
    description: str = None,
    column_descriptions: dict[str, str] = None,
) -> mm_schema.Table:
    """Converts a dictionary to a microscope-metrics table"""
    if any(len(dictionary[k]) != len(dictionary[list(dictionary)[0]]) for k in dictionary):
        logger.error(f"Table {name} could not created as the columns have different lengths")
        raise ValueError(
            f"Table {name} could not be created. All columns should have the same length"
        )

    if not all(dictionary[k] for k in dictionary):
        logger.warning(f"Table {name} was created empty. All the column values are empty")

    return _create_table(
        name=name,
        description=description,
        column_descriptions=column_descriptions,
        data=dictionary,
    )


def df_to_table(
    dataframe: pd.DataFrame,
    name: str,
    description: str = None,
    column_descriptions: Dict[str, str] = None,
) -> mm_schema.Table:
    """Converts a df to a microscope-metrics table"""
    return _create_table(
        name=name,
        description=description,
        column_descriptions=column_descriptions,
        data=dataframe,
    )


def validate_requirements(
    images_list: list[mm_schema.Image],
    required_dimensions: int = 5,
    require_equal_shapes: bool = True,
    axis_to_check_shape: list[int] | None = None,
    require_equal_channels: bool = True,
    require_lateral_voxel_size: bool = False,
    require_axial_voxel_size: bool = False,
    require_equal_voxel_size: bool = True,
    saturation_threshold: float | None = None,
    bit_depth: int | None = None,
) -> bool:
    logger.info("Validating requirements...")
    if not images_list:
        logger.error("No images provided")
        raise DataFormatError("No images provided")

    images_shape = images_list[0].array_data.shape
    images_channels = images_list[0].channel_series.channels
    voxel_size_micron = (
        images_list[0].voxel_size_z_micron,
        images_list[0].voxel_size_y_micron,
        images_list[0].voxel_size_x_micron,
    )
    saturated_channels = {}

    if require_equal_shapes and axis_to_check_shape is None:
        axis_to_check_shape = list(range(required_dimensions))

    for image in images_list:
        # Check required dimensions
        if len(image.array_data.shape) != required_dimensions:
            logger.error(f"Image {image.name} must be {required_dimensions}D")
            raise DataFormatError(
                f"Image {image.name} must be {required_dimensions}D. {len(image.array_data.shape)}D was provided."
            )

        # Check shapes
        if require_equal_shapes:
            logger.info(f"Checking image {image.name} shape...")
            for axis in axis_to_check_shape:
                if images_shape[axis] != image.array_data.shape[axis]:
                    logger.error("Not all images have the same required shape")
                    raise DataFormatError(
                        "Not all images have the same shapes where required. Please make sure that"
                        "all dimensions are consistent.",
                    )

        # Check channels
        if require_equal_channels:
            logger.info(f"Checking image {image.name} channels...")
            if image.channel_series.channels != images_channels:
                logger.error("Not all images have the same channels")
                raise DataFormatError(
                    "Not all images have the same channels. Please make sure that"
                    "all channels are consistent.",
                )

        # Check pixel sizes
        if require_equal_voxel_size:
            logger.info(f"Checking image {image.name} voxel sizes...")
            if voxel_size_micron != (
                image.voxel_size_z_micron,
                image.voxel_size_y_micron,
                image.voxel_size_x_micron,
            ):
                logger.error("Not all images have the same voxel sizes")
                raise DataFormatError(
                    "Not all images have the same voxel sizes. "
                    "Please make sure that all input data have the same voxel sizes.",
                )
        if require_lateral_voxel_size and (not voxel_size_micron[1] or not voxel_size_micron[2]):
            logger.error("No physical lateral voxel size provided")
            raise DataFormatError("No physical lateral voxel size provided")
        if require_axial_voxel_size and not voxel_size_micron[0]:
            logger.error("No axial voxel size provided")
            raise DataFormatError("No axial voxel size provided")

        # Check image saturation
        if saturation_threshold is not None:
            logger.info(f"Checking image {image.name} saturation...")
            saturated_channels[image.name] = []

            for c in range(image.array_data.shape[-1]):
                if is_saturated(
                    channel=image.array_data[..., c],
                    threshold=saturation_threshold,
                    detector_bit_depth=bit_depth,
                ):
                    logger.error(f"Image {image.name}: channel {c} is saturated")
                    saturated_channels[image.name].append(c)

    if any(len(saturated_channels[name]) for name in saturated_channels):
        logger.error(f"Channels {saturated_channels} are saturated")
        raise SaturationError(f"Channels {saturated_channels} are saturated")


def csv_power_measurements_parser(csv_file):
    """
    This function parses the csv file containing input data for input power measurements
    analysis:
    - LightSources.
    - MeasurementDevices.
    - AcquisitionDateTime.
    - InputData: as for today, containing the PowerMeasurements.

    Parameters
    ----------
    csv_file: a file object

    Returns
    -------

    """
    light_sources = []
    power_meters = []
    acquisition_datetime = None
    input_data = {}
    mode = None

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue  # remove empty lines
            if row[0].replace(" ", "") == "#light_sources":
                mode = "light_sources"
                columns = next(reader)
                continue
            if row[0].replace(" ", "") == "#power_meters":
                mode = "power_meters"
                columns = next(reader)
                continue
            if row[0].replace(" ", "") == "#acquisition_datetime":
                acquisition_datetime = next(reader)[0]
                continue
            if row[0].replace(" ", "") == "#input_data":
                mode = "input_data"
                input_key = next(reader)[0].replace(" ", "").replace("#", "")
                input_data[input_key] = []
                columns = next(reader)
                continue

            if mode == "light_sources":
                row_dict = dict(zip(columns, row))
                light_sources.append(row_dict)

            elif mode == "power_meters":
                row_dict = dict(zip(columns, row))
                power_meters.append(row_dict)

            elif mode == "input_data":
                row_dict = dict(zip(columns, row))
                input_data[input_key].append(row_dict)

    try:
        [ls.pop("") for ls in light_sources]
    except KeyError:
        pass
    try:
        [pm.pop("") for pm in power_meters]
    except KeyError:
        pass
    light_sources = {ls["name"]: mm_schema.LightSource(**ls) for ls in light_sources}
    power_meters = {pm["name"]: mm_schema.PowerMeter(**pm) for pm in power_meters}
    power_measurements = [
        mm_schema.PowerMeasurement(
            light_source=light_sources[pms.pop("light_source")],
            power_meter=power_meters[pms.pop("power_meter")],
            **pms,
        )
        for pms in input_data["power_measurements"]
    ]

    return power_measurements
