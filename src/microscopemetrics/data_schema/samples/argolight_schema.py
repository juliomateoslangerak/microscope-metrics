# Auto generated from argolight_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-11T18:00:43
# Schema: microscopemetrics_samples_argolight_schema
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
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
    ExperimenterOrcid,
    ImageAsNumpy,
    KeyValues,
    KeyValuesKeys,
    MetricsDataset,
    SampleType,
    TableAsPandasDF,
)

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = CurieNamespace(
    "",
    "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/",
)


# Types

# Class references


@dataclass
class ArgolightBDataset(MetricsDataset):
    """
    An Argolight sample pattern B dataset
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBDataset"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightBDataset"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBDataset"
    )

    argolight_b_image: Union[dict, ImageAsNumpy] = None
    spots_distance: float = None
    processed: Union[bool, Bool] = False
    saturation_threshold: float = 0.01
    sigma_z: float = 1.0
    sigma_y: float = 3.0
    sigma_x: float = 3.0
    bit_depth: Optional[int] = None
    lower_threshold_correction_factors: Optional[Union[float, List[float]]] = empty_list()
    upper_threshold_correction_factors: Optional[Union[float, List[float]]] = empty_list()
    remove_center_cross: Optional[Union[bool, Bool]] = False
    spots_labels_image: Optional[Union[dict, ImageAsNumpy]] = None
    spots_centroids: Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]] = empty_list()
    intensity_measurements: Optional[Union[dict, KeyValues]] = None
    distance_measurements: Optional[Union[str, KeyValuesKeys]] = None
    spots_properties: Optional[Union[dict, TableAsPandasDF]] = None
    spots_distances: Optional[Union[dict, TableAsPandasDF]] = None
    name: Optional[str] = "ArgolightBDataset"
    description: Optional[str] = "This dataset contains the results of the Argolight B analysis"
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.argolight_b_image):
            self.MissingRequiredField("argolight_b_image")
        if not isinstance(self.argolight_b_image, ImageAsNumpy):
            self.argolight_b_image = ImageAsNumpy(**as_dict(self.argolight_b_image))

        if self._is_empty(self.saturation_threshold):
            self.MissingRequiredField("saturation_threshold")
        if not isinstance(self.saturation_threshold, float):
            self.saturation_threshold = float(self.saturation_threshold)

        if self._is_empty(self.spots_distance):
            self.MissingRequiredField("spots_distance")
        if not isinstance(self.spots_distance, float):
            self.spots_distance = float(self.spots_distance)

        if self._is_empty(self.sigma_z):
            self.MissingRequiredField("sigma_z")
        if not isinstance(self.sigma_z, float):
            self.sigma_z = float(self.sigma_z)

        if self._is_empty(self.sigma_y):
            self.MissingRequiredField("sigma_y")
        if not isinstance(self.sigma_y, float):
            self.sigma_y = float(self.sigma_y)

        if self._is_empty(self.sigma_x):
            self.MissingRequiredField("sigma_x")
        if not isinstance(self.sigma_x, float):
            self.sigma_x = float(self.sigma_x)

        if self.bit_depth is not None and not isinstance(self.bit_depth, int):
            self.bit_depth = int(self.bit_depth)

        if not isinstance(self.lower_threshold_correction_factors, list):
            self.lower_threshold_correction_factors = (
                [self.lower_threshold_correction_factors]
                if self.lower_threshold_correction_factors is not None
                else []
            )
        self.lower_threshold_correction_factors = [
            v if isinstance(v, float) else float(v) for v in self.lower_threshold_correction_factors
        ]

        if not isinstance(self.upper_threshold_correction_factors, list):
            self.upper_threshold_correction_factors = (
                [self.upper_threshold_correction_factors]
                if self.upper_threshold_correction_factors is not None
                else []
            )
        self.upper_threshold_correction_factors = [
            v if isinstance(v, float) else float(v) for v in self.upper_threshold_correction_factors
        ]

        if self.remove_center_cross is not None and not isinstance(self.remove_center_cross, Bool):
            self.remove_center_cross = Bool(self.remove_center_cross)

        if self.spots_labels_image is not None and not isinstance(
            self.spots_labels_image, ImageAsNumpy
        ):
            self.spots_labels_image = ImageAsNumpy(**as_dict(self.spots_labels_image))

        self._normalize_inlined_as_dict(
            slot_name="spots_centroids", slot_type=ROI, key_name="image", keyed=False
        )

        if self.intensity_measurements is not None and not isinstance(
            self.intensity_measurements, KeyValues
        ):
            self.intensity_measurements = KeyValues(**as_dict(self.intensity_measurements))

        if self.distance_measurements is not None and not isinstance(
            self.distance_measurements, KeyValuesKeys
        ):
            self.distance_measurements = KeyValuesKeys(self.distance_measurements)

        if self.spots_properties is not None and not isinstance(
            self.spots_properties, TableAsPandasDF
        ):
            self.spots_properties = TableAsPandasDF(**as_dict(self.spots_properties))

        if self.spots_distances is not None and not isinstance(
            self.spots_distances, TableAsPandasDF
        ):
            self.spots_distances = TableAsPandasDF(**as_dict(self.spots_distances))

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.inputs, list):
            self.inputs = [self.inputs] if self.inputs is not None else []
        self.inputs = [v if isinstance(v, str) else str(v) for v in self.inputs]

        if not isinstance(self.outputs, list):
            self.outputs = [self.outputs] if self.outputs is not None else []
        self.outputs = [v if isinstance(v, str) else str(v) for v in self.outputs]

        super().__post_init__(**kwargs)


@dataclass
class ArgolightEDataset(MetricsDataset):
    """
    An Argolight sample pattern E dataset.
    It contains resolution data on the axis indicated:
    - axis 1 = Y resolution = lines along X axis
    - axis 2 = X resolution = lines along Y axis
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEDataset"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightEDataset"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEDataset"
    )

    argolight_e_image: Union[dict, ImageAsNumpy] = None
    axis: int = None
    processed: Union[bool, Bool] = False
    saturation_threshold: float = 0.01
    bit_depth: Optional[int] = None
    measured_band: Optional[float] = 0.4
    peaks_rois: Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]] = empty_list()
    key_measurements: Optional[Union[str, KeyValuesKeys]] = None
    intensity_profiles: Optional[Union[dict, TableAsPandasDF]] = None
    name: Optional[str] = "ArgolightEDataset"
    description: Optional[str] = "This dataset contains the results of the Argolight E analysis"
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.argolight_e_image):
            self.MissingRequiredField("argolight_e_image")
        if not isinstance(self.argolight_e_image, ImageAsNumpy):
            self.argolight_e_image = ImageAsNumpy(**as_dict(self.argolight_e_image))

        if self._is_empty(self.saturation_threshold):
            self.MissingRequiredField("saturation_threshold")
        if not isinstance(self.saturation_threshold, float):
            self.saturation_threshold = float(self.saturation_threshold)

        if self._is_empty(self.axis):
            self.MissingRequiredField("axis")
        if not isinstance(self.axis, int):
            self.axis = int(self.axis)

        if self.bit_depth is not None and not isinstance(self.bit_depth, int):
            self.bit_depth = int(self.bit_depth)

        if self.measured_band is not None and not isinstance(self.measured_band, float):
            self.measured_band = float(self.measured_band)

        self._normalize_inlined_as_dict(
            slot_name="peaks_rois", slot_type=ROI, key_name="image", keyed=False
        )

        if self.key_measurements is not None and not isinstance(
            self.key_measurements, KeyValuesKeys
        ):
            self.key_measurements = KeyValuesKeys(self.key_measurements)

        if self.intensity_profiles is not None and not isinstance(
            self.intensity_profiles, TableAsPandasDF
        ):
            self.intensity_profiles = TableAsPandasDF(**as_dict(self.intensity_profiles))

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.inputs, list):
            self.inputs = [self.inputs] if self.inputs is not None else []
        self.inputs = [v if isinstance(v, str) else str(v) for v in self.inputs]

        if not isinstance(self.outputs, list):
            self.outputs = [self.outputs] if self.outputs is not None else []
        self.outputs = [v if isinstance(v, str) else str(v) for v in self.outputs]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.bit_depth = Slot(
    uri=DEFAULT_.bit_depth,
    name="bit_depth",
    curie=DEFAULT_.curie("bit_depth"),
    model_uri=DEFAULT_.bit_depth,
    domain=None,
    range=Optional[int],
)

