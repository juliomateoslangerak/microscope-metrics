# Slot: sigma_x


_Input parameter: smoothing factor for objects detection in the X axis_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:sigma_x](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:sigma_x)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBInput](ArgolightBInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)

* Required: True

* Minimum Value: 0

* Maximum Value: 10





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: sigma_x
description: 'Input parameter: smoothing factor for objects detection in the X axis'
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(3.0)
alias: sigma_x
domain_of:
- ArgolightBInput
range: float
required: true
minimum_value: 0
maximum_value: 10

```
</details>