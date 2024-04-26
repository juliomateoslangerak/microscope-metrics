# This is a place to hold mere utilities for metrics

import json
import warnings
from configparser import ConfigParser
from typing import Optional

import numpy as np
from numpy import float64, ndarray
from scipy import special
from scipy.optimize import curve_fit, fsolve

INT_DETECTOR_BIT_DEPTHS = [8, 10, 11, 12, 15, 16, 32]
FLOAT_DETECTOR_BIT_DEPTHS = [32, 64]


## Some useful functions
def convert_SI(val, unit_in, unit_out):
    si = {
        "nanometer": 0.000000001,
        "micrometer": 0.000001,
        "millimeter": 0.001,
        "meter": 1.0,
    }
    return val * si[unit_in.lower()] / si[unit_out.lower()]


# def airy_fun(x, centre, a, exp):  # , amp, bg):
#     if (x - centre) == 0:
#         return a * .5 ** exp
#     else:
#         return a * (special.j1(x - centre) / (x - centre)) ** exp
#
#
# def multi_airy_fun(x, *params):
#     y = np.zeros_like(x)
#     for i in range(0, len(params), 3):
#         y = y + airy_fun(x, params[i], params[i+1], params[i+2])
#     return y
def airy_fun(x: ndarray, centre: float64, amp: float64) -> ndarray:  # , exp):  # , amp, bg):
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
        warnings.warn(f"No gaussian fit found. Reason: {mesg}")

    fitted_profile = gaussian_fun(x, popt[0], popt[1], popt[2], popt[3])
    fwhm = popt[3] * 2.35482

    # Calculate the fit quality using the coefficient of determination (R^2)
    y_mean = np.mean(profile)
    sst = np.sum((profile - y_mean) ** 2)
    ssr = np.sum((profile - fitted_profile) ** 2)
    cd_r2 = 1 - (ssr / sst)

    return fitted_profile, cd_r2, fwhm, popt[2]


def fit_airy(profile, guess=None):
    profile = (profile - profile.min()) / (profile.max() - profile.min())
    if guess is None:
        guess = [profile.argmax(), 4 * profile.max()]
    x = np.linspace(0, profile.shape[0], profile.shape[0], endpoint=False)
    popt, pcov, infodict, mesg, ier = curve_fit(
        f=airy_fun, xdata=x, ydata=profile, p0=guess, full_output=True
    )

    if ier not in [1, 2, 3, 4]:
        warnings.warn(f"No airy fit found. Reason: {mesg}")

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

    return fitted_profile, cd_r2, fwhm, popt[0]


def multi_airy_fun(x: ndarray, *params) -> ndarray:
    y = np.zeros_like(x)
    for i in range(0, len(params), 2):
        y = y + airy_fun(x, params[i], params[i + 1])
    return y


def robust_z_score(data):
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    return 0.6745 * (data - median) / mad


def z_score(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    return (data - mean) / std_dev


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


# This class is not used after introduction of pydantic.
class MetricsConfig(ConfigParser):
    def getjson(self, section, option, **kwargs):
        value = self.get(section, option, **kwargs)
        try:
            output = json.loads(value)
        except json.JSONDecodeError as e:
            raise e
        return output

    def getlist(self, section, option, **kwargs):
        output = self.getjson(section, option, **kwargs)

        if type(output) is list:
            return output
        else:
            raise Exception(
                f'The config option "{option}" in section "{section}" is not formatted as a list'
            )

    def getlistint(self, section, option, **kwargs):
        try:
            output = [int(x) for x in self.getlist(section, option, **kwargs)]
            return output
        except Exception as e:
            print(
                f'Some element in config option "{option}" in section "{section}" cannot be coerced into a integer'
            )
            raise e

    def getlistfloat(self, section, option, **kwargs):
        try:
            output = [float(x) for x in self.getlist(section, option, **kwargs)]
            return output
        except Exception as e:
            print(
                f'Some element in config option "{option}" in section "{section}" cannot be coerced into a float'
            )
            raise e


def is_saturated(
    channel: ndarray, threshold: float = 0.0, detector_bit_depth: Optional[int] = None
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
