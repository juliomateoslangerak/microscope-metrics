# Auto generated from field_illumination_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-09T11:48:19
# Schema: microscopemetrics_samples_field_illum_schema
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml
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
from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String, Uri
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    URI,
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

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = CurieNamespace(
    "",
    "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/",
)


# Types

# Class references
class ExperimenterOrcid(extended_str):
    pass


class KeyValuePairName(extended_str):
    pass


class TagId(extended_int):
    pass


@dataclass
class NamedObject(YAMLRoot):
    """
    An object with a name and a description
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/NamedObject"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "NamedObject"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/NamedObject"
    )

    name: str = None
    description: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class MetricsObject(NamedObject):
    """
    A base object for all microscope-metrics objects
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/MetricsObject"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsObject"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/MetricsObject"
    )

    name: str = None
    description: str = None


@dataclass
class Sample(NamedObject):
    """
    A sample is a standard physical object that is imaged by a microscope
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Sample"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Sample"
    )

    name: str = None
    description: str = None
    type: str = None
    protocol: Union[dict, "Protocol"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        if self._is_empty(self.protocol):
            self.MissingRequiredField("protocol")
        if not isinstance(self.protocol, Protocol):
            self.protocol = Protocol(**as_dict(self.protocol))

        super().__post_init__(**kwargs)


@dataclass
class Protocol(NamedObject):
    """
    Set of instructions for preparing and imaging a sample
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Protocol"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Protocol"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Protocol"
    )

    name: str = None
    description: str = None
    version: str = None
    url: str = None
    authors: Optional[
        Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.version):
            self.MissingRequiredField("version")
        if not isinstance(self.version, str):
            self.version = str(self.version)

        if self._is_empty(self.url):
            self.MissingRequiredField("url")
        if not isinstance(self.url, str):
            self.url = str(self.url)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [
            v if isinstance(v, ExperimenterOrcid) else ExperimenterOrcid(v) for v in self.authors
        ]

        super().__post_init__(**kwargs)


@dataclass
class Experimenter(YAMLRoot):
    """
    The person that performed the experiment or developed the protocol
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Experimenter"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Experimenter"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Experimenter"
    )

    orcid: Union[str, ExperimenterOrcid] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.orcid):
            self.MissingRequiredField("orcid")
        if not isinstance(self.orcid, ExperimenterOrcid):
            self.orcid = ExperimenterOrcid(self.orcid)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class MetricsDataset(NamedObject):
    """
    A base object on which microscope-metrics runs the analysis
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/MetricsDataset"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsDataset"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/MetricsDataset"
    )

    name: str = None
    description: str = None
    processed: Union[bool, Bool] = False
    sample: Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]] = empty_list()
    experimenter: Optional[
        Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]
    ] = empty_list()
    acquisition_date: Optional[Union[str, XSDDate]] = None
    processing_date: Optional[Union[str, XSDDate]] = None
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.processed):
            self.MissingRequiredField("processed")
        if not isinstance(self.processed, Bool):
            self.processed = Bool(self.processed)

        self._normalize_inlined_as_dict(
            slot_name="sample", slot_type=Sample, key_name="name", keyed=False
        )

        if not isinstance(self.experimenter, list):
            self.experimenter = [self.experimenter] if self.experimenter is not None else []
        self.experimenter = [
            v if isinstance(v, ExperimenterOrcid) else ExperimenterOrcid(v)
            for v in self.experimenter
        ]

        if self.acquisition_date is not None and not isinstance(self.acquisition_date, XSDDate):
            self.acquisition_date = XSDDate(self.acquisition_date)

        if self.processing_date is not None and not isinstance(self.processing_date, XSDDate):
            self.processing_date = XSDDate(self.processing_date)

        if not isinstance(self.inputs, list):
            self.inputs = [self.inputs] if self.inputs is not None else []
        self.inputs = [v if isinstance(v, str) else str(v) for v in self.inputs]

        if not isinstance(self.outputs, list):
            self.outputs = [self.outputs] if self.outputs is not None else []
        self.outputs = [v if isinstance(v, str) else str(v) for v in self.outputs]

        super().__post_init__(**kwargs)


