# Slot: corner_fraction


_Input parameter: the proportion of the image to be considered as corner or center_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:corner_fraction](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:corner_fraction)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[FieldIlluminationInput](FieldIlluminationInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 0





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: corner_fraction
description: 'Input parameter: the proportion of the image to be considered as corner
  or center'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(0.1)
alias: corner_fraction
domain_of:
- FieldIlluminationInput
range: float
required: true
minimum_value: 0
maximum_value: 0

```
</details>