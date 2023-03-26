import numpy as np
import pandas as pd
import scipy
from skimage.filters import gaussian
from skimage.measure import regionprops

from microscopemetrics.samples import *
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
        image on a 3d ndarray format cxy.
    map_size : int
        size of the intensity map.
    Returns
    -------
    intensity_map : ndarray
        3d ndarray representing the intensity map of the chosen image.
    """
    output = np.zeros((image.shape[0], map_size, map_size))
    for c in range(image.shape[0]):
        output[c, :, :] = _channel_intensity_map(np.squeeze(image[c, :, :]), map_size)

    # We want to return a 5d array (adding z and t) for compatibility with the rest of the code
    return np.expand_dims(output, axis=(0, 2))


def _channel_line_profile(channel, start, end, profile_size: int):
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


def _image_line_profile(image: np.ndarray, profile_size: int):
    """
    Compute the intensity profile along a line between x0-y0 and x1-y1
    Parameters
    ----------
    image : ndarray.
        image on a 3d ndarray format cxy.
    profile_size : int
        size of the intensity profile.
    Returns
    -------
    line_pixel_values : ndarray
        2d ndarray representing the values of the chosen line of pixels for each channel.
    """
    profile_coordinates = {
        "leftTop_to_rightBottom": ((0, 0), (image.shape[1], image.shape[2])),
        "leftBottom_to_rightTop": ((0, image.shape[2]), (image.shape[1], 0)),
        "center_horizontal": ((0, image.shape[2] // 2), (image.shape[1], image.shape[2] // 2)),
        "center_vertical": ((image.shape[1] // 2, 0), (image.shape[1] // 2, image.shape[2])),
    }
    output = pd.DataFrame()
    for profile_name, (start, end) in profile_coordinates.items():
        profiles = np.zeros((image.shape[0], 255))
        for c in range(image.shape[0]):
            profiles[c, :] = _channel_line_profile(
                np.squeeze(image[c, :, :]), start, end, profile_size
            )
        output = pd.concat(
            [
                output,
                pd.DataFrame(
                    profiles.T, columns=[f"ch_{c}_{profile_name}" for c in range(image.shape[0])]
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

    # calculate the corner fraction in pixels (cfp) of the image size to use as the corner size and the center range (cr)
    cfp = int(corner_fraction * (channel.shape[0] + channel.shape[1]) / 2)
    cr_x = int((channel.shape[0] - cfp) / 2)
    cr_y = int((channel.shape[1] - cfp) / 2)

    return {
        "top-left_intensity_mean": np.mean(channel[0:cfp, 0:cfp]),
        "top-left_intensity_ratio": np.mean(channel[0:cfp, 0:cfp]) / max_intensity,
        "top-center_intensity_mean": np.mean(channel[0:cfp, cr_x:-cr_x]),
        "top-center_intensity_ratio": np.mean(channel[0:cfp, cr_x:-cr_x]) / max_intensity,
        "top-right_intensity_mean": np.mean(channel[0:cfp, -cfp:-1]),
        "top-right_intensity_ratio": np.mean(channel[0:cfp, -cfp:-1]) / max_intensity,
        "middle-left_intensity_mean": np.mean(channel[cr_y:-cr_y, 0:cfp]),
        "middle-left_intensity_ratio": np.mean(channel[cr_y:-cr_y, 0:cfp]) / max_intensity,
        "middle-center_intensity_mean": np.mean(channel[cr_y:-cr_y, cr_x:-cr_x]),
        "middle-center_intensity_ratio": np.mean(channel[cr_y:-cr_y, cr_x:-cr_x]) / max_intensity,
        "middle-right_intensity_mean": np.mean(channel[cr_y:-cr_y, -cfp:-1]),
        "middle-right_intensity_ratio": np.mean(channel[cr_y:-cr_y, -cfp:-1]) / max_intensity,
        "bottom-left_intensity_mean": np.mean(channel[-cfp:-1, 0:cfp]),
        "bottom-left_intensity_ratio": np.mean(channel[-cfp:-1, 0:cfp]) / max_intensity,
        "bottom-center_intensity_mean": np.mean(channel[-cfp:-1, cr_x:-cr_x]),
        "bottom-center_intensity_ratio": np.mean(channel[-cfp:-1, cr_x:-cr_x]) / max_intensity,
        "bottom-right_intensity_mean": np.mean(channel[-cfp:-1, -cfp:-1]),
        "bottom-right_intensity_ratio": np.mean(channel[-cfp:-1, -cfp:-1]) / max_intensity,
    }


def _channel_area_deciles(channel: np.array) -> dict:
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


def _image_properties(image, corner_fraction: float, sigma: float, center_threshold: float):
    """
    given an image in a 3d ndarray format (cxy), this function return intensities for the corner and central regions
    and their ratio over the maximum intensity value of the array.
    Parameters
    ----------
    image : np.array
        image on a 2d np.array format.
    Returns
    -------
    profiles_statistics : pd.DataFrame
        pd.DataFrame showing the intensity values of the different regions and
        their ratio over the maximum intensity value of the array. One row per channel.
    """
    properties = None
    for c in range(image.shape[0]):
        channel_properties = {"channel": c}
        channel_properties.update(
            _channel_max_intensity_properties(image[c], sigma, center_threshold)
        )
        channel_properties.update(_channel_corner_properties(image[c], corner_fraction))
        channel_properties.update(_channel_area_deciles(image[c]))
        if c == 0:
            properties = pd.DataFrame(channel_properties, index=[c])
        else:
            properties = pd.concat(
                [
                    properties,
                    pd.DataFrame(channel_properties, index=[c]),
                ],
            )

    return properties


@register_image_analysis
class FieldHomogeneityAnalysis(Analysis):
    """This analysis creates a report on field illumination homogeneity based on input images"""

    def __init__(self):
        super().__init__(
            output_description="This analysis returns an analysis on the homogeneity of the field illumination"
        )

        self.add_data_requirement(
            name="image",
            description="An homogeneity provided as a numpy array with 5D zctxy shape",
            data_type=np.ndarray,
        )
        self.add_metadata_requirement(
            name="bit_depth",
            description="Detector bit depth",
            data_type=int,
            optional=True,
        )
        self.add_metadata_requirement(
            name="threshold",
            description="Tolerated saturation threshold",
            data_type=float,
            optional=True,
            default=0.01,
        )
        self.add_metadata_requirement(
            name="center_threshold",
            description="The threshold for the center of the image",
            data_type=float,
            optional=True,
            default=0.9,
        )
        self.add_metadata_requirement(
            name="corner_fraction",
            description="The proportion of the image to be considered as corner or center",
            data_type=float,
            optional=True,
            default=0.1,
        )
        self.add_metadata_requirement(
            name="sigma",
            description="The sigma for the smoothing gaussian filter",
            data_type=float,
            optional=True,
            default=2,
        )
        self.add_metadata_requirement(
            name="intensity_map_size",
            description="The size of the intensity map in pixels",
            data_type=int,
            optional=True,
            default=100,
        )

    def run(self):
        logger.info("Validating requirements...")
        if len(self.list_unmet_requirements()):
            logger.error(
                f"The following metadata requirements ara not met: {self.list_unmet_requirements()}"
            )
            return False

        # Check image shape
        logger.info("Checking image shape...")
        image = self.get_data_values("image")
        if len(image.shape) != 5:
            logger.error("Image must be 5D")
            return False
        if image.shape[0] != 1 or image.shape[2] != 1:
            logger.warning(
                "Image must be single z and single timepoint. Using first z and timepoint."
            )
        image = image[0, :, 0, :, :].reshape((image.shape[1], image.shape[3], image.shape[4]))

        # Check image saturation
        logger.info("Checking image saturation...")
        saturated_channels = []
        for c in range(image.shape[0]):
            if is_saturated(
                channel=image[c, :, :],
                threshold=self.get_metadata_values(name="threshold"),
                detector_bit_depth=self.get_metadata_values(name="bit_depth"),
            ):
                logger.error(f"Channel {c} is saturated")
                saturated_channels.append(c)
        if len(saturated_channels):
            logger.error(f"Channels {saturated_channels} are saturated")
            return False

        self.output.append(
            model.Table(
                name="regions_properties_table",
                description="Dataframe containing properties of the regions",
                table=_image_properties(
                    image=image,
                    corner_fraction=self.get_metadata_values("corner_fraction"),
                    sigma=self.get_metadata_values("sigma"),
                    center_threshold=self.get_metadata_values("center_threshold"),
                ),
            )
        )

        self.output.append(
            model.Image(
                name="intensity_map",
                description="Intensity map",
                data=_image_intensity_map(
                    image=image, map_size=self.get_metadata_values("intensity_map_size")
                ),
            )
        )

        self.output.append(
            model.Table(
                name="intensity_plot_data",
                description="Dataframe containing intensity plot data"
                "for each channel in the diagonal as well as the"
                "horizontal and vertical image centers",
                table=_image_line_profile(image, profile_size=255),
            )
        )

        # intensity_plot_data = get_intensity_plot(image)

        # profile_stat_table = _image_properties(image)

        # self.output.append(
        #     model.Table(
        #         name="norm_intensity_data",
        #         description="Dataframe containing coordinates",
        #         table=image_norm,
        #     )
        # )
        #
        # self.output.append(
        #     model.Table(
        #         name="intensity_plot_data",
        #         description="Dataframe containing coordinates",
        #         table=intensity_plot_data,
        #     )
        # )
        #
        # self.output.append(
        #     model.Table(
        #         name="profile_stat_table",
        #         description="Dataframe containing coordinates",
        #         table=profile_stat_table,
        #     )
        # )

        return True
