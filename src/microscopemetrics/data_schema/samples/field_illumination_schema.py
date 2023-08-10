# Auto generated from field_illumination_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-08-10T11:11:01
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
    ExperimenterOrcid,
    Image5D,
    ImageAsNumpy,
    MetricsDataset,
    Sample,
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
    "https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illum_schema.yaml/",
)


# Types

# Class references


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

    image: Union[dict, ImageAsNumpy] = None
    processed: Union[bool, Bool] = False
    saturation_threshold: float = 0.01
    center_threshold: float = 0.9
    corner_fraction: float = 0.1
    sigma: float = 2.0
    intensity_map_size: int = 64
    bit_depth: Optional[int] = None
    regions_properties_table: Optional[Union[dict, TableAsPandasDF]] = None
    intensity_map: Optional[Union[dict, Image5D]] = None
    intensity_plot_data: Optional[Union[dict, TableAsPandasDF]] = None
    name: Optional[str] = "FieldIlluminationDataset"
    description: Optional[
        str
    ] = "This dataset contains the results of the field illumination analysis"
    inputs: Optional[Union[str, List[str]]] = empty_list()
    outputs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.image):
            self.MissingRequiredField("image")
        if not isinstance(self.image, ImageAsNumpy):
            self.image = ImageAsNumpy(**as_dict(self.image))

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
            self.regions_properties_table, TableAsPandasDF
        ):
            self.regions_properties_table = TableAsPandasDF(
                **as_dict(self.regions_properties_table)
            )

        if self.intensity_map is not None and not isinstance(self.intensity_map, Image5D):
            self.intensity_map = Image5D(**as_dict(self.intensity_map))

        if self.intensity_plot_data is not None and not isinstance(
            self.intensity_plot_data, TableAsPandasDF
        ):
            self.intensity_plot_data = TableAsPandasDF(**as_dict(self.intensity_plot_data))

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


slots.image = Slot(
    uri=DEFAULT_.image,
    name="image",
    curie=DEFAULT_.curie("image"),
    model_uri=DEFAULT_.image,
    domain=None,
    range=Union[dict, ImageAsNumpy],
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
    range=Optional[Union[dict, TableAsPandasDF]],
)

slots.intensity_map = Slot(
    uri=DEFAULT_.intensity_map,
    name="intensity_map",
    curie=DEFAULT_.curie("intensity_map"),
    model_uri=DEFAULT_.intensity_map,
    domain=None,
    range=Optional[Union[dict, Image5D]],
)

slots.intensity_plot_data = Slot(
    uri=DEFAULT_.intensity_plot_data,
    name="intensity_plot_data",
    curie=DEFAULT_.curie("intensity_plot_data"),
    model_uri=DEFAULT_.intensity_plot_data,
    domain=None,
    range=Optional[Union[dict, TableAsPandasDF]],
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
