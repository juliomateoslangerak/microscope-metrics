# Slot: alpha


_The alpha value of the color (optional)_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:alpha](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:alpha)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Color](Color.md) | A color as defined by RGB values and an optional alpha value |  no  |







## Properties

* Range: [Integer](Integer.md)

* Minimum Value: 0

* Maximum Value: 255





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: alpha
description: The alpha value of the color (optional)
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: int(255)
alias: alpha
owner: Color
domain_of:
- Color
range: integer
required: false
minimum_value: 0
maximum_value: 255

```
</details>