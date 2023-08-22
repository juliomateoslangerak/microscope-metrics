# Auto generated from argolight_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-22T14:55:22
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

    input: Union[dict, "ArgolightBInput"] = None
    processed: Union[bool, Bool] = False
    output: Optional[Union[dict, "ArgolightBOutput"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.input):
            self.MissingRequiredField("input")
        if not isinstance(self.input, ArgolightBInput):
            self.input = ArgolightBInput(**as_dict(self.input))

        if self.output is not None and not isinstance(self.output, ArgolightBOutput):
            self.output = ArgolightBOutput(**as_dict(self.output))

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

    input: Union[dict, "ArgolightEInput"] = None
    processed: Union[bool, Bool] = False
    output: Optional[Union[dict, "ArgolightEOutput"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.input):
            self.MissingRequiredField("input")
        if not isinstance(self.input, ArgolightEInput):
            self.input = ArgolightEInput(**as_dict(self.input))

        if self.output is not None and not isinstance(self.output, ArgolightEOutput):
            self.output = ArgolightEOutput(**as_dict(self.output))

        super().__post_init__(**kwargs)


@dataclass
class ArgolightBInput(MetricsInput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBInput"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightBInput"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBInput"
    )

    argolight_b_image: Union[dict, ImageAsNumpy] = None
    spots_distance: float = None
    saturation_threshold: float = 0.01
    sigma_z: float = 1.0
    sigma_y: float = 3.0
    sigma_x: float = 3.0
    bit_depth: Optional[int] = None
    lower_threshold_correction_factors: Optional[Union[float, List[float]]] = empty_list()
    upper_threshold_correction_factors: Optional[Union[float, List[float]]] = empty_list()
    remove_center_cross: Optional[Union[bool, Bool]] = False

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

        super().__post_init__(**kwargs)


@dataclass
class ArgolightEInput(MetricsInput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEInput"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightEInput"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEInput"
    )

    argolight_e_image: Union[dict, ImageAsNumpy] = None
    axis: int = None
    saturation_threshold: float = 0.01
    measured_band: float = 0.4
    prominence_threshold: float = 0.264
    bit_depth: Optional[int] = None

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

        if self._is_empty(self.measured_band):
            self.MissingRequiredField("measured_band")
        if not isinstance(self.measured_band, float):
            self.measured_band = float(self.measured_band)

        if self._is_empty(self.prominence_threshold):
            self.MissingRequiredField("prominence_threshold")
        if not isinstance(self.prominence_threshold, float):
            self.prominence_threshold = float(self.prominence_threshold)

        if self.bit_depth is not None and not isinstance(self.bit_depth, int):
            self.bit_depth = int(self.bit_depth)

        super().__post_init__(**kwargs)


@dataclass
class ArgolightBOutput(MetricsOutput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBOutput"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightBOutput"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBOutput"
    )

    spots_labels_image: Optional[Union[str, ImageAsNumpyImageUrl]] = None
    spots_centroids: Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]] = empty_list()
    intensity_measurements: Optional[Union[dict, "ArgolightBIntensityKeyValues"]] = None
    distance_measurements: Optional[Union[dict, "ArgolightBDistanceKeyValues"]] = None
    spots_properties: Optional[Union[dict, TableAsDict]] = None
    spots_distances: Optional[Union[dict, TableAsDict]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.spots_labels_image is not None and not isinstance(
            self.spots_labels_image, ImageAsNumpyImageUrl
        ):
            self.spots_labels_image = ImageAsNumpyImageUrl(self.spots_labels_image)

        if not isinstance(self.spots_centroids, list):
            self.spots_centroids = (
                [self.spots_centroids] if self.spots_centroids is not None else []
            )
        self.spots_centroids = [
            v if isinstance(v, ROI) else ROI(**as_dict(v)) for v in self.spots_centroids
        ]

        if self.intensity_measurements is not None and not isinstance(
            self.intensity_measurements, ArgolightBIntensityKeyValues
        ):
            self.intensity_measurements = ArgolightBIntensityKeyValues(
                **as_dict(self.intensity_measurements)
            )

        if self.distance_measurements is not None and not isinstance(
            self.distance_measurements, ArgolightBDistanceKeyValues
        ):
            self.distance_measurements = ArgolightBDistanceKeyValues(
                **as_dict(self.distance_measurements)
            )

        if self.spots_properties is not None and not isinstance(self.spots_properties, TableAsDict):
            self.spots_properties = TableAsDict(**as_dict(self.spots_properties))

        if self.spots_distances is not None and not isinstance(self.spots_distances, TableAsDict):
            self.spots_distances = TableAsDict(**as_dict(self.spots_distances))

        super().__post_init__(**kwargs)


@dataclass
class ArgolightEOutput(MetricsOutput):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEOutput"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightEOutput"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEOutput"
    )

    peaks_rois: Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]] = empty_list()
    key_measurements: Optional[Union[dict, "ArgolightEKeyValues"]] = None
    intensity_profiles: Optional[Union[dict, TableAsDict]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.peaks_rois, list):
            self.peaks_rois = [self.peaks_rois] if self.peaks_rois is not None else []
        self.peaks_rois = [v if isinstance(v, ROI) else ROI(**as_dict(v)) for v in self.peaks_rois]

        if self.key_measurements is not None and not isinstance(
            self.key_measurements, ArgolightEKeyValues
        ):
            self.key_measurements = ArgolightEKeyValues(**as_dict(self.key_measurements))

        if self.intensity_profiles is not None and not isinstance(
            self.intensity_profiles, TableAsDict
        ):
            self.intensity_profiles = TableAsDict(**as_dict(self.intensity_profiles))

        super().__post_init__(**kwargs)


