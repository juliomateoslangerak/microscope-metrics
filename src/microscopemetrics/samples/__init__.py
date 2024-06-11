# Main samples module defining the sample superclass
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Union

import microscopemetrics_schema.datamodel as mm_schema
import numpy as np
import pandas as pd

# We are defining some global dictionaries to register the different analysis types
IMAGE_ANALYSIS_REGISTRY = {}
DATASET_ANALYSIS_REGISTRY = {}
PROGRESSION_ANALYSIS_REGISTRY = {}


# Decorators to register exposed analysis functions
def register_image_analysis(cls):
    IMAGE_ANALYSIS_REGISTRY[cls.__name__] = cls
    return cls


def register_dataset_analysis(cls):
    DATASET_ANALYSIS_REGISTRY[cls.__name__] = cls
    return cls


def register_progression_analysis(cls):
    PROGRESSION_ANALYSIS_REGISTRY[cls.__name__] = cls
    return cls


# Create a logging service
logger = logging.getLogger(__name__)
# TODO: work on the loggers


# def get_references(
#     objects: Union[mm_schema.MetricsObject, list[mm_schema.MetricsObject]]
# ) -> List[mm_schema.DataReference]:
#     """Get the references of a metrics object or a list of metrics objects"""
#     if isinstance(objects, mm_schema.MetricsObject):
#         return mm_schema.DataReference(
#             data_uri=objects.data_uri,
#             # HACK: This is a temporary fix to get the first element of the tuple
#             omero_host=objects.omero_host[0],
#             omero_port=objects.omero_port[0],
#             omero_object_type=objects.omero_object_type[0],
#             omero_object_id=objects.omero_object_id,
#         )
#
#     elif isinstance(objects, list):
#         return [get_references(obj) for obj in objects]
#     else:
#         raise ValueError("Input should be a metrics object or a list of metrics objects")


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


# def numpy_to_mask_inlined(
#     array: np.ndarray,
#     name: str = None,
#     description: str = None,
#     image_url: str = None,
#     source_image_url: Union[str, List[str]] = None,
# ) -> mm_schema.ImageMask:
#     """Converts a bool numpy array with dimensions order yx to an inlined mask"""
#     if array.ndim != 2:
#         raise ValueError("Input array should be 2D")
#     if array.dtype != bool and array.dtype == np.uint8:
#         try:
#             array = array.astype(bool)
#         except ValueError:
#             raise ValueError("Input array could not be casted to type bool")
#     if array.dtype != bool:
#         raise ValueError("Input array should be of type bool")
#
#     return mm_schema.ImageMask(
#         name=name,
#         description=description,
#         image_url=image_url,
#         source_image_url=source_image_url,
#         data=array.flatten().tolist(),
#         shape_y=array.shape[0],
#         shape_x=array.shape[1],
#     )
#
#
# def numpy_to_image_inlined(
#     array: np.ndarray,
#     name: str = None,
#     description: str = None,
#     image_url: str = None,
#     source_image_url: Union[str, List[str]] = None,
# ) -> mm_schema.ImageInline:
#     """Converts a numpy array with dimensions order tzyxc or yx to an inlined image"""
#     if array.ndim == 5:
#         return mm_schema.Image5D(
#             name=name,
#             description=description,
#             image_url=image_url,
#             source_image_url=source_image_url,
#             data=array.flatten().tolist(),
#             shape_t=array.shape[0],
#             shape_z=array.shape[1],
#             shape_y=array.shape[2],
#             shape_x=array.shape[3],
#             shape_c=array.shape[4],
#         )
#     elif array.ndim == 2:
#         return mm_schema.Image2D(
#             name=name,
#             description=description,
#             image_url=image_url,
#             source_image_url=source_image_url,
#             data=array.flatten().tolist(),
#             shape_y=array.shape[0],
#             shape_x=array.shape[1],
#         )
#     else:
#         raise NotImplementedError(
#             f"Array of dimension {array.ndim} is not supported by this function"
#         )


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
        columns = [mm_schema.Column(name=n) for n, v in data.items()]
    elif isinstance(data, pd.DataFrame):
        columns = [mm_schema.Column(name=n) for n in data.columns]
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
        column_series=mm_schema.ColumnSeries(columns=columns),
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
