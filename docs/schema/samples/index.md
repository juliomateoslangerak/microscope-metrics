# microscopemetrics_samples_argolight_schema



URI: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml

Name: microscopemetrics_samples_argolight_schema



## Classes

| Class | Description |
| --- | --- |
| [ChannelSeries](ChannelSeries.md) | A series whose values represent channel |
| [Color](Color.md) | A color as defined by RGB values and an optional alpha value |
| [Column](Column.md) | A column |
| [Comment](Comment.md) | A comment |
| [Experimenter](Experimenter.md) | The person that performed the experiment or developed the protocol |
| [KeyValues](KeyValues.md) | A collection of key-value pairs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightBDistanceKeyValues](ArgolightBDistanceKeyValues.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightBIntensityKeyValues](ArgolightBIntensityKeyValues.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightEKeyValues](ArgolightEKeyValues.md) | None |
| [MetaObject](MetaObject.md) | None |
| [MetricsInput](MetricsInput.md) | An abstract class for analysis inputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightBInput](ArgolightBInput.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightEInput](ArgolightEInput.md) | None |
| [MetricsOutput](MetricsOutput.md) | An abstract class for analysis outputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightBOutput](ArgolightBOutput.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightEOutput](ArgolightEOutput.md) | None |
| [NamedObject](NamedObject.md) | An object with a name and a description |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightBDataset](ArgolightBDataset.md) | An Argolight sample pattern B dataset |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ArgolightEDataset](ArgolightEDataset.md) | An Argolight sample pattern E dataset.
It contains resolution data on the axis indicated:
- axis 1 = Y resolution = lines along X axis
- axis 2 = X resolution = lines along Y axis |
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
| [alpha](alpha.md) | The alpha value of the color (optional) |
| [argolight_b_image](argolight_b_image.md) | Input parameter: image of the argolight b pattern provided as a 5D numpy arra... |
| [argolight_e_image](argolight_e_image.md) | Image of the argolight e pattern provided as a 5D numpy array in the order TZ... |
| [authors](authors.md) | The authors of the protocol |
| [axis](axis.md) | Axis along which resolution is being measured |
| [b](b.md) | The blue value of the color |
| [bit_depth](bit_depth.md) | Detector bit depth |
| [c](c.md) |  |
| [channel](channel.md) | The channel number to which the measurements apply |
| [channel_A](channel_A.md) | The first channel number to which the measurements apply |
| [channel_B](channel_B.md) | The second channel number to which the measurements apply |
| [columns](columns.md) | A list of the columns of the table |
| [comment](comment.md) | A human readable comment about the dataset |
| [data](data.md) |  |
| [description](description.md) | A description of an entity |
| [df](df.md) | A Pandas DataFrame object |
| [distance_measurements](distance_measurements.md) | Key Distance Measurements on Argolight spots |
| [experimenter](experimenter.md) | The experimenter that performed the imaging experiment |
| [fill_color](fill_color.md) | The fill color of the shape |
| [focus_slice](focus_slice.md) | Z position at which focus has been measured |
| [g](g.md) | The green value of the color |
| [h](h.md) | The height of the rectangle |
| [id](id.md) | The unique identifier for an entity |
| [image](image.md) | The image to which the ROI is applied |
| [image_url](image_url.md) | An URL linking to the image |
| [input](input.md) | An input element for the analysis |
| [intensity_measurements](intensity_measurements.md) | Key Intensity Measurements on Argolight spots |
| [intensity_profiles](intensity_profiles.md) | Intensity profiles of the argolight lines provided as tables |
| [is_open](is_open.md) | Is the polygon open |
| [key_measurements](key_measurements.md) | Key Measurements on Argolight E images |
| [label](label.md) | The label of the ROI |
| [lower_threshold_correction_factors](lower_threshold_correction_factors.md) | Input parameter: correction factor for the lower thresholds |
| [mad_3d_dist](mad_3d_dist.md) | Median absolute deviation of the 3D distances between spots for each permutat... |
| [mad_mean_intensity](mad_mean_intensity.md) | Median absolute deviation of all spots integrated intensity for each channel |
| [mad_z_dist](mad_z_dist.md) | Median absolute deviation of the Z distances between spots for each permutati... |
| [mask](mask.md) | The mask image |
| [max_intensity](max_intensity.md) | Integrated intensity of the most intense spot for each channel |
| [max_intensity_roi](max_intensity_roi.md) | ROI number of the most intense spot for each channel |
| [mean_3d_dist](mean_3d_dist.md) | Mean of the 3D distances between spots for each permutation of channel A and ... |
| [mean_intensity](mean_intensity.md) | Mean of all spots integrated intensity for each channel |
| [mean_z_dist](mean_z_dist.md) | Mean of the Z distances between spots for each permutation of channel A and B |
| [measured_band](measured_band.md) | Fraction of the image across which intensity profiles are measured |
| [median_3d_dist](median_3d_dist.md) | Median of the 3D distances between spots for each permutation of channel A an... |
| [median_intensity](median_intensity.md) | Median of all spots integrated intensity for each channel |
| [median_z_dist](median_z_dist.md) | Median of the Z distances between spots for each permutation of channel A and... |
| [min_intensity](min_intensity.md) | Integrated intensity of the least intense spot for each channel |
| [min_intensity_roi](min_intensity_roi.md) | ROI number of the least intense spot for each channel |
| [min_max_intensity_ratio](min_max_intensity_ratio.md) | Ratio between the integrated intensities between the most intense and the lea... |
| [name](name.md) | The name of an entity |
| [nr_of_spots](nr_of_spots.md) | Number of argolight spots detected for each channel |
| [orcid](orcid.md) | The ORCID of the experimenter |
| [output](output.md) | An output element from the analysis |
| [peak_height_A](peak_height_A.md) | Height of first peak in the intensity profiles |
| [peak_height_B](peak_height_B.md) | Height of second peak in the intensity profiles |
| [peak_position_A](peak_position_A.md) | Position of first peak in the intensity profiles |
| [peak_position_B](peak_position_B.md) | Position of second peak in the intensity profiles |
| [peak_prominence_A](peak_prominence_A.md) | Prominence of first peak in the intensity profiles |
| [peak_prominence_B](peak_prominence_B.md) | Prominence of second peak in the intensity profiles |
| [peaks_rois](peaks_rois.md) | ROIs of the peaks found in the argolight images |
| [processed](processed.md) | Has the dataset been processed by microscope-metrics |
| [processing_date](processing_date.md) | The date of the processing by microscope-metrics |
| [processing_log](processing_log.md) | The log of the processing by microscope-metrics |
| [prominence_threshold](prominence_threshold.md) | Peak prominence used as a threshold to distinguish two peaks |
| [protocol](protocol.md) | The protocol used to prepare the sample |
| [r](r.md) | The red value of the color |
| [rayleigh_resolution](rayleigh_resolution.md) | Rayleigh resolution measured |
| [remove_center_cross](remove_center_cross.md) | Input parameter: remove the center cross found in some Argolight patterns |
| [sample](sample.md) | The sample that was imaged |
| [saturation_threshold](saturation_threshold.md) | Tolerated saturation threshold |
| [shapes](shapes.md) |  |
| [sigma_x](sigma_x.md) | Input parameter: smoothing factor for objects detection in the X axis |
| [sigma_y](sigma_y.md) | Input parameter: smoothing factor for objects detection in the Y axis |
| [sigma_z](sigma_z.md) | Input parameter: smoothing factor for objects detection in the Z axis |
| [source_image_url](source_image_url.md) | A list of URLs linking to the images that were used as a source |
| [spots_centroids](spots_centroids.md) | Centroids of the argolight spots provided as a list of ROIs, one per channel |
| [spots_distance](spots_distance.md) | Input parameter: distance between argolight spots |
| [spots_distances](spots_distances.md) | Table of distances between argolight spots |
| [spots_labels_image](spots_labels_image.md) | Labels image of the argolight segmented spots provided as a 5D numpy array in... |
| [spots_properties](spots_properties.md) | Table of properties of the argolight spots |
| [std_3d_dist](std_3d_dist.md) | Standard deviation of the 3D distances between spots for each permutation of ... |
| [std_mean_intensity](std_mean_intensity.md) | Standard deviation of all spots integrated intensity for each channel |
| [std_z_dist](std_z_dist.md) | Standard deviation of the Z distances between spots for each permutation of c... |
| [stroke_color](stroke_color.md) | The stroke color of the shape |
| [stroke_width](stroke_width.md) | The stroke width of the shape |
| [t](t.md) |  |
| [text](text.md) | The text of the tag |
| [type](type.md) | The type of the sample |
| [upper_threshold_correction_factors](upper_threshold_correction_factors.md) | Input parameter: correction factor for the upper thresholds |
| [url](url.md) | The URL where the protocol can be found |
| [values](values.md) |  |
| [version](version.md) | The version of the protocol |
| [vertexes](vertexes.md) | A list of vertexes defining the polygon |
| [w](w.md) | The width of the rectangle |
| [x](x.md) |  |
| [x1](x1.md) | The x coordinate of the first point of the line |
| [x2](x2.md) | The x coordinate of the second point of the line |
| [x_rad](x_rad.md) | The x radius of the ellipse |
| [y](y.md) |  |
| [y1](y1.md) | The y coordinate of the first point of the line |
| [y2](y2.md) | The y coordinate of the second point of the line |
| [y_rad](y_rad.md) | The y radius of the ellipse |
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
