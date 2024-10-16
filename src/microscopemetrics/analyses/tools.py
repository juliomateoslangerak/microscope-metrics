"""These are some possibly useful code snippets"""

import logging
from itertools import permutations
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy import ndimage, special
from scipy.optimize import curve_fit, fsolve
from scipy.spatial.distance import cdist
from skimage.feature import peak_local_max
from skimage.filters import apply_hysteresis_threshold, gaussian, threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import ball, closing, cube, octahedron, square
from skimage.segmentation import clear_border

# Creating logging services
logger = logging.getLogger(__name__)

INT_DETECTOR_BIT_DEPTHS = [8, 10, 11, 12, 15, 16, 32]
FLOAT_DETECTOR_BIT_DEPTHS = [32, 64]


def airy_fun(
    x: np.ndarray, centre: np.float64, amp: np.float64
) -> np.ndarray:  # , exp):  # , amp, bg):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(
            (x - centre) == 0,
            amp * 0.5**2,
            amp * (special.j1(x - centre) / (x - centre)) ** 2,
        )


def gaussian_fun(x, background, amplitude, center, sd):
    gauss = np.exp(-np.power(x - center, 2.0) / (2 * np.power(sd, 2.0)))
    return background + (amplitude - background) * gauss


def fit_gaussian(profile, guess=None):
    if guess is None:
        guess = [profile.min(), profile.max(), profile.argmax(), 0.8]
    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)
    popt, pcov, infodict, mesg, ier = curve_fit(
        f=gaussian_fun, xdata=x, ydata=profile, p0=guess, maxfev=5000, full_output=True
    )

    if ier not in [1, 2, 3, 4]:
        logger.warning(f"No gaussian fit found. Reason: {mesg}")

    fitted_profile = gaussian_fun(x, popt[0], popt[1], popt[2], popt[3])
    fwhm = popt[3] * 2.35482

    # Calculate the fit quality using the coefficient of determination (R^2)
    y_mean = np.mean(profile)
    sst = np.sum((profile - y_mean) ** 2)
    ssr = np.sum((profile - fitted_profile) ** 2)
    cd_r2 = 1 - (ssr / sst)

    return fitted_profile, cd_r2, fwhm, popt


def fit_airy(profile, guess=None):
    profile = (profile - profile.min()) / (profile.max() - profile.min())
    if guess is None:
        guess = [profile.argmax(), 4 * profile.max()]
    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)
    popt, pcov, infodict, mesg, ier = curve_fit(
        f=airy_fun, xdata=x, ydata=profile, p0=guess, full_output=True
    )

    if ier not in [1, 2, 3, 4]:
        logger.warning(f"No airy fit found. Reason: {mesg}")

    fitted_profile = airy_fun(x, popt[0], popt[1])

    # Calculate the FWHM
    def _f(d):
        return airy_fun(d, popt[0], popt[1]) - (fitted_profile.max() - fitted_profile.min()) / 2

    guess = np.array([fitted_profile.argmax() - 1, fitted_profile.argmax() + 1])
    v = fsolve(_f, guess)
    fwhm = abs(v[1] - v[0])

    # Calculate the fit quality using the coefficient of determination (R^2)
    y_mean = np.mean(profile)
    sst = np.sum((profile - y_mean) ** 2)
    ssr = np.sum((profile - fitted_profile) ** 2)
    cd_r2 = 1 - (ssr / sst)

    return fitted_profile, cd_r2, fwhm, popt


def multi_airy_fun(x: np.ndarray, *params) -> np.ndarray:
    y = np.zeros_like(x)
    for i in range(0, len(params), 2):
        y = y + airy_fun(x, params[i], params[i + 1])
    return y


