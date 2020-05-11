# Main samples module defining the sample superclass

# class Parameter:

from types import SimpleNamespace


class Configurator:
    """This is a superclass taking care of the configuration of a new sample. Helps generating configuration files and
    defines configuration parameters necessary for the different analyses.
    """
    # The configuration section has to be defined for every subclass
    CONFIG_SECTION: str = None
    ANALYSES = list()

    def __init__(self, config):
        self.config = config
        # self.validate_config()

    @classmethod
    def register_sample(cls, sample_class):
        cls.SAMPLE_CLASS = sample_class
        return sample_class

    @classmethod
    def register_analyses(cls):
        pass


class Analyzer:
    """This is the superclass defining the interface to a sample object. You should subclass this in order to create a
    new sample."""
    def __init__(self, config, image_analysis_to_func={}, dataset_analysis_to_func={}, microscope_analysis_to_func={}):
        """Add to the init subclass a dictionary mapping analyses strings to functions
        :type config: config section
        :param config: config section specifying sample options
        :type image_analysis_to_func: dict
        :param image_analysis_to_func: dictionary mapping image analyses strings to functions
        :type dataset_analysis_to_func: dict
        :param dataset_analysis_to_func: dictionary mapping dataset analyses strings to functions
        :type microscope_analysis_to_func: dict
        :param microscope_analysis_to_func: dictionary mapping microscope analyses strings to functions
        """
        self.config = config
        self.image_analysis_to_func = image_analysis_to_func
        self.dataset_analysis_to_func = dataset_analysis_to_func
        self.microscope_analysis_to_func = microscope_analysis_to_func

    @classmethod
    def get_module(cls):
        """Returns the module name of the class. Without path and extension.
        :returns a string with the module name
        """
        return cls.__module__.split(sep='.')[-1]

    def validate_dataset(self):
        """Override this method to integrate all the logic of dataset validation"""
        pass

    def _verify_limits(self, key_values, config):
        """Verifies that the numeric values provided in the key_values dictionary are within the ranges found in the config"""
        for option in config.options():
            # Evaluate upper limits
            if option.endswith('_upper_limit'):
                key = option.rstrip('_upper_limit')
                value = key_values[key]
                try:
                    limit = eval(config.get(option))
                except NameError:
                    limit = self._evaluate_limits(key_values, config.get(option))
                if limit is not None and value >= limit:
                    key_values[key + '_upper_pass'] = 'No'
                else:
                    key_values[key + '_upper_pass'] = 'Yes'

            # Evaluate lower limits
            if option.endswith('_lower_limit'):
                key = option.rstrip('_lower_limit')
                value = key_values[key]
                try:
                    limit = eval(config.get(option))
                except NameError:
                    limit = self._evaluate_limits(key_values, config.get(option))
                if limit is not None and value > limit:
                    key_values[key + '_lower_pass'] = 'Yes'
                else:
                    key_values[key + '_lower_pass'] = 'No'

        return key_values

    @staticmethod
    def _evaluate_limits(self, key_values, expression):
        # We keep the evaluation in a separate function to avoid namespace conflict
        locals().update(key_values)
        try:
            limit = eval(expression)
        except NameError as e:
            limit = None
            raise e(f'Could not evaluate expression {expression} as a limit')
        finally:
            return limit

    def analyze_dataset(self, dataset, config=None):
        """Override this method to integrate all the logic of the analyses of a dataset according the config settings
        :param dataset: a dataset object to be analyzed
        :param config: the configuration with which this dataset has to be analyzed. If None is provided, the configuration of the sample instance will be used

        :returns a list of images
                 a list of tags
                 a list of dicts
                 a dict containing table_names and tables
        """
        pass

    def analyze_image(self, image, analyses, config, verify_limits=True):
        """A passthrough to the different analysis implemented on the sample.
        :param image: an image object to be analyzed
        :param analyses: a str of list of str specifying the analysis to be made. string to functions to be run
                         are mapped through
        :param config: a dictionary with the configuration to analyze the image the configuration

        :returns a list of image objects
                 a list of roi objects
                 a list of tags
                 a list of dicts
                 a dict containing table_names and tables
        """
        out_images = list()
        out_rois = list()
        out_tags = list()
        out_dicts = list()
        out_tables = dict()
        if isinstance(analyses, str):
            analyses = [analyses]

        for analysis in analyses:
            images, rois, tags, dicts, tables = self.image_analysis_to_func[analysis](image, config)
            out_images.extend(images)
            out_rois.extend(rois)
            out_tags.extend(tags)
            if verify_limits:
                validated_dicts = []
                for d in dicts:
                    validated_dicts.append(self._verify_limits(d, config))
                out_dicts.extend(validated_dicts)
            else:
                out_dicts.extend(dicts)
            out_tables.update(tables)

        return out_images, out_rois, out_tags, out_dicts, out_tables

    @staticmethod
    def _create_roi(shapes, name=None, description=None):
        """A helper function to create ROIs"""
        roi = {'name': name,
               'desc': description,
               'shapes': shapes}
        return roi

    @staticmethod
    def _create_shape(shape_type, **kwargs):
        """A helper function to create roi shapes"""
        if shape_type in ['point', 'line', 'rectangle', 'ellipse', 'polygon']:
            shape = {'type': shape_type,
                     'args': kwargs}
            return shape
        else:
            raise ValueError('Cannot recognize that type of shape')
