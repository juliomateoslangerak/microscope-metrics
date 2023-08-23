# Auto generated from model.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-07-21T19:04:48
# Schema: microscope-metrics
#
# id: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py
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
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/')


# Types

# Class references
class ExperimenterOrcid(extended_str):
    pass


class ImageName(extended_str):
    pass


class ImageMaskName(ImageName):
    pass


class Image2DName(ImageName):
    pass


class Image5DName(ImageName):
    pass


class KeyValuePairName(extended_str):
    pass


class MetricsOutputTagId(extended_int):
    pass


class TagId(extended_int):
    pass


@dataclass
class NamedObject(YAMLRoot):
    """
    An object with a name and a description
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/NamedObject")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "NamedObject"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/NamedObject")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsObject")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsObject"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsObject")

    name: str = None
    description: str = None

@dataclass
class Sample(NamedObject):
    """
    A sample is a standard physical object that is imaged by a microscope
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Sample")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Sample")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Protocol")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Protocol"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Protocol")

    name: str = None
    description: str = None
    version: str = None
    url: str = None
    authors: Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]] = empty_list()

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
        self.authors = [v if isinstance(v, ExperimenterOrcid) else ExperimenterOrcid(v) for v in self.authors]

        super().__post_init__(**kwargs)


@dataclass
class Experimenter(YAMLRoot):
    """
    The person that performed the experiment or developed the protocol
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Experimenter")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Experimenter"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Experimenter")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsDataset")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsDataset"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsDataset")

    name: str = None
    description: str = None
    data: Union[Union[dict, "MetricsData"], List[Union[dict, "MetricsData"]]] = None
    sample: Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]] = empty_list()
    experimenter: Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]] = empty_list()
    metadata: Optional[Union[Union[dict, "MetricsMetadata"], List[Union[dict, "MetricsMetadata"]]]] = empty_list()
    output: Optional[Union[Union[dict, "MetricsOutput"], List[Union[dict, "MetricsOutput"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        self._normalize_inlined_as_dict(slot_name="data", slot_type=MetricsData, key_name="name", keyed=False)

        self._normalize_inlined_as_dict(slot_name="sample", slot_type=Sample, key_name="name", keyed=False)

        if not isinstance(self.experimenter, list):
            self.experimenter = [self.experimenter] if self.experimenter is not None else []
        self.experimenter = [v if isinstance(v, ExperimenterOrcid) else ExperimenterOrcid(v) for v in self.experimenter]

        self._normalize_inlined_as_dict(slot_name="metadata", slot_type=MetricsMetadata, key_name="name", keyed=False)

        self._normalize_inlined_as_dict(slot_name="output", slot_type=MetricsOutput, key_name="name", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class MetricsInput(MetricsObject):
    """
    A base object for all microscope-metrics inputs
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsInput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsInput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsInput")

    name: str = None
    description: str = None

@dataclass
class MetricsData(MetricsInput):
    """
    A base object for all microscope-metrics input data
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsData")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsData"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsData")

    name: str = None
    description: str = None

@dataclass
class MetricsMetadata(MetricsInput):
    """
    A base object for all microscope-metrics input metadata
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsMetadata")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsMetadata"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsMetadata")

    name: str = None
    description: str = None