def is_saturated(
    channel: np.ndarray, threshold: float = 0.0, detector_bit_depth: Optional[int] = None
) -> bool:
    """
    Checks if the channel is saturated.
    A warning if it suspects that the detector bit depth does not match the datatype.
    thresh: float
        Threshold for the ratio of saturated pixels to total pixels
    detector_bit_depth: int
        Bit depth of the detector. Sometimes, detectors bit depth are not matching the datatype of the measureemnts.
        Here it can be specified the bit depth of the detector if known. The function is going to raise
        If None, it will be inferred from the channel dtype.
    """
    if detector_bit_depth is not None:
        if (
            detector_bit_depth not in INT_DETECTOR_BIT_DEPTHS
            and detector_bit_depth not in FLOAT_DETECTOR_BIT_DEPTHS
        ):
            raise ValueError(
                f"The detector bit depth provided ({detector_bit_depth}) is not supported. Supported values are {INT_DETECTOR_BIT_DEPTHS} for integer detectors and {FLOAT_DETECTOR_BIT_DEPTHS} for floating point detectors."
            )
        if (
            np.issubdtype(channel.dtype, np.integer)
            and detector_bit_depth not in INT_DETECTOR_BIT_DEPTHS
        ):
            raise ValueError(
                f"The channel datatype {channel.dtype} does not match the detector bit depth {detector_bit_depth}. The channel might be saturated."
            )
        elif (
            np.issubdtype(channel.dtype, np.floating)
            and detector_bit_depth not in FLOAT_DETECTOR_BIT_DEPTHS
        ):
            raise ValueError(
                f"The channel datatype {channel.dtype} does not match the detector bit depth {detector_bit_depth}. The channel might be saturated."
            )
        else:
            if np.issubdtype(channel.dtype, np.integer):
                if detector_bit_depth > np.iinfo(channel.dtype).bits:
                    raise ValueError(
                        f"The channel datatype {channel.dtype} does not support the detector bit depth {detector_bit_depth}. The channel might be saturated."
                    )
                else:
                    max_limit = pow(2, detector_bit_depth) - 1
            elif np.issubdtype(channel.dtype, np.floating):
                if detector_bit_depth != np.finfo(channel.dtype).bits:
                    raise ValueError(
                        f"The channel datatype {channel.dtype} does not support the detector bit depth {detector_bit_depth}. The channel might be saturated."
                    )
                else:
                    max_limit = np.finfo(channel.dtype).max

    else:
        if np.issubdtype(channel.dtype, np.integer):
            max_limit = np.iinfo(channel.dtype).max
        elif np.issubdtype(channel.dtype, np.floating):
            max_limit = np.finfo(channel.dtype).max
        else:
            raise ValueError("The channel provided is not a valid numpy dtype.")

    if channel.max() > max_limit:
        raise ValueError(
            "The channel provided has values larger than the bit depth of the detector."
        )

    saturation_matrix = channel == max_limit
    saturation_ratio = np.count_nonzero(saturation_matrix) / channel.size

    return saturation_ratio > threshold


def _segment_channel(
    channel,
    min_distance,
    method,
    threshold,
    sigma,
    low_corr_factor,
    high_corr_factor,
):
    """Segment a channel (3D numpy array ZYX)"""
    if threshold is None:
        threshold = threshold_otsu(channel)

    if sigma is not None:
        channel = gaussian(image=channel, sigma=sigma, preserve_range=True, channel_axis=None)

    if method == "hysteresis":  # We may try here hysteresis threshold
        thresholded = apply_hysteresis_threshold(
            channel, low=threshold * low_corr_factor, high=threshold * high_corr_factor
        )

    elif method == "local_max":  # We are applying a local maxima algorithm
        peaks = peak_local_max(
            channel,
            min_distance=min_distance,
            threshold_abs=(threshold * 0.5),
        )
        thresholded = np.copy(channel)
        thresholded[tuple(peaks.T)] = thresholded.max()
        thresholded = apply_hysteresis_threshold(
            thresholded,
            low=threshold * low_corr_factor,
            high=threshold * high_corr_factor,
        )
    else:
        raise Exception("A valid segmentation method was not provided")

    closed = closing(thresholded, cube(min_distance))
    cleared = clear_border(closed)
    return label(cleared)


