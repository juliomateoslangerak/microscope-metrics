# Slot: description


_A description of an entity_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:description](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:description)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[NamedObject](NamedObject.md) | An object with a name and a description |  no  |
[ArgolightBDataset](ArgolightBDataset.md) | An Argolight sample pattern B dataset |  no  |
[ArgolightEDataset](ArgolightEDataset.md) | An Argolight sample pattern E dataset |  no  |
[MetricsObject](MetricsObject.md) | A base object for all microscope-metrics objects |  no  |
[Sample](Sample.md) | A sample is a standard physical object that is imaged by a microscope |  no  |
[Protocol](Protocol.md) | Set of instructions for preparing and imaging a sample |  no  |
[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |  no  |
[Image](Image.md) | A base object for all microscope-metrics images |  no  |
[ImageAsNumpy](ImageAsNumpy.md) | An image as a numpy array in TZYXC order |  no  |
[ImageInline](ImageInline.md) | A base object for all microscope-metrics images that are stored as arrays in ... |  no  |
[ImageMask](ImageMask.md) | A base object for all microscope-metrics masks |  no  |
[Image2D](Image2D.md) | A 2D image in YX order |  no  |
[Image5D](Image5D.md) | A 5D image in TZYXC order |  no  |
[ROI](ROI.md) | A ROI |  no  |
[Tag](Tag.md) | A tag |  no  |
[Table](Table.md) | A table |  no  |
[TableAsPandasDF](TableAsPandasDF.md) | A table as a Pandas DataFrame |  no  |
[TableAsDict](TableAsDict.md) | A table inlined in a metrics dataset |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: description
description: A description of an entity
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
alias: description
domain_of:
- NamedObject
- ROI
- Tag
range: string

```
</details>