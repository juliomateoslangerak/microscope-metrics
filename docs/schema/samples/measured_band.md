# Slot: measured_band


_Fraction of the image across which intensity profiles are measured_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:measured_band](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:measured_band)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightEInput](ArgolightEInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 1





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: measured_band
description: Fraction of the image across which intensity profiles are measured
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(0.4)
alias: measured_band
domain_of:
- ArgolightEInput
range: float
required: true
minimum_value: 0
maximum_value: 1

```
</details>