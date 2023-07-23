from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class NamedObject(ConfiguredBaseModel):
    """
    An object with a name and a description
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class MetricsObject(NamedObject):
    """
    A base object for all microscope-metrics objects
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Sample(NamedObject):
    """
    A sample is a standard physical object that is imaged by a microscope
    """
    type: str = Field(...)
    protocol: Protocol = Field(...)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Protocol(NamedObject):
    """
    Set of instructions for preparing and imaging a sample
    """
    version: str = Field(...)
    authors: Optional[List[str]] = Field(default_factory=list)
    url: str = Field(...)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Experimenter(ConfiguredBaseModel):
    """
    The person that performed the experiment or developed the protocol
    """
    name: Optional[str] = Field(None, description="""The name of the experimenter""")
    orcid: str = Field(..., description="""The ORCID of the experimenter""")
    


class MetricsDataset(NamedObject):
    """
    A base object on which microscope-metrics runs the analysis
    """
    sample: Optional[List[Sample]] = Field(default_factory=list)
    experimenter: Optional[List[str]] = Field(default_factory=list)
    data: List[MetricsData] = Field(default_factory=list)
    metadata: Optional[List[MetricsMetadata]] = Field(default_factory=list)
    output: Optional[List[MetricsOutput]] = Field(default_factory=list)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class MetricsInput(MetricsObject):
    """
    A base object for all microscope-metrics inputs
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class MetricsData(MetricsInput):
    """
    A base object for all microscope-metrics input data
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class MetricsMetadata(MetricsInput):
    """
    A base object for all microscope-metrics input metadata
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class MetricsOutput(MetricsObject):
    """
    A base object for all microscope-metrics outputs
    """
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Image(ConfiguredBaseModel):
    """
    A base object for all microscope-metrics output images
    """
    name: str = Field(...)
    data: List[Union[float, int]] = Field(default_factory=list)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    


class ImageMask(Image):
    """
    A base object for all microscope-metrics output masks
    """
    x_position: Optional[float] = Field(None)
    y_position: Optional[float] = Field(None)
    x: PixelSeries = Field(...)
    y: PixelSeries = Field(...)
    data: Optional[bool] = Field(None)
    name: str = Field(...)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    


class Image2D(Image):
    """
    A 2D image in XY order
    """
    x: PixelSeries = Field(...)
    y: PixelSeries = Field(...)
    name: str = Field(...)
    data: List[Union[float, int]] = Field(default_factory=list)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    


class MetricsOutputImage2D(Image2D, MetricsOutput):
    """
    A microscope-metrics output 2Dimage
    """
    x: PixelSeries = Field(...)
    y: PixelSeries = Field(...)
    name: str = Field(...)
    data: List[Union[float, int]] = Field(default_factory=list)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    description: str = Field(..., description="""A description of an entity""")
    


class Image5D(Image):
    """
    A 5D image in TZYXC order
    """
    t: TimeSeries = Field(...)
    z: PixelSeries = Field(...)
    y: PixelSeries = Field(...)
    x: PixelSeries = Field(...)
    c: ChannelSeries = Field(...)
    name: str = Field(...)
    data: List[Union[float, int]] = Field(default_factory=list)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    


class MetricsOutputImage5D(Image5D, MetricsOutput):
    """
    A microscope-metrics output 5Dimage
    """
    t: TimeSeries = Field(...)
    z: PixelSeries = Field(...)
    y: PixelSeries = Field(...)
    x: PixelSeries = Field(...)
    c: ChannelSeries = Field(...)
    name: str = Field(...)
    data: List[Union[float, int]] = Field(default_factory=list)
    roi: Optional[List[ROI]] = Field(default_factory=list)
    description: str = Field(..., description="""A description of an entity""")
    


class PixelSeries(ConfiguredBaseModel):
    """
    A series whose values represent pixels or voxels
    """
    values: List[int] = Field(default_factory=list)
    


class Channel(ConfiguredBaseModel):
    """
    A channel
    """
    name: Optional[str] = Field(None)
    rendering_color: Optional[Color] = Field(None)
    emission_wavelength: Optional[float] = Field(None)
    excitation_wavelength: Optional[float] = Field(None)
    


class ChannelSeries(ConfiguredBaseModel):
    """
    A series whose values represent channel
    """
    values: List[Channel] = Field(default_factory=list)
    


class TimeSeries(ConfiguredBaseModel):
    """
    A series whose values represent time
    """
    values: List[float] = Field(default_factory=list)
    


class ROI(ConfiguredBaseModel):
    """
    A ROI. Collection of shapes
    """
    shapes: Optional[List[Shape]] = Field(default_factory=list)
    


class Shape(ConfiguredBaseModel):
    """
    A shape
    """
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Point(Shape):
    """
    A point as defined by x and y coordinates
    """
    x: Optional[float] = Field(None)
    y: Optional[float] = Field(None)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Line(Shape):
    """
    A line as defined by x1, y1, x2, y2 coordinates
    """
    x1: Optional[float] = Field(None)
    y1: Optional[float] = Field(None)
    x2: Optional[float] = Field(None)
    x3: Optional[float] = Field(None)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Rectangle(Shape):
    """
    A rectangle as defined by x, y coordinates and width, height
    """
    x: Optional[float] = Field(None)
    y: Optional[float] = Field(None)
    w: Optional[float] = Field(None)
    h: Optional[float] = Field(None)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Ellipse(Shape):
    """
    An ellipse as defined by x, y coordinates and x and y radii
    """
    x: Optional[float] = Field(None)
    y: Optional[float] = Field(None)
    x_rad: Optional[float] = Field(None)
    y_rad: Optional[float] = Field(None)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Polygon(Shape):
    """
    A polygon as defined by a series of vertexes and a boolean to indicate if closed or not
    """
    vertexes: List[Vertex] = Field(default_factory=list)
    is_open: Optional[bool] = Field(False)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Vertex(ConfiguredBaseModel):
    """
    A vertex as defined by x and y coordinates
    """
    x: float = Field(...)
    y: float = Field(...)
    


class Mask(Shape):
    """
    A mask as defined by a boolean image
    """
    mask: Optional[str] = Field(None)
    z: Optional[float] = Field(None)
    c: Optional[int] = Field(None)
    t: Optional[int] = Field(None)
    fill_color: Optional[Color] = Field(None)
    stroke_color: Optional[Color] = Field(None)
    stroke_width: Optional[int] = Field(None)
    


class Color(ConfiguredBaseModel):
    """
    A color as defined by RGB values and an optional alpha value
    """
    R: int = Field(..., ge=0, le=255)
    G: int = Field(..., ge=0, le=255)
    B: int = Field(..., ge=0, le=255)
    alpha: Optional[int] = Field(None, ge=0, le=255)
    


class KeyValuesCollection(ConfiguredBaseModel):
    """
    A collection of key-value pairs
    """
    key_values: Dict[str, KeyValuePair] = Field(default_factory=dict)
    


class MetricsOutputKeyValues(KeyValuesCollection, MetricsOutput):
    """
    A microscope-metrics output collection of key-value pairs
    """
    key_values: Dict[str, KeyValuePair] = Field(default_factory=dict)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class KeyValuePair(ConfiguredBaseModel):
    """
    A key-value pair
    """
    name: str = Field(...)
    value: Optional[str] = Field(None)
    


class Tag(ConfiguredBaseModel):
    """
    A tag
    """
    id: int = Field(...)
    text: str = Field(...)
    description: Optional[str] = Field(None)
    


class MetricsOutputTag(Tag, MetricsOutput):
    """
    A microscope-metrics output tag
    """
    id: int = Field(...)
    text: str = Field(...)
    description: Optional[str] = Field(None)
    name: str = Field(..., description="""The name of an entity""")
    


class Comment(ConfiguredBaseModel):
    """
    A comment
    """
    text: str = Field(...)
    


class MetricsOutputComment(Comment, MetricsOutput):
    """
    A microscope-metrics output comment
    """
    text: str = Field(...)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Table(ConfiguredBaseModel):
    """
    A table
    """
    columns: List[Column] = Field(default_factory=list)
    


class MetricsOutputTable(Table, MetricsOutput):
    """
    A microscope-metrics output collection of tables
    """
    columns: List[Column] = Field(default_factory=list)
    name: str = Field(..., description="""The name of an entity""")
    description: str = Field(..., description="""A description of an entity""")
    


class Column(ConfiguredBaseModel):
    """
    A column
    """
    name: str = Field(...)
    values: List[str] = Field(default_factory=list)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
NamedObject.update_forward_refs()
MetricsObject.update_forward_refs()
Sample.update_forward_refs()
Protocol.update_forward_refs()
Experimenter.update_forward_refs()
MetricsDataset.update_forward_refs()
MetricsInput.update_forward_refs()
MetricsData.update_forward_refs()
MetricsMetadata.update_forward_refs()
MetricsOutput.update_forward_refs()
Image.update_forward_refs()
ImageMask.update_forward_refs()
Image2D.update_forward_refs()
MetricsOutputImage2D.update_forward_refs()
Image5D.update_forward_refs()
MetricsOutputImage5D.update_forward_refs()
PixelSeries.update_forward_refs()
Channel.update_forward_refs()
ChannelSeries.update_forward_refs()
TimeSeries.update_forward_refs()
ROI.update_forward_refs()
Shape.update_forward_refs()
Point.update_forward_refs()
Line.update_forward_refs()
Rectangle.update_forward_refs()
Ellipse.update_forward_refs()
Polygon.update_forward_refs()
Vertex.update_forward_refs()
Mask.update_forward_refs()
Color.update_forward_refs()
KeyValuesCollection.update_forward_refs()
MetricsOutputKeyValues.update_forward_refs()
KeyValuePair.update_forward_refs()
Tag.update_forward_refs()
MetricsOutputTag.update_forward_refs()
Comment.update_forward_refs()
MetricsOutputComment.update_forward_refs()
Table.update_forward_refs()
MetricsOutputTable.update_forward_refs()
Column.update_forward_refs()

