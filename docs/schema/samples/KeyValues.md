# Class: KeyValues


_A collection of key-value pairs_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:KeyValues](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:KeyValues)




```mermaid
 classDiagram
    class KeyValues
      KeyValues <|-- ArgolightBIntensityKeyValues
      KeyValues <|-- ArgolightBDistanceKeyValues
      KeyValues <|-- ArgolightEKeyValues
      
      
```





## Inheritance
* **KeyValues**
    * [ArgolightBIntensityKeyValues](ArgolightBIntensityKeyValues.md)
    * [ArgolightBDistanceKeyValues](ArgolightBDistanceKeyValues.md)
    * [ArgolightEKeyValues](ArgolightEKeyValues.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |









## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:KeyValues |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:KeyValues |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: KeyValues
description: A collection of key-value pairs
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
abstract: true

```
</details>

### Induced

<details>
```yaml
name: KeyValues
description: A collection of key-value pairs
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
abstract: true

```
</details>