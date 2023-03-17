from abc import ABC


class Reporter(ABC):
    """This is the superclass taking care of creating reports for a particular type of sample.
    You should subclass this when you create a new sample."""

    def __init__(
        self,
        config,
        image_report_to_func={},
        dataset_report_to_func={},
        microscope_report_to_func={},
    ):
        """Add to the init subclass a dictionary mapping analyses strings to functions
        :type config: analysis_config section
        :param config: analysis_config section specifying sample options
        :type image_report_to_func: dict
        :param image_report_to_func: dictionary mapping image analyses strings to functions
        :type dataset_report_to_func: dict
        :param dataset_report_to_func: dictionary mapping dataset analyses strings to functions
        :type microscope_report_to_func: dict
        :param microscope_report_to_func: dictionary mapping microscope analyses strings to functions
        """
        self.config = config
        self.image_report_to_func = image_report_to_func
        self.dataset_report_to_func = dataset_report_to_func
        self.microscope_report_to_func = microscope_report_to_func

    def produce_image_report(self, image):
        pass

    def produce_dataset_report(self, dataset):
        pass

    def produce_device_report(self, device):
        pass

    # TODO: move this where it belongs
    # # Helper functions
    # def get_tables(self, omero_object, namespace_start='', name_filter=''):
    #     tables_list = list()
    #     resources = omero_object._conn.getSharedResources()
    #     for ann in omero_object.listAnnotations():
    #         if isinstance(ann, gw.FileAnnotationWrapper) and \
    #                 ann.getNs().startswith(namespace_start) and \
    #                 name_filter in ann.getFileName():
    #             table_file = omero_object._conn.getObject("OriginalFile", attributes={'name': ann.getFileName()})
    #             table = resources.openTable(table_file._obj)
    #             tables_list.append(table)
    #
    #     return tables_list
    #