slots.saturation_threshold = Slot(
    uri=DEFAULT_.saturation_threshold,
    name="saturation_threshold",
    curie=DEFAULT_.curie("saturation_threshold"),
    model_uri=DEFAULT_.saturation_threshold,
    domain=None,
    range=float,
)

slots.argolight_b_image = Slot(
    uri=DEFAULT_.argolight_b_image,
    name="argolight_b_image",
    curie=DEFAULT_.curie("argolight_b_image"),
    model_uri=DEFAULT_.argolight_b_image,
    domain=None,
    range=Union[dict, ImageAsNumpy],
)

slots.spots_distance = Slot(
    uri=DEFAULT_.spots_distance,
    name="spots_distance",
    curie=DEFAULT_.curie("spots_distance"),
    model_uri=DEFAULT_.spots_distance,
    domain=None,
    range=float,
)

slots.sigma_z = Slot(
    uri=DEFAULT_.sigma_z,
    name="sigma_z",
    curie=DEFAULT_.curie("sigma_z"),
    model_uri=DEFAULT_.sigma_z,
    domain=None,
    range=float,
)

slots.sigma_y = Slot(
    uri=DEFAULT_.sigma_y,
    name="sigma_y",
    curie=DEFAULT_.curie("sigma_y"),
    model_uri=DEFAULT_.sigma_y,
    domain=None,
    range=float,
)