@dataclass
class ArgolightBIntensityKeyValues(KeyValues):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBIntensityKeyValues"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightBIntensityKeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBIntensityKeyValues"
    )

    channel: Optional[Union[int, List[int]]] = empty_list()
    nr_of_spots: Optional[Union[int, List[int]]] = empty_list()
    max_intensity: Optional[Union[float, List[float]]] = empty_list()
    max_intensity_roi: Optional[Union[int, List[int]]] = empty_list()
    min_intensity: Optional[Union[float, List[float]]] = empty_list()
    min_intensity_roi: Optional[Union[int, List[int]]] = empty_list()
    mean_intensity: Optional[Union[float, List[float]]] = empty_list()
    median_intensity: Optional[Union[float, List[float]]] = empty_list()
    std_mean_intensity: Optional[Union[float, List[float]]] = empty_list()
    mad_mean_intensity: Optional[Union[float, List[float]]] = empty_list()
    min_max_intensity_ratio: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.channel, list):
            self.channel = [self.channel] if self.channel is not None else []
        self.channel = [v if isinstance(v, int) else int(v) for v in self.channel]

        if not isinstance(self.nr_of_spots, list):
            self.nr_of_spots = [self.nr_of_spots] if self.nr_of_spots is not None else []
        self.nr_of_spots = [v if isinstance(v, int) else int(v) for v in self.nr_of_spots]

        if not isinstance(self.max_intensity, list):
            self.max_intensity = [self.max_intensity] if self.max_intensity is not None else []
        self.max_intensity = [v if isinstance(v, float) else float(v) for v in self.max_intensity]

        if not isinstance(self.max_intensity_roi, list):
            self.max_intensity_roi = (
                [self.max_intensity_roi] if self.max_intensity_roi is not None else []
            )
        self.max_intensity_roi = [
            v if isinstance(v, int) else int(v) for v in self.max_intensity_roi
        ]

        if not isinstance(self.min_intensity, list):
            self.min_intensity = [self.min_intensity] if self.min_intensity is not None else []
        self.min_intensity = [v if isinstance(v, float) else float(v) for v in self.min_intensity]

        if not isinstance(self.min_intensity_roi, list):
            self.min_intensity_roi = (
                [self.min_intensity_roi] if self.min_intensity_roi is not None else []
            )
        self.min_intensity_roi = [
            v if isinstance(v, int) else int(v) for v in self.min_intensity_roi
        ]

        if not isinstance(self.mean_intensity, list):
            self.mean_intensity = [self.mean_intensity] if self.mean_intensity is not None else []
        self.mean_intensity = [v if isinstance(v, float) else float(v) for v in self.mean_intensity]

        if not isinstance(self.median_intensity, list):
            self.median_intensity = (
                [self.median_intensity] if self.median_intensity is not None else []
            )
        self.median_intensity = [
            v if isinstance(v, float) else float(v) for v in self.median_intensity
        ]

        if not isinstance(self.std_mean_intensity, list):
            self.std_mean_intensity = (
                [self.std_mean_intensity] if self.std_mean_intensity is not None else []
            )
        self.std_mean_intensity = [
            v if isinstance(v, float) else float(v) for v in self.std_mean_intensity
        ]

        if not isinstance(self.mad_mean_intensity, list):
            self.mad_mean_intensity = (
                [self.mad_mean_intensity] if self.mad_mean_intensity is not None else []
            )
        self.mad_mean_intensity = [
            v if isinstance(v, float) else float(v) for v in self.mad_mean_intensity
        ]

        if not isinstance(self.min_max_intensity_ratio, list):
            self.min_max_intensity_ratio = (
                [self.min_max_intensity_ratio] if self.min_max_intensity_ratio is not None else []
            )
        self.min_max_intensity_ratio = [
            v if isinstance(v, float) else float(v) for v in self.min_max_intensity_ratio
        ]

        super().__post_init__(**kwargs)


