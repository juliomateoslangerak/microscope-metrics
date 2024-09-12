import logging
from configparser import NoOptionError
from enum import Enum, EnumMeta
from math import asin, cos, sin

# from microscopemetrics.interface import omero as interface


module_logger = logging.getLogger("metrics.devices.devices")


DTYPES = {
    "int": (tuple,),
    "float": (tuple,),
    "bool": (type(None),),
    "str": (int,),
    "tuple": (type(None),),
}


def _call_if_callable(f):
    """Call callables, or return value of non-callables."""
    return f() if callable(f) else f


class _Setting:
    """The code of this class was copied from https://github.com/MicronOxford/microscope"""

    # Settings classes should be private: devices should use a factory method
    # rather than instantiate settings directly; most already use add_setting
    # for this.
    # TODO: Implement a get units
    def __init__(
        self,
        name,
        dtype,
        get_from_db_func,
        get_from_conf_func,
        get_from_name_func,
        set_func,
        values=None,
    ):
        """Create a setting.
        :param name: the setting's name
        :param dtype: a data type from ('int', 'float', 'bool', 'enum', 'str')
        :param get_from_db_func: a function to get the value from the database interface
        :param get_from_conf_func: a function to get the value from the device configuration
        :param get_from_name_func: a function to get the value from the image name
        :param values: a description of allowed values dependent on dtype,
                       or function that returns a description
        Setters and getters accept or return:
            the setting value for int, float, bool and str;
            the setting index into a list, dict or Enum type for enum.
        """
        self.name = name
        if dtype not in DTYPES:
            raise Exception("Unsupported dtype.")
        elif not (isinstance(values, DTYPES[dtype]) or callable(values)):
            raise Exception(
                "Invalid values type for %s '%s':"
                " expected function or %s" % (dtype, name, DTYPES[dtype])
            )
        self.dtype = dtype
        self._get_from_db = get_from_db_func
        self._get_from_conf = get_from_conf_func
        self._get_from_name = get_from_name_func
        self._values = values

    def describe(self):
        """Returns a dictionary describing the setting"""
        return {"type": self.dtype, "values": self.values()}

    def get(self, **kwargs):
        """Get a setting"""
        if self._get_from_db is not None:
            value = self._get_from_db(**kwargs)
            if value is not None:
                return value
        if self._get_from_conf is not None:
            value = self._get_from_conf(**kwargs)
            if value is not None:
                return value
        if self._get_from_name is not None:
            value = self._get_from_name(**kwargs)
            if value is not None:
                return value
        module_logger.warning(f"Device setting could not be retrieved: {self.name}")

    def values(self):
        values = _call_if_callable(self._values)
        if values is not None:
            if self.dtype == "enum":
                if isinstance(values, dict):
                    return list(values.items())
                else:
                    # self._values is a list or tuple
                    return list(enumerate(values))
            elif self._values is not None:
                return values


