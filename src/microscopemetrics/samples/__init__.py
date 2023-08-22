# Main samples module defining the sample superclass

import logging
from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np

from microscopemetrics.data_schema import core_schema

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


def numpy_to_inlined_mask(
    array: np.ndarray,
    name: str = None,
    description: str = None,
    image_url: str = None,
    source_image_url: Union[str, List[str]] = None,
) -> core_schema.ImageMask:
    """Converts a bool numpy array to an inlined mask"""
    if array.ndim != 2:
        raise ValueError("Input array should be 2D")
    if array.dtype != bool:
        try:
            array = array.astype(bool, casting="safe")
        except ValueError:
            raise ValueError("Input array should be of type bool")

    return core_schema.ImageMask(
        name=name,
        description=description,
        image_url=image_url,
        source_image_url=source_image_url,
        data=array.flatten().tolist(),
        y=core_schema.PixelSeries(values=array.shape[0]),
        x=core_schema.PixelSeries(values=array.shape[1]),
    )


def numpy_to_inlined_image(
    array: np.ndarray,
    name: str = None,
    description: str = None,
    image_url: str = None,
    source_image_url: Union[str, List[str]] = None,
) -> core_schema.ImageInline:
    """Converts a numpy array to an inlined image"""
    if array.ndim == 5:
        return core_schema.Image5D(
            name=name,
            description=description,
            image_url=image_url,
            source_image_url=source_image_url,
            data=array.flatten().tolist(),
            t=core_schema.TimeSeries(values=array.shape[0]),
            z=core_schema.PixelSeries(values=array.shape[1]),
            y=core_schema.PixelSeries(values=array.shape[2]),
            x=core_schema.PixelSeries(values=array.shape[3]),
            c=core_schema.ChannelSeries(values=array.shape[4]),
        )
    elif array.ndim == 2:
        return core_schema.Image2D(
            name=name,
            description=description,
            image_url=image_url,
            source_image_url=source_image_url,
            data=array.flatten().tolist(),
            y=core_schema.PixelSeries(values=array.shape[0]),
            x=core_schema.PixelSeries(values=array.shape[1]),
        )
    else:
        raise NotImplementedError(
            f"Array of dimension {array.ndim} is not supported by this function"
        )


def dict_to_inlined_table(
    dictionary: dict[str, list],
    name: str = None,
    description: str = None,
) -> core_schema.Table:
    """Converts a dictionary to an microscope-metrics inlined table"""
    return core_schema.TableAsDict(
        name=name,
        description=description,
        columns=[dict(zip(dictionary, row)) for row in zip(*dictionary.values())],
    )


class AnalysisMixin(ABC):
    """This is a mixin class defining some helper functions to work with the linkml autogenerated schema."""

    def __init__(self):
        pass

    def describe_requirements(self):
        print(self.input.describe_requirements())

    def validate_requirements(self) -> bool:
        logger.info("Validating requirements...")
        # TODO: check image dimensions/shape
        return True
