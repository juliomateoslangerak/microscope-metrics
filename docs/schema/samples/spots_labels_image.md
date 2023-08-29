# Slot: spots_labels_image


_Labels image of the argolight segmented spots provided as a 5D numpy array in the order TZYXC. Image intensities correspond to ROI labels_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:spots_labels_image](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:spots_labels_image)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBOutput](ArgolightBOutput.md) |  |  no  |







## Properties

* Range: [ImageAsNumpy](ImageAsNumpy.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: spots_labels_image
description: Labels image of the argolight segmented spots provided as a 5D numpy
  array in the order TZYXC. Image intensities correspond to ROI labels
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
alias: spots_labels_image
owner: ArgolightBOutput
domain_of:
- ArgolightBOutput
range: ImageAsNumpy
required: false

```
</details>