@dataclass
class FieldIlluminationDataset(MetricsDataset):
    """
    A field illumination dataset
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/FieldIlluminationDataset"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "FieldIlluminationDataset"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/FieldIlluminationDataset"
    )

    name: str = None
    description: str = None
    image: Union[dict, "Image5D"] = None
    processed: Union[bool, Bool] = False
    saturation_threshold: float = 0.01
    center_threshold: float = 0.9
    corner_fraction: float = 0.1
    sigma: float = 2.0
    intensity_map_size: int = 64
    bit_depth: Optional[int] = None
    regions_properties_table: Optional[Union[dict, "Table"]] = None
    intensity_map: Optional[
        Union[Union[dict, "Image2D"], List[Union[dict, "Image2D"]]]
    ] = empty_list()
    intensity_plot_data: Optional[Union[dict, "Table"]] = None
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.image):
            self.MissingRequiredField("image")
        if not isinstance(self.image, Image5D):
            self.image = Image5D(**as_dict(self.image))

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

        if self.regions_properties_table is not None and not isinstance(
            self.regions_properties_table, Table
        ):
            self.regions_properties_table = Table(**as_dict(self.regions_properties_table))

        self._normalize_inlined_as_dict(
            slot_name="intensity_map", slot_type=Image2D, key_name="name", keyed=False
        )

        if self.intensity_plot_data is not None and not isinstance(self.intensity_plot_data, Table):
            self.intensity_plot_data = Table(**as_dict(self.intensity_plot_data))

        if not isinstance(self.inputs, list):
            self.inputs = [self.inputs] if self.inputs is not None else []
        self.inputs = [v if isinstance(v, str) else str(v) for v in self.inputs]

        if not isinstance(self.outputs, list):
            self.outputs = [self.outputs] if self.outputs is not None else []
        self.outputs = [v if isinstance(v, str) else str(v) for v in self.outputs]

        super().__post_init__(**kwargs)


@dataclass
class Image(MetricsObject):
    """
    A base object for all microscope-metrics images. It may contain ROIs
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Image"
    )

    name: str = None
    description: str = None


@dataclass
class ImageReference(Image):
    """
    A base object for all microscope-metrics image stored as references
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageReference"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageReference"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/ImageReference"
    )

    name: str = None
    description: str = None
    data: Union[str, URI] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        if not isinstance(self.data, URI):
            self.data = URI(self.data)

        super().__post_init__(**kwargs)


@dataclass
class ImageInline(Image):
    """
    A base object for all microscope-metrics images that are stored as arrays in line. It may contain ROIs
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageInline"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageInline"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/ImageInline"
    )

    name: str = None
    description: str = None
    data: Union[str, List[str]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        if not isinstance(self.data, list):
            self.data = [self.data] if self.data is not None else []
        self.data = [v if isinstance(v, str) else str(v) for v in self.data]

        super().__post_init__(**kwargs)


@dataclass
class ImageMask(Image):
    """
    A base object for all microscope-metrics masks
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageMask"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageMask"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/ImageMask"
    )

    name: str = None
    description: str = None
    x: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None
    x_position: Optional[float] = 0.0
    y_position: Optional[float] = 0.0
    data: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, PixelSeries):
            self.x = PixelSeries(**as_dict(self.x))

        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, PixelSeries):
            self.y = PixelSeries(**as_dict(self.y))

        if self.x_position is not None and not isinstance(self.x_position, float):
            self.x_position = float(self.x_position)

        if self.y_position is not None and not isinstance(self.y_position, float):
            self.y_position = float(self.y_position)

        if self.data is not None and not isinstance(self.data, Bool):
            self.data = Bool(self.data)

        super().__post_init__(**kwargs)


@dataclass
class Image2D(Image):
    """
    A 2D image in XY order
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image2D"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image2D"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Image2D"
    )

    name: str = None
    description: str = None
    x: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, PixelSeries):
            self.x = PixelSeries(**as_dict(self.x))

        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, PixelSeries):
            self.y = PixelSeries(**as_dict(self.y))

        super().__post_init__(**kwargs)


@dataclass
class Image5D(Image):
    """
    A 5D image in TZYXC order
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image5D"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image5D"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Image5D"
    )

    name: str = None
    description: str = None
    t: Union[dict, "TimeSeries"] = None
    z: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None
    x: Union[dict, "PixelSeries"] = None
    c: Union[dict, "ChannelSeries"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.t):
            self.MissingRequiredField("t")
        if not isinstance(self.t, TimeSeries):
            self.t = TimeSeries(**as_dict(self.t))

        if self._is_empty(self.z):
            self.MissingRequiredField("z")
        if not isinstance(self.z, PixelSeries):
            self.z = PixelSeries(**as_dict(self.z))

        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, PixelSeries):
            self.y = PixelSeries(**as_dict(self.y))

        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, PixelSeries):
            self.x = PixelSeries(**as_dict(self.x))

        if self._is_empty(self.c):
            self.MissingRequiredField("c")
        if not isinstance(self.c, ChannelSeries):
            self.c = ChannelSeries(**as_dict(self.c))

        super().__post_init__(**kwargs)


@dataclass
class PixelSeries(YAMLRoot):
    """
    A series whose values represent pixels or voxels
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/PixelSeries"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PixelSeries"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/PixelSeries"
    )

    values: Union[int, List[int]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.values):
            self.MissingRequiredField("values")
        if not isinstance(self.values, list):
            self.values = [self.values] if self.values is not None else []
        self.values = [v if isinstance(v, int) else int(v) for v in self.values]

        super().__post_init__(**kwargs)