class Device:
    """A superclass for all the microscope devices and eventually other type of devices."""

    def __init__(self, device_config):
        self.device_config = device_config
        self._settings = {}

    def add_setting(
        self,
        name,
        dtype,
        get_from_db_func,
        get_from_conf_func,
        get_from_name_func,
        set_func,
        values=None,
    ):
        """Add a setting definition.
        :param name: the setting's name
        :param dtype: a data type from ('int', 'float', 'bool', 'enum', 'str')
        :param get_from_db_func: a function to get the value from the interface to the database
        :param get_from_conf_func: a function to get the value from the configuration
        :param get_from_name_func: a function to get the value from the image name
        :param set_func: a function to set the value
        :param values: a description of allowed values dependent on dtype,
                       or function that returns a description
        A client needs some way of knowing a setting name and data type,
        retrieving the current value and, if settable, a way to retrieve
        allowable values, and set the value.
        """
        if dtype not in DTYPES:
            raise Exception("Unsupported dtype.")
        elif not (isinstance(values, DTYPES[dtype]) or callable(values)):
            raise Exception(
                "Invalid values type for %s '%s':"
                " expected function or %s" % (dtype, name, DTYPES[dtype])
            )
        else:
            self._settings[name] = _Setting(
                name,
                dtype,
                get_from_db_func,
                get_from_conf_func,
                get_from_name_func,
                set_func,
                values,
            )

    def get_setting(self, name, **kwargs):
        """Tries to get a specified setting from the following sources by order of preference:
        - Image from the database interface
        - The microscope analysis_config linked through the image name
        - Directly in the image name"""

        try:
            return self._settings[name].get(**kwargs)
        except Exception as err:
            module_logger.error("in get_setting(%s):", name, exc_info=err)
            raise

    def get_all_settings(self, **kwargs):
        """Return settings as a dict."""

        def catch(f):
            try:
                return f(**kwargs)
            except Exception as err:
                module_logger.error(f"getting {f.__self__.name}: {err}")
                return None

        return {k: catch(v.get) for k, v in self._settings.items()}

    def set_setting(self, name, value):
        """Set a setting."""
        try:
            self._settings[name].set(value)
        except Exception as err:
            module_logger.error("in set_setting(%s):", name, exc_info=err)
            raise

    def describe_setting(self, name):
        """Return ordered setting descriptions as a list of dicts."""
        return self._settings[name].describe()

    def describe_settings(self):
        """Return ordered setting descriptions as a list of dicts."""
        return [(k, v.describe()) for (k, v) in self._settings.items()]

    def settings_to_conf(self):
        pass

    def update_settings(self, incoming, init=False):
        """Update settings based on dict of settings and values."""
        if init:
            # Assume nothing about state: set everything.
            my_keys = set(self._settings.keys())
            their_keys = set(incoming.keys())
            update_keys = my_keys & their_keys
            if update_keys != my_keys:
                missing = ", ".join([k for k in my_keys - their_keys])
                msg = "update_settings init=True but missing keys: %s." % missing
                _logger.debug(msg)
                raise Exception(msg)
        else:
            # Only update changed values.
            my_keys = set(self._settings.keys())
            their_keys = set(incoming.keys())
            update_keys = set(
                key for key in my_keys & their_keys if self.get_setting(key) != incoming[key]
            )
        results = {}
        # Update values.
        for key in update_keys:
            if key not in my_keys or not self._settings[key].set:
                # Setting not recognised or no set function implemented
                results[key] = NotImplemented
                update_keys.remove(key)
                continue
            if _call_if_callable(self._settings[key].readonly):
                continue
            self._settings[key].set(incoming[key])
        # Read back values in second loop.
        for key in update_keys:
            results[key] = self._settings[key].get()
        return results


class Microscope(Device):
    """A superclass for the microscopes. Inherit this class when you create a new type of microscope."""

    def __init__(self, device_config):
        super().__init__(device_config)

    def _get_conf_objective_nr(self, image):
        img_name = image.getName()
        obj_nrs = [
            i
            for i, token in enumerate(self.device_config.getlist("OBJECTIVES", "names"))
            if token in img_name
        ]
        if len(obj_nrs) > 1:
            module_logger.error(
                "More than one reference to an objective lens was found in the image name. Only the first one will be considered."
            )
        elif len(obj_nrs) == 0:
            module_logger.info("No references to any objective lens were found in the image name")
            return None
        return obj_nrs[0]

    def _get_conf_objective_setting(self, option, image):
        obj_nr = self._get_conf_objective_nr(image)
        if obj_nr is None:
            return None
        try:
            values = eval(self.device_config.get("OBJECTIVES", option))
        except NoOptionError as e:
            module_logger.error(
                f"No parameters for {option} have been defined in the device configuration"
            )

        except NameError as e:
            module_logger.error(
                f"There was an error reading microscope objectives configuration option: {option}"
            )
            return None
        if values is None:
            module_logger.info(
                f"No information available for {option} in the microscope objectives configuration "
            )
            return None
        else:
            return values[obj_nr]

    def _get_conf_channel_nrs(self, image):
        img_name = image.getName()
        ch_nrs = list()
        token_positions = list()
        for ch, ch_token in enumerate(self.device_config.getlist("CHANNELS", "names")):
            token_pos = img_name.find(ch_token)
            if token_pos == -1:  # token not in name
                continue
            else:
                token_positions.append(token_pos)
                ch_nrs.append(ch)
        # Sort channels according to their position in the name
        ch_nrs = tuple(ch for _, ch in sorted(zip(token_positions, ch_nrs)))
        if len(ch_nrs) == 0:
            module_logger.info("No references to any channel were found in the image name")
            return None
        return ch_nrs

    def _get_conf_channel_settings(self, option, image):
        ch_nrs = self._get_conf_channel_nrs(image)
        if ch_nrs is None:
            return None
        try:
            values = eval(self.device_config.get("CHANNELS", option))
        except NameError as e:
            module_logger.error(
                f"There was an error reading microscope channel configuration option: {option}"
            )
            return None
        if values is None:
            module_logger.info(
                f"No information available for {option} in the microscope channels configuration "
            )
            return None
        else:
            return tuple(values[ch] for ch in ch_nrs)

    def _get_metadata_from_name(self, token_left, token_right, metadata_type, image):
        name = image.getName()
        start = name.find(token_left)
        if start == -1:
            return None
        name = name[start + len(token_left) :]
        end = name.find(token_right)
        value = metadata_type(name[:end])
        if metadata_type is None:
            return value
        else:
            try:
                value = metadata_type(value)
            except ValueError as e:
                module_logger.error(
                    f"Could not cast {value} into {metadata_type}. Please verify file naming for token {token_left}"
                )
                return None

        return value


