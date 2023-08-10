# Auto generated from core_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-10T14:19:48
# Schema: microscopemetrics_core_schema
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
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
    "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/",
)


# Types

# Class references
class ExperimenterOrcid(extended_str):
    pass


class KeyValuePairName(extended_str):
    pass


class TagId(extended_int):
    pass


MetaObject = Any


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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/NamedObject"
    )

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/MetricsObject"
    )


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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Sample"
    )

    type: Union[str, "SampleType"] = None
    protocol: Union[dict, "Protocol"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SampleType):
            self.type = SampleType(self.type)

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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Protocol"
    )

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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Experimenter"
    )

    orcid: Union[str, ExperimenterOrcid] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.orcid):
            self.MissingRequiredField("orcid")
        if not isinstance(self.orcid, ExperimenterOrcid):
            self.orcid = ExperimenterOrcid(self.orcid)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/MetricsDataset"
    )

    processed: Union[bool, Bool] = False
    sample: Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]] = empty_list()
    experimenter: Optional[
        Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]
    ] = empty_list()
    acquisition_date: Optional[Union[str, XSDDate]] = None
    processing_date: Optional[Union[str, XSDDate]] = None
    processing_log: Optional[str] = None
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.processed):
            self.MissingRequiredField("processed")
        if not isinstance(self.processed, Bool):
            self.processed = Bool(self.processed)

        self._normalize_inlined_as_dict(
            slot_name="sample", slot_type=Sample, key_name="type", keyed=False
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

        if self.processing_log is not None and not isinstance(self.processing_log, str):
            self.processing_log = str(self.processing_log)

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
    A base object for all microscope-metrics images
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image"
    )

    uri: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.uri is not None and not isinstance(self.uri, URI):
            self.uri = URI(self.uri)

        super().__post_init__(**kwargs)


@dataclass
class ImageAsNumpy(Image):
    """
    An image as a numpy array in TZYXC order
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageAsNumpy"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageAsNumpy"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageAsNumpy"
    )

    data: Optional[Union[dict, MetaObject]] = None


@dataclass
class ImageInline(Image):
    """
    A base object for all microscope-metrics images that are stored as arrays in line
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageInline"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageInline"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageInline"
    )

    data: Union[float, List[float]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        if not isinstance(self.data, list):
            self.data = [self.data] if self.data is not None else []
        self.data = [v if isinstance(v, float) else float(v) for v in self.data]

        super().__post_init__(**kwargs)


@dataclass
class ImageMask(ImageInline):
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ImageMask"
    )

    x: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None
    data: Union[Union[bool, Bool], List[Union[bool, Bool]]] = None
    x_position: Optional[float] = 0.0
    y_position: Optional[float] = 0.0

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, PixelSeries):
            self.x = PixelSeries(**as_dict(self.x))

        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, PixelSeries):
            self.y = PixelSeries(**as_dict(self.y))

        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        if not isinstance(self.data, list):
            self.data = [self.data] if self.data is not None else []
        self.data = [v if isinstance(v, Bool) else Bool(v) for v in self.data]

        if self.x_position is not None and not isinstance(self.x_position, float):
            self.x_position = float(self.x_position)

        if self.y_position is not None and not isinstance(self.y_position, float):
            self.y_position = float(self.y_position)

        super().__post_init__(**kwargs)


