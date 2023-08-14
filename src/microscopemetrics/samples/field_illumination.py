from datetime import datetime
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import scipy
from numpy import float64, ndarray
from skimage.filters import gaussian
from skimage.measure import regionprops

import microscopemetrics.data_schema.samples.field_illumination_schema as schema
from microscopemetrics.samples import AnalysisMixin, logger, numpy_to_inlined_image
from microscopemetrics.utilities.utilities import is_saturated


def _channel_intensity_map(channel, map_size: int):
    """
    Compute the intensity map of a channel
    Parameters
    ----------
    channel : np.array.
        image on a 2d ndarray format.
    map_size : int
        size of the intensity map.
    Returns
    -------
    intensity_map : ndarray
        2d ndarray representing the intensity map of the chosen channel.
    """
    channel = channel / channel.max()
    return scipy.ndimage.zoom(channel, map_size / channel.shape[0])


def _image_intensity_map(image: np.ndarray, map_size: int):
    """
    Compute the intensity map of an image
    Parameters
    ----------
    image : ndarray.
        image on a 3d ndarray format yxc.
    map_size : int
        size of the intensity map.
    Returns
    -------
    intensity_map : ndarray
        3d ndarray representing the intensity map of the chosen image.
    """
    output = np.zeros((map_size, map_size, image.shape[2]))
    for c in range(image.shape[2]):
        output[:, :, c] = _channel_intensity_map(np.squeeze(image[:, :, c]), map_size)

    # We want to return a 5d array (adding z and t) for compatibility with the rest of the code
    return np.expand_dims(output, axis=(0, 1))


def _channel_line_profile(
    channel: ndarray, start: Tuple[int, int], end: Tuple[int, int], profile_size: int
) -> ndarray:
    """
    Compute the intensity profile along a line between x0-y0 and x1-y1 using cubic interpolation
    Parameters
    ----------
    channel : np.array.
        image on a 2d ndarray format.
    start : (int, int)
        coordinates of the starting pixel
    end : (int, int)
        coordinates of the ending pixel
    Returns
    -------
    line_pixel_values : ndarray
        1d ndarray representing the values of the chosen line of pixels.
    """
    x, y = np.linspace(start[0], end[0], profile_size), np.linspace(start[1], end[1], profile_size)

    return scipy.ndimage.map_coordinates(channel, np.vstack((x, y)))


