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
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PSFBeadsKeyMeasurements](PSFBeadsKeyMeasurements.md) | None |
| [MetaObject](MetaObject.md) | None |
| [MetricsInput](MetricsInput.md) | An abstract class for analysis inputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PSFBeadsInput](PSFBeadsInput.md) | None |
| [MetricsOutput](MetricsOutput.md) | An abstract class for analysis outputs |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PSFBeadsOutput](PSFBeadsOutput.md) | None |
| [NamedObject](NamedObject.md) | An object with a name and a description |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PSFBeadsDataset](PSFBeadsDataset.md) | A dataset of PSF beads dataset
 |
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
| [authors](authors.md) | The authors of the protocol |
| [b](b.md) | The blue value of the color |
| [bead_centroids](bead_centroids.md) | The centroids of the beads |
| [bead_crops](bead_crops.md) | The crops of the beads provided as a 5D numpy array in the order TZYXC |
| [bit_depth](bit_depth.md) | Detector bit depth |
| [c](c.md) |  |
| [cluster_bead_centroids](cluster_bead_centroids.md) | The centroids of the beads detected but discarded as being too intense and po... |
| [columns](columns.md) | A list of the columns of the table |
| [comment](comment.md) | A human readable comment about the dataset |
| [data](data.md) |  |
| [description](description.md) | A description of an entity |
| [df](df.md) | A Pandas DataFrame object |
| [edge_bead_centroids](edge_bead_centroids.md) | The centroids of the beads detected but discarded as too close to the edge of... |
| [experimenter](experimenter.md) | The experimenter that performed the imaging experiment |
| [fill_color](fill_color.md) | The fill color of the shape |
| [g](g.md) | The green value of the color |
| [h](h.md) | The height of the rectangle |
| [id](id.md) | The unique identifier for an entity |
| [image](image.md) | The image to which the ROI is applied |
| [image_url](image_url.md) | An URL linking to the image |
| [input](input.md) | An input element for the PSF beads analysis |
| [is_open](is_open.md) | Is the polygon open |
| [key_measurements](key_measurements.md) | The key measurements of the PSF beads analysis |
| [label](label.md) | The label of the ROI |
| [mask](mask.md) | The mask image |
| [min_lateral_distance_factor](min_lateral_distance_factor.md) | Minimal distance that has to separate laterally the beads represented as the ... |
| [name](name.md) | The name of an entity |
| [nr_of_beads_analyzed](nr_of_beads_analyzed.md) | Number of beads analyzed per channel |
| [nr_of_beads_discarded](nr_of_beads_discarded.md) | Sum of the beads discarded per channel for either being too close to the edge... |
| [orcid](orcid.md) | The ORCID of the experimenter |
| [output](output.md) | An output element for the PSF beads analysis |
| [pixel_size_x](pixel_size_x.md) | Physical size of the voxel in the X axis |
| [pixel_size_y](pixel_size_y.md) | Physical size of the voxel in the Y axis |
| [pixel_size_z](pixel_size_z.md) | Physical size of the voxel in the Z axis |
| [processed](processed.md) | Has the dataset been processed by microscope-metrics |
| [processing_date](processing_date.md) | The date of the processing by microscope-metrics |
| [processing_log](processing_log.md) | The log of the processing by microscope-metrics |
| [protocol](protocol.md) | The protocol used to prepare the sample |
| [psf_beads_image](psf_beads_image.md) | The image containing the beads provided as a 5D numpy array in the order TZYX... |
| [psf_properties](psf_properties.md) | Properties associated with the analysis of the beads |
| [psf_x_profiles](psf_x_profiles.md) | The intensity profiles along the x axis of the beads |
| [psf_y_profiles](psf_y_profiles.md) | The intensity profiles along the y axis of the beads |
| [psf_z_profiles](psf_z_profiles.md) | The intensity profiles along the z axis of the beads |
| [r](r.md) | The red value of the color |
| [resolution_mean_fwhm_x_microns](resolution_mean_fwhm_x_microns.md) | Mean FWHM in the X axis in microns |
| [resolution_mean_fwhm_x_pixels](resolution_mean_fwhm_x_pixels.md) | Mean FWHM in the X axis in pixels |
| [resolution_mean_fwhm_y_microns](resolution_mean_fwhm_y_microns.md) | Mean FWHM in the Y axis in microns |
| [resolution_mean_fwhm_y_pixels](resolution_mean_fwhm_y_pixels.md) | Mean FWHM in the Y axis in pixels |
| [resolution_mean_fwhm_z_microns](resolution_mean_fwhm_z_microns.md) | Mean FWHM in the Z axis in microns |
| [resolution_mean_fwhm_z_pixels](resolution_mean_fwhm_z_pixels.md) | Mean FWHM in the Z axis in pixels |
| [resolution_median_fwhm_x_microns](resolution_median_fwhm_x_microns.md) | Median FWHM in the X axis in microns |
| [resolution_median_fwhm_x_pixels](resolution_median_fwhm_x_pixels.md) | Median FWHM in the X axis in pixels |
| [resolution_median_fwhm_y_microns](resolution_median_fwhm_y_microns.md) | Median FWHM in the Y axis in microns |
| [resolution_median_fwhm_y_pixels](resolution_median_fwhm_y_pixels.md) | Median FWHM in the Y axis in pixels |
| [resolution_median_fwhm_z_microns](resolution_median_fwhm_z_microns.md) | Median FWHM in the Z axis in microns |
| [resolution_median_fwhm_z_pixels](resolution_median_fwhm_z_pixels.md) | Median FWHM in the Z axis in pixels |
| [resolution_stdev_fwhm_x_microns](resolution_stdev_fwhm_x_microns.md) | Standard deviation of the FWHM in the X axis in microns |
| [resolution_stdev_fwhm_x_pixels](resolution_stdev_fwhm_x_pixels.md) | Standard deviation of the FWHM in the X axis in pixels |
| [resolution_stdev_fwhm_y_microns](resolution_stdev_fwhm_y_microns.md) | Standard deviation of the FWHM in the Y axis in microns |
| [resolution_stdev_fwhm_y_pixels](resolution_stdev_fwhm_y_pixels.md) | Standard deviation of the FWHM in the Y axis in pixels |
| [resolution_stdev_fwhm_z_microns](resolution_stdev_fwhm_z_microns.md) | Standard deviation of the FWHM in the Z axis in microns |
| [resolution_stdev_fwhm_z_pixels](resolution_stdev_fwhm_z_pixels.md) | Standard deviation of the FWHM in the Z axis in pixels |
| [sample](sample.md) | The sample that was imaged |
| [saturation_threshold](saturation_threshold.md) | Tolerated saturation threshold |
| [self_proximity_bead_centroids](self_proximity_bead_centroids.md) | The centroids of the beads detected but discarded as too close to another bea... |
| [shapes](shapes.md) |  |
| [sigma_x](sigma_x.md) | When provided, gaussian smoothing sigma to be applied to the image in the X a... |
| [sigma_y](sigma_y.md) | When provided, gaussian smoothing sigma to be applied to the image in teh Y a... |
| [sigma_z](sigma_z.md) | When provided, gaussian smoothing sigma to be applied to the image in the Z a... |
| [source_image_url](source_image_url.md) | A list of URLs linking to the images that were used as a source |
| [stroke_color](stroke_color.md) | The stroke color of the shape |
| [stroke_width](stroke_width.md) | The stroke width of the shape |
| [t](t.md) |  |
| [text](text.md) | The text of the tag |
| [type](type.md) | The type of the sample |
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
