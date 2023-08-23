# Slot: field_illumination_image


_Input parameter: homogeneity image provided as a numpy array in the order. While the analysis accepts multiple channels, the T and Z dimensions are expected to be 1._



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:field_illumination_image](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:field_illumination_image)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[FieldIlluminationInput](FieldIlluminationInput.md) |  |  no  |







## Properties

* Range: [ImageAsNumpy](ImageAsNumpy.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: field_illumination_image
description: 'Input parameter: homogeneity image provided as a numpy array in the
  order. While the analysis accepts multiple channels, the T and Z dimensions are
  expected to be 1.'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
alias: field_illumination_image
domain_of:
- FieldIlluminationInput
range: ImageAsNumpy
required: true
inlined: true

```
</details>