@dataclass
class Channel(YAMLRoot):
    """
    A channel
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Channel"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Channel"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Channel"
    )

    name: Optional[str] = None
    rendering_color: Optional[Union[dict, "Color"]] = None
    emission_wavelength: Optional[float] = None
    excitation_wavelength: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.rendering_color is not None and not isinstance(self.rendering_color, Color):
            self.rendering_color = Color(**as_dict(self.rendering_color))

        if self.emission_wavelength is not None and not isinstance(self.emission_wavelength, float):
            self.emission_wavelength = float(self.emission_wavelength)

        if self.excitation_wavelength is not None and not isinstance(
            self.excitation_wavelength, float
        ):
            self.excitation_wavelength = float(self.excitation_wavelength)

        super().__post_init__(**kwargs)


@dataclass
class ChannelSeries(YAMLRoot):
    """
    A series whose values represent channel
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ChannelSeries"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ChannelSeries"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/ChannelSeries"
    )

    values: Union[Union[dict, Channel], List[Union[dict, Channel]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.values):
            self.MissingRequiredField("values")
        if not isinstance(self.values, list):
            self.values = [self.values] if self.values is not None else []
        self.values = [v if isinstance(v, Channel) else Channel(**as_dict(v)) for v in self.values]

        super().__post_init__(**kwargs)


@dataclass
class TimeSeries(YAMLRoot):
    """
    A series whose values represent time
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TimeSeries"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "TimeSeries"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/TimeSeries"
    )

    values: Union[float, List[float]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.values):
            self.MissingRequiredField("values")
        if not isinstance(self.values, list):
            self.values = [self.values] if self.values is not None else []
        self.values = [v if isinstance(v, float) else float(v) for v in self.values]

        super().__post_init__(**kwargs)


@dataclass
class ROI(YAMLRoot):
    """
    A ROI. Collection of shapes and an image to which they are applied
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ROI"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ROI"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/ROI"
    )

    image: Union[Union[dict, Image], List[Union[dict, Image]]] = None
    shapes: Optional[Union[Union[dict, "Shape"], List[Union[dict, "Shape"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.image):
            self.MissingRequiredField("image")
        self._normalize_inlined_as_dict(
            slot_name="image", slot_type=Image, key_name="name", keyed=False
        )

        if not isinstance(self.shapes, list):
            self.shapes = [self.shapes] if self.shapes is not None else []
        self.shapes = [v if isinstance(v, Shape) else Shape(**as_dict(v)) for v in self.shapes]

        super().__post_init__(**kwargs)


@dataclass
class Shape(YAMLRoot):
    """
    A shape
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Shape"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Shape"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Shape"
    )

    z: Optional[float] = None
    c: Optional[int] = None
    t: Optional[int] = None
    fill_color: Optional[Union[dict, "Color"]] = None
    stroke_color: Optional[Union[dict, "Color"]] = None
    stroke_width: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.z is not None and not isinstance(self.z, float):
            self.z = float(self.z)

        if self.c is not None and not isinstance(self.c, int):
            self.c = int(self.c)

        if self.t is not None and not isinstance(self.t, int):
            self.t = int(self.t)

        if self.fill_color is not None and not isinstance(self.fill_color, Color):
            self.fill_color = Color(**as_dict(self.fill_color))

        if self.stroke_color is not None and not isinstance(self.stroke_color, Color):
            self.stroke_color = Color(**as_dict(self.stroke_color))

        if self.stroke_width is not None and not isinstance(self.stroke_width, int):
            self.stroke_width = int(self.stroke_width)

        super().__post_init__(**kwargs)


@dataclass
class Point(Shape):
    """
    A point as defined by x and y coordinates
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Point"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Point"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Point"
    )

    x: Optional[float] = None
    y: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.y is not None and not isinstance(self.y, float):
            self.y = float(self.y)

        super().__post_init__(**kwargs)


@dataclass
class Line(Shape):
    """
    A line as defined by x1, y1, x2, y2 coordinates
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Line"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Line"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Line"
    )

    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    x3: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.x1 is not None and not isinstance(self.x1, float):
            self.x1 = float(self.x1)

        if self.y1 is not None and not isinstance(self.y1, float):
            self.y1 = float(self.y1)

        if self.x2 is not None and not isinstance(self.x2, float):
            self.x2 = float(self.x2)

        if self.x3 is not None and not isinstance(self.x3, float):
            self.x3 = float(self.x3)

        super().__post_init__(**kwargs)


@dataclass
class Rectangle(Shape):
    """
    A rectangle as defined by x, y coordinates and width, height
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Rectangle"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Rectangle"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Rectangle"
    )

    x: Optional[float] = None
    y: Optional[float] = None
    w: Optional[float] = None
    h: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.y is not None and not isinstance(self.y, float):
            self.y = float(self.y)

        if self.w is not None and not isinstance(self.w, float):
            self.w = float(self.w)

        if self.h is not None and not isinstance(self.h, float):
            self.h = float(self.h)

        super().__post_init__(**kwargs)


@dataclass
class Ellipse(Shape):
    """
    An ellipse as defined by x, y coordinates and x and y radii
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Ellipse"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Ellipse"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Ellipse"
    )

    x: Optional[float] = None
    y: Optional[float] = None
    x_rad: Optional[float] = None
    y_rad: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.y is not None and not isinstance(self.y, float):
            self.y = float(self.y)

        if self.x_rad is not None and not isinstance(self.x_rad, float):
            self.x_rad = float(self.x_rad)

        if self.y_rad is not None and not isinstance(self.y_rad, float):
            self.y_rad = float(self.y_rad)

        super().__post_init__(**kwargs)


@dataclass
class Polygon(Shape):
    """
    A polygon as defined by a series of vertexes and a boolean to indicate if closed or not
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Polygon"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Polygon"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Polygon"
    )

    vertexes: Union[Union[dict, "Vertex"], List[Union[dict, "Vertex"]]] = None
    is_open: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.vertexes):
            self.MissingRequiredField("vertexes")
        self._normalize_inlined_as_dict(
            slot_name="vertexes", slot_type=Vertex, key_name="x", keyed=False
        )

        if self.is_open is not None and not isinstance(self.is_open, Bool):
            self.is_open = Bool(self.is_open)

        super().__post_init__(**kwargs)


