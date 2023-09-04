# Auto generated from psf_beads_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2023-09-05T01:40:15
# Schema: microscopemetrics_samples_argolight_schema
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from ..core_schema import Comment, ExperimenterOrcid, Image5DImageUrl, ImageAsNumpyImageUrl, KeyValues, MetricsDataset, MetricsInput, MetricsOutput, Roi, SampleType, TableAsDict
from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDate

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/')


# Types

# Class references



@dataclass
class PSFBeadsDataset(MetricsDataset):
    """
    A dataset of PSF beads dataset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsDataset")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PSFBeadsDataset"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsDataset")

    input: Union[dict, "PSFBeadsInput"] = None
    processed: Union[bool, Bool] = False
    output: Optional[Union[dict, "PSFBeadsOutput"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.input):
            self.MissingRequiredField("input")
        if not isinstance(self.input, PSFBeadsInput):
            self.input = PSFBeadsInput(**as_dict(self.input))

        if self.output is not None and not isinstance(self.output, PSFBeadsOutput):
            self.output = PSFBeadsOutput(**as_dict(self.output))

        super().__post_init__(**kwargs)


@dataclass
class PSFBeadsInput(MetricsInput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsInput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PSFBeadsInput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsInput")

    psf_beads_image: Union[Union[str, ImageAsNumpyImageUrl], List[Union[str, ImageAsNumpyImageUrl]]] = None
    min_lateral_distance_factor: int = 20
    sigma_z: Optional[float] = None
    sigma_x: Optional[float] = None
    sigma_y: Optional[float] = None
    pixel_size_z: Optional[float] = None
    pixel_size_y: Optional[float] = None
    pixel_size_x: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.psf_beads_image):
            self.MissingRequiredField("psf_beads_image")
        if not isinstance(self.psf_beads_image, list):
            self.psf_beads_image = [self.psf_beads_image] if self.psf_beads_image is not None else []
        self.psf_beads_image = [v if isinstance(v, ImageAsNumpyImageUrl) else ImageAsNumpyImageUrl(v) for v in self.psf_beads_image]

        if self._is_empty(self.min_lateral_distance_factor):
            self.MissingRequiredField("min_lateral_distance_factor")
        if not isinstance(self.min_lateral_distance_factor, int):
            self.min_lateral_distance_factor = int(self.min_lateral_distance_factor)

        if self.sigma_z is not None and not isinstance(self.sigma_z, float):
            self.sigma_z = float(self.sigma_z)

        if self.sigma_x is not None and not isinstance(self.sigma_x, float):
            self.sigma_x = float(self.sigma_x)

        if self.sigma_y is not None and not isinstance(self.sigma_y, float):
            self.sigma_y = float(self.sigma_y)

        if self.pixel_size_z is not None and not isinstance(self.pixel_size_z, float):
            self.pixel_size_z = float(self.pixel_size_z)

        if self.pixel_size_y is not None and not isinstance(self.pixel_size_y, float):
            self.pixel_size_y = float(self.pixel_size_y)

        if self.pixel_size_x is not None and not isinstance(self.pixel_size_x, float):
            self.pixel_size_x = float(self.pixel_size_x)

        super().__post_init__(**kwargs)


@dataclass
class PSFBeadsOutput(MetricsOutput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsOutput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PSFBeadsOutput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsOutput")

    bead_crops: Optional[Union[Union[str, Image5DImageUrl], List[Union[str, Image5DImageUrl]]]] = empty_list()
    bead_centroids: Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]] = empty_list()
    edge_bead_centroids: Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]] = empty_list()
    self_proximity_bead_centroids: Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]] = empty_list()
    cluster_bead_centroids: Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]] = empty_list()
    key_measurements: Optional[Union[dict, "PSFBeadsKeyMeasurements"]] = None
    psf_properties: Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]] = empty_list()
    psf_z_profiles: Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]] = empty_list()
    psf_y_profiles: Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]] = empty_list()
    psf_x_profiles: Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.bead_crops, list):
            self.bead_crops = [self.bead_crops] if self.bead_crops is not None else []
        self.bead_crops = [v if isinstance(v, Image5DImageUrl) else Image5DImageUrl(v) for v in self.bead_crops]

        if not isinstance(self.bead_centroids, list):
            self.bead_centroids = [self.bead_centroids] if self.bead_centroids is not None else []
        self.bead_centroids = [v if isinstance(v, Roi) else Roi(**as_dict(v)) for v in self.bead_centroids]

        if not isinstance(self.edge_bead_centroids, list):
            self.edge_bead_centroids = [self.edge_bead_centroids] if self.edge_bead_centroids is not None else []
        self.edge_bead_centroids = [v if isinstance(v, Roi) else Roi(**as_dict(v)) for v in self.edge_bead_centroids]

        if not isinstance(self.self_proximity_bead_centroids, list):
            self.self_proximity_bead_centroids = [self.self_proximity_bead_centroids] if self.self_proximity_bead_centroids is not None else []
        self.self_proximity_bead_centroids = [v if isinstance(v, Roi) else Roi(**as_dict(v)) for v in self.self_proximity_bead_centroids]

        if not isinstance(self.cluster_bead_centroids, list):
            self.cluster_bead_centroids = [self.cluster_bead_centroids] if self.cluster_bead_centroids is not None else []
        self.cluster_bead_centroids = [v if isinstance(v, Roi) else Roi(**as_dict(v)) for v in self.cluster_bead_centroids]

        if self.key_measurements is not None and not isinstance(self.key_measurements, PSFBeadsKeyMeasurements):
            self.key_measurements = PSFBeadsKeyMeasurements(**as_dict(self.key_measurements))

        self._normalize_inlined_as_dict(slot_name="psf_properties", slot_type=TableAsDict, key_name="columns", keyed=False)

        self._normalize_inlined_as_dict(slot_name="psf_z_profiles", slot_type=TableAsDict, key_name="columns", keyed=False)

        self._normalize_inlined_as_dict(slot_name="psf_y_profiles", slot_type=TableAsDict, key_name="columns", keyed=False)

        self._normalize_inlined_as_dict(slot_name="psf_x_profiles", slot_type=TableAsDict, key_name="columns", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class PSFBeadsKeyMeasurements(KeyValues):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsKeyMeasurements")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PSFBeadsKeyMeasurements"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/PSFBeadsKeyMeasurements")

    nr_of_beads_analyzed: Optional[Union[int, List[int]]] = empty_list()
    nr_of_beads_discarded: Optional[Union[int, List[int]]] = empty_list()
    resolution_mean_fwhm_z_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_z_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_z_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_mean_fwhm_y_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_y_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_y_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_mean_fwhm_x_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_x_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_x_pixels: Optional[Union[float, List[float]]] = empty_list()
    resolution_mean_fwhm_z_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_z_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_z_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_mean_fwhm_y_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_y_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_y_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_mean_fwhm_x_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_median_fwhm_x_microns: Optional[Union[float, List[float]]] = empty_list()
    resolution_stdev_fwhm_x_microns: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.nr_of_beads_analyzed, list):
            self.nr_of_beads_analyzed = [self.nr_of_beads_analyzed] if self.nr_of_beads_analyzed is not None else []
        self.nr_of_beads_analyzed = [v if isinstance(v, int) else int(v) for v in self.nr_of_beads_analyzed]

        if not isinstance(self.nr_of_beads_discarded, list):
            self.nr_of_beads_discarded = [self.nr_of_beads_discarded] if self.nr_of_beads_discarded is not None else []
        self.nr_of_beads_discarded = [v if isinstance(v, int) else int(v) for v in self.nr_of_beads_discarded]

        if not isinstance(self.resolution_mean_fwhm_z_pixels, list):
            self.resolution_mean_fwhm_z_pixels = [self.resolution_mean_fwhm_z_pixels] if self.resolution_mean_fwhm_z_pixels is not None else []
        self.resolution_mean_fwhm_z_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_z_pixels]

        if not isinstance(self.resolution_median_fwhm_z_pixels, list):
            self.resolution_median_fwhm_z_pixels = [self.resolution_median_fwhm_z_pixels] if self.resolution_median_fwhm_z_pixels is not None else []
        self.resolution_median_fwhm_z_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_z_pixels]

        if not isinstance(self.resolution_stdev_fwhm_z_pixels, list):
            self.resolution_stdev_fwhm_z_pixels = [self.resolution_stdev_fwhm_z_pixels] if self.resolution_stdev_fwhm_z_pixels is not None else []
        self.resolution_stdev_fwhm_z_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_z_pixels]

        if not isinstance(self.resolution_mean_fwhm_y_pixels, list):
            self.resolution_mean_fwhm_y_pixels = [self.resolution_mean_fwhm_y_pixels] if self.resolution_mean_fwhm_y_pixels is not None else []
        self.resolution_mean_fwhm_y_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_y_pixels]

        if not isinstance(self.resolution_median_fwhm_y_pixels, list):
            self.resolution_median_fwhm_y_pixels = [self.resolution_median_fwhm_y_pixels] if self.resolution_median_fwhm_y_pixels is not None else []
        self.resolution_median_fwhm_y_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_y_pixels]

        if not isinstance(self.resolution_stdev_fwhm_y_pixels, list):
            self.resolution_stdev_fwhm_y_pixels = [self.resolution_stdev_fwhm_y_pixels] if self.resolution_stdev_fwhm_y_pixels is not None else []
        self.resolution_stdev_fwhm_y_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_y_pixels]

        if not isinstance(self.resolution_mean_fwhm_x_pixels, list):
            self.resolution_mean_fwhm_x_pixels = [self.resolution_mean_fwhm_x_pixels] if self.resolution_mean_fwhm_x_pixels is not None else []
        self.resolution_mean_fwhm_x_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_x_pixels]

        if not isinstance(self.resolution_median_fwhm_x_pixels, list):
            self.resolution_median_fwhm_x_pixels = [self.resolution_median_fwhm_x_pixels] if self.resolution_median_fwhm_x_pixels is not None else []
        self.resolution_median_fwhm_x_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_x_pixels]

        if not isinstance(self.resolution_stdev_fwhm_x_pixels, list):
            self.resolution_stdev_fwhm_x_pixels = [self.resolution_stdev_fwhm_x_pixels] if self.resolution_stdev_fwhm_x_pixels is not None else []
        self.resolution_stdev_fwhm_x_pixels = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_x_pixels]

        if not isinstance(self.resolution_mean_fwhm_z_microns, list):
            self.resolution_mean_fwhm_z_microns = [self.resolution_mean_fwhm_z_microns] if self.resolution_mean_fwhm_z_microns is not None else []
        self.resolution_mean_fwhm_z_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_z_microns]

        if not isinstance(self.resolution_median_fwhm_z_microns, list):
            self.resolution_median_fwhm_z_microns = [self.resolution_median_fwhm_z_microns] if self.resolution_median_fwhm_z_microns is not None else []
        self.resolution_median_fwhm_z_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_z_microns]

        if not isinstance(self.resolution_stdev_fwhm_z_microns, list):
            self.resolution_stdev_fwhm_z_microns = [self.resolution_stdev_fwhm_z_microns] if self.resolution_stdev_fwhm_z_microns is not None else []
        self.resolution_stdev_fwhm_z_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_z_microns]

        if not isinstance(self.resolution_mean_fwhm_y_microns, list):
            self.resolution_mean_fwhm_y_microns = [self.resolution_mean_fwhm_y_microns] if self.resolution_mean_fwhm_y_microns is not None else []
        self.resolution_mean_fwhm_y_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_y_microns]

        if not isinstance(self.resolution_median_fwhm_y_microns, list):
            self.resolution_median_fwhm_y_microns = [self.resolution_median_fwhm_y_microns] if self.resolution_median_fwhm_y_microns is not None else []
        self.resolution_median_fwhm_y_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_y_microns]

        if not isinstance(self.resolution_stdev_fwhm_y_microns, list):
            self.resolution_stdev_fwhm_y_microns = [self.resolution_stdev_fwhm_y_microns] if self.resolution_stdev_fwhm_y_microns is not None else []
        self.resolution_stdev_fwhm_y_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_y_microns]

        if not isinstance(self.resolution_mean_fwhm_x_microns, list):
            self.resolution_mean_fwhm_x_microns = [self.resolution_mean_fwhm_x_microns] if self.resolution_mean_fwhm_x_microns is not None else []
        self.resolution_mean_fwhm_x_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_mean_fwhm_x_microns]

        if not isinstance(self.resolution_median_fwhm_x_microns, list):
            self.resolution_median_fwhm_x_microns = [self.resolution_median_fwhm_x_microns] if self.resolution_median_fwhm_x_microns is not None else []
        self.resolution_median_fwhm_x_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_median_fwhm_x_microns]

        if not isinstance(self.resolution_stdev_fwhm_x_microns, list):
            self.resolution_stdev_fwhm_x_microns = [self.resolution_stdev_fwhm_x_microns] if self.resolution_stdev_fwhm_x_microns is not None else []
        self.resolution_stdev_fwhm_x_microns = [v if isinstance(v, float) else float(v) for v in self.resolution_stdev_fwhm_x_microns]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.psf_beads_image = Slot(uri=DEFAULT_.psf_beads_image, name="psf_beads_image", curie=DEFAULT_.curie('psf_beads_image'),
                   model_uri=DEFAULT_.psf_beads_image, domain=None, range=Union[Union[str, ImageAsNumpyImageUrl], List[Union[str, ImageAsNumpyImageUrl]]])

slots.min_lateral_distance_factor = Slot(uri=DEFAULT_.min_lateral_distance_factor, name="min_lateral_distance_factor", curie=DEFAULT_.curie('min_lateral_distance_factor'),
                   model_uri=DEFAULT_.min_lateral_distance_factor, domain=None, range=int)

slots.sigma_z = Slot(uri=DEFAULT_.sigma_z, name="sigma_z", curie=DEFAULT_.curie('sigma_z'),
                   model_uri=DEFAULT_.sigma_z, domain=None, range=Optional[float])

slots.sigma_y = Slot(uri=DEFAULT_.sigma_y, name="sigma_y", curie=DEFAULT_.curie('sigma_y'),
                   model_uri=DEFAULT_.sigma_y, domain=None, range=Optional[float])

slots.sigma_x = Slot(uri=DEFAULT_.sigma_x, name="sigma_x", curie=DEFAULT_.curie('sigma_x'),
                   model_uri=DEFAULT_.sigma_x, domain=None, range=Optional[float])

slots.pixel_size_z = Slot(uri=DEFAULT_.pixel_size_z, name="pixel_size_z", curie=DEFAULT_.curie('pixel_size_z'),
                   model_uri=DEFAULT_.pixel_size_z, domain=None, range=Optional[float])

slots.pixel_size_y = Slot(uri=DEFAULT_.pixel_size_y, name="pixel_size_y", curie=DEFAULT_.curie('pixel_size_y'),
                   model_uri=DEFAULT_.pixel_size_y, domain=None, range=Optional[float])

slots.pixel_size_x = Slot(uri=DEFAULT_.pixel_size_x, name="pixel_size_x", curie=DEFAULT_.curie('pixel_size_x'),
                   model_uri=DEFAULT_.pixel_size_x, domain=None, range=Optional[float])

slots.nr_of_beads_analyzed = Slot(uri=DEFAULT_.nr_of_beads_analyzed, name="nr_of_beads_analyzed", curie=DEFAULT_.curie('nr_of_beads_analyzed'),
                   model_uri=DEFAULT_.nr_of_beads_analyzed, domain=None, range=Optional[Union[int, List[int]]])

slots.nr_of_beads_discarded = Slot(uri=DEFAULT_.nr_of_beads_discarded, name="nr_of_beads_discarded", curie=DEFAULT_.curie('nr_of_beads_discarded'),
                   model_uri=DEFAULT_.nr_of_beads_discarded, domain=None, range=Optional[Union[int, List[int]]])

slots.resolution_mean_fwhm_z_pixels = Slot(uri=DEFAULT_.resolution_mean_fwhm_z_pixels, name="resolution_mean_fwhm_z_pixels", curie=DEFAULT_.curie('resolution_mean_fwhm_z_pixels'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_z_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_z_pixels = Slot(uri=DEFAULT_.resolution_median_fwhm_z_pixels, name="resolution_median_fwhm_z_pixels", curie=DEFAULT_.curie('resolution_median_fwhm_z_pixels'),
                   model_uri=DEFAULT_.resolution_median_fwhm_z_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_z_pixels = Slot(uri=DEFAULT_.resolution_stdev_fwhm_z_pixels, name="resolution_stdev_fwhm_z_pixels", curie=DEFAULT_.curie('resolution_stdev_fwhm_z_pixels'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_z_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_mean_fwhm_y_pixels = Slot(uri=DEFAULT_.resolution_mean_fwhm_y_pixels, name="resolution_mean_fwhm_y_pixels", curie=DEFAULT_.curie('resolution_mean_fwhm_y_pixels'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_y_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_y_pixels = Slot(uri=DEFAULT_.resolution_median_fwhm_y_pixels, name="resolution_median_fwhm_y_pixels", curie=DEFAULT_.curie('resolution_median_fwhm_y_pixels'),
                   model_uri=DEFAULT_.resolution_median_fwhm_y_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_y_pixels = Slot(uri=DEFAULT_.resolution_stdev_fwhm_y_pixels, name="resolution_stdev_fwhm_y_pixels", curie=DEFAULT_.curie('resolution_stdev_fwhm_y_pixels'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_y_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_mean_fwhm_x_pixels = Slot(uri=DEFAULT_.resolution_mean_fwhm_x_pixels, name="resolution_mean_fwhm_x_pixels", curie=DEFAULT_.curie('resolution_mean_fwhm_x_pixels'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_x_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_x_pixels = Slot(uri=DEFAULT_.resolution_median_fwhm_x_pixels, name="resolution_median_fwhm_x_pixels", curie=DEFAULT_.curie('resolution_median_fwhm_x_pixels'),
                   model_uri=DEFAULT_.resolution_median_fwhm_x_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_x_pixels = Slot(uri=DEFAULT_.resolution_stdev_fwhm_x_pixels, name="resolution_stdev_fwhm_x_pixels", curie=DEFAULT_.curie('resolution_stdev_fwhm_x_pixels'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_x_pixels, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_mean_fwhm_z_microns = Slot(uri=DEFAULT_.resolution_mean_fwhm_z_microns, name="resolution_mean_fwhm_z_microns", curie=DEFAULT_.curie('resolution_mean_fwhm_z_microns'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_z_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_z_microns = Slot(uri=DEFAULT_.resolution_median_fwhm_z_microns, name="resolution_median_fwhm_z_microns", curie=DEFAULT_.curie('resolution_median_fwhm_z_microns'),
                   model_uri=DEFAULT_.resolution_median_fwhm_z_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_z_microns = Slot(uri=DEFAULT_.resolution_stdev_fwhm_z_microns, name="resolution_stdev_fwhm_z_microns", curie=DEFAULT_.curie('resolution_stdev_fwhm_z_microns'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_z_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_mean_fwhm_y_microns = Slot(uri=DEFAULT_.resolution_mean_fwhm_y_microns, name="resolution_mean_fwhm_y_microns", curie=DEFAULT_.curie('resolution_mean_fwhm_y_microns'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_y_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_y_microns = Slot(uri=DEFAULT_.resolution_median_fwhm_y_microns, name="resolution_median_fwhm_y_microns", curie=DEFAULT_.curie('resolution_median_fwhm_y_microns'),
                   model_uri=DEFAULT_.resolution_median_fwhm_y_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_y_microns = Slot(uri=DEFAULT_.resolution_stdev_fwhm_y_microns, name="resolution_stdev_fwhm_y_microns", curie=DEFAULT_.curie('resolution_stdev_fwhm_y_microns'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_y_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_mean_fwhm_x_microns = Slot(uri=DEFAULT_.resolution_mean_fwhm_x_microns, name="resolution_mean_fwhm_x_microns", curie=DEFAULT_.curie('resolution_mean_fwhm_x_microns'),
                   model_uri=DEFAULT_.resolution_mean_fwhm_x_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_median_fwhm_x_microns = Slot(uri=DEFAULT_.resolution_median_fwhm_x_microns, name="resolution_median_fwhm_x_microns", curie=DEFAULT_.curie('resolution_median_fwhm_x_microns'),
                   model_uri=DEFAULT_.resolution_median_fwhm_x_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.resolution_stdev_fwhm_x_microns = Slot(uri=DEFAULT_.resolution_stdev_fwhm_x_microns, name="resolution_stdev_fwhm_x_microns", curie=DEFAULT_.curie('resolution_stdev_fwhm_x_microns'),
                   model_uri=DEFAULT_.resolution_stdev_fwhm_x_microns, domain=None, range=Optional[Union[float, List[float]]])

slots.pSFBeadsDataset__input = Slot(uri=DEFAULT_.input, name="pSFBeadsDataset__input", curie=DEFAULT_.curie('input'),
                   model_uri=DEFAULT_.pSFBeadsDataset__input, domain=None, range=Union[dict, PSFBeadsInput])

slots.pSFBeadsDataset__output = Slot(uri=DEFAULT_.output, name="pSFBeadsDataset__output", curie=DEFAULT_.curie('output'),
                   model_uri=DEFAULT_.pSFBeadsDataset__output, domain=None, range=Optional[Union[dict, PSFBeadsOutput]])

slots.pSFBeadsOutput__bead_crops = Slot(uri=DEFAULT_.bead_crops, name="pSFBeadsOutput__bead_crops", curie=DEFAULT_.curie('bead_crops'),
                   model_uri=DEFAULT_.pSFBeadsOutput__bead_crops, domain=None, range=Optional[Union[Union[str, Image5DImageUrl], List[Union[str, Image5DImageUrl]]]])

slots.pSFBeadsOutput__bead_centroids = Slot(uri=DEFAULT_.bead_centroids, name="pSFBeadsOutput__bead_centroids", curie=DEFAULT_.curie('bead_centroids'),
                   model_uri=DEFAULT_.pSFBeadsOutput__bead_centroids, domain=None, range=Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]])

slots.pSFBeadsOutput__edge_bead_centroids = Slot(uri=DEFAULT_.edge_bead_centroids, name="pSFBeadsOutput__edge_bead_centroids", curie=DEFAULT_.curie('edge_bead_centroids'),
                   model_uri=DEFAULT_.pSFBeadsOutput__edge_bead_centroids, domain=None, range=Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]])

slots.pSFBeadsOutput__self_proximity_bead_centroids = Slot(uri=DEFAULT_.self_proximity_bead_centroids, name="pSFBeadsOutput__self_proximity_bead_centroids", curie=DEFAULT_.curie('self_proximity_bead_centroids'),
                   model_uri=DEFAULT_.pSFBeadsOutput__self_proximity_bead_centroids, domain=None, range=Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]])

slots.pSFBeadsOutput__cluster_bead_centroids = Slot(uri=DEFAULT_.cluster_bead_centroids, name="pSFBeadsOutput__cluster_bead_centroids", curie=DEFAULT_.curie('cluster_bead_centroids'),
                   model_uri=DEFAULT_.pSFBeadsOutput__cluster_bead_centroids, domain=None, range=Optional[Union[Union[dict, Roi], List[Union[dict, Roi]]]])

slots.pSFBeadsOutput__key_measurements = Slot(uri=DEFAULT_.key_measurements, name="pSFBeadsOutput__key_measurements", curie=DEFAULT_.curie('key_measurements'),
                   model_uri=DEFAULT_.pSFBeadsOutput__key_measurements, domain=None, range=Optional[Union[dict, PSFBeadsKeyMeasurements]])

slots.pSFBeadsOutput__psf_properties = Slot(uri=DEFAULT_.psf_properties, name="pSFBeadsOutput__psf_properties", curie=DEFAULT_.curie('psf_properties'),
                   model_uri=DEFAULT_.pSFBeadsOutput__psf_properties, domain=None, range=Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]])

slots.pSFBeadsOutput__psf_z_profiles = Slot(uri=DEFAULT_.psf_z_profiles, name="pSFBeadsOutput__psf_z_profiles", curie=DEFAULT_.curie('psf_z_profiles'),
                   model_uri=DEFAULT_.pSFBeadsOutput__psf_z_profiles, domain=None, range=Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]])

slots.pSFBeadsOutput__psf_y_profiles = Slot(uri=DEFAULT_.psf_y_profiles, name="pSFBeadsOutput__psf_y_profiles", curie=DEFAULT_.curie('psf_y_profiles'),
                   model_uri=DEFAULT_.pSFBeadsOutput__psf_y_profiles, domain=None, range=Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]])

slots.pSFBeadsOutput__psf_x_profiles = Slot(uri=DEFAULT_.psf_x_profiles, name="pSFBeadsOutput__psf_x_profiles", curie=DEFAULT_.curie('psf_x_profiles'),
                   model_uri=DEFAULT_.pSFBeadsOutput__psf_x_profiles, domain=None, range=Optional[Union[Union[dict, TableAsDict], List[Union[dict, TableAsDict]]]])