@dataclass
class Image2D(ImageInline):
    """
    A 2D image in YX order
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image2D"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image2D"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image2D"
    )

    data: Union[float, List[float]] = None
    y: Union[dict, "PixelSeries"] = None
    x: Union[dict, "PixelSeries"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.y):
            self.MissingRequiredField("y")
        if not isinstance(self.y, PixelSeries):
            self.y = PixelSeries(**as_dict(self.y))

        if self._is_empty(self.x):
            self.MissingRequiredField("x")
        if not isinstance(self.x, PixelSeries):
            self.x = PixelSeries(**as_dict(self.x))

        super().__post_init__(**kwargs)


@dataclass
class Image5D(ImageInline):
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Image5D"
    )

    data: Union[float, List[float]] = None
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
    A series whose values represent pixels or voxels or a single integer defining the shape of the dimension
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/PixelSeries"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PixelSeries"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/PixelSeries"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ChannelSeries"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TimeSeries"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/ROI"
    )

    image: Union[Union[dict, Image], List[Union[dict, Image]]] = None
    shapes: Optional[Union[Union[dict, "Shape"], List[Union[dict, "Shape"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.image):
            self.MissingRequiredField("image")
        if not isinstance(self.image, list):
            self.image = [self.image] if self.image is not None else []
        self.image = [v if isinstance(v, Image) else Image(**as_dict(v)) for v in self.image]

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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Shape"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Point"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Line"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Rectangle"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Ellipse"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Polygon"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Vertex"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Mask"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Color"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/KeyValues"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/KeyValuePair"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Tag"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Comment"
    )

    text: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


class Table(MetricsObject):
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Table"
    )


@dataclass
class TableAsPandasDF(Table):
    """
    A table as a Pandas DataFrame
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TableAsPandasDF"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "TableAsPandasDF"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TableAsPandasDF"
    )

    df: Union[dict, MetaObject] = None


