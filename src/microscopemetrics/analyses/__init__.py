# Main analyses module defining the sample superclass
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Union

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

# Create a logging service
logger = logging.getLogger(__name__)


def get_object_id(
    objects: Union[mm_schema.MetricsObject, List[mm_schema.MetricsObject]]
) -> Union[str, List[str]]:
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
            name=channel_names[i] if channel_names is not None else None,
            description=channel_descriptions[i] if channel_descriptions is not None else None,
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


def validate_requirements() -> bool:
    logger.info("Validating requirements...")
    # TODO: check image dimensions/shape
    return True