def segment_image(
    image: np.ndarray,
    min_distance: float,
    threshold: float = None,
    sigma=None,
    method: str = "local_max",
    low_corr_factors: List[float] = None,
    high_corr_factors: List[float] = None,
):
    """Segment an image and return a labels object.
    Image must be provided as TZYXC numpy array
    """
    logger.info("Image being segmented...")

    if low_corr_factors is None or (
        isinstance(low_corr_factors, list) and len(low_corr_factors) == 0
    ):
        low_corr_factors = [0.95] * image.shape[4]
        logger.warning("No low correction factor specified. Using defaults")
    if high_corr_factors is None or (
        isinstance(high_corr_factors, list) and len(high_corr_factors) == 0
    ):
        high_corr_factors = [1.05] * image.shape[4]
        logger.warning("No high correction factor specified. Using defaults")

    if len(high_corr_factors) != image.shape[4] or len(low_corr_factors) != image.shape[4]:
        raise Exception("The number of correction factors does not match the number of channels.")

    # We create an empty array to store the output
    labels_image = np.zeros(image.shape, dtype=np.uint16)
    for c in range(image.shape[4]):
        for t in range(image.shape[0]):
            labels_image[t, :, :, :, c] = _segment_channel(
                image[t, :, :, :, c],
                min_distance=min_distance,
                method=method,
                threshold=threshold,
                sigma=sigma,
                low_corr_factor=low_corr_factors[c],
                high_corr_factor=high_corr_factors[c],
            )
    return labels_image


def _compute_channel_spots_properties(
    channel, label_channel, remove_center_cross=False, pixel_size=None
):
    """Analyzes and extracts the properties of a single channel"""

    regions = regionprops(label_channel, channel)

    ch_properties = [
        {
            "label": region.label,
            "area": region.area,
            "centroid": region.centroid,
            "weighted_centroid": region.weighted_centroid,
            "max_intensity": region.max_intensity,
            "mean_intensity": region.mean_intensity,
            "min_intensity": region.min_intensity,
            "integrated_intensity": region.mean_intensity * region.area,
        }
        for region in regions
    ]

    if (
        remove_center_cross
    ):  # Argolight spots pattern contains a central cross that we might want to remove
        largest_area = 0
        largest_region = None
        for region in ch_properties:
            if region["area"] > largest_area:  # We assume the cross is the largest area
                largest_area = region["area"]
                largest_region = region
        if largest_region:
            ch_properties.remove(largest_region)
    ch_positions = np.array([x["weighted_centroid"] for x in ch_properties])
    if pixel_size:
        ch_positions = ch_positions[0:] * pixel_size

    return ch_properties, ch_positions


def compute_spots_properties(image, labels, remove_center_cross=False, pixel_size=None):
    """Computes a number of properties for the PSF-like spots found on an image provided they are segmented.
    Image must be provided as a TZYXC 5d numpy array"""
    properties = []
    positions = []

    for c in range(image.shape[4]):
        for t in range(image.shape[0]):
            pr, pos = _compute_channel_spots_properties(
                channel=image[t, :, :, :, c],
                label_channel=labels[t, :, :, :, c],
                remove_center_cross=remove_center_cross,
                pixel_size=pixel_size,
            )
            properties.append(pr)
            positions.append(pos)

    return properties, positions


