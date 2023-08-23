# Slot: center_threshold


_Input parameter: relative threshold for what is going to be considered as the intensity center of the image_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:center_threshold](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:center_threshold)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[FieldIlluminationInput](FieldIlluminationInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 1





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: center_threshold
description: 'Input parameter: relative threshold for what is going to be considered
  as the intensity center of the image'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(0.9)
alias: center_threshold
domain_of:
- FieldIlluminationInput
range: float
required: true
minimum_value: 0
maximum_value: 1

```
</details>