# Slot: processed


_Has the dataset been processed by microscope-metrics_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:processed](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:processed)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ArgolightBDataset](ArgolightBDataset.md) | An Argolight sample pattern B dataset |  no  |
[ArgolightEDataset](ArgolightEDataset.md) | An Argolight sample pattern E dataset |  no  |
[MetricsDataset](MetricsDataset.md) | A base object on which microscope-metrics runs the analysis |  no  |







## Properties

* Range: [Boolean](Boolean.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: processed
description: Has the dataset been processed by microscope-metrics
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
rank: 1000
multivalued: false
ifabsent: 'False'
alias: processed
owner: MetricsDataset
domain_of:
- MetricsDataset
range: boolean
required: true

```
</details>