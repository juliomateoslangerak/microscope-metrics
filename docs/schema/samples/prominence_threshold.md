# Slot: prominence_threshold


_Peak prominence used as a threshold to distinguish two peaks.  Defaults to the value defined by the Rayleigh criteria_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:prominence_threshold](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:prominence_threshold)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightEInput](ArgolightEInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 0





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: prominence_threshold
description: Peak prominence used as a threshold to distinguish two peaks.  Defaults
  to the value defined by the Rayleigh criteria
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(0.264)
alias: prominence_threshold
domain_of:
- ArgolightEInput
range: float
required: true
minimum_value: 0
maximum_value: 0

```
</details>