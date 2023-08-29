# Class: ArgolightBDataset


_An Argolight sample pattern B dataset_





URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:ArgolightBDataset](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:ArgolightBDataset)




```mermaid
 classDiagram
    class ArgolightBDataset
      MetricsDataset <|-- ArgolightBDataset
      
      ArgolightBDataset : acquisition_date
        
      ArgolightBDataset : comment
        
          ArgolightBDataset --|> Comment : comment
        
      ArgolightBDataset : description
        
      ArgolightBDataset : experimenter
        
          ArgolightBDataset --|> Experimenter : experimenter
        
      ArgolightBDataset : input
        
          ArgolightBDataset --|> ArgolightBInput : input
        
      ArgolightBDataset : name
        
      ArgolightBDataset : output
        
          ArgolightBDataset --|> ArgolightBOutput : output
        
      ArgolightBDataset : processed
        
      ArgolightBDataset : processing_date
        
      ArgolightBDataset : processing_log
        
      ArgolightBDataset : sample
        
          ArgolightBDataset --|> Sample : sample
        
      
```





## Inheritance
* [NamedObject](NamedObject.md)
    * [MetricsDataset](MetricsDataset.md)
        * **ArgolightBDataset**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [input](input.md) | 1..1 <br/> [ArgolightBInput](ArgolightBInput.md) | An input element for the analysis | direct |
| [output](output.md) | 0..1 <br/> [ArgolightBOutput](ArgolightBOutput.md) | An output element from the analysis | direct |
| [sample](sample.md) | 0..1 <br/> [Sample](Sample.md) | The sample that was imaged | [MetricsDataset](MetricsDataset.md) |
| [experimenter](experimenter.md) | 0..* <br/> [Experimenter](Experimenter.md) | The experimenter that performed the imaging experiment | [MetricsDataset](MetricsDataset.md) |
| [acquisition_date](acquisition_date.md) | 0..1 <br/> [Date](Date.md) | The date of the acquisition | [MetricsDataset](MetricsDataset.md) |
| [processed](processed.md) | 1..1 <br/> [Boolean](Boolean.md) | Has the dataset been processed by microscope-metrics | [MetricsDataset](MetricsDataset.md) |
| [processing_date](processing_date.md) | 0..1 <br/> [Date](Date.md) | The date of the processing by microscope-metrics | [MetricsDataset](MetricsDataset.md) |
| [processing_log](processing_log.md) | 0..1 <br/> [String](String.md) | The log of the processing by microscope-metrics | [MetricsDataset](MetricsDataset.md) |
| [comment](comment.md) | 0..* <br/> [Comment](Comment.md) | A human readable comment about the dataset | [MetricsDataset](MetricsDataset.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of an entity | [NamedObject](NamedObject.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | A description of an entity | [NamedObject](NamedObject.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:ArgolightBDataset |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:ArgolightBDataset |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ArgolightBDataset
description: An Argolight sample pattern B dataset
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: MetricsDataset
attributes:
  input:
    name: input
    description: An input element for the analysis
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    range: ArgolightBInput
    required: true
  output:
    name: output
    description: An output element from the analysis
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    range: ArgolightBOutput
    required: false
rules:
- preconditions:
    slot_conditions:
      processed:
        name: processed
        equals_number: 1
  postconditions:
    slot_conditions:
      output:
        name: output
        required: true

```
</details>

### Induced

<details>
```yaml
name: ArgolightBDataset
description: An Argolight sample pattern B dataset
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: MetricsDataset
attributes:
  input:
    name: input
    description: An input element for the analysis
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: input
    owner: ArgolightBDataset
    domain_of:
    - ArgolightBDataset
    - ArgolightEDataset
    range: ArgolightBInput
    required: true
  output:
    name: output
    description: An output element from the analysis
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: output
    owner: ArgolightBDataset
    domain_of:
    - ArgolightBDataset
    - ArgolightEDataset
    range: ArgolightBOutput
    required: false
  sample:
    name: sample
    description: The sample that was imaged
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    alias: sample
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: Sample
    inlined: false
  experimenter:
    name: experimenter
    description: The experimenter that performed the imaging experiment
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    alias: experimenter
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: Experimenter
  acquisition_date:
    name: acquisition_date
    description: The date of the acquisition
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    alias: acquisition_date
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: date
  processed:
    name: processed
    description: Has the dataset been processed by microscope-metrics
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    ifabsent: 'False'
    alias: processed
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: boolean
    required: true
  processing_date:
    name: processing_date
    description: The date of the processing by microscope-metrics
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    alias: processing_date
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: date
  processing_log:
    name: processing_log
    description: The log of the processing by microscope-metrics
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    alias: processing_log
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: string
  comment:
    name: comment
    description: A human readable comment about the dataset
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    alias: comment
    owner: ArgolightBDataset
    domain_of:
    - MetricsDataset
    range: Comment
    required: false
  name:
    name: name
    description: The name of an entity
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: name
    owner: ArgolightBDataset
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
    owner: ArgolightBDataset
    domain_of:
    - NamedObject
    - Roi
    - Tag
    range: string
rules:
- preconditions:
    slot_conditions:
      processed:
        name: processed
        equals_number: 1
  postconditions:
    slot_conditions:
      output:
        name: output
        required: true

```
</details>