class WideFieldMicroscope(Microscope):
    """A Widefield microscope"""

    def __init__(self, device_config):
        super().__init__(device_config)

        # Setting some objective lens settings
        self.add_setting(
            "objective_lens_refractive_index",
            "float",
            # get_from_db_func=interface._get_objective_lens_refractive_index,
            get_from_db_func=self._get_objective_lens_refractive_index,
            get_from_conf_func=self._get_conf_objective_lens_refr_index,
            get_from_name_func=self._get_name_objective_lens_refr_index,
            set_func=None,
            values=(1.0, 2.0),
        )
        self.add_setting(
            "objective_lens_na",
            "float",
            # get_from_db_func=interface._get_objective_lens_na,
            get_from_db_func=self._get_objective_lens_na,
            get_from_conf_func=self._get_conf_objective_lens_na,
            get_from_name_func=self._get_name_objective_lens_na,
            set_func=None,
            values=(0.0, 2.0),
        )
        self.add_setting(
            "objective_lens_nominal_magnification",
            "float",
            # get_from_db_func=interface._get_objective_lens_nominal_magnification,
            get_from_db_func=self._get_objective_lens_nominal_magnification,
            get_from_conf_func=self._get_conf_objective_lens_nominal_magnification,
            get_from_name_func=self._get_name_objective_lens_nominal_magnification,
            set_func=None,
            values=(1.0, 1000.0),
        )

        # Setting some channel settings
        self.add_setting(
            "excitation_wavelengths",
            "tuple",
            # get_from_db_func=interface._get_excitation_wavelengths,
            get_from_db_func=self._get_excitation_wavelengths,
            get_from_conf_func=self._get_conf_excitation_wavelengths,
            get_from_name_func=self._get_name_excitation_wavelengths,
            set_func=None,
            values=None,
        )
        self.add_setting(
            "emission_wavelengths",
            "tuple",
            # get_from_db_func=interface._get_emission_wavelengths,
            get_from_db_func=self._get_emission_wavelengths,
            get_from_conf_func=self._get_conf_emission_wavelengths,
            get_from_name_func=self._get_name_emission_wavelengths,
            set_func=None,
            values=None,
        )

    def get_all_settings(self, **kwargs):
        settings = super().get_all_settings(**kwargs)
        settings.update(self.get_theoretical_res(**kwargs))
        settings.update(self.get_nyquist(**kwargs))

        return settings

    def _get_conf_objective_lens_refr_index(self, image):
        return self._get_conf_objective_setting("objective_lens_refractive_index", image)

    def _get_name_objective_lens_refr_index(self, image):
        return self._get_metadata_from_name("_RI=", "_", float, image)

    def _get_conf_objective_lens_na(self, image):
        return self._get_conf_objective_setting("objective_lens_na", image)

    def _get_name_objective_lens_na(self, image):
        return self._get_metadata_from_name("_NA=", "_", float, image)

    def _get_conf_objective_lens_nominal_magnification(self, image):
        return self._get_conf_objective_setting("objective_lens_nominal_magnification", image)

    def _get_name_objective_lens_nominal_magnification(self, image):
        return self._get_metadata_from_name("_MAG=", "_", float, image)

    def _get_conf_excitation_wavelengths(self, image):
        return self._get_conf_channel_settings("excitation_wavelengths", image)

    def _get_name_excitation_wavelengths(self, image):
        return self._get_metadata_from_name("_EX=", "_", list, image)

    def _get_conf_emission_wavelengths(self, image):
        return self._get_conf_channel_settings("emission_wavelengths", image)

    def _get_name_emission_wavelengths(self, image):
        return self._get_metadata_from_name("_EM=", "_", list, image)

    # TODO: to move to interface
    def _get_objective_lens_refractive_index(self, image):
        objective_settings = image.getObjectiveSettings()
        if objective_settings is None:
            return None
        return objective_settings.getRefractiveIndex()

    def _get_objective_lens_na(self, image):
        objective_settings = image.getObjectiveSettings()
        if objective_settings is None:
            return None
        objective = objective_settings.getObjective()
        if objective is None:
            return None
        return objective.getLensNA()

    def _get_objective_lens_nominal_magnification(self, image):
        objective_settings = image.getObjectiveSettings()
        if objective_settings is None:
            return None
        objective = objective_settings.getObjective()
        if objective is None:
            return None
        return objective.getNominalMagnification()

    def _get_excitation_wavelengths(self, image):
        channels = image.getChannels()
        if channels is None:
            return None
        wavelengths = tuple(ch.getExcitationWave() for ch in channels)
        if not all(wavelengths):
            return None
        else:
            return wavelengths

    def _get_emission_wavelengths(self, image):
        channels = image.getChannels()
        if channels is None:
            return None
        wavelengths = tuple(ch.getEmissionWave() for ch in channels)
        if not all(wavelengths):
            return None
        else:
            return wavelengths

    def get_theoretical_res_fwhm(self, **kwargs):
        """Returns a dictionary containing the lateral and axial FWHM theoretical resolutions for every channel in image.

        :param image: an image object
        :return: a dictionary in the form:
                 {'resolution_theoretical_fwhm_lateral': list of lateral resolutions for every channel,
                  'resolution_theoretical_fwhm_axial': list of axial resolutions for every channel,
                  'resolution_theoretical_fwhm_units': string specifying units}
        """
        theoretical_res = {
            "resolution_theoretical_fwhm_lateral": [],
            "resolution_theoretical_fwhm_axial": [],
            "resolution_theoretical_fwhm_units": "NANOMETER",
        }
        na = self.get_setting("objective_lens_na", **kwargs)
        for em in self.get_setting("emission_wavelengths", **kwargs):
            try:
                theoretical_res["resolution_theoretical_fwhm_lateral"].append(0.353 * em / na)
            except TypeError as e:
                module_logger.warning(
                    "FWHM theoretical resolution could not be calculated. Verify configuration files."
                )
                theoretical_res["resolution_theoretical_fwhm_lateral"].append(None)
            try:
                theoretical_res["resolution_theoretical_fwhm_axial"].append(
                    None
                )  # TODO: find formula for fwhm axial resolution
            except TypeError as e:
                module_logger.warning(
                    "FWHM theoretical resolution could not be calculated. Verify configuration files."
                )
                theoretical_res["resolution_theoretical_fwhm_axial"].append(None)

        return theoretical_res

    def get_theoretical_res_rayleigh(self, **kwargs):
        """Returns a dictionary containing the lateral and axial Rayleigh theoretical resolutions for every channel in image.

        :param image: an image object
        :return: a dictionary in the form:
                 {'resolution_theoretical_rayleigh_lateral': list of lateral resolutions for every channel,
                  'resolution_theoretical_rayleigh_axial': list of axial resolutions for every channel,
                  'resolution_theoretical_rayleigh_units': string specifying units}
        """
        theoretical_res = {
            "resolution_theoretical_rayleigh_lateral": [],
            "resolution_theoretical_rayleigh_axial": [],
            "resolution_theoretical_rayleigh_units": "NANOMETER",
        }
        na = self.get_setting("objective_lens_na", **kwargs)
        ri = self.get_setting("objective_lens_refractive_index", **kwargs)
        for em in self.get_setting("emission_wavelengths", **kwargs):
            try:
                theoretical_res["resolution_theoretical_rayleigh_lateral"].append(0.61 * em / na)
            except TypeError as e:
                module_logger.warning(
                    "Rayleigh theoretical lateral resolution could not be calculated. Verify configuration files."
                )
                theoretical_res["resolution_theoretical_rayleigh_lateral"].append(None)
            try:
                theoretical_res["resolution_theoretical_rayleigh_axial"].append(2 * em * ri / na**2)
            except TypeError as e:
                module_logger.warning(
                    "Rayleigh theoretical axial resolution could not be calculated. Verify configuration files."
                )
                theoretical_res["resolution_theoretical_rayleigh_axial"].append(None)

        return theoretical_res

    def get_theoretical_res(self, **kwargs):
        """Returns a dictionary containing the theoretical resolutions for every channel in image in all the
        implemented methods."""
        theoretical_res = dict()
        theoretical_res.update(self.get_theoretical_res_fwhm(**kwargs))
        theoretical_res.update(self.get_theoretical_res_rayleigh(**kwargs))

        return theoretical_res

    def get_nyquist(self, **kwargs):
        """Returns a dictionary containing the nyquist sampling criteria values for every channel in image."""
        nyquist_delta = {
            "nyquist_lateral": [],
            "nyquist_axial": [],
            "nyquist_units": "NANOMETER",
        }  # TODO: FIX units for nyquist and resolution. Get them from wavelength units.
        na = self.get_setting("objective_lens_na", **kwargs)
        ri = self.get_setting("objective_lens_refractive_index", **kwargs)
        for em in self.get_setting("emission_wavelengths", **kwargs):
            try:
                nyquist_delta["nyquist_lateral"].append(em / (4 * ri * (na / ri)))
            except TypeError as e:
                module_logger.warning(
                    "Lateral Nyquist criterion could not be calculated. Verify configuration files."
                )
                nyquist_delta["nyquist_lateral"].append(None)
            try:
                nyquist_delta["nyquist_axial"].append(em / (2 * ri * (1 - cos(asin(na / ri)))))
            except TypeError as e:
                module_logger.warning(
                    "Axial Nyquist criterion could not be calculated. Verify configuration files."
                )
                nyquist_delta["nyquist_axial"].append(None)

        return nyquist_delta
        #
        # def calculate_theoretcal_resolution(microscope_type, na, refractive_index, emission_wave, excitation_wave=None):
        #     theoretical_res = {}
        #     if microscope_type is None:
        #         module_logger.warning(
        #             'Microscope type undefined to calculate theoretical resolution. Falling back into Wide-Field')
        #         theoretical_res = calculate_theoretcal_resolution('wf', na, refractive_index, emission_wave,
        #                                                           excitation_wave=excitation_wave)
        #     elif microscope_type.lower() in ['wf', 'wide-field', 'widefield']:
        #         theoretical_res['fwhm_lateral'] = .353 * emission_wave / na
        #         theoretical_res['rayleigh_lateral'] = .61 * emission_wave / na
        #         theoretical_res['rayleigh_axial'] = 2 * emission_wave * refractive_index / na ** 2
        #         theoretical_res['units'] = 'NANOMETER'
        #     elif microscope_type.lower() in ['confocal']:
        #         theoretical_res['fwhm_lateral'] = .353 * emission_wave / na
        #         theoretical_res['rayleigh_lateral'] = .4 * emission_wave / na
        #         theoretical_res['rayleigh_axial'] = 1.4 * emission_wave * refractive_index / na ** 2
        #         theoretical_res['units'] = 'NANOMETER'
        #     else:
        #         module_logger.warning(
        #             'Could not find microscope type to calculate theoretical resolution. Falling back into Wide-Field')
        #         theoretical_res = calculate_theoretcal_resolution('wf', na, refractive_index, emission_wave,
        #                                                           excitation_wave=excitation_wave)
        #
        #     return theoretical_res

        #
        # if refractive_index is None:
        #     module_logger.warning('Refractive index is being guessed. Nyquist criteria will not be correct.')
        #     if na > .8:
        #         refractive_index = 1.5
        #     else:
        #         refractive_index = 1.0
        # alpha = asin(na / refractive_index)
        # # Theoretical resolutions for confocal microscope are only attained with very closed pinhole
        # # We add a tolerance factor to render theoretical resolution more realistic
        # tolerance = 1.6
        # nyquist_delta = {}
        # if microscope_type is None:
        #     module_logger.warning(
        #         'Microscope type undefined to calculate Nyquist criterion. Falling back into Wide-Field')
        #     nyquist_delta = calculate_nyquist('wf', na, refractive_index, emission_wave, excitation_wave)
        # elif microscope_type.lower() in ['wf', 'wide-field', 'widefield']:
        #     nyquist_delta['lateral'] = emission_wave / (4 * refractive_index * sin(alpha))
        #     nyquist_delta['axial'] = emission_wave / (2 * refractive_index * (1 - cos(alpha)))
        #     nyquist_delta['units'] = 'NANOMETER'
        # elif microscope_type.lower() in ['confocal']:
        #     nyquist_delta['lateral'] = tolerance * excitation_wave / (8 * refractive_index * sin(alpha))
        #     nyquist_delta['axial'] = tolerance * excitation_wave / (4 * refractive_index * (1 - cos(alpha)))
        #     nyquist_delta['units'] = 'NANOMETER'
        # else:
        #     module_logger.warning(
        #         'Could not find microscope type to calculate Nyquist criterion. Falling back into Wide-Field')
        #     nyquist_delta = calculate_nyquist('wf', na, refractive_index, emission_wave, excitation_wave)
        #
        # return nyquist_delta
