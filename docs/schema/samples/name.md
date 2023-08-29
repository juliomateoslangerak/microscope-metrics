# Slot: name


_The name of an entity_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:name](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:name)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[NamedObject](NamedObject.md) | An object with a name and a description |  no  |
[FieldIlluminationDataset](FieldIlluminationDataset.md) | A field illumination dataset |  no  |
[MetricsObject](MetricsObject.md) | A base object for all microscope-metrics objects |  no  |
[Sample](Sample.md) | A sample is a standard physical object that is imaged by a microscope |  no  |
[Protocol](Protocol.md) | Set of instructions for preparing and imaging a sample |  no  |
[Experimenter](Experimenter.md) | The person that performed the experiment or developed the protocol |  no  |
[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |  no  |
[Image](Image.md) | A base object for all microscope-metrics images |  no  |
[ImageAsNumpy](ImageAsNumpy.md) | An image as a numpy array in TZYXC order |  no  |
[ImageInline](ImageInline.md) | A base object for all microscope-metrics images that are stored as arrays in ... |  no  |
[ImageMask](ImageMask.md) | A base object for all microscope-metrics masks |  no  |
[Image2D](Image2D.md) | A 2D image in YX order |  no  |
[Image5D](Image5D.md) | A 5D image in TZYXC order |  no  |
[Table](Table.md) | A table |  no  |
[TableAsPandasDF](TableAsPandasDF.md) | A table as a Pandas DataFrame |  no  |
[TableAsDict](TableAsDict.md) | A table inlined in a metrics dataset |  no  |
[Column](Column.md) | A column |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: name
description: The name of an entity
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
alias: name
domain_of:
- NamedObject
- Experimenter
- Column
range: string
required: false

```
</details>