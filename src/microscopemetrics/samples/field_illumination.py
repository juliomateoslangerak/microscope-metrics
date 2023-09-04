from datetime import datetime
from typing import Dict, Tuple

import numpy as np
import scipy
from skimage.filters import gaussian
from skimage.measure import regionprops

import microscopemetrics.data_schema.samples.field_illumination_schema as schema
from microscopemetrics.data_schema import core_schema
from microscopemetrics.samples import AnalysisMixin, logger, numpy_to_inlined_image
from microscopemetrics.utilities.utilities import is_saturated


def _channel_intensity_map(channel: np.ndarray, map_size: int):
    """
    Compute the intensity map of a channel
    Parameters
    ----------
    channel : np.array.
        image on a 2d np.ndarray format.
    map_size : int
        size of the intensity map.
    Returns
    -------
    intensity_map : np.ndarray
        2d np.ndarray representing the intensity map of the chosen channel.
    """
    channel = channel / channel.max()
    return scipy.ndimage.zoom(channel, map_size / channel.shape[0])


def _image_intensity_map(image: np.ndarray, map_size: int):
    """
    Compute the intensity map of an image
    Parameters
    ----------
    image : np.ndarray.
        image on a 3d np.ndarray format yxc.
    map_size : int
        size of the intensity map.
    Returns
    -------
    intensity_map : np.ndarray
        3d np.ndarray representing the intensity map of the chosen image.
    """
    output = np.zeros((map_size, map_size, image.shape[2]))
    for c in range(image.shape[2]):
        output[:, :, c] = _channel_intensity_map(np.squeeze(image[:, :, c]), map_size)

    # We want to return a 5d array (adding z and t) for compatibility with the rest of the code
    return np.expand_dims(output, axis=(0, 1))


def _channel_line_profile(
    channel: np.ndarray, start: Tuple[int, int], end: Tuple[int, int], profile_size: int
) -> np.ndarray:
    """
    Compute the intensity profile along a line between x0-y0 and x1-y1 using cubic interpolation
    Parameters
    ----------
    channel : np.array.
        image on a 2d np.ndarray format.
    start : (int, int)
        coordinates of the starting pixel
    end : (int, int)
        coordinates of the ending pixel
    Returns
    -------
    line_pixel_values : np.ndarray
        1d np.ndarray representing the values of the chosen line of pixels.
    """
    x, y = np.linspace(start[0], end[0], profile_size), np.linspace(start[1], end[1], profile_size)

    return scipy.ndimage.map_coordinates(channel, np.vstack((x, y)))