@dataclass
class Vertex(YAMLRoot):
    """
    A vertex as defined by x and y coordinates
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Vertex"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Vertex"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Vertex"
    )

    x: float = None
    y: float = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, float):
            self.x = float(self.x)

        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, float):
            self.y = float(self.y)

        super().__post_init__(**kwargs)


@dataclass
class Mask(Shape):
    """
    A mask as defined by a boolean image
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Mask"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Mask"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Mask"
    )

    mask: Optional[Union[dict, ImageMask]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.mask is not None and not isinstance(self.mask, ImageMask):
            self.mask = ImageMask(**as_dict(self.mask))

        super().__post_init__(**kwargs)


@dataclass
class Color(YAMLRoot):
    """
    A color as defined by RGB values and an optional alpha value
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Color"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Color"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Color"
    )

    R: int = None
    G: int = None
    B: int = None
    alpha: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.R):
            self.MissingRequiredField("R")
        if not isinstance(self.R, int):
            self.R = int(self.R)

        if self._is_empty(self.G):
            self.MissingRequiredField("G")
        if not isinstance(self.G, int):
            self.G = int(self.G)

        if self._is_empty(self.B):
            self.MissingRequiredField("B")
        if not isinstance(self.B, int):
            self.B = int(self.B)

        if self.alpha is not None and not isinstance(self.alpha, int):
            self.alpha = int(self.alpha)

        super().__post_init__(**kwargs)


@dataclass
class KeyValues(YAMLRoot):
    """
    A collection of key-value pairs
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/KeyValues"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "KeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/KeyValues"
    )

    key_values: Union[
        Dict[Union[str, KeyValuePairName], Union[dict, "KeyValuePair"]],
        List[Union[dict, "KeyValuePair"]],
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.key_values):
            self.MissingRequiredField("key_values")
        self._normalize_inlined_as_dict(
            slot_name="key_values", slot_type=KeyValuePair, key_name="name", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass
class KeyValuePair(YAMLRoot):
    """
    A key-value pair
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/KeyValuePair"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "KeyValuePair"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/KeyValuePair"
    )

    name: Union[str, KeyValuePairName] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, KeyValuePairName):
            self.name = KeyValuePairName(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class Tag(YAMLRoot):
    """
    A tag
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Tag"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Tag"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Tag"
    )

    id: Union[int, TagId] = None
    text: str = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TagId):
            self.id = TagId(self.id)

        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Comment(YAMLRoot):
    """
    A comment
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Comment"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Comment"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Comment"
    )

    text: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass
class Table(YAMLRoot):
    """
    A table
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Table"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Table"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Table"
    )

    columns: Union[Union[dict, "Column"], List[Union[dict, "Column"]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.columns):
            self.MissingRequiredField("columns")
        self._normalize_inlined_as_dict(
            slot_name="columns", slot_type=Column, key_name="name", keyed=False
        )

        super().__post_init__(**kwargs)


@dataclass
class Column(YAMLRoot):
    """
    A column
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Column"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Column"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/Column"
    )

    name: str = None
    values: Union[str, List[str]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self._is_empty(self.values):
            self.MissingRequiredField("values")
        if not isinstance(self.values, list):
            self.values = [self.values] if self.values is not None else []
        self.values = [v if isinstance(v, str) else str(v) for v in self.values]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.image = Slot(
    uri=DEFAULT_.image,
    name="image",
    curie=DEFAULT_.curie("image"),
    model_uri=DEFAULT_.image,
    domain=None,
    range=Union[dict, Image5D],
)

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

slots.center_threshold = Slot(
    uri=DEFAULT_.center_threshold,
    name="center_threshold",
    curie=DEFAULT_.curie("center_threshold"),
    model_uri=DEFAULT_.center_threshold,
    domain=None,
    range=float,
)

slots.corner_fraction = Slot(
    uri=DEFAULT_.corner_fraction,
    name="corner_fraction",
    curie=DEFAULT_.curie("corner_fraction"),
    model_uri=DEFAULT_.corner_fraction,
    domain=None,
    range=float,
)

slots.sigma = Slot(
    uri=DEFAULT_.sigma,
    name="sigma",
    curie=DEFAULT_.curie("sigma"),
    model_uri=DEFAULT_.sigma,
    domain=None,
    range=float,
)

slots.intensity_map_size = Slot(
    uri=DEFAULT_.intensity_map_size,
    name="intensity_map_size",
    curie=DEFAULT_.curie("intensity_map_size"),
    model_uri=DEFAULT_.intensity_map_size,
    domain=None,
    range=int,
)

slots.regions_properties_table = Slot(
    uri=DEFAULT_.regions_properties_table,
    name="regions_properties_table",
    curie=DEFAULT_.curie("regions_properties_table"),
    model_uri=DEFAULT_.regions_properties_table,
    domain=None,
    range=Optional[Union[dict, Table]],
)

slots.intensity_map = Slot(
    uri=DEFAULT_.intensity_map,
    name="intensity_map",
    curie=DEFAULT_.curie("intensity_map"),
    model_uri=DEFAULT_.intensity_map,
    domain=None,
    range=Optional[Union[Union[dict, Image2D], List[Union[dict, Image2D]]]],
)

slots.intensity_plot_data = Slot(
    uri=DEFAULT_.intensity_plot_data,
    name="intensity_plot_data",
    curie=DEFAULT_.curie("intensity_plot_data"),
    model_uri=DEFAULT_.intensity_plot_data,
    domain=None,
    range=Optional[Union[dict, Table]],
)

slots.id = Slot(
    uri="str(uriorcurie)", name="id", curie=None, model_uri=DEFAULT_.id, domain=None, range=URIRef
)

slots.name = Slot(
    uri="str(uriorcurie)", name="name", curie=None, model_uri=DEFAULT_.name, domain=None, range=str
)

slots.description = Slot(
    uri="str(uriorcurie)",
    name="description",
    curie=None,
    model_uri=DEFAULT_.description,
    domain=None,
    range=str,
)

slots.sample__type = Slot(
    uri="str(uriorcurie)",
    name="sample__type",
    curie=None,
    model_uri=DEFAULT_.sample__type,
    domain=None,
    range=str,
)

slots.sample__protocol = Slot(
    uri="str(uriorcurie)",
    name="sample__protocol",
    curie=None,
    model_uri=DEFAULT_.sample__protocol,
    domain=None,
    range=Union[dict, Protocol],
)

slots.protocol__version = Slot(
    uri="str(uriorcurie)",
    name="protocol__version",
    curie=None,
    model_uri=DEFAULT_.protocol__version,
    domain=None,
    range=str,
)

slots.protocol__authors = Slot(
    uri="str(uriorcurie)",
    name="protocol__authors",
    curie=None,
    model_uri=DEFAULT_.protocol__authors,
    domain=None,
    range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]],
)

slots.protocol__url = Slot(
    uri="str(uriorcurie)",
    name="protocol__url",
    curie=None,
    model_uri=DEFAULT_.protocol__url,
    domain=None,
    range=str,
)

slots.experimenter__name = Slot(
    uri="str(uriorcurie)",
    name="experimenter__name",
    curie=None,
    model_uri=DEFAULT_.experimenter__name,
    domain=None,
    range=Optional[str],
)

slots.experimenter__orcid = Slot(
    uri="str(uriorcurie)",
    name="experimenter__orcid",
    curie=None,
    model_uri=DEFAULT_.experimenter__orcid,
    domain=None,
    range=URIRef,
)

slots.metricsDataset__sample = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__sample",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__sample,
    domain=None,
    range=Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]],
)

slots.metricsDataset__experimenter = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__experimenter",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__experimenter,
    domain=None,
    range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]],
)

slots.metricsDataset__acquisition_date = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__acquisition_date",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__acquisition_date,
    domain=None,
    range=Optional[Union[str, XSDDate]],
)

slots.metricsDataset__processed = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__processed",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__processed,
    domain=None,
    range=Union[bool, Bool],
)

slots.metricsDataset__processing_date = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__processing_date",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__processing_date,
    domain=None,
    range=Optional[Union[str, XSDDate]],
)

slots.metricsDataset__inputs = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__inputs",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__inputs,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.metricsDataset__outputs = Slot(
    uri="str(uriorcurie)",
    name="metricsDataset__outputs",
    curie=None,
    model_uri=DEFAULT_.metricsDataset__outputs,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.imageReference__data = Slot(
    uri="str(uriorcurie)",
    name="imageReference__data",
    curie=None,
    model_uri=DEFAULT_.imageReference__data,
    domain=None,
    range=Union[str, URI],
)

slots.imageInline__data = Slot(
    uri="str(uriorcurie)",
    name="imageInline__data",
    curie=None,
    model_uri=DEFAULT_.imageInline__data,
    domain=None,
    range=Union[str, List[str]],
)

slots.imageMask__x_position = Slot(
    uri="str(uriorcurie)",
    name="imageMask__x_position",
    curie=None,
    model_uri=DEFAULT_.imageMask__x_position,
    domain=None,
    range=Optional[float],
)

slots.imageMask__y_position = Slot(
    uri="str(uriorcurie)",
    name="imageMask__y_position",
    curie=None,
    model_uri=DEFAULT_.imageMask__y_position,
    domain=None,
    range=Optional[float],
)

slots.imageMask__x = Slot(
    uri="str(uriorcurie)",
    name="imageMask__x",
    curie=None,
    model_uri=DEFAULT_.imageMask__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.imageMask__y = Slot(
    uri="str(uriorcurie)",
    name="imageMask__y",
    curie=None,
    model_uri=DEFAULT_.imageMask__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.imageMask__data = Slot(
    uri="str(uriorcurie)",
    name="imageMask__data",
    curie=None,
    model_uri=DEFAULT_.imageMask__data,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.image2D__x = Slot(
    uri="str(uriorcurie)",
    name="image2D__x",
    curie=None,
    model_uri=DEFAULT_.image2D__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image2D__y = Slot(
    uri="str(uriorcurie)",
    name="image2D__y",
    curie=None,
    model_uri=DEFAULT_.image2D__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__t = Slot(
    uri="str(uriorcurie)",
    name="image5D__t",
    curie=None,
    model_uri=DEFAULT_.image5D__t,
    domain=None,
    range=Union[dict, TimeSeries],
)

slots.image5D__z = Slot(
    uri="str(uriorcurie)",
    name="image5D__z",
    curie=None,
    model_uri=DEFAULT_.image5D__z,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__y = Slot(
    uri="str(uriorcurie)",
    name="image5D__y",
    curie=None,
    model_uri=DEFAULT_.image5D__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__x = Slot(
    uri="str(uriorcurie)",
    name="image5D__x",
    curie=None,
    model_uri=DEFAULT_.image5D__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__c = Slot(
    uri="str(uriorcurie)",
    name="image5D__c",
    curie=None,
    model_uri=DEFAULT_.image5D__c,
    domain=None,
    range=Union[dict, ChannelSeries],
)

slots.pixelSeries__values = Slot(
    uri="str(uriorcurie)",
    name="pixelSeries__values",
    curie=None,
    model_uri=DEFAULT_.pixelSeries__values,
    domain=None,
    range=Union[int, List[int]],
)

slots.channel__name = Slot(
    uri="str(uriorcurie)",
    name="channel__name",
    curie=None,
    model_uri=DEFAULT_.channel__name,
    domain=None,
    range=Optional[str],
)

slots.channel__rendering_color = Slot(
    uri="str(uriorcurie)",
    name="channel__rendering_color",
    curie=None,
    model_uri=DEFAULT_.channel__rendering_color,
    domain=None,
    range=Optional[Union[dict, Color]],
)

slots.channel__emission_wavelength = Slot(
    uri="str(uriorcurie)",
    name="channel__emission_wavelength",
    curie=None,
    model_uri=DEFAULT_.channel__emission_wavelength,
    domain=None,
    range=Optional[float],
)

slots.channel__excitation_wavelength = Slot(
    uri="str(uriorcurie)",
    name="channel__excitation_wavelength",
    curie=None,
    model_uri=DEFAULT_.channel__excitation_wavelength,
    domain=None,
    range=Optional[float],
)

slots.channelSeries__values = Slot(
    uri="str(uriorcurie)",
    name="channelSeries__values",
    curie=None,
    model_uri=DEFAULT_.channelSeries__values,
    domain=None,
    range=Union[Union[dict, Channel], List[Union[dict, Channel]]],
)

slots.timeSeries__values = Slot(
    uri="str(uriorcurie)",
    name="timeSeries__values",
    curie=None,
    model_uri=DEFAULT_.timeSeries__values,
    domain=None,
    range=Union[float, List[float]],
)

slots.rOI__image = Slot(
    uri="str(uriorcurie)",
    name="rOI__image",
    curie=None,
    model_uri=DEFAULT_.rOI__image,
    domain=None,
    range=Union[Union[dict, Image], List[Union[dict, Image]]],
)

slots.rOI__shapes = Slot(
    uri="str(uriorcurie)",
    name="rOI__shapes",
    curie=None,
    model_uri=DEFAULT_.rOI__shapes,
    domain=None,
    range=Optional[Union[Union[dict, Shape], List[Union[dict, Shape]]]],
)

slots.shape__z = Slot(
    uri="str(uriorcurie)",
    name="shape__z",
    curie=None,
    model_uri=DEFAULT_.shape__z,
    domain=None,
    range=Optional[float],
)

slots.shape__c = Slot(
    uri="str(uriorcurie)",
    name="shape__c",
    curie=None,
    model_uri=DEFAULT_.shape__c,
    domain=None,
    range=Optional[int],
)

slots.shape__t = Slot(
    uri="str(uriorcurie)",
    name="shape__t",
    curie=None,
    model_uri=DEFAULT_.shape__t,
    domain=None,
    range=Optional[int],
)

slots.shape__fill_color = Slot(
    uri="str(uriorcurie)",
    name="shape__fill_color",
    curie=None,
    model_uri=DEFAULT_.shape__fill_color,
    domain=None,
    range=Optional[Union[dict, Color]],
)

slots.shape__stroke_color = Slot(
    uri="str(uriorcurie)",
    name="shape__stroke_color",
    curie=None,
    model_uri=DEFAULT_.shape__stroke_color,
    domain=None,
    range=Optional[Union[dict, Color]],
)

slots.shape__stroke_width = Slot(
    uri="str(uriorcurie)",
    name="shape__stroke_width",
    curie=None,
    model_uri=DEFAULT_.shape__stroke_width,
    domain=None,
    range=Optional[int],
)

slots.point__x = Slot(
    uri="str(uriorcurie)",
    name="point__x",
    curie=None,
    model_uri=DEFAULT_.point__x,
    domain=None,
    range=Optional[float],
)

slots.point__y = Slot(
    uri="str(uriorcurie)",
    name="point__y",
    curie=None,
    model_uri=DEFAULT_.point__y,
    domain=None,
    range=Optional[float],
)

slots.line__x1 = Slot(
    uri="str(uriorcurie)",
    name="line__x1",
    curie=None,
    model_uri=DEFAULT_.line__x1,
    domain=None,
    range=Optional[float],
)

slots.line__y1 = Slot(
    uri="str(uriorcurie)",
    name="line__y1",
    curie=None,
    model_uri=DEFAULT_.line__y1,
    domain=None,
    range=Optional[float],
)

slots.line__x2 = Slot(
    uri="str(uriorcurie)",
    name="line__x2",
    curie=None,
    model_uri=DEFAULT_.line__x2,
    domain=None,
    range=Optional[float],
)

slots.line__x3 = Slot(
    uri="str(uriorcurie)",
    name="line__x3",
    curie=None,
    model_uri=DEFAULT_.line__x3,
    domain=None,
    range=Optional[float],
)

slots.rectangle__x = Slot(
    uri="str(uriorcurie)",
    name="rectangle__x",
    curie=None,
    model_uri=DEFAULT_.rectangle__x,
    domain=None,
    range=Optional[float],
)

slots.rectangle__y = Slot(
    uri="str(uriorcurie)",
    name="rectangle__y",
    curie=None,
    model_uri=DEFAULT_.rectangle__y,
    domain=None,
    range=Optional[float],
)

slots.rectangle__w = Slot(
    uri="str(uriorcurie)",
    name="rectangle__w",
    curie=None,
    model_uri=DEFAULT_.rectangle__w,
    domain=None,
    range=Optional[float],
)

slots.rectangle__h = Slot(
    uri="str(uriorcurie)",
    name="rectangle__h",
    curie=None,
    model_uri=DEFAULT_.rectangle__h,
    domain=None,
    range=Optional[float],
)

slots.ellipse__x = Slot(
    uri="str(uriorcurie)",
    name="ellipse__x",
    curie=None,
    model_uri=DEFAULT_.ellipse__x,
    domain=None,
    range=Optional[float],
)

slots.ellipse__y = Slot(
    uri="str(uriorcurie)",
    name="ellipse__y",
    curie=None,
    model_uri=DEFAULT_.ellipse__y,
    domain=None,
    range=Optional[float],
)

slots.ellipse__x_rad = Slot(
    uri="str(uriorcurie)",
    name="ellipse__x_rad",
    curie=None,
    model_uri=DEFAULT_.ellipse__x_rad,
    domain=None,
    range=Optional[float],
)

slots.ellipse__y_rad = Slot(
    uri="str(uriorcurie)",
    name="ellipse__y_rad",
    curie=None,
    model_uri=DEFAULT_.ellipse__y_rad,
    domain=None,
    range=Optional[float],
)

slots.polygon__vertexes = Slot(
    uri="str(uriorcurie)",
    name="polygon__vertexes",
    curie=None,
    model_uri=DEFAULT_.polygon__vertexes,
    domain=None,
    range=Union[Union[dict, Vertex], List[Union[dict, Vertex]]],
)

slots.polygon__is_open = Slot(
    uri="str(uriorcurie)",
    name="polygon__is_open",
    curie=None,
    model_uri=DEFAULT_.polygon__is_open,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.vertex__x = Slot(
    uri="str(uriorcurie)",
    name="vertex__x",
    curie=None,
    model_uri=DEFAULT_.vertex__x,
    domain=None,
    range=float,
)

slots.vertex__y = Slot(
    uri="str(uriorcurie)",
    name="vertex__y",
    curie=None,
    model_uri=DEFAULT_.vertex__y,
    domain=None,
    range=float,
)

slots.mask__mask = Slot(
    uri="str(uriorcurie)",
    name="mask__mask",
    curie=None,
    model_uri=DEFAULT_.mask__mask,
    domain=None,
    range=Optional[Union[dict, ImageMask]],
)

slots.color__R = Slot(
    uri="str(uriorcurie)",
    name="color__R",
    curie=None,
    model_uri=DEFAULT_.color__R,
    domain=None,
    range=int,
)

slots.color__G = Slot(
    uri="str(uriorcurie)",
    name="color__G",
    curie=None,
    model_uri=DEFAULT_.color__G,
    domain=None,
    range=int,
)

slots.color__B = Slot(
    uri="str(uriorcurie)",
    name="color__B",
    curie=None,
    model_uri=DEFAULT_.color__B,
    domain=None,
    range=int,
)

slots.color__alpha = Slot(
    uri="str(uriorcurie)",
    name="color__alpha",
    curie=None,
    model_uri=DEFAULT_.color__alpha,
    domain=None,
    range=Optional[int],
)

slots.keyValues__key_values = Slot(
    uri="str(uriorcurie)",
    name="keyValues__key_values",
    curie=None,
    model_uri=DEFAULT_.keyValues__key_values,
    domain=None,
    range=Union[
        Dict[Union[str, KeyValuePairName], Union[dict, KeyValuePair]],
        List[Union[dict, KeyValuePair]],
    ],
)

slots.keyValuePair__name = Slot(
    uri="str(uriorcurie)",
    name="keyValuePair__name",
    curie=None,
    model_uri=DEFAULT_.keyValuePair__name,
    domain=None,
    range=URIRef,
)

slots.keyValuePair__value = Slot(
    uri="str(uriorcurie)",
    name="keyValuePair__value",
    curie=None,
    model_uri=DEFAULT_.keyValuePair__value,
    domain=None,
    range=Optional[str],
)

slots.tag__id = Slot(
    uri="str(uriorcurie)",
    name="tag__id",
    curie=None,
    model_uri=DEFAULT_.tag__id,
    domain=None,
    range=URIRef,
)

slots.tag__text = Slot(
    uri="str(uriorcurie)",
    name="tag__text",
    curie=None,
    model_uri=DEFAULT_.tag__text,
    domain=None,
    range=str,
)

slots.tag__description = Slot(
    uri="str(uriorcurie)",
    name="tag__description",
    curie=None,
    model_uri=DEFAULT_.tag__description,
    domain=None,
    range=Optional[str],
)

slots.comment__text = Slot(
    uri="str(uriorcurie)",
    name="comment__text",
    curie=None,
    model_uri=DEFAULT_.comment__text,
    domain=None,
    range=str,
)

slots.table__columns = Slot(
    uri="str(uriorcurie)",
    name="table__columns",
    curie=None,
    model_uri=DEFAULT_.table__columns,
    domain=None,
    range=Union[Union[dict, Column], List[Union[dict, Column]]],
)

slots.column__name = Slot(
    uri="str(uriorcurie)",
    name="column__name",
    curie=None,
    model_uri=DEFAULT_.column__name,
    domain=None,
    range=str,
)

slots.column__values = Slot(
    uri="str(uriorcurie)",
    name="column__values",
    curie=None,
    model_uri=DEFAULT_.column__values,
    domain=None,
    range=Union[str, List[str]],
)

slots.FieldIlluminationDataset_inputs = Slot(
    uri=DEFAULT_.inputs,
    name="FieldIlluminationDataset_inputs",
    curie=DEFAULT_.curie("inputs"),
    model_uri=DEFAULT_.FieldIlluminationDataset_inputs,
    domain=FieldIlluminationDataset,
    range=Optional[Union[str, List[str]]],
)

slots.FieldIlluminationDataset_outputs = Slot(
    uri=DEFAULT_.outputs,
    name="FieldIlluminationDataset_outputs",
    curie=DEFAULT_.curie("outputs"),
    model_uri=DEFAULT_.FieldIlluminationDataset_outputs,
    domain=FieldIlluminationDataset,
    range=Optional[Union[str, List[str]]],
)
