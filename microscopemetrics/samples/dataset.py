from datetime import datetime

# Import sample superclass
from microscopemetrics.samples.samples import Analysis, Configurator

# Creating logging services
import logging

module_logger = logging.getLogger("metrics.samples.dataset")


class DatasetConfigurator(Configurator):
    """This class handles the configuration properties of the excitation_power sample
    - Defines configuration properties
    - Helps in the generation of analysis_config files"""

    CONFIG_SECTION = "DATASET"
    ANALYSES = ["laser_power_measurement"]

    def __init__(self, config):
        super().__init__(config)


@DatasetConfigurator.register_sample_analysis
class DatasetAnalysis(Analysis):
    """This class handles the Excitation_power sample:
    - Defines the logic of the associated analyses
    - Defines the creation of reports"""

    def __init__(self, config=None):
        dataset_analysis_to_func = {
            "laser_power_measurement": self.analyze_laser_power_measurement,
        }
        self.configurator = DatasetConfigurator(config)
        super().__init__(
            config=config, dataset_analysis_to_func=dataset_analysis_to_func
        )

    @staticmethod
    def analyze_laser_power_measurement(dataset, config):
        """Opens a Map annotation where the user can enter the power measurements of the Excitation lasers. Those shoudl
        be blocked upon validation

        :param dataset: dataset instance
        :param config: MetricsConfig instance defining analysis configuration.
                       Must contain the analysis parameters defined by the configurator

        :returns a list of images
                 a list of rois
                 a list of tags
                 a list of dicts
                 a dict containing table_names and tables
        """
        module_logger.info(f"Generating light sources annotation...")

        wavelengths = config.getlistint("laser_power_measurement_wavelengths", None)
        power_units = config.get("laser_power_measurement_units")
        measurement_method = config.get("laser_power_measurement_method")

        if wavelengths is None:
            module_logger.error(
                "Config defined to do excitation power measurements but No wavelengths were provided"
            )
            wavelengths = list()

        key_values = {"analysis_date": datetime.now().strftime("%Y-%m-%d")}
        for wave in wavelengths:
            key_values.update({str(wave): ""})
        key_values["power_units"] = power_units
        key_values["measurement_method"] = measurement_method

        out_images = []
        out_rois = []
        out_tags = []
        out_dicts = [key_values]
        out_editables = [True]
        out_tables = []

        return out_images, out_rois, out_tags, out_dicts, out_editables, out_tables
