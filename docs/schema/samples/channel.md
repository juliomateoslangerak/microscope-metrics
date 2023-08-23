# Slot: channel


_The channel number to which the measurements apply_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:channel](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:channel)




## Inheritance

* **channel**
    * [channel_A](channel_A.md)
    * [channel_B](channel_B.md)





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBIntensityKeyValues](ArgolightBIntensityKeyValues.md) |  |  no  |
[ArgolightEKeyValues](ArgolightEKeyValues.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: channel
description: The channel number to which the measurements apply
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: true
alias: channel
domain_of:
- ArgolightBIntensityKeyValues
- ArgolightEKeyValues
range: integer

```
</details>