@dataclass
class ArgolightBDistanceKeyValues(KeyValues):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBDistanceKeyValues"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightBDistanceKeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightBDistanceKeyValues"
    )

    channel_A: Optional[Union[int, List[int]]] = empty_list()
    channel_B: Optional[Union[int, List[int]]] = empty_list()
    mean_3d_dist: Optional[Union[float, List[float]]] = empty_list()
    median_3d_dist: Optional[Union[float, List[float]]] = empty_list()
    std_3d_dist: Optional[Union[float, List[float]]] = empty_list()
    mad_3d_dist: Optional[Union[float, List[float]]] = empty_list()
    mean_z_dist: Optional[Union[float, List[float]]] = empty_list()
    median_z_dist: Optional[Union[float, List[float]]] = empty_list()
    std_z_dist: Optional[Union[float, List[float]]] = empty_list()
    mad_z_dist: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.channel_A, list):
            self.channel_A = [self.channel_A] if self.channel_A is not None else []
        self.channel_A = [v if isinstance(v, int) else int(v) for v in self.channel_A]

        if not isinstance(self.channel_B, list):
            self.channel_B = [self.channel_B] if self.channel_B is not None else []
        self.channel_B = [v if isinstance(v, int) else int(v) for v in self.channel_B]

        if not isinstance(self.mean_3d_dist, list):
            self.mean_3d_dist = [self.mean_3d_dist] if self.mean_3d_dist is not None else []
        self.mean_3d_dist = [v if isinstance(v, float) else float(v) for v in self.mean_3d_dist]

        if not isinstance(self.median_3d_dist, list):
            self.median_3d_dist = [self.median_3d_dist] if self.median_3d_dist is not None else []
        self.median_3d_dist = [v if isinstance(v, float) else float(v) for v in self.median_3d_dist]

        if not isinstance(self.std_3d_dist, list):
            self.std_3d_dist = [self.std_3d_dist] if self.std_3d_dist is not None else []
        self.std_3d_dist = [v if isinstance(v, float) else float(v) for v in self.std_3d_dist]

        if not isinstance(self.mad_3d_dist, list):
            self.mad_3d_dist = [self.mad_3d_dist] if self.mad_3d_dist is not None else []
        self.mad_3d_dist = [v if isinstance(v, float) else float(v) for v in self.mad_3d_dist]

        if not isinstance(self.mean_z_dist, list):
            self.mean_z_dist = [self.mean_z_dist] if self.mean_z_dist is not None else []
        self.mean_z_dist = [v if isinstance(v, float) else float(v) for v in self.mean_z_dist]

        if not isinstance(self.median_z_dist, list):
            self.median_z_dist = [self.median_z_dist] if self.median_z_dist is not None else []
        self.median_z_dist = [v if isinstance(v, float) else float(v) for v in self.median_z_dist]

        if not isinstance(self.std_z_dist, list):
            self.std_z_dist = [self.std_z_dist] if self.std_z_dist is not None else []
        self.std_z_dist = [v if isinstance(v, float) else float(v) for v in self.std_z_dist]

        if not isinstance(self.mad_z_dist, list):
            self.mad_z_dist = [self.mad_z_dist] if self.mad_z_dist is not None else []
        self.mad_z_dist = [v if isinstance(v, float) else float(v) for v in self.mad_z_dist]

        super().__post_init__(**kwargs)


