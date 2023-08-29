# Slot: bit_depth


_Detector bit depth_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:bit_depth](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:bit_depth)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBInput](ArgolightBInput.md) |  |  no  |
[ArgolightEInput](ArgolightEInput.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)

* Minimum Value: 1

* Maximum Value: 64





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: bit_depth
description: Detector bit depth
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
alias: bit_depth
domain_of:
- ArgolightBInput
- ArgolightEInput
range: integer
minimum_value: 1
maximum_value: 64

```
</details>