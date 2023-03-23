# This is a place to hold mere utilities for metrics

import json
import warnings
from configparser import ConfigParser

import numpy as np
from scipy import special

DETECTOR_BIT_DEPTHS = [10, 11, 12, 15]


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
def airy_fun(x, centre, amp):  # , exp):  # , amp, bg):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(
            (x - centre) == 0,
            amp * 0.5**2,
            amp * (special.j1(x - centre) / (x - centre)) ** 2,
        )


def gaussian_fun(x, background, amplitude, center, sd):
    gauss = np.exp(-np.power(x - center, 2.0) / (2 * np.power(sd, 2.0)))
    return background + (amplitude - background) * gauss


def multi_airy_fun(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 2):
        y = y + airy_fun(x, params[i], params[i + 1])
    return y


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


def is_saturated(channel, threshold=0.0, detector_bit_depth=None):
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
    if detector_bit_depth is None:
        if np.issubdtype(channel.dtype, np.integer):
            max_limit = np.iinfo(channel.dtype).max
        elif np.issubdtype(channel.dtype, np.floating):
            max_limit = np.finfo(channel.dtype).max
        else:
            raise ValueError("The channel provided is not a valid numpy dtype.")

        for bit_depth in DETECTOR_BIT_DEPTHS:
            try:
                saturated = is_saturated(
                    channel, threshold=threshold, detector_bit_depth=bit_depth
                )
            except ValueError:
                continue
        if saturated:
            warnings.warn(
                "The channel might be saturated. The channel saturation matches a common detector bit depth"
            )

    else:
        max_limit = pow(2, detector_bit_depth) - 1
        if np.any(channel > max_limit):
            raise ValueError(
                "The channel provided has values larger than the bit depth of the detector."
            )

    saturation_matrix = channel == max_limit
    saturation_ratio = np.count_nonzero(saturation_matrix) / channel.size

    return saturation_ratio > threshold
