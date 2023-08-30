# Slot: source_image_url


_A list of URLs linking to the images that were used as a source_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:source_image_url](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:source_image_url)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Image](Image.md) | A base object for all microscope-metrics images |  no  |
[ImageAsNumpy](ImageAsNumpy.md) | An image as a numpy array in TZYXC order |  no  |
[ImageInline](ImageInline.md) | A base object for all microscope-metrics images that are stored as arrays in ... |  no  |
[ImageMask](ImageMask.md) | A base object for all microscope-metrics masks |  no  |
[Image2D](Image2D.md) | A 2D image in YX order |  no  |
[Image5D](Image5D.md) | A 5D image in TZYXC order |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: source_image_url
description: A list of URLs linking to the images that were used as a source
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: true
alias: source_image_url
domain_of:
- Image
range: string
required: false

```
</details>