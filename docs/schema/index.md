# microscopemetrics_core_schema



URI: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml

Name: microscopemetrics_core_schema



## Classes

| Class | Description |
| --- | --- |
| [ChannelSeries](ChannelSeries.md) | A series whose values represent channel |
| [Color](Color.md) | A color as defined by RGB values and an optional alpha value |
| [Column](Column.md) | A column |
| [Comment](Comment.md) | A comment |
| [Experimenter](Experimenter.md) | The person that performed the experiment or developed the protocol |
| [KeyValues](KeyValues.md) | A collection of key-value pairs |
| [MetaObject](MetaObject.md) | None |
| [MetricsInput](MetricsInput.md) | An abstract class for analysis inputs |
| [MetricsOutput](MetricsOutput.md) | An abstract class for analysis outputs |
| [NamedObject](NamedObject.md) | An object with a name and a description |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetricsObject](MetricsObject.md) | A base object for all microscope-metrics objects |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Image](Image.md) | A base object for all microscope-metrics images |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ImageAsNumpy](ImageAsNumpy.md) | An image as a numpy array in TZYXC order |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ImageInline](ImageInline.md) | A base object for all microscope-metrics images that are stored as arrays in line |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Image2D](Image2D.md) | A 2D image in YX order |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Image5D](Image5D.md) | A 5D image in TZYXC order |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ImageMask](ImageMask.md) | A base object for all microscope-metrics masks |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Table](Table.md) | A table |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TableAsDict](TableAsDict.md) | A table inlined in a metrics dataset |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TableAsPandasDF](TableAsPandasDF.md) | A table as a Pandas DataFrame |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Protocol](Protocol.md) | Set of instructions for preparing and imaging a sample |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Sample](Sample.md) | A sample is a standard physical object that is imaged by a microscope |
| [PixelSeries](PixelSeries.md) | A series whose values represent pixels or voxels or a single integer defining the shape of the dimension |
| [ROI](ROI.md) | A ROI. Collection of shapes and an image to which they are applied |
| [Shape](Shape.md) | A shape |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Ellipse](Ellipse.md) | An ellipse as defined by x, y coordinates and x and y radii |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Line](Line.md) | A line as defined by x1, y1, x2, y2 coordinates |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Mask](Mask.md) | A mask as defined by a boolean image |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Point](Point.md) | A point as defined by x and y coordinates |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Polygon](Polygon.md) | A polygon as defined by a series of vertexes and a boolean to indicate if closed or not |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Rectangle](Rectangle.md) | A rectangle as defined by x, y coordinates and width, height |
| [Tag](Tag.md) | A tag |
| [TimeSeries](TimeSeries.md) | A series whose values represent time |
| [Vertex](Vertex.md) | A vertex as defined by x and y coordinates |



## Slots

| Slot | Description |
| --- | --- |
| [acquisition_date](acquisition_date.md) |  |
| [alpha](alpha.md) |  |
| [authors](authors.md) |  |
| [b](b.md) |  |
| [bit_depth](bit_depth.md) | Detector bit depth |
| [c](c.md) |  |
| [columns](columns.md) |  |
| [data](data.md) |  |
| [description](description.md) | A description of an entity |
| [df](df.md) |  |
| [experimenter](experimenter.md) |  |
| [fill_color](fill_color.md) |  |
| [g](g.md) |  |
| [h](h.md) |  |
| [id](id.md) | The unique identifier for an entity |
| [image](image.md) |  |
| [image_url](image_url.md) | An URL linking to the image |
| [is_open](is_open.md) |  |
| [label](label.md) |  |
| [mask](mask.md) |  |
| [name](name.md) | The name of an entity |
| [orcid](orcid.md) | The ORCID of the experimenter |
| [processed](processed.md) |  |
| [processing_date](processing_date.md) |  |
| [processing_log](processing_log.md) |  |
| [protocol](protocol.md) |  |
| [r](r.md) |  |
| [sample](sample.md) |  |
| [saturation_threshold](saturation_threshold.md) | Tolerated saturation threshold |
| [shapes](shapes.md) |  |
| [source_image_url](source_image_url.md) | A list of URLs linking to the images that were used as a source |
| [stroke_color](stroke_color.md) |  |
| [stroke_width](stroke_width.md) |  |
| [t](t.md) |  |
| [text](text.md) |  |
| [type](type.md) |  |
| [url](url.md) |  |
| [values](values.md) |  |
| [version](version.md) |  |
| [vertexes](vertexes.md) |  |
| [w](w.md) |  |
| [x](x.md) |  |
| [x1](x1.md) |  |
| [x2](x2.md) |  |
| [x_rad](x_rad.md) |  |
| [y](y.md) |  |
| [y1](y1.md) |  |
| [y2](y2.md) |  |
| [y_rad](y_rad.md) |  |
| [z](z.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
