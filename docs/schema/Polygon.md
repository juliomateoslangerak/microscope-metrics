# Class: Polygon


_A polygon as defined by a series of vertexes and a boolean to indicate if closed or not_





URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/:Polygon](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/:Polygon)




```mermaid
 classDiagram
    class Polygon
      Shape <|-- Polygon
      
      Polygon : c
        
      Polygon : fill_color
        
          Polygon --|> Color : fill_color
        
      Polygon : is_open
        
      Polygon : label
        
      Polygon : stroke_color
        
          Polygon --|> Color : stroke_color
        
      Polygon : stroke_width
        
      Polygon : t
        
      Polygon : vertexes
        
          Polygon --|> Vertex : vertexes
        
      Polygon : z
        
      
```





## Inheritance
* [Shape](Shape.md)
    * **Polygon**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [vertexes](vertexes.md) | 1..* <br/> [Vertex](Vertex.md) | A list of vertexes defining the polygon | direct |
| [is_open](is_open.md) | 1..1 <br/> [Boolean](Boolean.md) | Is the polygon open | direct |
| [label](label.md) | 0..1 <br/> [String](String.md) | The label of the shape | [Shape](Shape.md) |
| [z](z.md) | 0..1 <br/> [Float](Float.md) | The z coordinate of the shape | [Shape](Shape.md) |
| [c](c.md) | 0..1 <br/> [Integer](Integer.md) | The c coordinate of the shape | [Shape](Shape.md) |
| [t](t.md) | 0..1 <br/> [Integer](Integer.md) | The t coordinate of the shape | [Shape](Shape.md) |
| [fill_color](fill_color.md) | 0..1 <br/> [Color](Color.md) | The fill color of the shape | [Shape](Shape.md) |
| [stroke_color](stroke_color.md) | 0..1 <br/> [Color](Color.md) | The stroke color of the shape | [Shape](Shape.md) |
| [stroke_width](stroke_width.md) | 0..1 <br/> [Integer](Integer.md) | The stroke width of the shape | [Shape](Shape.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/:Polygon |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml/:Polygon |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Polygon
description: A polygon as defined by a series of vertexes and a boolean to indicate
  if closed or not
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
is_a: Shape
attributes:
  vertexes:
    name: vertexes
    description: A list of vertexes defining the polygon
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    range: Vertex
    required: true
    inlined: true
    inlined_as_list: true
  is_open:
    name: is_open
    description: Is the polygon open. By default, it is closed (false)
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    ifabsent: 'False'
    range: boolean
    required: true

```
</details>

### Induced

<details>
```yaml
name: Polygon
description: A polygon as defined by a series of vertexes and a boolean to indicate
  if closed or not
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
is_a: Shape
attributes:
  vertexes:
    name: vertexes
    description: A list of vertexes defining the polygon
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: true
    alias: vertexes
    owner: Polygon
    domain_of:
    - Polygon
    range: Vertex
    required: true
    inlined: true
    inlined_as_list: true
  is_open:
    name: is_open
    description: Is the polygon open. By default, it is closed (false)
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    multivalued: false
    ifabsent: 'False'
    alias: is_open
    owner: Polygon
    domain_of:
    - Polygon
    range: boolean
    required: true
  label:
    name: label
    description: The label of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: label
    owner: Polygon
    domain_of:
    - roi
    - Shape
    range: string
    required: false
  z:
    name: z
    description: The z coordinate of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: z
    owner: Polygon
    domain_of:
    - Image5D
    - Shape
    range: float
    required: false
  c:
    name: c
    description: The c coordinate of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: c
    owner: Polygon
    domain_of:
    - Image5D
    - Shape
    range: integer
    required: false
  t:
    name: t
    description: The t coordinate of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: t
    owner: Polygon
    domain_of:
    - Image5D
    - Shape
    range: integer
    required: false
  fill_color:
    name: fill_color
    description: The fill color of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: fill_color
    owner: Polygon
    domain_of:
    - Shape
    range: Color
    required: false
  stroke_color:
    name: stroke_color
    description: The stroke color of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: stroke_color
    owner: Polygon
    domain_of:
    - Shape
    range: Color
    required: false
  stroke_width:
    name: stroke_width
    description: The stroke width of the shape
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    ifabsent: int(1)
    alias: stroke_width
    owner: Polygon
    domain_of:
    - Shape
    range: integer
    required: false

```
</details>