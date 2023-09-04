# Slot: saturation_threshold


_Tolerated saturation threshold. If the amount of saturated pixels is above this threshold,  the image is considered as saturated and the analysis is not performed._



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:saturation_threshold](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:saturation_threshold)



<!-- no inheritance hierarchy -->







## Properties

* Range: [Float](Float.md)

* Minimum Value: 0

* Maximum Value: 1





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: saturation_threshold
description: Tolerated saturation threshold. If the amount of saturated pixels is
  above this threshold,  the image is considered as saturated and the analysis is
  not performed.
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: float(0.01)
alias: saturation_threshold
range: float
minimum_value: 0
maximum_value: 1

```
</details>