@dataclass
class ArgolightEKeyValues(KeyValues):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEKeyValues"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ArgolightEKeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/ArgolightEKeyValues"
    )

    channel: Optional[Union[int, List[int]]] = empty_list()
    focus_slice: Optional[Union[int, List[int]]] = empty_list()
    rayleigh_resolution: Optional[Union[float, List[float]]] = empty_list()
    peak_position_A: Optional[Union[float, List[float]]] = empty_list()
    peak_position_B: Optional[Union[float, List[float]]] = empty_list()
    peak_height_A: Optional[Union[float, List[float]]] = empty_list()
    peak_height_B: Optional[Union[float, List[float]]] = empty_list()
    peak_prominence_A: Optional[Union[float, List[float]]] = empty_list()
    peak_prominence_B: Optional[Union[float, List[float]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.channel, list):
            self.channel = [self.channel] if self.channel is not None else []
        self.channel = [v if isinstance(v, int) else int(v) for v in self.channel]

        if not isinstance(self.focus_slice, list):
            self.focus_slice = [self.focus_slice] if self.focus_slice is not None else []
        self.focus_slice = [v if isinstance(v, int) else int(v) for v in self.focus_slice]

        if not isinstance(self.rayleigh_resolution, list):
            self.rayleigh_resolution = (
                [self.rayleigh_resolution] if self.rayleigh_resolution is not None else []
            )
        self.rayleigh_resolution = [
            v if isinstance(v, float) else float(v) for v in self.rayleigh_resolution
        ]

        if not isinstance(self.peak_position_A, list):
            self.peak_position_A = (
                [self.peak_position_A] if self.peak_position_A is not None else []
            )
        self.peak_position_A = [
            v if isinstance(v, float) else float(v) for v in self.peak_position_A
        ]

        if not isinstance(self.peak_position_B, list):
            self.peak_position_B = (
                [self.peak_position_B] if self.peak_position_B is not None else []
            )
        self.peak_position_B = [
            v if isinstance(v, float) else float(v) for v in self.peak_position_B
        ]

        if not isinstance(self.peak_height_A, list):
            self.peak_height_A = [self.peak_height_A] if self.peak_height_A is not None else []
        self.peak_height_A = [v if isinstance(v, float) else float(v) for v in self.peak_height_A]

        if not isinstance(self.peak_height_B, list):
            self.peak_height_B = [self.peak_height_B] if self.peak_height_B is not None else []
        self.peak_height_B = [v if isinstance(v, float) else float(v) for v in self.peak_height_B]

        if not isinstance(self.peak_prominence_A, list):
            self.peak_prominence_A = (
                [self.peak_prominence_A] if self.peak_prominence_A is not None else []
            )
        self.peak_prominence_A = [
            v if isinstance(v, float) else float(v) for v in self.peak_prominence_A
        ]

        if not isinstance(self.peak_prominence_B, list):
            self.peak_prominence_B = (
                [self.peak_prominence_B] if self.peak_prominence_B is not None else []
            )
        self.peak_prominence_B = [
            v if isinstance(v, float) else float(v) for v in self.peak_prominence_B
        ]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.channel = Slot(
    uri=DEFAULT_.channel,
    name="channel",
    curie=DEFAULT_.curie("channel"),
    model_uri=DEFAULT_.channel,
    domain=None,
    range=Optional[Union[int, List[int]]],
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

slots.nr_of_spots = Slot(
    uri=DEFAULT_.nr_of_spots,
    name="nr_of_spots",
    curie=DEFAULT_.curie("nr_of_spots"),
    model_uri=DEFAULT_.nr_of_spots,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.max_intensity = Slot(
    uri=DEFAULT_.max_intensity,
    name="max_intensity",
    curie=DEFAULT_.curie("max_intensity"),
    model_uri=DEFAULT_.max_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.max_intensity_roi = Slot(
    uri=DEFAULT_.max_intensity_roi,
    name="max_intensity_roi",
    curie=DEFAULT_.curie("max_intensity_roi"),
    model_uri=DEFAULT_.max_intensity_roi,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.min_intensity = Slot(
    uri=DEFAULT_.min_intensity,
    name="min_intensity",
    curie=DEFAULT_.curie("min_intensity"),
    model_uri=DEFAULT_.min_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.min_intensity_roi = Slot(
    uri=DEFAULT_.min_intensity_roi,
    name="min_intensity_roi",
    curie=DEFAULT_.curie("min_intensity_roi"),
    model_uri=DEFAULT_.min_intensity_roi,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.mean_intensity = Slot(
    uri=DEFAULT_.mean_intensity,
    name="mean_intensity",
    curie=DEFAULT_.curie("mean_intensity"),
    model_uri=DEFAULT_.mean_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.median_intensity = Slot(
    uri=DEFAULT_.median_intensity,
    name="median_intensity",
    curie=DEFAULT_.curie("median_intensity"),
    model_uri=DEFAULT_.median_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.std_mean_intensity = Slot(
    uri=DEFAULT_.std_mean_intensity,
    name="std_mean_intensity",
    curie=DEFAULT_.curie("std_mean_intensity"),
    model_uri=DEFAULT_.std_mean_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.mad_mean_intensity = Slot(
    uri=DEFAULT_.mad_mean_intensity,
    name="mad_mean_intensity",
    curie=DEFAULT_.curie("mad_mean_intensity"),
    model_uri=DEFAULT_.mad_mean_intensity,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.min_max_intensity_ratio = Slot(
    uri=DEFAULT_.min_max_intensity_ratio,
    name="min_max_intensity_ratio",
    curie=DEFAULT_.curie("min_max_intensity_ratio"),
    model_uri=DEFAULT_.min_max_intensity_ratio,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.channel_A = Slot(
    uri=DEFAULT_.channel_A,
    name="channel_A",
    curie=DEFAULT_.curie("channel_A"),
    model_uri=DEFAULT_.channel_A,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.channel_B = Slot(
    uri=DEFAULT_.channel_B,
    name="channel_B",
    curie=DEFAULT_.curie("channel_B"),
    model_uri=DEFAULT_.channel_B,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.mean_3d_dist = Slot(
    uri=DEFAULT_.mean_3d_dist,
    name="mean_3d_dist",
    curie=DEFAULT_.curie("mean_3d_dist"),
    model_uri=DEFAULT_.mean_3d_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.median_3d_dist = Slot(
    uri=DEFAULT_.median_3d_dist,
    name="median_3d_dist",
    curie=DEFAULT_.curie("median_3d_dist"),
    model_uri=DEFAULT_.median_3d_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.std_3d_dist = Slot(
    uri=DEFAULT_.std_3d_dist,
    name="std_3d_dist",
    curie=DEFAULT_.curie("std_3d_dist"),
    model_uri=DEFAULT_.std_3d_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.mad_3d_dist = Slot(
    uri=DEFAULT_.mad_3d_dist,
    name="mad_3d_dist",
    curie=DEFAULT_.curie("mad_3d_dist"),
    model_uri=DEFAULT_.mad_3d_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.mean_z_dist = Slot(
    uri=DEFAULT_.mean_z_dist,
    name="mean_z_dist",
    curie=DEFAULT_.curie("mean_z_dist"),
    model_uri=DEFAULT_.mean_z_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.median_z_dist = Slot(
    uri=DEFAULT_.median_z_dist,
    name="median_z_dist",
    curie=DEFAULT_.curie("median_z_dist"),
    model_uri=DEFAULT_.median_z_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.std_z_dist = Slot(
    uri=DEFAULT_.std_z_dist,
    name="std_z_dist",
    curie=DEFAULT_.curie("std_z_dist"),
    model_uri=DEFAULT_.std_z_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.mad_z_dist = Slot(
    uri=DEFAULT_.mad_z_dist,
    name="mad_z_dist",
    curie=DEFAULT_.curie("mad_z_dist"),
    model_uri=DEFAULT_.mad_z_dist,
    domain=None,
    range=Optional[Union[float, List[float]]],
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
    range=float,
)

slots.prominence_threshold = Slot(
    uri=DEFAULT_.prominence_threshold,
    name="prominence_threshold",
    curie=DEFAULT_.curie("prominence_threshold"),
    model_uri=DEFAULT_.prominence_threshold,
    domain=None,
    range=float,
)

slots.focus_slice = Slot(
    uri=DEFAULT_.focus_slice,
    name="focus_slice",
    curie=DEFAULT_.curie("focus_slice"),
    model_uri=DEFAULT_.focus_slice,
    domain=None,
    range=Optional[Union[int, List[int]]],
)

slots.rayleigh_resolution = Slot(
    uri=DEFAULT_.rayleigh_resolution,
    name="rayleigh_resolution",
    curie=DEFAULT_.curie("rayleigh_resolution"),
    model_uri=DEFAULT_.rayleigh_resolution,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_position_A = Slot(
    uri=DEFAULT_.peak_position_A,
    name="peak_position_A",
    curie=DEFAULT_.curie("peak_position_A"),
    model_uri=DEFAULT_.peak_position_A,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_position_B = Slot(
    uri=DEFAULT_.peak_position_B,
    name="peak_position_B",
    curie=DEFAULT_.curie("peak_position_B"),
    model_uri=DEFAULT_.peak_position_B,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_height_A = Slot(
    uri=DEFAULT_.peak_height_A,
    name="peak_height_A",
    curie=DEFAULT_.curie("peak_height_A"),
    model_uri=DEFAULT_.peak_height_A,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_height_B = Slot(
    uri=DEFAULT_.peak_height_B,
    name="peak_height_B",
    curie=DEFAULT_.curie("peak_height_B"),
    model_uri=DEFAULT_.peak_height_B,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_prominence_A = Slot(
    uri=DEFAULT_.peak_prominence_A,
    name="peak_prominence_A",
    curie=DEFAULT_.curie("peak_prominence_A"),
    model_uri=DEFAULT_.peak_prominence_A,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.peak_prominence_B = Slot(
    uri=DEFAULT_.peak_prominence_B,
    name="peak_prominence_B",
    curie=DEFAULT_.curie("peak_prominence_B"),
    model_uri=DEFAULT_.peak_prominence_B,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.argolightBDataset__input = Slot(
    uri=DEFAULT_.input,
    name="argolightBDataset__input",
    curie=DEFAULT_.curie("input"),
    model_uri=DEFAULT_.argolightBDataset__input,
    domain=None,
    range=Union[dict, ArgolightBInput],
)

slots.argolightBDataset__output = Slot(
    uri=DEFAULT_.output,
    name="argolightBDataset__output",
    curie=DEFAULT_.curie("output"),
    model_uri=DEFAULT_.argolightBDataset__output,
    domain=None,
    range=Optional[Union[dict, ArgolightBOutput]],
)

slots.argolightBOutput__spots_labels_image = Slot(
    uri=DEFAULT_.spots_labels_image,
    name="argolightBOutput__spots_labels_image",
    curie=DEFAULT_.curie("spots_labels_image"),
    model_uri=DEFAULT_.argolightBOutput__spots_labels_image,
    domain=None,
    range=Optional[Union[str, ImageAsNumpyImageUrl]],
)

slots.argolightBOutput__spots_centroids = Slot(
    uri=DEFAULT_.spots_centroids,
    name="argolightBOutput__spots_centroids",
    curie=DEFAULT_.curie("spots_centroids"),
    model_uri=DEFAULT_.argolightBOutput__spots_centroids,
    domain=None,
    range=Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]],
)

slots.argolightBOutput__intensity_measurements = Slot(
    uri=DEFAULT_.intensity_measurements,
    name="argolightBOutput__intensity_measurements",
    curie=DEFAULT_.curie("intensity_measurements"),
    model_uri=DEFAULT_.argolightBOutput__intensity_measurements,
    domain=None,
    range=Optional[Union[dict, ArgolightBIntensityKeyValues]],
)

slots.argolightBOutput__distance_measurements = Slot(
    uri=DEFAULT_.distance_measurements,
    name="argolightBOutput__distance_measurements",
    curie=DEFAULT_.curie("distance_measurements"),
    model_uri=DEFAULT_.argolightBOutput__distance_measurements,
    domain=None,
    range=Optional[Union[dict, ArgolightBDistanceKeyValues]],
)

slots.argolightBOutput__spots_properties = Slot(
    uri=DEFAULT_.spots_properties,
    name="argolightBOutput__spots_properties",
    curie=DEFAULT_.curie("spots_properties"),
    model_uri=DEFAULT_.argolightBOutput__spots_properties,
    domain=None,
    range=Optional[Union[dict, TableAsDict]],
)

slots.argolightBOutput__spots_distances = Slot(
    uri=DEFAULT_.spots_distances,
    name="argolightBOutput__spots_distances",
    curie=DEFAULT_.curie("spots_distances"),
    model_uri=DEFAULT_.argolightBOutput__spots_distances,
    domain=None,
    range=Optional[Union[dict, TableAsDict]],
)

slots.argolightEDataset__input = Slot(
    uri=DEFAULT_.input,
    name="argolightEDataset__input",
    curie=DEFAULT_.curie("input"),
    model_uri=DEFAULT_.argolightEDataset__input,
    domain=None,
    range=Union[dict, ArgolightEInput],
)

slots.argolightEDataset__output = Slot(
    uri=DEFAULT_.output,
    name="argolightEDataset__output",
    curie=DEFAULT_.curie("output"),
    model_uri=DEFAULT_.argolightEDataset__output,
    domain=None,
    range=Optional[Union[dict, ArgolightEOutput]],
)

slots.argolightEOutput__peaks_rois = Slot(
    uri=DEFAULT_.peaks_rois,
    name="argolightEOutput__peaks_rois",
    curie=DEFAULT_.curie("peaks_rois"),
    model_uri=DEFAULT_.argolightEOutput__peaks_rois,
    domain=None,
    range=Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]],
)

slots.argolightEOutput__key_measurements = Slot(
    uri=DEFAULT_.key_measurements,
    name="argolightEOutput__key_measurements",
    curie=DEFAULT_.curie("key_measurements"),
    model_uri=DEFAULT_.argolightEOutput__key_measurements,
    domain=None,
    range=Optional[Union[dict, ArgolightEKeyValues]],
)

slots.argolightEOutput__intensity_profiles = Slot(
    uri=DEFAULT_.intensity_profiles,
    name="argolightEOutput__intensity_profiles",
    curie=DEFAULT_.curie("intensity_profiles"),
    model_uri=DEFAULT_.argolightEOutput__intensity_profiles,
    domain=None,
    range=Optional[Union[dict, TableAsDict]],
)