@dataclass
class TableInlined(Table):
    """
    A table inlined in a metrics dataset
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TableInlined"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "TableInlined"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/TableInlined"
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
        "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/Column"
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
class SampleType(EnumDefinitionImpl):
    """
    The type of sample
    """

    FieldIllumination = PermissibleValue(text="FieldIllumination")

    _defn = EnumDefinition(
        name="SampleType",
        description="The type of sample",
    )


# Slots
class slots:
    pass


slots.uri = Slot(
    uri=DEFAULT_.uri,
    name="uri",
    curie=DEFAULT_.curie("uri"),
    model_uri=DEFAULT_.uri,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.id = Slot(
    uri=DEFAULT_.id,
    name="id",
    curie=DEFAULT_.curie("id"),
    model_uri=DEFAULT_.id,
    domain=None,
    range=URIRef,
)

slots.name = Slot(
    uri=DEFAULT_.name,
    name="name",
    curie=DEFAULT_.curie("name"),
    model_uri=DEFAULT_.name,
    domain=None,
    range=Optional[str],
)

slots.description = Slot(
    uri=DEFAULT_.description,
    name="description",
    curie=DEFAULT_.curie("description"),
    model_uri=DEFAULT_.description,
    domain=None,
    range=Optional[str],
)

slots.sample__type = Slot(
    uri=DEFAULT_.type,
    name="sample__type",
    curie=DEFAULT_.curie("type"),
    model_uri=DEFAULT_.sample__type,
    domain=None,
    range=Union[str, "SampleType"],
)

slots.sample__protocol = Slot(
    uri=DEFAULT_.protocol,
    name="sample__protocol",
    curie=DEFAULT_.curie("protocol"),
    model_uri=DEFAULT_.sample__protocol,
    domain=None,
    range=Union[dict, Protocol],
)

slots.protocol__version = Slot(
    uri=DEFAULT_.version,
    name="protocol__version",
    curie=DEFAULT_.curie("version"),
    model_uri=DEFAULT_.protocol__version,
    domain=None,
    range=str,
)

slots.protocol__authors = Slot(
    uri=DEFAULT_.authors,
    name="protocol__authors",
    curie=DEFAULT_.curie("authors"),
    model_uri=DEFAULT_.protocol__authors,
    domain=None,
    range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]],
)

slots.protocol__url = Slot(
    uri=DEFAULT_.url,
    name="protocol__url",
    curie=DEFAULT_.curie("url"),
    model_uri=DEFAULT_.protocol__url,
    domain=None,
    range=str,
)

slots.experimenter__name = Slot(
    uri=DEFAULT_.name,
    name="experimenter__name",
    curie=DEFAULT_.curie("name"),
    model_uri=DEFAULT_.experimenter__name,
    domain=None,
    range=str,
)

slots.experimenter__orcid = Slot(
    uri=DEFAULT_.orcid,
    name="experimenter__orcid",
    curie=DEFAULT_.curie("orcid"),
    model_uri=DEFAULT_.experimenter__orcid,
    domain=None,
    range=URIRef,
)

slots.metricsDataset__sample = Slot(
    uri=DEFAULT_.sample,
    name="metricsDataset__sample",
    curie=DEFAULT_.curie("sample"),
    model_uri=DEFAULT_.metricsDataset__sample,
    domain=None,
    range=Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]],
)

slots.metricsDataset__experimenter = Slot(
    uri=DEFAULT_.experimenter,
    name="metricsDataset__experimenter",
    curie=DEFAULT_.curie("experimenter"),
    model_uri=DEFAULT_.metricsDataset__experimenter,
    domain=None,
    range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]],
)

slots.metricsDataset__acquisition_date = Slot(
    uri=DEFAULT_.acquisition_date,
    name="metricsDataset__acquisition_date",
    curie=DEFAULT_.curie("acquisition_date"),
    model_uri=DEFAULT_.metricsDataset__acquisition_date,
    domain=None,
    range=Optional[Union[str, XSDDate]],
)

slots.metricsDataset__processed = Slot(
    uri=DEFAULT_.processed,
    name="metricsDataset__processed",
    curie=DEFAULT_.curie("processed"),
    model_uri=DEFAULT_.metricsDataset__processed,
    domain=None,
    range=Union[bool, Bool],
)

slots.metricsDataset__processing_date = Slot(
    uri=DEFAULT_.processing_date,
    name="metricsDataset__processing_date",
    curie=DEFAULT_.curie("processing_date"),
    model_uri=DEFAULT_.metricsDataset__processing_date,
    domain=None,
    range=Optional[Union[str, XSDDate]],
)

slots.metricsDataset__processing_log = Slot(
    uri=DEFAULT_.processing_log,
    name="metricsDataset__processing_log",
    curie=DEFAULT_.curie("processing_log"),
    model_uri=DEFAULT_.metricsDataset__processing_log,
    domain=None,
    range=Optional[str],
)

slots.metricsDataset__inputs = Slot(
    uri=DEFAULT_.inputs,
    name="metricsDataset__inputs",
    curie=DEFAULT_.curie("inputs"),
    model_uri=DEFAULT_.metricsDataset__inputs,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.metricsDataset__outputs = Slot(
    uri=DEFAULT_.outputs,
    name="metricsDataset__outputs",
    curie=DEFAULT_.curie("outputs"),
    model_uri=DEFAULT_.metricsDataset__outputs,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.imageAsNumpy__data = Slot(
    uri=DEFAULT_.data,
    name="imageAsNumpy__data",
    curie=DEFAULT_.curie("data"),
    model_uri=DEFAULT_.imageAsNumpy__data,
    domain=None,
    range=Optional[Union[dict, MetaObject]],
)

slots.imageInline__data = Slot(
    uri=DEFAULT_.data,
    name="imageInline__data",
    curie=DEFAULT_.curie("data"),
    model_uri=DEFAULT_.imageInline__data,
    domain=None,
    range=Union[float, List[float]],
)

slots.imageMask__x_position = Slot(
    uri=DEFAULT_.x_position,
    name="imageMask__x_position",
    curie=DEFAULT_.curie("x_position"),
    model_uri=DEFAULT_.imageMask__x_position,
    domain=None,
    range=Optional[float],
)

slots.imageMask__y_position = Slot(
    uri=DEFAULT_.y_position,
    name="imageMask__y_position",
    curie=DEFAULT_.curie("y_position"),
    model_uri=DEFAULT_.imageMask__y_position,
    domain=None,
    range=Optional[float],
)

slots.imageMask__x = Slot(
    uri=DEFAULT_.x,
    name="imageMask__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.imageMask__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.imageMask__y = Slot(
    uri=DEFAULT_.y,
    name="imageMask__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.imageMask__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.imageMask__data = Slot(
    uri=DEFAULT_.data,
    name="imageMask__data",
    curie=DEFAULT_.curie("data"),
    model_uri=DEFAULT_.imageMask__data,
    domain=None,
    range=Union[Union[bool, Bool], List[Union[bool, Bool]]],
)

slots.image2D__y = Slot(
    uri=DEFAULT_.y,
    name="image2D__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.image2D__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image2D__x = Slot(
    uri=DEFAULT_.x,
    name="image2D__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.image2D__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__t = Slot(
    uri=DEFAULT_.t,
    name="image5D__t",
    curie=DEFAULT_.curie("t"),
    model_uri=DEFAULT_.image5D__t,
    domain=None,
    range=Union[dict, TimeSeries],
)

slots.image5D__z = Slot(
    uri=DEFAULT_.z,
    name="image5D__z",
    curie=DEFAULT_.curie("z"),
    model_uri=DEFAULT_.image5D__z,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__y = Slot(
    uri=DEFAULT_.y,
    name="image5D__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.image5D__y,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__x = Slot(
    uri=DEFAULT_.x,
    name="image5D__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.image5D__x,
    domain=None,
    range=Union[dict, PixelSeries],
)

slots.image5D__c = Slot(
    uri=DEFAULT_.c,
    name="image5D__c",
    curie=DEFAULT_.curie("c"),
    model_uri=DEFAULT_.image5D__c,
    domain=None,
    range=Union[dict, ChannelSeries],
)

slots.pixelSeries__values = Slot(
    uri=DEFAULT_.values,
    name="pixelSeries__values",
    curie=DEFAULT_.curie("values"),
    model_uri=DEFAULT_.pixelSeries__values,
    domain=None,
    range=Union[int, List[int]],
)

slots.channelSeries__values = Slot(
    uri=DEFAULT_.values,
    name="channelSeries__values",
    curie=DEFAULT_.curie("values"),
    model_uri=DEFAULT_.channelSeries__values,
    domain=None,
    range=Union[int, List[int]],
)

slots.timeSeries__values = Slot(
    uri=DEFAULT_.values,
    name="timeSeries__values",
    curie=DEFAULT_.curie("values"),
    model_uri=DEFAULT_.timeSeries__values,
    domain=None,
    range=Union[float, List[float]],
)

slots.rOI__image = Slot(
    uri=DEFAULT_.image,
    name="rOI__image",
    curie=DEFAULT_.curie("image"),
    model_uri=DEFAULT_.rOI__image,
    domain=None,
    range=Union[Union[dict, Image], List[Union[dict, Image]]],
)

slots.rOI__shapes = Slot(
    uri=DEFAULT_.shapes,
    name="rOI__shapes",
    curie=DEFAULT_.curie("shapes"),
    model_uri=DEFAULT_.rOI__shapes,
    domain=None,
    range=Optional[Union[Union[dict, Shape], List[Union[dict, Shape]]]],
)

slots.shape__z = Slot(
    uri=DEFAULT_.z,
    name="shape__z",
    curie=DEFAULT_.curie("z"),
    model_uri=DEFAULT_.shape__z,
    domain=None,
    range=Optional[float],
)

slots.shape__c = Slot(
    uri=DEFAULT_.c,
    name="shape__c",
    curie=DEFAULT_.curie("c"),
    model_uri=DEFAULT_.shape__c,
    domain=None,
    range=Optional[int],
)

slots.shape__t = Slot(
    uri=DEFAULT_.t,
    name="shape__t",
    curie=DEFAULT_.curie("t"),
    model_uri=DEFAULT_.shape__t,
    domain=None,
    range=Optional[int],
)

slots.shape__fill_color = Slot(
    uri=DEFAULT_.fill_color,
    name="shape__fill_color",
    curie=DEFAULT_.curie("fill_color"),
    model_uri=DEFAULT_.shape__fill_color,
    domain=None,
    range=Optional[Union[dict, Color]],
)

slots.shape__stroke_color = Slot(
    uri=DEFAULT_.stroke_color,
    name="shape__stroke_color",
    curie=DEFAULT_.curie("stroke_color"),
    model_uri=DEFAULT_.shape__stroke_color,
    domain=None,
    range=Optional[Union[dict, Color]],
)

slots.shape__stroke_width = Slot(
    uri=DEFAULT_.stroke_width,
    name="shape__stroke_width",
    curie=DEFAULT_.curie("stroke_width"),
    model_uri=DEFAULT_.shape__stroke_width,
    domain=None,
    range=Optional[int],
)

slots.point__x = Slot(
    uri=DEFAULT_.x,
    name="point__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.point__x,
    domain=None,
    range=Optional[float],
)

slots.point__y = Slot(
    uri=DEFAULT_.y,
    name="point__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.point__y,
    domain=None,
    range=Optional[float],
)

slots.line__x1 = Slot(
    uri=DEFAULT_.x1,
    name="line__x1",
    curie=DEFAULT_.curie("x1"),
    model_uri=DEFAULT_.line__x1,
    domain=None,
    range=Optional[float],
)

slots.line__y1 = Slot(
    uri=DEFAULT_.y1,
    name="line__y1",
    curie=DEFAULT_.curie("y1"),
    model_uri=DEFAULT_.line__y1,
    domain=None,
    range=Optional[float],
)

slots.line__x2 = Slot(
    uri=DEFAULT_.x2,
    name="line__x2",
    curie=DEFAULT_.curie("x2"),
    model_uri=DEFAULT_.line__x2,
    domain=None,
    range=Optional[float],
)

slots.line__x3 = Slot(
    uri=DEFAULT_.x3,
    name="line__x3",
    curie=DEFAULT_.curie("x3"),
    model_uri=DEFAULT_.line__x3,
    domain=None,
    range=Optional[float],
)

slots.rectangle__x = Slot(
    uri=DEFAULT_.x,
    name="rectangle__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.rectangle__x,
    domain=None,
    range=Optional[float],
)

slots.rectangle__y = Slot(
    uri=DEFAULT_.y,
    name="rectangle__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.rectangle__y,
    domain=None,
    range=Optional[float],
)

slots.rectangle__w = Slot(
    uri=DEFAULT_.w,
    name="rectangle__w",
    curie=DEFAULT_.curie("w"),
    model_uri=DEFAULT_.rectangle__w,
    domain=None,
    range=Optional[float],
)

slots.rectangle__h = Slot(
    uri=DEFAULT_.h,
    name="rectangle__h",
    curie=DEFAULT_.curie("h"),
    model_uri=DEFAULT_.rectangle__h,
    domain=None,
    range=Optional[float],
)

slots.ellipse__x = Slot(
    uri=DEFAULT_.x,
    name="ellipse__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.ellipse__x,
    domain=None,
    range=Optional[float],
)

slots.ellipse__y = Slot(
    uri=DEFAULT_.y,
    name="ellipse__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.ellipse__y,
    domain=None,
    range=Optional[float],
)

slots.ellipse__x_rad = Slot(
    uri=DEFAULT_.x_rad,
    name="ellipse__x_rad",
    curie=DEFAULT_.curie("x_rad"),
    model_uri=DEFAULT_.ellipse__x_rad,
    domain=None,
    range=Optional[float],
)

slots.ellipse__y_rad = Slot(
    uri=DEFAULT_.y_rad,
    name="ellipse__y_rad",
    curie=DEFAULT_.curie("y_rad"),
    model_uri=DEFAULT_.ellipse__y_rad,
    domain=None,
    range=Optional[float],
)

slots.polygon__vertexes = Slot(
    uri=DEFAULT_.vertexes,
    name="polygon__vertexes",
    curie=DEFAULT_.curie("vertexes"),
    model_uri=DEFAULT_.polygon__vertexes,
    domain=None,
    range=Union[Union[dict, Vertex], List[Union[dict, Vertex]]],
)

slots.polygon__is_open = Slot(
    uri=DEFAULT_.is_open,
    name="polygon__is_open",
    curie=DEFAULT_.curie("is_open"),
    model_uri=DEFAULT_.polygon__is_open,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.vertex__x = Slot(
    uri=DEFAULT_.x,
    name="vertex__x",
    curie=DEFAULT_.curie("x"),
    model_uri=DEFAULT_.vertex__x,
    domain=None,
    range=float,
)

slots.vertex__y = Slot(
    uri=DEFAULT_.y,
    name="vertex__y",
    curie=DEFAULT_.curie("y"),
    model_uri=DEFAULT_.vertex__y,
    domain=None,
    range=float,
)

slots.mask__mask = Slot(
    uri=DEFAULT_.mask,
    name="mask__mask",
    curie=DEFAULT_.curie("mask"),
    model_uri=DEFAULT_.mask__mask,
    domain=None,
    range=Optional[Union[dict, ImageMask]],
)

slots.color__R = Slot(
    uri=DEFAULT_.R,
    name="color__R",
    curie=DEFAULT_.curie("R"),
    model_uri=DEFAULT_.color__R,
    domain=None,
    range=int,
)

slots.color__G = Slot(
    uri=DEFAULT_.G,
    name="color__G",
    curie=DEFAULT_.curie("G"),
    model_uri=DEFAULT_.color__G,
    domain=None,
    range=int,
)

slots.color__B = Slot(
    uri=DEFAULT_.B,
    name="color__B",
    curie=DEFAULT_.curie("B"),
    model_uri=DEFAULT_.color__B,
    domain=None,
    range=int,
)

slots.color__alpha = Slot(
    uri=DEFAULT_.alpha,
    name="color__alpha",
    curie=DEFAULT_.curie("alpha"),
    model_uri=DEFAULT_.color__alpha,
    domain=None,
    range=Optional[int],
)

slots.keyValues__key_values = Slot(
    uri=DEFAULT_.key_values,
    name="keyValues__key_values",
    curie=DEFAULT_.curie("key_values"),
    model_uri=DEFAULT_.keyValues__key_values,
    domain=None,
    range=Union[
        Dict[Union[str, KeyValuePairName], Union[dict, KeyValuePair]],
        List[Union[dict, KeyValuePair]],
    ],
)

slots.keyValuePair__name = Slot(
    uri=DEFAULT_.name,
    name="keyValuePair__name",
    curie=DEFAULT_.curie("name"),
    model_uri=DEFAULT_.keyValuePair__name,
    domain=None,
    range=URIRef,
)

slots.keyValuePair__value = Slot(
    uri=DEFAULT_.value,
    name="keyValuePair__value",
    curie=DEFAULT_.curie("value"),
    model_uri=DEFAULT_.keyValuePair__value,
    domain=None,
    range=Optional[str],
)

slots.tag__id = Slot(
    uri=DEFAULT_.id,
    name="tag__id",
    curie=DEFAULT_.curie("id"),
    model_uri=DEFAULT_.tag__id,
    domain=None,
    range=URIRef,
)

slots.tag__text = Slot(
    uri=DEFAULT_.text,
    name="tag__text",
    curie=DEFAULT_.curie("text"),
    model_uri=DEFAULT_.tag__text,
    domain=None,
    range=str,
)

slots.tag__description = Slot(
    uri=DEFAULT_.description,
    name="tag__description",
    curie=DEFAULT_.curie("description"),
    model_uri=DEFAULT_.tag__description,
    domain=None,
    range=Optional[str],
)

slots.comment__text = Slot(
    uri=DEFAULT_.text,
    name="comment__text",
    curie=DEFAULT_.curie("text"),
    model_uri=DEFAULT_.comment__text,
    domain=None,
    range=str,
)

slots.tableAsPandasDF__df = Slot(
    uri=DEFAULT_.df,
    name="tableAsPandasDF__df",
    curie=DEFAULT_.curie("df"),
    model_uri=DEFAULT_.tableAsPandasDF__df,
    domain=None,
    range=Union[dict, MetaObject],
)

slots.tableInlined__columns = Slot(
    uri=DEFAULT_.columns,
    name="tableInlined__columns",
    curie=DEFAULT_.curie("columns"),
    model_uri=DEFAULT_.tableInlined__columns,
    domain=None,
    range=Union[Union[dict, Column], List[Union[dict, Column]]],
)

slots.column__name = Slot(
    uri=DEFAULT_.name,
    name="column__name",
    curie=DEFAULT_.curie("name"),
    model_uri=DEFAULT_.column__name,
    domain=None,
    range=str,
)

slots.column__values = Slot(
    uri=DEFAULT_.values,
    name="column__values",
    curie=DEFAULT_.curie("values"),
    model_uri=DEFAULT_.column__values,
    domain=None,
    range=Union[str, List[str]],
)
