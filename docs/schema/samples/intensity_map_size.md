# Slot: intensity_map_size


_Input parameter: the size of the output intensity map in pixels_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:intensity_map_size](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:intensity_map_size)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[FieldIlluminationInput](FieldIlluminationInput.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)

* Required: True

* Minimum Value: 5

* Maximum Value: 512





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: intensity_map_size
description: 'Input parameter: the size of the output intensity map in pixels'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
ifabsent: int(64)
alias: intensity_map_size
domain_of:
- FieldIlluminationInput
range: integer
required: true
minimum_value: 5
maximum_value: 512

```
</details>