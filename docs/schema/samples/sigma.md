# Slot: sigma


_Input parameter: the sigma for the smoothing gaussian filter to be applied prior to analysis_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:sigma](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml/:sigma)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[FieldIlluminationInput](FieldIlluminationInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 100





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml




## LinkML Source

<details>
```yaml
name: sigma
description: 'Input parameter: the sigma for the smoothing gaussian filter to be applied
  prior to analysis'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/field_illumination_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(2.0)
alias: sigma
domain_of:
- FieldIlluminationInput
range: float
required: true
minimum_value: 0
maximum_value: 100

```
</details>