def _image_line_profile(image: np.ndarray, profile_size: int):
    """
    Compute the intensity profile along a line between x0-y0 and x1-y1
    Parameters
    ----------
    image : np.ndarray.
        image on a 3d np.ndarray format yxc.
    profile_size : int
        size of the intensity profile.
    Returns
    -------
    line_pixel_values : np.ndarray
        2d np.ndarray representing the values of the chosen line of pixels for each channel.
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
    output = []
    for profile_name, (start, end) in profile_coordinates.items():
        profiles = np.zeros((image.shape[2], 255))
        for c in range(image.shape[2]):
            profiles[c, :] = _channel_line_profile(
                np.squeeze(image[:, :, c]), start, end, profile_size
            )
        output = output + [
            {f"ch_{c:02}_{profile_name}": {"values": profiles[c].tolist()}}
            for c in range(image.shape[2])
        ]

    return output


def _line_profile_shapes(image: np.ndarray):
    stroke_color = {"r": 0, "g": 0, "b": 255, "alpha": 200}
    return [
        core_schema.Line(
            label="leftTop_to_rightBottom",
            x1=0,
            y1=0,
            x2=image.shape[1],
            y2=image.shape[0],
            stroke_color=stroke_color,
        ),
        core_schema.Line(
            label="leftBottom_to_rightTop",
            x1=0,
            y1=image.shape[0],
            x2=image.shape[1],
            y2=0,
            stroke_color=stroke_color,
        ),
        core_schema.Line(
            label="center_horizontal",
            x1=0,
            y1=image.shape[0] // 2,
            x2=image.shape[1],
            y2=image.shape[0] // 2,
            stroke_color=stroke_color,
        ),
        core_schema.Line(
            label="center_vertical",
            x1=image.shape[1] // 2,
            y1=0,
            x2=image.shape[1] // 2,
            y2=image.shape[0],
            stroke_color=stroke_color,
        ),
    ]


def _c_shape(label, x, y, size, s_col):
    return core_schema.Rectangle(label=label, x=x, y=y, w=size, h=size, stroke_color=s_col)


def _corner_shapes(image: np.ndarray, corner_fraction: float):
    cfp = int(corner_fraction * (image.shape[0] + image.shape[1]) / 2)
    cr_y = int((image.shape[0] - cfp) / 2)
    cr_x = int((image.shape[1] - cfp) / 2)
    stroke_color = {"r": 0, "g": 255, "b": 0, "alpha": 200}

    return [
        _c_shape("top_left", x=0, y=0, size=cfp, s_col=stroke_color),
        _c_shape("top_center", x=cr_x, y=0, size=cfp, s_col=stroke_color),
        _c_shape("top_right", x=image.shape[1] - cfp, y=0, size=cfp, s_col=stroke_color),
        _c_shape("middle_left", x=0, y=cr_y, size=cfp, s_col=stroke_color),
        _c_shape("middle_center", x=cr_x, y=cr_y, size=cfp, s_col=stroke_color),
        _c_shape("middle_right", x=image.shape[1] - cfp, y=cr_y, size=cfp, s_col=stroke_color),
        _c_shape("bottom_left", x=0, y=image.shape[0] - cfp, size=cfp, s_col=stroke_color),
        _c_shape("bottom_center", x=cr_x, y=image.shape[0] - cfp, size=cfp, s_col=stroke_color),
        _c_shape(
            "bottom_right",
            x=image.shape[1] - cfp,
            y=image.shape[0] - cfp,
            size=cfp,
            s_col=stroke_color,
        ),
    ]


def _segment_channel(channel: np.ndarray, threshold: float, sigma: float):
    if sigma is not None:
        channel = gaussian(image=channel, sigma=sigma, preserve_range=True, channel_axis=None)

    channel_norm = channel / np.max(channel)
    return (channel_norm > threshold).astype(int)


def _channel_max_intensity_properties(
    channel: np.ndarray, sigma: float, center_threshold: float
) -> dict:
    """Computes the center of mass and the max intensity of the maximum intensity region of an image.
    Parameters
    ----------
    channel : np.array.
        2d np.ndarray.
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
        "center_of_mass_y": image_properties[0].centroid_weighted[0],
        "center_of_mass_x": image_properties[0].centroid_weighted[1],
        "max_intensity": max_intensity,
        "max_intensity_pos_y": max_intensity_indexes[0],
        "max_intensity_pos_x": max_intensity_indexes[1],
    }


