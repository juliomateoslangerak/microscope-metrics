# Slot: sigma_x


_When provided, gaussian smoothing sigma to be applied to the image in the X axis prior to bead detection. Does not apply to resolution measurements_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:sigma_x](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:sigma_x)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[PSFBeadsInput](PSFBeadsInput.md) |  |  no  |







## Properties

* Range: [Float](Float.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: sigma_x
description: When provided, gaussian smoothing sigma to be applied to the image in
  the X axis prior to bead detection. Does not apply to resolution measurements
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
alias: sigma_x
domain_of:
- PSFBeadsInput
range: float
required: false

```
</details>