def compute_distances_matrix(positions, max_distance, pixel_size=None):
    """Calculates Mutual Closest Neighbour distances between all channels and returns the values as"""
    logger.info("Computing distances between spots")

    if len(positions) < 2:
        raise Exception("Not enough dimensions to do a distance measurement")

    channel_permutations = list(permutations(range(len(positions)), 2))

    if not pixel_size:  # TODO: make sure the units are corrected if no pixel size
        pixel_size = np.array((1, 1, 1))
        logger.warning("No pixel size specified. Using the unit")
    else:
        pixel_size = np.array(pixel_size)

    distances_rows = []

    for a, b in channel_permutations:
        distances_matrix = cdist(positions[a], positions[b], w=pixel_size)

        distances_rows.extend(
            {
                "channel_a": a,
                "channel_b": b,
                "z_coord_a": pos_A[0],
                "y_coord_a": pos_A[1],
                "x_coord_a": pos_A[2],
                "z_coord_b": positions[b][d.argmin()][0],
                "y_coord_b": positions[b][d.argmin()][1],
                "x_coord_b": positions[b][d.argmin()][2],
                "z_dist": pos_A[0] - positions[b][d.argmin()][0],
                "y_dist": pos_A[1] - positions[b][d.argmin()][1],
                "x_dist": pos_A[2] - positions[b][d.argmin()][2],
                "dist_3d": d.min(),
                "labels_a": i,
                "labels_b": d.argmin(),
            }
            for i, (pos_A, d) in enumerate(zip(positions[a], distances_matrix))
            if d.min() < max_distance
        )

    return pd.DataFrame(distances_rows)


def _radial_mean(image, bins=None):
    """Computes the radial mean from an input 2d image.
    Taken from scipy-lecture-notes 2.6.8.4
    """
    # TODO: workout a binning = image size
    if not bins:
        bins = 200
    size_x, size_y = image.shape
    x, y = np.ogrid[0:size_x, 0:size_y]

    r = np.hypot(x - size_x / 2, y - size_y / 2)

    rbin = (bins * r / r.max()).astype(np.int)

    return ndimage.mean(image, labels=rbin, index=np.arange(1, rbin.max() + 1))


def _channel_fft_2d(channel):
    channel_fft = np.fft.rfft2(channel)
    return np.fft.fftshift(np.abs(channel_fft), axes=1)


def fft_2d(image):
    # Create an empty array to contain the transform
    fft = np.zeros(shape=(image.shape[1], image.shape[2], image.shape[3] // 2 + 1), dtype="float64")
    for c in range(image.shape[2]):
        fft[c, :, :] = _channel_fft_2d(image[..., c, :, :])

    return fft


def _channel_fft_3d(channel):
    channel_fft = np.fft.rfftn(channel)
    return np.fft.fftshift(np.abs(channel_fft), axes=1)


def fft_3d(image):
    fft = np.zeros(
        shape=(
            image.shape[0],
            image.shape[1],
            image.shape[2],
            image.shape[3],
            image.shape[4] // 2 + 1,
        ),  # We only compute the real part of the FFT
        dtype="float64",
    )
    for c in range(image.shape[-3]):
        fft[..., c, :, :] = _channel_fft_3d(image[..., c, :, :])

    return fft


def wavelength_to_rgb(wavelength, gamma=0.8):
    """
    Copied from https://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    wavelength = float(wavelength)
    if 380 < wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        r = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        g = 0.0
        b = (1.0 * attenuation) ** gamma
    elif 440 < wavelength <= 490:
        r = 0.0
        g = ((wavelength - 440) / (490 - 440)) ** gamma
        b = 1.0
    elif 490 < wavelength <= 510:
        r = 0.0
        g = 1.0
        b = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 < wavelength <= 580:
        r = ((wavelength - 510) / (580 - 510)) ** gamma
        g = 1.0
        b = 0.0
    elif 580 < wavelength <= 645:
        r = 1.0
        g = (-(wavelength - 645) / (645 - 580)) ** gamma
        b = 0.0
    elif 645 < wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        r = (1.0 * attenuation) ** gamma
        g = 0.0
        b = 0.0
    else:
        r = 0.0
        g = 0.0
        b = 0.0
    r *= int(r * 255)
    g *= int(g * 255)
    g *= int(g * 255)
    return r, g, b