def _channel_corner_properties(channel: np.ndarray, corner_fraction: float) -> dict:
    max_intensity = np.max(channel)

    # Calculate the corner fraction in pixels (cfp) of the image size
    # to use as the corner size and the center range (cr)
    cfp = int(corner_fraction * (channel.shape[0] + channel.shape[1]) / 2)
    cr_y = int((channel.shape[0] - cfp) / 2)
    cr_x = int((channel.shape[1] - cfp) / 2)

    return {
        "top_left_intensity_mean": np.mean(channel[0:cfp, 0:cfp]),
        "top_left_intensity_ratio": np.mean(channel[0:cfp, 0:cfp]) / max_intensity,
        "top_center_intensity_mean": np.mean(channel[cr_x:-cr_x, 0:cfp]),
        "top_center_intensity_ratio": np.mean(channel[cr_x:-cr_x, 0:cfp]) / max_intensity,
        "top_right_intensity_mean": np.mean(channel[-cfp:-1, 0:cfp]),
        "top_right_intensity_ratio": np.mean(channel[-cfp:-1, 0:cfp]) / max_intensity,
        "middle_left_intensity_mean": np.mean(channel[0:cfp, cr_y:-cr_y]),
        "middle_left_intensity_ratio": np.mean(channel[0:cfp, cr_y:-cr_y]) / max_intensity,
        "middle_center_intensity_mean": np.mean(channel[cr_x:-cr_x, cr_y:-cr_y]),
        "middle_center_intensity_ratio": np.mean(channel[cr_x:-cr_x, cr_y:-cr_y]) / max_intensity,
        "middle_right_intensity_mean": np.mean(channel[-cfp:-1, cr_y:-cr_y]),
        "middle_right_intensity_ratio": np.mean(channel[-cfp:-1, cr_y:-cr_y]) / max_intensity,
        "bottom_left_intensity_mean": np.mean(channel[0:cfp, -cfp:-1]),
        "bottom_left_intensity_ratio": np.mean(channel[0:cfp, -cfp:-1]) / max_intensity,
        "bottom_center_intensity_mean": np.mean(channel[cr_x:-cr_x, -cfp:-1]),
        "bottom_center_intensity_ratio": np.mean(channel[cr_x:-cr_x, -cfp:-1]) / max_intensity,
        "bottom_right_intensity_mean": np.mean(channel[-cfp:-1, -cfp:-1]),
        "bottom_right_intensity_ratio": np.mean(channel[-cfp:-1, -cfp:-1]) / max_intensity,
    }


def _channel_area_deciles(channel: np.ndarray) -> dict:
    """Computes the intensity deciles of an image.
    Parameters
    ----------
    channel : np.array.
        2d np.ndarray.
    Returns
    -------
    deciles: dict
        dict enclosing the intensity deciles of the provided channel.
    """
    channel = channel / np.max(channel)
    return {f"decile_{i}": np.percentile(channel, i * 10) for i in range(10)}


def _image_properties(
    image: np.ndarray, corner_fraction: float, sigma: float, center_threshold: float
):
    """
    given an image in a 3d np.ndarray format (yxc), this function return intensities for the corner and central regions
    and their ratio over the maximum intensity value of the array.
    Parameters
    ----------
    image : np.ndarray
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

        self.output.key_values = schema.FieldIlluminationKeyValues(
            **_image_properties(
                image=image,
                corner_fraction=self.input.corner_fraction,
                sigma=self.input.sigma,
                center_threshold=self.input.center_threshold,
            )
        )

        self.output.intensity_map = numpy_to_inlined_image(
            array=_image_intensity_map(image=image, map_size=self.input.intensity_map_size),
            name=f"{self.input.field_illumination_image.name}_intensity_map",
            description=f"Intensity map of {self.input.field_illumination_image.name}",
            image_url=self.input.field_illumination_image.image_url,
            source_image_url=self.input.field_illumination_image.source_image_url,
        )

        self.output.intensity_profiles = schema.TableAsDict(
            name="intensity_profiles", columns=_image_line_profile(image, profile_size=255)
        )

        self.output.profile_rois = core_schema.Roi(
            label="Profile ROIs",
            description="ROIs used to compute the intensity profiles",
            image=self.input.field_illumination_image.image_url,
            shapes=_line_profile_shapes(image),
        )

        self.output.corner_rois = core_schema.Roi(
            label="Corner ROIs",
            description="ROIs used to compute the corner intensities",
            image=self.input.field_illumination_image.image_url,
            shapes=_corner_shapes(image, self.input.corner_fraction),
        )

        self.output.center_of_illumination = core_schema.Roi(
            label="Center of illumination",
            description="Point ROI marking the center of illumination",
            image=self.input.field_illumination_image.image_url,
            shapes=[
                core_schema.Point(
                    label=f"ch{c:02}_center",
                    y=self.output.key_values.center_of_mass_y[c],
                    x=self.output.key_values.center_of_mass_x[c],
                    c=c,
                    stroke_color={"r": 255, "g": 0, "b": 0, "alpha": 200},
                    fill_color={"r": 255, "g": 0, "b": 0, "alpha": 200},
                    stroke_width=5,
                )
                for c in range(image.shape[2])
            ],
        )

        self.processing_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.processed = True

        return True