@dataclass
class MetricsOutput(MetricsObject):
    """
    A base object for all microscope-metrics outputs
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutput")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutput"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutput")

    name: str = None
    description: str = None

@dataclass
class MetricsOutputImage2D(YAMLRoot):
    """
    A microscope-metrics output 2Dimage
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputImage2D")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputImage2D"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputImage2D")

    name: str = None
    description: str = None
    data: Union[str, List[str]] = None
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
class MetricsOutputImage5D(YAMLRoot):
    """
    A microscope-metrics output 5Dimage
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputImage5D")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputImage5D"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputImage5D")

    name: str = None
    description: str = None
    data: Union[str, List[str]] = None
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
class Image(YAMLRoot):
    """
    A base object for all microscope-metrics output images
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image")

    name: Union[str, ImageName] = None
    data: Union[str, List[str]] = None
    roi: Optional[Union[Union[dict, "ROI"], List[Union[dict, "ROI"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ImageName):
            self.name = ImageName(self.name)

        if self._is_empty(self.data):
            self.MissingRequiredField("data")
        if not isinstance(self.data, list):
            self.data = [self.data] if self.data is not None else []
        self.data = [v if isinstance(v, str) else str(v) for v in self.data]

        if not isinstance(self.roi, list):
            self.roi = [self.roi] if self.roi is not None else []
        self.roi = [v if isinstance(v, ROI) else ROI(**as_dict(v)) for v in self.roi]

        super().__post_init__(**kwargs)


@dataclass
class ImageMask(Image):
    """
    A base object for all microscope-metrics output masks
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ImageMask")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ImageMask"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ImageMask")

    name: Union[str, ImageMaskName] = None
    x: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None
    x_position: Optional[float] = 0.0
    y_position: Optional[float] = 0.0
    data: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ImageMaskName):
            self.name = ImageMaskName(self.name)

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image2D")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image2D"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image2D")

    name: Union[str, Image2DName] = None
    data: Union[str, List[str]] = None
    x: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, Image2DName):
            self.name = Image2DName(self.name)

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image5D")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Image5D"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Image5D")

    name: Union[str, Image5DName] = None
    data: Union[str, List[str]] = None
    t: Union[dict, "TimeSeries"] = None
    z: Union[dict, "PixelSeries"] = None
    y: Union[dict, "PixelSeries"] = None
    x: Union[dict, "PixelSeries"] = None
    c: Union[dict, "ChannelSeries"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, Image5DName):
            self.name = Image5DName(self.name)

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/PixelSeries")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "PixelSeries"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/PixelSeries")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Channel")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Channel"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Channel")

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

        if self.excitation_wavelength is not None and not isinstance(self.excitation_wavelength, float):
            self.excitation_wavelength = float(self.excitation_wavelength)

        super().__post_init__(**kwargs)


@dataclass
class ChannelSeries(YAMLRoot):
    """
    A series whose values represent channel
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ChannelSeries")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ChannelSeries"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ChannelSeries")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/TimeSeries")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "TimeSeries"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/TimeSeries")

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
    A ROI. Collection of shapes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ROI")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "ROI"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/ROI")

    shapes: Optional[Union[Union[dict, "Shape"], List[Union[dict, "Shape"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Shape")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Shape"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Shape")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Point")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Point"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Point")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Line")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Line"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Line")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Rectangle")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Rectangle"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Rectangle")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Ellipse")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Ellipse"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Ellipse")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Polygon")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Polygon"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Polygon")

    vertexes: Union[Union[dict, "Vertex"], List[Union[dict, "Vertex"]]] = None
    is_open: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.vertexes):
            self.MissingRequiredField("vertexes")
        self._normalize_inlined_as_dict(slot_name="vertexes", slot_type=Vertex, key_name="x", keyed=False)

        if self.is_open is not None and not isinstance(self.is_open, Bool):
            self.is_open = Bool(self.is_open)

        super().__post_init__(**kwargs)


