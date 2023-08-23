# Slot: upper_threshold_correction_factors


_Input parameter: correction factor for the upper thresholds. Must be a tuple with len = nr of channels or a float if all equal_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:upper_threshold_correction_factors](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:upper_threshold_correction_factors)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBInput](ArgolightBInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: upper_threshold_correction_factors
description: 'Input parameter: correction factor for the upper thresholds. Must be
  a tuple with len = nr of channels or a float if all equal'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: true
alias: upper_threshold_correction_factors
domain_of:
- ArgolightBInput
range: float
required: false

```
</details>