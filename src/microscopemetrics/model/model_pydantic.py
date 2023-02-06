from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'
    
class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True, 
                validate_all = True, 
                underscore_attrs_are_private = True, 
                extra = 'forbid', 
                arbitrary_types_allowed = True):
    pass                    


class LengthUnits(str, Enum):
    
    METER = "METER"
    CENTIMETER = "CENTIMETER"
    MILLIMETER = "MILLIMETER"
    MICROMETER = "MICROMETER"
    NANOMETER = "NANOMETER"
    
    

class PersonStatus(str, Enum):
    
    ALIVE = "ALIVE"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"
    
    

class Sample(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    type: str = Field(None)
    preparation_protocol: str = Field(None)
    


class Protocol(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    version: str = Field(None)
    authors: Optional[str] = Field(None)
    url: str = Field(None)
    


class Experimenter(ConfiguredBaseModel):
    
    name: Optional[str] = Field(None)
    orcid: Optional[str] = Field(None)
    


class Data(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    


class Metadata(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    


class MetricsDataset(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    sample: Optional[List[str]] = Field(default_factory=list)
    data: Optional[List[str]] = Field(default_factory=list)
    metadata: Optional[List[str]] = Field(default_factory=list)
    output: Optional[List[MetricsOutput]] = Field(default_factory=list)
    


class MetricsOutput(ConfiguredBaseModel):
    
    name: str = Field(None)
    description: str = Field(None)
    


class OutputImage(MetricsOutput):
    
    data: Optional[List[int]] = Field(default_factory=list)
    name: str = Field(None)
    description: str = Field(None)
    


class OutputROI(MetricsOutput):
    
    shapes: Optional[List[Shape]] = Field(default_factory=list)
    name: str = Field(None)
    description: str = Field(None)
    


class Shape(ConfiguredBaseModel):
    
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Color(ConfiguredBaseModel):
    
    R: int = Field(None, ge=0, le=255)
    G: int = Field(None, ge=0, le=255)
    B: int = Field(None, ge=0, le=255)
    alpha: Optional[int] = Field(None, ge=0, le=255)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Sample.update_forward_refs()
Protocol.update_forward_refs()
Experimenter.update_forward_refs()
Data.update_forward_refs()
Metadata.update_forward_refs()
MetricsDataset.update_forward_refs()
MetricsOutput.update_forward_refs()
OutputImage.update_forward_refs()
OutputROI.update_forward_refs()
Shape.update_forward_refs()
Color.update_forward_refs()