slots.sigma_x = Slot(
    uri=DEFAULT_.sigma_x,
    name="sigma_x",
    curie=DEFAULT_.curie("sigma_x"),
    model_uri=DEFAULT_.sigma_x,
    domain=None,
    range=float,
)

slots.lower_threshold_correction_factors = Slot(
    uri=DEFAULT_.lower_threshold_correction_factors,
    name="lower_threshold_correction_factors",
    curie=DEFAULT_.curie("lower_threshold_correction_factors"),
    model_uri=DEFAULT_.lower_threshold_correction_factors,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.upper_threshold_correction_factors = Slot(
    uri=DEFAULT_.upper_threshold_correction_factors,
    name="upper_threshold_correction_factors",
    curie=DEFAULT_.curie("upper_threshold_correction_factors"),
    model_uri=DEFAULT_.upper_threshold_correction_factors,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.remove_center_cross = Slot(
    uri=DEFAULT_.remove_center_cross,
    name="remove_center_cross",
    curie=DEFAULT_.curie("remove_center_cross"),
    model_uri=DEFAULT_.remove_center_cross,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.spots_labels_image = Slot(
    uri=DEFAULT_.spots_labels_image,
    name="spots_labels_image",
    curie=DEFAULT_.curie("spots_labels_image"),
    model_uri=DEFAULT_.spots_labels_image,
    domain=None,
    range=Optional[Union[dict, ImageAsNumpy]],
)

slots.spots_centroids = Slot(
    uri=DEFAULT_.spots_centroids,
    name="spots_centroids",
    curie=DEFAULT_.curie("spots_centroids"),
    model_uri=DEFAULT_.spots_centroids,
    domain=None,
    range=Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]],
)

slots.intensity_measurements = Slot(
    uri=DEFAULT_.intensity_measurements,
    name="intensity_measurements",
    curie=DEFAULT_.curie("intensity_measurements"),
    model_uri=DEFAULT_.intensity_measurements,
    domain=None,
    range=Optional[Union[dict, KeyValues]],
)

slots.distance_measurements = Slot(
    uri=DEFAULT_.distance_measurements,
    name="distance_measurements",
    curie=DEFAULT_.curie("distance_measurements"),
    model_uri=DEFAULT_.distance_measurements,
    domain=None,
    range=Optional[Union[str, KeyValuesKeys]],
)

slots.spots_properties = Slot(
    uri=DEFAULT_.spots_properties,
    name="spots_properties",
    curie=DEFAULT_.curie("spots_properties"),
    model_uri=DEFAULT_.spots_properties,
    domain=None,
    range=Optional[Union[dict, TableAsPandasDF]],
)

slots.spots_distances = Slot(
    uri=DEFAULT_.spots_distances,
    name="spots_distances",
    curie=DEFAULT_.curie("spots_distances"),
    model_uri=DEFAULT_.spots_distances,
    domain=None,
    range=Optional[Union[dict, TableAsPandasDF]],
)

slots.argolight_e_image = Slot(
    uri=DEFAULT_.argolight_e_image,
    name="argolight_e_image",
    curie=DEFAULT_.curie("argolight_e_image"),
    model_uri=DEFAULT_.argolight_e_image,
    domain=None,
    range=Union[dict, ImageAsNumpy],
)

slots.axis = Slot(
    uri=DEFAULT_.axis,
    name="axis",
    curie=DEFAULT_.curie("axis"),
    model_uri=DEFAULT_.axis,
    domain=None,
    range=int,
)

slots.measured_band = Slot(
    uri=DEFAULT_.measured_band,
    name="measured_band",
    curie=DEFAULT_.curie("measured_band"),
    model_uri=DEFAULT_.measured_band,
    domain=None,
    range=Optional[float],
)

slots.peaks_rois = Slot(
    uri=DEFAULT_.peaks_rois,
    name="peaks_rois",
    curie=DEFAULT_.curie("peaks_rois"),
    model_uri=DEFAULT_.peaks_rois,
    domain=None,
    range=Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]],
)