@dataclass
class Vertex(YAMLRoot):
    """
    A vertex as defined by x and y coordinates
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Vertex")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Vertex"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Vertex")

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

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Mask")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Mask"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Mask")

    mask: Optional[Union[str, ImageMaskName]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.mask is not None and not isinstance(self.mask, ImageMaskName):
            self.mask = ImageMaskName(self.mask)

        super().__post_init__(**kwargs)


@dataclass
class Color(YAMLRoot):
    """
    A color as defined by RGB values and an optional alpha value
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Color")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Color"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Color")

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
class MetricsOutputKeyValues(YAMLRoot):
    """
    A microscope-metrics output collection of key-value pairs
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputKeyValues")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputKeyValues"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputKeyValues")

    name: str = None
    description: str = None
    key_values: Union[Dict[Union[str, KeyValuePairName], Union[dict, "KeyValuePair"]], List[Union[dict, "KeyValuePair"]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.key_values):
            self.MissingRequiredField("key_values")
        self._normalize_inlined_as_dict(slot_name="key_values", slot_type=KeyValuePair, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class KeyValuesCollection(YAMLRoot):
    """
    A collection of key-value pairs
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/KeyValuesCollection")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "KeyValuesCollection"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/KeyValuesCollection")

    key_values: Union[Dict[Union[str, KeyValuePairName], Union[dict, "KeyValuePair"]], List[Union[dict, "KeyValuePair"]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.key_values):
            self.MissingRequiredField("key_values")
        self._normalize_inlined_as_dict(slot_name="key_values", slot_type=KeyValuePair, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class KeyValuePair(YAMLRoot):
    """
    A key-value pair
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/KeyValuePair")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "KeyValuePair"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/KeyValuePair")

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
class MetricsOutputTag(YAMLRoot):
    """
    A microscope-metrics output tag
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputTag")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputTag"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputTag")

    id: Union[int, MetricsOutputTagId] = None
    name: str = None
    description: str = None
    text: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetricsOutputTagId):
            self.id = MetricsOutputTagId(self.id)

        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass
class Tag(YAMLRoot):
    """
    A tag
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Tag")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Tag"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Tag")

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
class MetricsOutputComment(YAMLRoot):
    """
    A microscope-metrics output comment
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputComment")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputComment"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputComment")

    name: str = None
    description: str = None
    text: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass
class Comment(YAMLRoot):
    """
    A comment
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Comment")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Comment"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Comment")

    text: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass
class MetricsOutputTable(YAMLRoot):
    """
    A microscope-metrics output collection of tables
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputTable")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "MetricsOutputTable"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/MetricsOutputTable")

    name: str = None
    description: str = None
    columns: Union[Union[dict, "Column"], List[Union[dict, "Column"]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.columns):
            self.MissingRequiredField("columns")
        self._normalize_inlined_as_dict(slot_name="columns", slot_type=Column, key_name="name", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Table(YAMLRoot):
    """
    A table
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Table")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Table"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Table")

    columns: Union[Union[dict, "Column"], List[Union[dict, "Column"]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.columns):
            self.MissingRequiredField("columns")
        self._normalize_inlined_as_dict(slot_name="columns", slot_type=Column, key_name="name", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Column(YAMLRoot):
    """
    A column
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Column")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "Column"
    class_model_uri: ClassVar[URIRef] = URIRef("https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/model/model.py/Column")

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

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.name = Slot(uri=DEFAULT_.name, name="name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.name, domain=None, range=str)

slots.description = Slot(uri=DEFAULT_.description, name="description", curie=DEFAULT_.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=str)

slots.sample__type = Slot(uri=DEFAULT_.type, name="sample__type", curie=DEFAULT_.curie('type'),
                   model_uri=DEFAULT_.sample__type, domain=None, range=str)

slots.sample__protocol = Slot(uri=DEFAULT_.protocol, name="sample__protocol", curie=DEFAULT_.curie('protocol'),
                   model_uri=DEFAULT_.sample__protocol, domain=None, range=Union[dict, Protocol])

slots.protocol__version = Slot(uri=DEFAULT_.version, name="protocol__version", curie=DEFAULT_.curie('version'),
                   model_uri=DEFAULT_.protocol__version, domain=None, range=str)

slots.protocol__authors = Slot(uri=DEFAULT_.authors, name="protocol__authors", curie=DEFAULT_.curie('authors'),
                   model_uri=DEFAULT_.protocol__authors, domain=None, range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]])

slots.protocol__url = Slot(uri=DEFAULT_.url, name="protocol__url", curie=DEFAULT_.curie('url'),
                   model_uri=DEFAULT_.protocol__url, domain=None, range=str)

slots.experimenter__name = Slot(uri=DEFAULT_.name, name="experimenter__name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.experimenter__name, domain=None, range=Optional[str])

slots.experimenter__orcid = Slot(uri=DEFAULT_.orcid, name="experimenter__orcid", curie=DEFAULT_.curie('orcid'),
                   model_uri=DEFAULT_.experimenter__orcid, domain=None, range=URIRef)

slots.metricsDataset__sample = Slot(uri=DEFAULT_.sample, name="metricsDataset__sample", curie=DEFAULT_.curie('sample'),
                   model_uri=DEFAULT_.metricsDataset__sample, domain=None, range=Optional[Union[Union[dict, Sample], List[Union[dict, Sample]]]])

slots.metricsDataset__experimenter = Slot(uri=DEFAULT_.experimenter, name="metricsDataset__experimenter", curie=DEFAULT_.curie('experimenter'),
                   model_uri=DEFAULT_.metricsDataset__experimenter, domain=None, range=Optional[Union[Union[str, ExperimenterOrcid], List[Union[str, ExperimenterOrcid]]]])

slots.metricsDataset__data = Slot(uri=DEFAULT_.data, name="metricsDataset__data", curie=DEFAULT_.curie('data'),
                   model_uri=DEFAULT_.metricsDataset__data, domain=None, range=Union[Union[dict, MetricsData], List[Union[dict, MetricsData]]])

slots.metricsDataset__metadata = Slot(uri=DEFAULT_.metadata, name="metricsDataset__metadata", curie=DEFAULT_.curie('metadata'),
                   model_uri=DEFAULT_.metricsDataset__metadata, domain=None, range=Optional[Union[Union[dict, MetricsMetadata], List[Union[dict, MetricsMetadata]]]])

slots.metricsDataset__output = Slot(uri=DEFAULT_.output, name="metricsDataset__output", curie=DEFAULT_.curie('output'),
                   model_uri=DEFAULT_.metricsDataset__output, domain=None, range=Optional[Union[Union[dict, MetricsOutput], List[Union[dict, MetricsOutput]]]])

slots.image__name = Slot(uri=DEFAULT_.name, name="image__name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.image__name, domain=None, range=URIRef)

slots.image__data = Slot(uri=DEFAULT_.data, name="image__data", curie=DEFAULT_.curie('data'),
                   model_uri=DEFAULT_.image__data, domain=None, range=Union[str, List[str]])

slots.image__roi = Slot(uri=DEFAULT_.roi, name="image__roi", curie=DEFAULT_.curie('roi'),
                   model_uri=DEFAULT_.image__roi, domain=None, range=Optional[Union[Union[dict, ROI], List[Union[dict, ROI]]]])

slots.imageMask__x_position = Slot(uri=DEFAULT_.x_position, name="imageMask__x_position", curie=DEFAULT_.curie('x_position'),
                   model_uri=DEFAULT_.imageMask__x_position, domain=None, range=Optional[float])

slots.imageMask__y_position = Slot(uri=DEFAULT_.y_position, name="imageMask__y_position", curie=DEFAULT_.curie('y_position'),
                   model_uri=DEFAULT_.imageMask__y_position, domain=None, range=Optional[float])

slots.imageMask__x = Slot(uri=DEFAULT_.x, name="imageMask__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.imageMask__x, domain=None, range=Union[dict, PixelSeries])

slots.imageMask__y = Slot(uri=DEFAULT_.y, name="imageMask__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.imageMask__y, domain=None, range=Union[dict, PixelSeries])

slots.imageMask__data = Slot(uri=DEFAULT_.data, name="imageMask__data", curie=DEFAULT_.curie('data'),
                   model_uri=DEFAULT_.imageMask__data, domain=None, range=Optional[Union[bool, Bool]])

slots.image2D__x = Slot(uri=DEFAULT_.x, name="image2D__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.image2D__x, domain=None, range=Union[dict, PixelSeries])

slots.image2D__y = Slot(uri=DEFAULT_.y, name="image2D__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.image2D__y, domain=None, range=Union[dict, PixelSeries])

slots.image5D__t = Slot(uri=DEFAULT_.t, name="image5D__t", curie=DEFAULT_.curie('t'),
                   model_uri=DEFAULT_.image5D__t, domain=None, range=Union[dict, TimeSeries])

slots.image5D__z = Slot(uri=DEFAULT_.z, name="image5D__z", curie=DEFAULT_.curie('z'),
                   model_uri=DEFAULT_.image5D__z, domain=None, range=Union[dict, PixelSeries])

slots.image5D__y = Slot(uri=DEFAULT_.y, name="image5D__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.image5D__y, domain=None, range=Union[dict, PixelSeries])

slots.image5D__x = Slot(uri=DEFAULT_.x, name="image5D__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.image5D__x, domain=None, range=Union[dict, PixelSeries])

slots.image5D__c = Slot(uri=DEFAULT_.c, name="image5D__c", curie=DEFAULT_.curie('c'),
                   model_uri=DEFAULT_.image5D__c, domain=None, range=Union[dict, ChannelSeries])

slots.pixelSeries__values = Slot(uri=DEFAULT_.values, name="pixelSeries__values", curie=DEFAULT_.curie('values'),
                   model_uri=DEFAULT_.pixelSeries__values, domain=None, range=Union[int, List[int]])

slots.channel__name = Slot(uri=DEFAULT_.name, name="channel__name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.channel__name, domain=None, range=Optional[str])

slots.channel__rendering_color = Slot(uri=DEFAULT_.rendering_color, name="channel__rendering_color", curie=DEFAULT_.curie('rendering_color'),
                   model_uri=DEFAULT_.channel__rendering_color, domain=None, range=Optional[Union[dict, Color]])

slots.channel__emission_wavelength = Slot(uri=DEFAULT_.emission_wavelength, name="channel__emission_wavelength", curie=DEFAULT_.curie('emission_wavelength'),
                   model_uri=DEFAULT_.channel__emission_wavelength, domain=None, range=Optional[float])

slots.channel__excitation_wavelength = Slot(uri=DEFAULT_.excitation_wavelength, name="channel__excitation_wavelength", curie=DEFAULT_.curie('excitation_wavelength'),
                   model_uri=DEFAULT_.channel__excitation_wavelength, domain=None, range=Optional[float])

slots.channelSeries__values = Slot(uri=DEFAULT_.values, name="channelSeries__values", curie=DEFAULT_.curie('values'),
                   model_uri=DEFAULT_.channelSeries__values, domain=None, range=Union[Union[dict, Channel], List[Union[dict, Channel]]])

slots.timeSeries__values = Slot(uri=DEFAULT_.values, name="timeSeries__values", curie=DEFAULT_.curie('values'),
                   model_uri=DEFAULT_.timeSeries__values, domain=None, range=Union[float, List[float]])

slots.rOI__shapes = Slot(uri=DEFAULT_.shapes, name="rOI__shapes", curie=DEFAULT_.curie('shapes'),
                   model_uri=DEFAULT_.rOI__shapes, domain=None, range=Optional[Union[Union[dict, Shape], List[Union[dict, Shape]]]])

slots.shape__z = Slot(uri=DEFAULT_.z, name="shape__z", curie=DEFAULT_.curie('z'),
                   model_uri=DEFAULT_.shape__z, domain=None, range=Optional[float])

slots.shape__c = Slot(uri=DEFAULT_.c, name="shape__c", curie=DEFAULT_.curie('c'),
                   model_uri=DEFAULT_.shape__c, domain=None, range=Optional[int])

slots.shape__t = Slot(uri=DEFAULT_.t, name="shape__t", curie=DEFAULT_.curie('t'),
                   model_uri=DEFAULT_.shape__t, domain=None, range=Optional[int])

slots.shape__fill_color = Slot(uri=DEFAULT_.fill_color, name="shape__fill_color", curie=DEFAULT_.curie('fill_color'),
                   model_uri=DEFAULT_.shape__fill_color, domain=None, range=Optional[Union[dict, Color]])

slots.shape__stroke_color = Slot(uri=DEFAULT_.stroke_color, name="shape__stroke_color", curie=DEFAULT_.curie('stroke_color'),
                   model_uri=DEFAULT_.shape__stroke_color, domain=None, range=Optional[Union[dict, Color]])

slots.shape__stroke_width = Slot(uri=DEFAULT_.stroke_width, name="shape__stroke_width", curie=DEFAULT_.curie('stroke_width'),
                   model_uri=DEFAULT_.shape__stroke_width, domain=None, range=Optional[int])

slots.point__x = Slot(uri=DEFAULT_.x, name="point__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.point__x, domain=None, range=Optional[float])

slots.point__y = Slot(uri=DEFAULT_.y, name="point__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.point__y, domain=None, range=Optional[float])

slots.line__x1 = Slot(uri=DEFAULT_.x1, name="line__x1", curie=DEFAULT_.curie('x1'),
                   model_uri=DEFAULT_.line__x1, domain=None, range=Optional[float])

slots.line__y1 = Slot(uri=DEFAULT_.y1, name="line__y1", curie=DEFAULT_.curie('y1'),
                   model_uri=DEFAULT_.line__y1, domain=None, range=Optional[float])

slots.line__x2 = Slot(uri=DEFAULT_.x2, name="line__x2", curie=DEFAULT_.curie('x2'),
                   model_uri=DEFAULT_.line__x2, domain=None, range=Optional[float])

slots.line__x3 = Slot(uri=DEFAULT_.x3, name="line__x3", curie=DEFAULT_.curie('x3'),
                   model_uri=DEFAULT_.line__x3, domain=None, range=Optional[float])

slots.rectangle__x = Slot(uri=DEFAULT_.x, name="rectangle__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.rectangle__x, domain=None, range=Optional[float])

slots.rectangle__y = Slot(uri=DEFAULT_.y, name="rectangle__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.rectangle__y, domain=None, range=Optional[float])

slots.rectangle__w = Slot(uri=DEFAULT_.w, name="rectangle__w", curie=DEFAULT_.curie('w'),
                   model_uri=DEFAULT_.rectangle__w, domain=None, range=Optional[float])

slots.rectangle__h = Slot(uri=DEFAULT_.h, name="rectangle__h", curie=DEFAULT_.curie('h'),
                   model_uri=DEFAULT_.rectangle__h, domain=None, range=Optional[float])

slots.ellipse__x = Slot(uri=DEFAULT_.x, name="ellipse__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.ellipse__x, domain=None, range=Optional[float])

slots.ellipse__y = Slot(uri=DEFAULT_.y, name="ellipse__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.ellipse__y, domain=None, range=Optional[float])

slots.ellipse__x_rad = Slot(uri=DEFAULT_.x_rad, name="ellipse__x_rad", curie=DEFAULT_.curie('x_rad'),
                   model_uri=DEFAULT_.ellipse__x_rad, domain=None, range=Optional[float])

slots.ellipse__y_rad = Slot(uri=DEFAULT_.y_rad, name="ellipse__y_rad", curie=DEFAULT_.curie('y_rad'),
                   model_uri=DEFAULT_.ellipse__y_rad, domain=None, range=Optional[float])

slots.polygon__vertexes = Slot(uri=DEFAULT_.vertexes, name="polygon__vertexes", curie=DEFAULT_.curie('vertexes'),
                   model_uri=DEFAULT_.polygon__vertexes, domain=None, range=Union[Union[dict, Vertex], List[Union[dict, Vertex]]])

slots.polygon__is_open = Slot(uri=DEFAULT_.is_open, name="polygon__is_open", curie=DEFAULT_.curie('is_open'),
                   model_uri=DEFAULT_.polygon__is_open, domain=None, range=Optional[Union[bool, Bool]])

slots.vertex__x = Slot(uri=DEFAULT_.x, name="vertex__x", curie=DEFAULT_.curie('x'),
                   model_uri=DEFAULT_.vertex__x, domain=None, range=float)

slots.vertex__y = Slot(uri=DEFAULT_.y, name="vertex__y", curie=DEFAULT_.curie('y'),
                   model_uri=DEFAULT_.vertex__y, domain=None, range=float)

slots.mask__mask = Slot(uri=DEFAULT_.mask, name="mask__mask", curie=DEFAULT_.curie('mask'),
                   model_uri=DEFAULT_.mask__mask, domain=None, range=Optional[Union[str, ImageMaskName]])

slots.color__R = Slot(uri=DEFAULT_.R, name="color__R", curie=DEFAULT_.curie('R'),
                   model_uri=DEFAULT_.color__R, domain=None, range=int)

slots.color__G = Slot(uri=DEFAULT_.G, name="color__G", curie=DEFAULT_.curie('G'),
                   model_uri=DEFAULT_.color__G, domain=None, range=int)

slots.color__B = Slot(uri=DEFAULT_.B, name="color__B", curie=DEFAULT_.curie('B'),
                   model_uri=DEFAULT_.color__B, domain=None, range=int)

slots.color__alpha = Slot(uri=DEFAULT_.alpha, name="color__alpha", curie=DEFAULT_.curie('alpha'),
                   model_uri=DEFAULT_.color__alpha, domain=None, range=Optional[int])

slots.keyValuesCollection__key_values = Slot(uri=DEFAULT_.key_values, name="keyValuesCollection__key_values", curie=DEFAULT_.curie('key_values'),
                   model_uri=DEFAULT_.keyValuesCollection__key_values, domain=None, range=Union[Dict[Union[str, KeyValuePairName], Union[dict, KeyValuePair]], List[Union[dict, KeyValuePair]]])

slots.keyValuePair__name = Slot(uri=DEFAULT_.name, name="keyValuePair__name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.keyValuePair__name, domain=None, range=URIRef)

slots.keyValuePair__value = Slot(uri=DEFAULT_.value, name="keyValuePair__value", curie=DEFAULT_.curie('value'),
                   model_uri=DEFAULT_.keyValuePair__value, domain=None, range=Optional[str])

slots.tag__id = Slot(uri=DEFAULT_.id, name="tag__id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.tag__id, domain=None, range=URIRef)

slots.tag__text = Slot(uri=DEFAULT_.text, name="tag__text", curie=DEFAULT_.curie('text'),
                   model_uri=DEFAULT_.tag__text, domain=None, range=str)

slots.tag__description = Slot(uri=DEFAULT_.description, name="tag__description", curie=DEFAULT_.curie('description'),
                   model_uri=DEFAULT_.tag__description, domain=None, range=Optional[str])

slots.comment__text = Slot(uri=DEFAULT_.text, name="comment__text", curie=DEFAULT_.curie('text'),
                   model_uri=DEFAULT_.comment__text, domain=None, range=str)

slots.table__columns = Slot(uri=DEFAULT_.columns, name="table__columns", curie=DEFAULT_.curie('columns'),
                   model_uri=DEFAULT_.table__columns, domain=None, range=Union[Union[dict, Column], List[Union[dict, Column]]])

slots.column__name = Slot(uri=DEFAULT_.name, name="column__name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.column__name, domain=None, range=str)

slots.column__values = Slot(uri=DEFAULT_.values, name="column__values", curie=DEFAULT_.curie('values'),
                   model_uri=DEFAULT_.column__values, domain=None, range=Union[str, List[str]])
