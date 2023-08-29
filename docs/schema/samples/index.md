# microscopemetrics_samples_field_illumination_schema



URI: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml

Name: microscopemetrics_samples_field_illumination_schema



## Classes

| Class | Description |
| --- | --- |
| [ChannelSeries](ChannelSeries.md) | A series whose values represent channel |
| [Color](Color.md) | A color as defined by RGB values and an optional alpha value |
| [Column](Column.md) | A column |
| [Comment](Comment.md) | A comment |
| [Experimenter](Experimenter.md) | The person that performed the experiment or developed the protocol |
| [KeyValues](KeyValues.md) | A collection of key-value pairs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FieldIlluminationKeyValues](FieldIlluminationKeyValues.md) | None |
| [MetaObject](MetaObject.md) | None |
| [MetricsInput](MetricsInput.md) | An abstract class for analysis inputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FieldIlluminationInput](FieldIlluminationInput.md) | None |
| [MetricsOutput](MetricsOutput.md) | An abstract class for analysis outputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FieldIlluminationOutput](FieldIlluminationOutput.md) | None |
| [NamedObject](NamedObject.md) | An object with a name and a description |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FieldIlluminationDataset](FieldIlluminationDataset.md) | A field illumination dataset |
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
| [Roi](Roi.md) | A ROI. Collection of shapes and an image to which they are applied |
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
| [acquisition_date](acquisition_date.md) | The date of the acquisition |
| [alpha](alpha.md) |  |
| [authors](authors.md) | The authors of the protocol |
| [b](b.md) |  |
| [bit_depth](bit_depth.md) | Detector bit depth |
| [bottom_center_intensity_mean](bottom_center_intensity_mean.md) | The mean intensity of the bottom-center of the image |
| [bottom_center_intensity_ratio](bottom_center_intensity_ratio.md) | The mean intensity of the bottom-center of the image  divided by the maximum ... |
| [bottom_left_intensity_mean](bottom_left_intensity_mean.md) | The mean intensity of the bottom-left of the image |
| [bottom_left_intensity_ratio](bottom_left_intensity_ratio.md) | The mean intensity of the bottom-left of the image  divided by the maximum in... |
| [bottom_right_intensity_mean](bottom_right_intensity_mean.md) | The mean intensity of the bottom-right of the image |
| [bottom_right_intensity_ratio](bottom_right_intensity_ratio.md) | The mean intensity of the bottom-right of the image  divided by the maximum i... |
| [c](c.md) |  |
| [center_of_mass_x](center_of_mass_x.md) | The x coordinate of the center of mass of the center of illumination region |
| [center_of_mass_y](center_of_mass_y.md) | The y coordinate of the center of mass of the center of illumination region |
| [center_threshold](center_threshold.md) | Input parameter: relative threshold for what is going to be considered as the... |
| [channel](channel.md) | The channel number to which the measurements apply |
| [columns](columns.md) |  |
| [comment](comment.md) | A human readable comment about the dataset |
| [corner_fraction](corner_fraction.md) | Input parameter: the proportion of the image to be considered as corner or ce... |
| [data](data.md) |  |
| [decile_0](decile_0.md) | The 0th decile of the intensity distribution of the maximum intensity |
| [decile_1](decile_1.md) | The 1st decile of the intensity distribution of the maximum intensity |
| [decile_2](decile_2.md) | The 2nd decile of the intensity distribution of the maximum intensity |
| [decile_3](decile_3.md) | The 3rd decile of the intensity distribution of the maximum intensity |
| [decile_4](decile_4.md) | The 4th decile of the intensity distribution of the maximum intensity |
| [decile_5](decile_5.md) | The 5th decile of the intensity distribution of the maximum intensity |
| [decile_6](decile_6.md) | The 6th decile of the intensity distribution of the maximum intensity |
| [decile_7](decile_7.md) | The 7th decile of the intensity distribution of the maximum intensity |
| [decile_8](decile_8.md) | The 8th decile of the intensity distribution of the maximum intensity |
| [decile_9](decile_9.md) | The 9th decile of the intensity distribution of the maximum intensity |
| [description](description.md) | A description of an entity |
| [df](df.md) |  |
| [experimenter](experimenter.md) | The experimenter that performed the imaging experiment |
| [field_illumination_image](field_illumination_image.md) | Input parameter: homogeneity image provided as a numpy array in the order |
| [fill_color](fill_color.md) |  |
| [g](g.md) |  |
| [h](h.md) |  |
| [id](id.md) | The unique identifier for an entity |
| [image](image.md) |  |
| [image_url](image_url.md) | An URL linking to the image |
| [input](input.md) |  |
| [intensity_map](intensity_map.md) | Intensity map of the field illumination |
| [intensity_map_size](intensity_map_size.md) | Input parameter: the size of the output intensity map in pixels |
| [intensity_profiles](intensity_profiles.md) | Intensity profiles for the field illumination analysis in the different direc... |
| [is_open](is_open.md) |  |
| [key_values](key_values.md) | Key-Value pairs containing the Key measurements for the field illumination an... |
| [label](label.md) |  |
| [mask](mask.md) |  |
| [max_intensity](max_intensity.md) | The maximum intensity of the center of illumination |
| [max_intensity_pos_x](max_intensity_pos_x.md) | The x coordinate of the maximum intensity of the center of illumination |
| [max_intensity_pos_y](max_intensity_pos_y.md) | The y coordinate of the maximum intensity of the center of illumination |
| [middle_center_intensity_mean](middle_center_intensity_mean.md) | The mean intensity of the middle-center of the image |
| [middle_center_intensity_ratio](middle_center_intensity_ratio.md) | The mean intensity of the middle-center of the image  divided by the maximum ... |
| [middle_left_intensity_mean](middle_left_intensity_mean.md) | The mean intensity of the middle-left of the image |
| [middle_left_intensity_ratio](middle_left_intensity_ratio.md) | The mean intensity of the middle-left of the image  divided by the maximum in... |
| [middle_right_intensity_mean](middle_right_intensity_mean.md) | The mean intensity of the middle-right of the image |
| [middle_right_intensity_ratio](middle_right_intensity_ratio.md) | The mean intensity of the middle-right of the image  divided by the maximum i... |
| [name](name.md) | The name of an entity |
| [nb_pixels](nb_pixels.md) | The area occupied by the center of illumination region |
| [orcid](orcid.md) | The ORCID of the experimenter |
| [output](output.md) |  |
| [processed](processed.md) | Has the dataset been processed by microscope-metrics |
| [processing_date](processing_date.md) | The date of the processing by microscope-metrics |
| [processing_log](processing_log.md) | The log of the processing by microscope-metrics |
| [profile_rois](profile_rois.md) | Output: ROIs used to compute the intensity profile |
| [protocol](protocol.md) | The protocol used to prepare the sample |
| [r](r.md) |  |
| [sample](sample.md) | The sample that was imaged |
| [saturation_threshold](saturation_threshold.md) | Tolerated saturation threshold |
| [shapes](shapes.md) |  |
| [sigma](sigma.md) | Input parameter: the sigma for the smoothing gaussian filter to be applied pr... |
| [source_image_url](source_image_url.md) | A list of URLs linking to the images that were used as a source |
| [stroke_color](stroke_color.md) |  |
| [stroke_width](stroke_width.md) |  |
| [t](t.md) |  |
| [text](text.md) |  |
| [top_center_intensity_mean](top_center_intensity_mean.md) | The mean intensity of the top-center of the image |
| [top_center_intensity_ratio](top_center_intensity_ratio.md) | The mean intensity of the top-center of the image  divided by the maximum int... |
| [top_left_intensity_mean](top_left_intensity_mean.md) | The mean intensity of the top-left corner of the image |
| [top_left_intensity_ratio](top_left_intensity_ratio.md) | The mean intensity of the top-left corner of the image  divided by the maximu... |
| [top_right_intensity_mean](top_right_intensity_mean.md) | The mean intensity of the top-right corner of the image |
| [top_right_intensity_ratio](top_right_intensity_ratio.md) | The mean intensity of the top-right corner of the image  divided by the maxim... |
| [type](type.md) | The type of the sample |
| [url](url.md) | The URL where the protocol can be found |
| [values](values.md) |  |
| [version](version.md) | The version of the protocol |
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