slots.key_measurements = Slot(
    uri=DEFAULT_.key_measurements,
    name="key_measurements",
    curie=DEFAULT_.curie("key_measurements"),
    model_uri=DEFAULT_.key_measurements,
    domain=None,
    range=Optional[Union[str, KeyValuesKeys]],
)

slots.intensity_profiles = Slot(
    uri=DEFAULT_.intensity_profiles,
    name="intensity_profiles",
    curie=DEFAULT_.curie("intensity_profiles"),
    model_uri=DEFAULT_.intensity_profiles,
    domain=None,
    range=Optional[Union[dict, TableAsPandasDF]],
)

slots.ArgolightBDataset_inputs = Slot(
    uri=DEFAULT_.inputs,
    name="ArgolightBDataset_inputs",
    curie=DEFAULT_.curie("inputs"),
    model_uri=DEFAULT_.ArgolightBDataset_inputs,
    domain=ArgolightBDataset,
    range=Optional[Union[str, List[str]]],
)

slots.ArgolightBDataset_outputs = Slot(
    uri=DEFAULT_.outputs,
    name="ArgolightBDataset_outputs",
    curie=DEFAULT_.curie("outputs"),
    model_uri=DEFAULT_.ArgolightBDataset_outputs,
    domain=ArgolightBDataset,
    range=Optional[Union[str, List[str]]],
)

slots.ArgolightEDataset_inputs = Slot(
    uri=DEFAULT_.inputs,
    name="ArgolightEDataset_inputs",
    curie=DEFAULT_.curie("inputs"),
    model_uri=DEFAULT_.ArgolightEDataset_inputs,
    domain=ArgolightEDataset,
    range=Optional[Union[str, List[str]]],
)

slots.ArgolightEDataset_outputs = Slot(
    uri=DEFAULT_.outputs,
    name="ArgolightEDataset_outputs",
    curie=DEFAULT_.curie("outputs"),
    model_uri=DEFAULT_.ArgolightEDataset_outputs,
    domain=ArgolightEDataset,
    range=Optional[Union[str, List[str]]],
)
