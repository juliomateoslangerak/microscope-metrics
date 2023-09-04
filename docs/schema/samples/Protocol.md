# Class: Protocol


_Set of instructions for preparing and imaging a sample_





URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Protocol](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Protocol)




```mermaid
 classDiagram
    class Protocol
      NamedObject <|-- Protocol
      
      Protocol : authors
        
          Protocol --|> Experimenter : authors
        
      Protocol : description
        
      Protocol : name
        
      Protocol : url
        
      Protocol : version
        
      
```





## Inheritance
* [NamedObject](NamedObject.md)
    * **Protocol**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [version](version.md) | 1..1 <br/> [String](String.md) | The version of the protocol | direct |
| [authors](authors.md) | 0..* <br/> [Experimenter](Experimenter.md) | The authors of the protocol | direct |
| [url](url.md) | 1..1 <br/> [String](String.md) | The URL where the protocol can be found | direct |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of an entity | [NamedObject](NamedObject.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | A description of an entity | [NamedObject](NamedObject.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Sample](Sample.md) | [protocol](protocol.md) | range | [Protocol](Protocol.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Protocol |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Protocol |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Protocol
description: Set of instructions for preparing and imaging a sample
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: NamedObject
attributes:
  version:
    name: version
    description: The version of the protocol
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: string
    required: true
  authors:
    name: authors
    description: The authors of the protocol
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    range: Experimenter
    inlined: false
  url:
    name: url
    description: The URL where the protocol can be found
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    identifier: true
    range: string
    required: true

```
</details>

### Induced

<details>
```yaml
name: Protocol
description: Set of instructions for preparing and imaging a sample
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: NamedObject
attributes:
  version:
    name: version
    description: The version of the protocol
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: version
    owner: Protocol
    domain_of:
    - Protocol
    range: string
    required: true
  authors:
    name: authors
    description: The authors of the protocol
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    alias: authors
    owner: Protocol
    domain_of:
    - Protocol
    range: Experimenter
    inlined: false
  url:
    name: url
    description: The URL where the protocol can be found
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    identifier: true
    alias: url
    owner: Protocol
    domain_of:
    - Protocol
    range: string
    required: true
  name:
    name: name
    description: The name of an entity
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: name
    owner: Protocol
    domain_of:
    - NamedObject
    - Experimenter
    - Column
    range: string
    required: false
  description:
    name: description
    description: A description of an entity
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: description
    owner: Protocol
    domain_of:
    - NamedObject
    - Roi
    - Tag
    range: string

```
</details>