def _image_line_profile(image: ndarray, profile_size: int):
    """
    Compute the intensity profile along a line between x0-y0 and x1-y1
    Parameters
    ----------
    image : ndarray.
        image on a 3d ndarray format yxc.
    profile_size : int
        size of the intensity profile.
    Returns
    -------
    line_pixel_values : ndarray
        2d ndarray representing the values of the chosen line of pixels for each channel.
    """
    profile_coordinates = {
        "leftTop_to_rightBottom": ((0, 0), (image.shape[1], image.shape[0])),
        "leftBottom_to_rightTop": ((0, image.shape[0]), (image.shape[1], 0)),
        "center_horizontal": (
            (0, image.shape[0] // 2),
            (image.shape[1], image.shape[0] // 2),
        ),
        "center_vertical": (
            (image.shape[1] // 2, 0),
            (image.shape[1] // 2, image.shape[0]),
        ),
    }
    output = pd.DataFrame()
    for profile_name, (start, end) in profile_coordinates.items():
        profiles = np.zeros((image.shape[2], 255))
        for c in range(image.shape[2]):
            profiles[c, :] = _channel_line_profile(
                np.squeeze(image[:, :, c]), start, end, profile_size
            )
        output = pd.concat(
            [
                output,
                pd.DataFrame(
                    profiles.T,
                    columns=[f"ch_{c}_{profile_name}" for c in range(image.shape[2])],
                ),
            ],
            axis=1,
        )

    return output


def _segment_channel(channel, threshold: float, sigma: float):
    if sigma is not None:
        channel = gaussian(image=channel, sigma=sigma, preserve_range=True, channel_axis=None)

    channel_norm = channel / np.max(channel)
    return (channel_norm > threshold).astype(int)


def _channel_max_intensity_properties(
    channel: np.array, sigma: float, center_threshold: float
) -> dict:
    """Computes the center of mass and the max intensity of the maximum intensity region of an image.
    Parameters
    ----------
    channel : np.array.
        2d ndarray.
    Returns
    -------
    center_of_mass: dict
        dict enclosing the number of pixels, the coordinates of the
        center of mass of the and the max intensity value of the max intensity
        area of the provided image.
    """
    max_intensity = np.max(channel)
    # TODO: check if there is more than one pixel with the same intensity.
    #  We take the first one but we should take the one closest to the center or use a find_peaks function
    max_intensity_indexes = np.unravel_index(np.argmax(channel), channel.shape)

    max_int_mask = _segment_channel(channel, center_threshold, sigma)
    image_properties = regionprops(max_int_mask, channel)

    return {
        "nb_pixels": image_properties[0].area,
        "center_of_mass_x": image_properties[0].centroid_weighted[0],
        "center_of_mass_y": image_properties[0].centroid_weighted[1],
        "max_intensity": max_intensity,
        "max_intensity_pos_x": max_intensity_indexes[0],
        "max_intensity_pos_y": max_intensity_indexes[1],
    }


def _channel_corner_properties(channel, corner_fraction=0.1):
    max_intensity = np.max(channel)

    # Calculate the corner fraction in pixels (cfp) of the image size
    # to use as the corner size and the center range (cr)
    cfp = int(corner_fraction * (channel.shape[0] + channel.shape[1]) / 2)
    cr_y = int((channel.shape[0] - cfp) / 2)
    cr_x = int((channel.shape[1] - cfp) / 2)

    return {
        "top-left_intensity_mean": np.mean(channel[0:cfp, 0:cfp]),
        "top-left_intensity_ratio": np.mean(channel[0:cfp, 0:cfp]) / max_intensity,
        "top-center_intensity_mean": np.mean(channel[cr_x:-cr_x, 0:cfp]),
        "top-center_intensity_ratio": np.mean(channel[cr_x:-cr_x, 0:cfp]) / max_intensity,
        "top-right_intensity_mean": np.mean(channel[-cfp:-1, 0:cfp]),
        "top-right_intensity_ratio": np.mean(channel[-cfp:-1, 0:cfp]) / max_intensity,
        "middle-left_intensity_mean": np.mean(channel[0:cfp, cr_y:-cr_y]),
        "middle-left_intensity_ratio": np.mean(channel[0:cfp, cr_y:-cr_y]) / max_intensity,
        "middle-center_intensity_mean": np.mean(channel[cr_x:-cr_x, cr_y:-cr_y]),
        "middle-center_intensity_ratio": np.mean(channel[cr_x:-cr_x, cr_y:-cr_y]) / max_intensity,
        "middle-right_intensity_mean": np.mean(channel[-cfp:-1, cr_y:-cr_y]),
        "middle-right_intensity_ratio": np.mean(channel[-cfp:-1, cr_y:-cr_y]) / max_intensity,
        "bottom-left_intensity_mean": np.mean(channel[0:cfp, -cfp:-1]),
        "bottom-left_intensity_ratio": np.mean(channel[0:cfp, -cfp:-1]) / max_intensity,
        "bottom-center_intensity_mean": np.mean(channel[cr_x:-cr_x, -cfp:-1]),
        "bottom-center_intensity_ratio": np.mean(channel[cr_x:-cr_x, -cfp:-1]) / max_intensity,
        "bottom-right_intensity_mean": np.mean(channel[-cfp:-1, -cfp:-1]),
        "bottom-right_intensity_ratio": np.mean(channel[-cfp:-1, -cfp:-1]) / max_intensity,
    }


def _channel_area_deciles(channel: ndarray) -> dict:
    """Computes the intensity deciles of an image.
    Parameters
    ----------
    channel : np.array.
        2d ndarray.
    Returns
    -------
    deciles: dict
        dict enclosing the intensity deciles of the provided channel.
    """
    channel = channel / np.max(channel)
    return {f"decile_{i}": np.percentile(channel, i * 10) for i in range(10)}


def _image_properties(
    image: ndarray, corner_fraction: float, sigma: float, center_threshold: float
):
    """
    given an image in a 3d ndarray format (cxy), this function return intensities for the corner and central regions
    and their ratio over the maximum intensity value of the array.
    Parameters
    ----------
    image : ndarray
        image on a 2d np.ndarray in yxc format.
    Returns
    -------
    profiles_statistics : dict
        Dictionary showing the intensity values of the different regions and
        their ratio over the maximum intensity value of the array.
        Dictionary values will be lists in case of multiple channels.
    """
    properties = []
    for c in range(image.shape[2]):
        channel_properties = {"channel": c}
        channel_properties.update(
            _channel_max_intensity_properties(image[:, :, c], sigma, center_threshold)
        )
        channel_properties.update(_channel_corner_properties(image[:, :, c], corner_fraction))
        channel_properties.update(_channel_area_deciles(image[:, :, c]))
        if image.shape[2] == 1:
            return channel_properties
        else:
            properties.append(channel_properties)

    properties = {k: [i[k] for i in properties] for k in properties[0]}
    return properties


class FieldIlluminationAnalysis(schema.FieldIlluminationDataset, AnalysisMixin):
    """This analysis creates a report on field illumination homogeneity based on input images"""

    def run(self) -> bool:
        self.validate_requirements()

        # Check image shape
        logger.info("Checking image shape...")
        image = self.input.field_illumination_image.data
        if len(image.shape) != 5:
            logger.error("Image must be 5D")
            return False
        if image.shape[0] != 1 or image.shape[1] != 1:
            logger.warning(
                "Image must be in TZYXC order, single z and single time-point. Using first z and time-point."
            )
        # For the analysis we are using only the first z and time-point
        image = image[0, 0, :, :, :].reshape((image.shape[2], image.shape[3], image.shape[4]))

        # Check image saturation
        logger.info("Checking image saturation...")
        saturated_channels = []
        for c in range(image.shape[2]):
            if is_saturated(
                channel=image[:, :, c],
                threshold=self.input.saturation_threshold,
                detector_bit_depth=self.input.bit_depth,
            ):
                logger.error(f"Channel {c} is saturated")
                saturated_channels.append(c)
        if len(saturated_channels):
            logger.error(f"Channels {saturated_channels} are saturated")
            return False

        self.output.regions_properties = _image_properties(
            image=image,
            corner_fraction=self.input.corner_fraction,
            sigma=self.input.sigma,
            center_threshold=self.input.center_threshold,
        )

        # self.output.regions_properties = schema.TableAsPandasDF(
        #     df=_image_properties(
        #         image=image,
        #         corner_fraction=self.input.corner_fraction,
        #         sigma=self.input.sigma,
        #         center_threshold=self.input.center_threshold,
        #     )
        # )

        self.output.intensity_map = numpy_to_inlined_image(
            array=_image_intensity_map(image=image, map_size=self.input.intensity_map_size),
            name=f"{self.input.field_illumination_image.name}_intensity_map",
            description=f"Intensity map of {self.input.field_illumination_image.uri}",
            uri=None,
        )

        self.output.intensity_plots = schema.TableAsPandasDF(
            df=_image_line_profile(image, profile_size=255)
        )

        self.processing_date = datetime.today()
        self.processed = True

        return True
