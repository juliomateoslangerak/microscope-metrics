# Auto generated from field_illumination_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2023-08-28T14:39:52
# Schema: microscopemetrics_samples_field_illumination_schema
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions,
)
from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    Bool,
    XSDDate,
    bnode,
    empty_dict,
    empty_list,
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str,
)
from rdflib import Namespace, URIRef

from ..core_schema import (
    ROI,
    Comment,
    ExperimenterOrcid,
    Image5DImageUrl,
    ImageAsNumpy,
    ImageAsNumpyImageUrl,
    KeyValues,
    MetricsDataset,
    MetricsInput,
    MetricsOutput,
    SampleType,
    TableAsDict,
)

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/')


# Types

# Class references



@dataclass
class FieldIlluminationDataset(MetricsDataset):
    """
    A field illumination dataset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationDataset")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "FieldIlluminationDataset"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationDataset")

    input: Union[dict, "FieldIlluminationInput"] = None
    processed: Union[bool, Bool] = False
    output: Optional[Union[dict, "FieldIlluminationOutput"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.input):
            self.MissingRequiredField("input")
        if not isinstance(self.input, FieldIlluminationInput):
            self.input = FieldIlluminationInput(**as_dict(self.input))

        if self.output is not None and not isinstance(self.output, FieldIlluminationOutput):
            self.output = FieldIlluminationOutput(**as_dict(self.output))

        super().__post_init__(**kwargs)


@dataclass
class FieldIlluminationInput(MetricsInput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationInput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "FieldIlluminationInput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationInput")

    field_illumination_image: Union[dict, ImageAsNumpy] = None
    saturation_threshold: float = 0.01
    center_threshold: float = 0.9
    corner_fraction: float = 0.1
    sigma: float = 2.0
    intensity_map_size: int = 64
    bit_depth: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.field_illumination_image):
            self.MissingRequiredField("field_illumination_image")
        if not isinstance(self.field_illumination_image, ImageAsNumpy):
            self.field_illumination_image = ImageAsNumpy(**as_dict(self.field_illumination_image))

        if self._is_empty(self.saturation_threshold):
            self.MissingRequiredField("saturation_threshold")
        if not isinstance(self.saturation_threshold, float):
            self.saturation_threshold = float(self.saturation_threshold)

        if self._is_empty(self.center_threshold):
            self.MissingRequiredField("center_threshold")
        if not isinstance(self.center_threshold, float):
            self.center_threshold = float(self.center_threshold)

        if self._is_empty(self.corner_fraction):
            self.MissingRequiredField("corner_fraction")
        if not isinstance(self.corner_fraction, float):
            self.corner_fraction = float(self.corner_fraction)

        if self._is_empty(self.sigma):
            self.MissingRequiredField("sigma")
        if not isinstance(self.sigma, float):
            self.sigma = float(self.sigma)

        if self._is_empty(self.intensity_map_size):
            self.MissingRequiredField("intensity_map_size")
        if not isinstance(self.intensity_map_size, int):
            self.intensity_map_size = int(self.intensity_map_size)

        if self.bit_depth is not None and not isinstance(self.bit_depth, int):
            self.bit_depth = int(self.bit_depth)

        super().__post_init__(**kwargs)


@dataclass
class FieldIlluminationOutput(MetricsOutput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationOutput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "FieldIlluminationOutput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationOutput")

    key_values: Optional[Union[dict, "FieldIlluminationKeyValues"]] = None
    intensity_profiles: Optional[Union[dict, TableAsDict]] = None
    intensity_map: Optional[Union[str, Image5DImageUrl]] = None
    profile_rois: Optional[Union[dict, ROI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.key_values is not None and not isinstance(self.key_values, FieldIlluminationKeyValues):
            self.key_values = FieldIlluminationKeyValues(**as_dict(self.key_values))

        if self.intensity_profiles is not None and not isinstance(self.intensity_profiles, TableAsDict):
            self.intensity_profiles = TableAsDict(**as_dict(self.intensity_profiles))

        if self.intensity_map is not None and not isinstance(self.intensity_map, Image5DImageUrl):
            self.intensity_map = Image5DImageUrl(self.intensity_map)

        if self.profile_rois is not None and not isinstance(self.profile_rois, ROI):
            self.profile_rois = ROI(**as_dict(self.profile_rois))

        super().__post_init__(**kwargs)


@dataclass
class FieldIlluminationKeyValues(KeyValues):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationKeyValues")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "FieldIlluminationKeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/FieldIlluminationKeyValues")

    channel: Optional[Union[int, List[int]]] = empty_list()
    nb_pixels: Optional[Union[int, List[int]]] = empty_list()
    center_of_mass_x: Optional[Union[float, List[float]]] = empty_list()
    center_of_mass_y: Optional[Union[float, List[float]]] = empty_list()
    max_intensity: Optional[Union[float, List[float]]] = empty_list()
    max_intensity_pos_x: Optional[Union[float, List[float]]] = empty_list()
    max_intensity_pos_y: Optional[Union[float, List[float]]] = empty_list()
    top_left_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    top_left_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    top_center_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    top_center_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    top_right_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    top_right_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    middle_left_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    middle_left_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    middle_center_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    middle_center_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    middle_right_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    middle_right_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    bottom_left_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    bottom_left_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    bottom_center_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    bottom_center_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    bottom_right_intensity_mean: Optional[Union[float, List[float]]] = empty_list()
    bottom_right_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()
    decile_0: Optional[Union[float, List[float]]] = empty_list()
    decile_1: Optional[Union[float, List[float]]] = empty_list()
    decile_2: Optional[Union[float, List[float]]] = empty_list()
    decile_3: Optional[Union[float, List[float]]] = empty_list()
    decile_4: Optional[Union[float, List[float]]] = empty_list()
    decile_5: Optional[Union[float, List[float]]] = empty_list()
    decile_6: Optional[Union[float, List[float]]] = empty_list()
    decile_7: Optional[Union[float, List[float]]] = empty_list()
    decile_8: Optional[Union[float, List[float]]] = empty_list()
    decile_9: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.channel, list):
            self.channel = [self.channel] if self.channel is not None else []
        self.channel = [v if isinstance(v, int) else int(v) for v in self.channel]

        if not isinstance(self.nb_pixels, list):
            self.nb_pixels = [self.nb_pixels] if self.nb_pixels is not None else []
        self.nb_pixels = [v if isinstance(v, int) else int(v) for v in self.nb_pixels]

        if not isinstance(self.center_of_mass_x, list):
            self.center_of_mass_x = [self.center_of_mass_x] if self.center_of_mass_x is not None else []
        self.center_of_mass_x = [v if isinstance(v, float) else float(v) for v in self.center_of_mass_x]

        if not isinstance(self.center_of_mass_y, list):
            self.center_of_mass_y = [self.center_of_mass_y] if self.center_of_mass_y is not None else []
        self.center_of_mass_y = [v if isinstance(v, float) else float(v) for v in self.center_of_mass_y]

        if not isinstance(self.max_intensity, list):
            self.max_intensity = [self.max_intensity] if self.max_intensity is not None else []
        self.max_intensity = [v if isinstance(v, float) else float(v) for v in self.max_intensity]

        if not isinstance(self.max_intensity_pos_x, list):
            self.max_intensity_pos_x = [self.max_intensity_pos_x] if self.max_intensity_pos_x is not None else []
        self.max_intensity_pos_x = [v if isinstance(v, float) else float(v) for v in self.max_intensity_pos_x]

        if not isinstance(self.max_intensity_pos_y, list):
            self.max_intensity_pos_y = [self.max_intensity_pos_y] if self.max_intensity_pos_y is not None else []
        self.max_intensity_pos_y = [v if isinstance(v, float) else float(v) for v in self.max_intensity_pos_y]

        if not isinstance(self.top_left_intensity_mean, list):
            self.top_left_intensity_mean = [self.top_left_intensity_mean] if self.top_left_intensity_mean is not None else []
        self.top_left_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.top_left_intensity_mean]

        if not isinstance(self.top_left_intensity_ratio, list):
            self.top_left_intensity_ratio = [self.top_left_intensity_ratio] if self.top_left_intensity_ratio is not None else []
        self.top_left_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.top_left_intensity_ratio]

        if not isinstance(self.top_center_intensity_mean, list):
            self.top_center_intensity_mean = [self.top_center_intensity_mean] if self.top_center_intensity_mean is not None else []
        self.top_center_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.top_center_intensity_mean]

        if not isinstance(self.top_center_intensity_ratio, list):
            self.top_center_intensity_ratio = [self.top_center_intensity_ratio] if self.top_center_intensity_ratio is not None else []
        self.top_center_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.top_center_intensity_ratio]

        if not isinstance(self.top_right_intensity_mean, list):
            self.top_right_intensity_mean = [self.top_right_intensity_mean] if self.top_right_intensity_mean is not None else []
        self.top_right_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.top_right_intensity_mean]

        if not isinstance(self.top_right_intensity_ratio, list):
            self.top_right_intensity_ratio = [self.top_right_intensity_ratio] if self.top_right_intensity_ratio is not None else []
        self.top_right_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.top_right_intensity_ratio]

        if not isinstance(self.middle_left_intensity_mean, list):
            self.middle_left_intensity_mean = [self.middle_left_intensity_mean] if self.middle_left_intensity_mean is not None else []
        self.middle_left_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.middle_left_intensity_mean]

        if not isinstance(self.middle_left_intensity_ratio, list):
            self.middle_left_intensity_ratio = [self.middle_left_intensity_ratio] if self.middle_left_intensity_ratio is not None else []
        self.middle_left_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.middle_left_intensity_ratio]

        if not isinstance(self.middle_center_intensity_mean, list):
            self.middle_center_intensity_mean = [self.middle_center_intensity_mean] if self.middle_center_intensity_mean is not None else []
        self.middle_center_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.middle_center_intensity_mean]

        if not isinstance(self.middle_center_intensity_ratio, list):
            self.middle_center_intensity_ratio = [self.middle_center_intensity_ratio] if self.middle_center_intensity_ratio is not None else []
        self.middle_center_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.middle_center_intensity_ratio]

        if not isinstance(self.middle_right_intensity_mean, list):
            self.middle_right_intensity_mean = [self.middle_right_intensity_mean] if self.middle_right_intensity_mean is not None else []
        self.middle_right_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.middle_right_intensity_mean]

        if not isinstance(self.middle_right_intensity_ratio, list):
            self.middle_right_intensity_ratio = [self.middle_right_intensity_ratio] if self.middle_right_intensity_ratio is not None else []
        self.middle_right_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.middle_right_intensity_ratio]

        if not isinstance(self.bottom_left_intensity_mean, list):
            self.bottom_left_intensity_mean = [self.bottom_left_intensity_mean] if self.bottom_left_intensity_mean is not None else []
        self.bottom_left_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.bottom_left_intensity_mean]

        if not isinstance(self.bottom_left_intensity_ratio, list):
            self.bottom_left_intensity_ratio = [self.bottom_left_intensity_ratio] if self.bottom_left_intensity_ratio is not None else []
        self.bottom_left_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.bottom_left_intensity_ratio]

        if not isinstance(self.bottom_center_intensity_mean, list):
            self.bottom_center_intensity_mean = [self.bottom_center_intensity_mean] if self.bottom_center_intensity_mean is not None else []
        self.bottom_center_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.bottom_center_intensity_mean]

        if not isinstance(self.bottom_center_intensity_ratio, list):
            self.bottom_center_intensity_ratio = [self.bottom_center_intensity_ratio] if self.bottom_center_intensity_ratio is not None else []
        self.bottom_center_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.bottom_center_intensity_ratio]

        if not isinstance(self.bottom_right_intensity_mean, list):
            self.bottom_right_intensity_mean = [self.bottom_right_intensity_mean] if self.bottom_right_intensity_mean is not None else []
        self.bottom_right_intensity_mean = [v if isinstance(v, float) else float(v) for v in self.bottom_right_intensity_mean]

        if not isinstance(self.bottom_right_intensity_ratio, list):
            self.bottom_right_intensity_ratio = [self.bottom_right_intensity_ratio] if self.bottom_right_intensity_ratio is not None else []
        self.bottom_right_intensity_ratio = [v if isinstance(v, float) else float(v) for v in self.bottom_right_intensity_ratio]

        if not isinstance(self.decile_0, list):
            self.decile_0 = [self.decile_0] if self.decile_0 is not None else []
        self.decile_0 = [v if isinstance(v, float) else float(v) for v in self.decile_0]

        if not isinstance(self.decile_1, list):
            self.decile_1 = [self.decile_1] if self.decile_1 is not None else []
        self.decile_1 = [v if isinstance(v, float) else float(v) for v in self.decile_1]

        if not isinstance(self.decile_2, list):
            self.decile_2 = [self.decile_2] if self.decile_2 is not None else []
        self.decile_2 = [v if isinstance(v, float) else float(v) for v in self.decile_2]

        if not isinstance(self.decile_3, list):
            self.decile_3 = [self.decile_3] if self.decile_3 is not None else []
        self.decile_3 = [v if isinstance(v, float) else float(v) for v in self.decile_3]

        if not isinstance(self.decile_4, list):
            self.decile_4 = [self.decile_4] if self.decile_4 is not None else []
        self.decile_4 = [v if isinstance(v, float) else float(v) for v in self.decile_4]

        if not isinstance(self.decile_5, list):
            self.decile_5 = [self.decile_5] if self.decile_5 is not None else []
        self.decile_5 = [v if isinstance(v, float) else float(v) for v in self.decile_5]

        if not isinstance(self.decile_6, list):
            self.decile_6 = [self.decile_6] if self.decile_6 is not None else []
        self.decile_6 = [v if isinstance(v, float) else float(v) for v in self.decile_6]

        if not isinstance(self.decile_7, list):
            self.decile_7 = [self.decile_7] if self.decile_7 is not None else []
        self.decile_7 = [v if isinstance(v, float) else float(v) for v in self.decile_7]

        if not isinstance(self.decile_8, list):
            self.decile_8 = [self.decile_8] if self.decile_8 is not None else []
        self.decile_8 = [v if isinstance(v, float) else float(v) for v in self.decile_8]

        if not isinstance(self.decile_9, list):
            self.decile_9 = [self.decile_9] if self.decile_9 is not None else []
        self.decile_9 = [v if isinstance(v, float) else float(v) for v in self.decile_9]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.field_illumination_image = Slot(uri=DEFAULT_.field_illumination_image, name="field_illumination_image", curie=DEFAULT_.curie('field_illumination_image'),
                   model_uri=DEFAULT_.field_illumination_image, domain=None, range=Union[dict, ImageAsNumpy])

slots.center_threshold = Slot(uri=DEFAULT_.center_threshold, name="center_threshold", curie=DEFAULT_.curie('center_threshold'),
                   model_uri=DEFAULT_.center_threshold, domain=None, range=float)

slots.corner_fraction = Slot(uri=DEFAULT_.corner_fraction, name="corner_fraction", curie=DEFAULT_.curie('corner_fraction'),
                   model_uri=DEFAULT_.corner_fraction, domain=None, range=float)

slots.sigma = Slot(uri=DEFAULT_.sigma, name="sigma", curie=DEFAULT_.curie('sigma'),
                   model_uri=DEFAULT_.sigma, domain=None, range=float)

slots.intensity_map_size = Slot(uri=DEFAULT_.intensity_map_size, name="intensity_map_size", curie=DEFAULT_.curie('intensity_map_size'),
                   model_uri=DEFAULT_.intensity_map_size, domain=None, range=int)

slots.channel = Slot(uri=DEFAULT_.channel, name="channel", curie=DEFAULT_.curie('channel'),
                   model_uri=DEFAULT_.channel, domain=None, range=Optional[Union[int, List[int]]])

slots.nb_pixels = Slot(uri=DEFAULT_.nb_pixels, name="nb_pixels", curie=DEFAULT_.curie('nb_pixels'),
                   model_uri=DEFAULT_.nb_pixels, domain=None, range=Optional[Union[int, List[int]]])

slots.center_of_mass_x = Slot(uri=DEFAULT_.center_of_mass_x, name="center_of_mass_x", curie=DEFAULT_.curie('center_of_mass_x'),
                   model_uri=DEFAULT_.center_of_mass_x, domain=None, range=Optional[Union[float, List[float]]])

slots.center_of_mass_y = Slot(uri=DEFAULT_.center_of_mass_y, name="center_of_mass_y", curie=DEFAULT_.curie('center_of_mass_y'),
                   model_uri=DEFAULT_.center_of_mass_y, domain=None, range=Optional[Union[float, List[float]]])

slots.max_intensity = Slot(uri=DEFAULT_.max_intensity, name="max_intensity", curie=DEFAULT_.curie('max_intensity'),
                   model_uri=DEFAULT_.max_intensity, domain=None, range=Optional[Union[float, List[float]]])

slots.max_intensity_pos_x = Slot(uri=DEFAULT_.max_intensity_pos_x, name="max_intensity_pos_x", curie=DEFAULT_.curie('max_intensity_pos_x'),
                   model_uri=DEFAULT_.max_intensity_pos_x, domain=None, range=Optional[Union[float, List[float]]])

slots.max_intensity_pos_y = Slot(uri=DEFAULT_.max_intensity_pos_y, name="max_intensity_pos_y", curie=DEFAULT_.curie('max_intensity_pos_y'),
                   model_uri=DEFAULT_.max_intensity_pos_y, domain=None, range=Optional[Union[float, List[float]]])

slots.top_left_intensity_mean = Slot(uri=DEFAULT_.top_left_intensity_mean, name="top_left_intensity_mean", curie=DEFAULT_.curie('top_left_intensity_mean'),
                   model_uri=DEFAULT_.top_left_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.top_left_intensity_ratio = Slot(uri=DEFAULT_.top_left_intensity_ratio, name="top_left_intensity_ratio", curie=DEFAULT_.curie('top_left_intensity_ratio'),
                   model_uri=DEFAULT_.top_left_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.top_center_intensity_mean = Slot(uri=DEFAULT_.top_center_intensity_mean, name="top_center_intensity_mean", curie=DEFAULT_.curie('top_center_intensity_mean'),
                   model_uri=DEFAULT_.top_center_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.top_center_intensity_ratio = Slot(uri=DEFAULT_.top_center_intensity_ratio, name="top_center_intensity_ratio", curie=DEFAULT_.curie('top_center_intensity_ratio'),
                   model_uri=DEFAULT_.top_center_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.top_right_intensity_mean = Slot(uri=DEFAULT_.top_right_intensity_mean, name="top_right_intensity_mean", curie=DEFAULT_.curie('top_right_intensity_mean'),
                   model_uri=DEFAULT_.top_right_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.top_right_intensity_ratio = Slot(uri=DEFAULT_.top_right_intensity_ratio, name="top_right_intensity_ratio", curie=DEFAULT_.curie('top_right_intensity_ratio'),
                   model_uri=DEFAULT_.top_right_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_left_intensity_mean = Slot(uri=DEFAULT_.middle_left_intensity_mean, name="middle_left_intensity_mean", curie=DEFAULT_.curie('middle_left_intensity_mean'),
                   model_uri=DEFAULT_.middle_left_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_left_intensity_ratio = Slot(uri=DEFAULT_.middle_left_intensity_ratio, name="middle_left_intensity_ratio", curie=DEFAULT_.curie('middle_left_intensity_ratio'),
                   model_uri=DEFAULT_.middle_left_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_center_intensity_mean = Slot(uri=DEFAULT_.middle_center_intensity_mean, name="middle_center_intensity_mean", curie=DEFAULT_.curie('middle_center_intensity_mean'),
                   model_uri=DEFAULT_.middle_center_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_center_intensity_ratio = Slot(uri=DEFAULT_.middle_center_intensity_ratio, name="middle_center_intensity_ratio", curie=DEFAULT_.curie('middle_center_intensity_ratio'),
                   model_uri=DEFAULT_.middle_center_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_right_intensity_mean = Slot(uri=DEFAULT_.middle_right_intensity_mean, name="middle_right_intensity_mean", curie=DEFAULT_.curie('middle_right_intensity_mean'),
                   model_uri=DEFAULT_.middle_right_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.middle_right_intensity_ratio = Slot(uri=DEFAULT_.middle_right_intensity_ratio, name="middle_right_intensity_ratio", curie=DEFAULT_.curie('middle_right_intensity_ratio'),
                   model_uri=DEFAULT_.middle_right_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_left_intensity_mean = Slot(uri=DEFAULT_.bottom_left_intensity_mean, name="bottom_left_intensity_mean", curie=DEFAULT_.curie('bottom_left_intensity_mean'),
                   model_uri=DEFAULT_.bottom_left_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_left_intensity_ratio = Slot(uri=DEFAULT_.bottom_left_intensity_ratio, name="bottom_left_intensity_ratio", curie=DEFAULT_.curie('bottom_left_intensity_ratio'),
                   model_uri=DEFAULT_.bottom_left_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_center_intensity_mean = Slot(uri=DEFAULT_.bottom_center_intensity_mean, name="bottom_center_intensity_mean", curie=DEFAULT_.curie('bottom_center_intensity_mean'),
                   model_uri=DEFAULT_.bottom_center_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_center_intensity_ratio = Slot(uri=DEFAULT_.bottom_center_intensity_ratio, name="bottom_center_intensity_ratio", curie=DEFAULT_.curie('bottom_center_intensity_ratio'),
                   model_uri=DEFAULT_.bottom_center_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_right_intensity_mean = Slot(uri=DEFAULT_.bottom_right_intensity_mean, name="bottom_right_intensity_mean", curie=DEFAULT_.curie('bottom_right_intensity_mean'),
                   model_uri=DEFAULT_.bottom_right_intensity_mean, domain=None, range=Optional[Union[float, List[float]]])

slots.bottom_right_intensity_ratio = Slot(uri=DEFAULT_.bottom_right_intensity_ratio, name="bottom_right_intensity_ratio", curie=DEFAULT_.curie('bottom_right_intensity_ratio'),
                   model_uri=DEFAULT_.bottom_right_intensity_ratio, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_0 = Slot(uri=DEFAULT_.decile_0, name="decile_0", curie=DEFAULT_.curie('decile_0'),
                   model_uri=DEFAULT_.decile_0, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_1 = Slot(uri=DEFAULT_.decile_1, name="decile_1", curie=DEFAULT_.curie('decile_1'),
                   model_uri=DEFAULT_.decile_1, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_2 = Slot(uri=DEFAULT_.decile_2, name="decile_2", curie=DEFAULT_.curie('decile_2'),
                   model_uri=DEFAULT_.decile_2, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_3 = Slot(uri=DEFAULT_.decile_3, name="decile_3", curie=DEFAULT_.curie('decile_3'),
                   model_uri=DEFAULT_.decile_3, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_4 = Slot(uri=DEFAULT_.decile_4, name="decile_4", curie=DEFAULT_.curie('decile_4'),
                   model_uri=DEFAULT_.decile_4, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_5 = Slot(uri=DEFAULT_.decile_5, name="decile_5", curie=DEFAULT_.curie('decile_5'),
                   model_uri=DEFAULT_.decile_5, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_6 = Slot(uri=DEFAULT_.decile_6, name="decile_6", curie=DEFAULT_.curie('decile_6'),
                   model_uri=DEFAULT_.decile_6, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_7 = Slot(uri=DEFAULT_.decile_7, name="decile_7", curie=DEFAULT_.curie('decile_7'),
                   model_uri=DEFAULT_.decile_7, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_8 = Slot(uri=DEFAULT_.decile_8, name="decile_8", curie=DEFAULT_.curie('decile_8'),
                   model_uri=DEFAULT_.decile_8, domain=None, range=Optional[Union[float, List[float]]])

slots.decile_9 = Slot(uri=DEFAULT_.decile_9, name="decile_9", curie=DEFAULT_.curie('decile_9'),
                   model_uri=DEFAULT_.decile_9, domain=None, range=Optional[Union[float, List[float]]])

slots.fieldIlluminationDataset__input = Slot(uri=DEFAULT_.input, name="fieldIlluminationDataset__input", curie=DEFAULT_.curie('input'),
                   model_uri=DEFAULT_.fieldIlluminationDataset__input, domain=None, range=Union[dict, FieldIlluminationInput])

slots.fieldIlluminationDataset__output = Slot(uri=DEFAULT_.output, name="fieldIlluminationDataset__output", curie=DEFAULT_.curie('output'),
                   model_uri=DEFAULT_.fieldIlluminationDataset__output, domain=None, range=Optional[Union[dict, FieldIlluminationOutput]])

slots.fieldIlluminationOutput__key_values = Slot(uri=DEFAULT_.key_values, name="fieldIlluminationOutput__key_values", curie=DEFAULT_.curie('key_values'),
                   model_uri=DEFAULT_.fieldIlluminationOutput__key_values, domain=None, range=Optional[Union[dict, FieldIlluminationKeyValues]])

slots.fieldIlluminationOutput__intensity_profiles = Slot(uri=DEFAULT_.intensity_profiles, name="fieldIlluminationOutput__intensity_profiles", curie=DEFAULT_.curie('intensity_profiles'),
                   model_uri=DEFAULT_.fieldIlluminationOutput__intensity_profiles, domain=None, range=Optional[Union[dict, TableAsDict]])

slots.fieldIlluminationOutput__intensity_map = Slot(uri=DEFAULT_.intensity_map, name="fieldIlluminationOutput__intensity_map", curie=DEFAULT_.curie('intensity_map'),
                   model_uri=DEFAULT_.fieldIlluminationOutput__intensity_map, domain=None, range=Optional[Union[str, Image5DImageUrl]])

slots.fieldIlluminationOutput__profile_rois = Slot(uri=DEFAULT_.profile_rois, name="fieldIlluminationOutput__profile_rois", curie=DEFAULT_.curie('profile_rois'),
                   model_uri=DEFAULT_.fieldIlluminationOutput__profile_rois, domain=None, range=Optional[Union[dict, ROI]])
