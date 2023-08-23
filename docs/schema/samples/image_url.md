# Slot: image_url


_An URL linking to the image_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:image_url](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:image_url)



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

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: image_url
description: An URL linking to the image
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
identifier: true
alias: image_url
domain_of:
- Image
range: string
required: true

```
</details>