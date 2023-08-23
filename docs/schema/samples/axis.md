# Slot: axis


_Axis along which resolution is being measured. 1=Y, 2=X_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:axis](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:axis)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightEInput](ArgolightEInput.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)

* Required: True

* Minimum Value: 1

* Maximum Value: 2





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: axis
description: Axis along which resolution is being measured. 1=Y, 2=X
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
alias: axis
domain_of:
- ArgolightEInput
range: integer
required: true
minimum_value: 1
maximum_value: 2

```
</details>