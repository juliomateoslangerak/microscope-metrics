# Class: Shape


_A shape_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Shape](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Shape)




```mermaid
 classDiagram
    class Shape
      Shape <|-- Point
      Shape <|-- Line
      Shape <|-- Rectangle
      Shape <|-- Ellipse
      Shape <|-- Polygon
      Shape <|-- Mask
      
      Shape : c
        
      Shape : fill_color
        
          Shape --|> Color : fill_color
        
      Shape : label
        
      Shape : stroke_color
        
          Shape --|> Color : stroke_color
        
      Shape : stroke_width
        
      Shape : t
        
      Shape : z
        
      
```





## Inheritance
* **Shape**
    * [Point](Point.md)
    * [Line](Line.md)
    * [Rectangle](Rectangle.md)
    * [Ellipse](Ellipse.md)
    * [Polygon](Polygon.md)
    * [Mask](Mask.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [label](label.md) | 0..1 <br/> [String](String.md) |  | direct |
| [z](z.md) | 0..1 <br/> [Float](Float.md) |  | direct |
| [c](c.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [t](t.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [fill_color](fill_color.md) | 0..1 <br/> [Color](Color.md) |  | direct |
| [stroke_color](stroke_color.md) | 0..1 <br/> [Color](Color.md) |  | direct |
| [stroke_width](stroke_width.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ROI](ROI.md) | [shapes](shapes.md) | range | [Shape](Shape.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Shape |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Shape |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Shape
description: A shape
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
abstract: true
attributes:
  label:
    name: label
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: string
    required: false
  z:
    name: z
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: float
    required: false
  c:
    name: c
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: integer
    required: false
  t:
    name: t
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: integer
    required: false
  fill_color:
    name: fill_color
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: Color
    required: false
  stroke_color:
    name: stroke_color
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: Color
    required: false
  stroke_width:
    name: stroke_width
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    ifabsent: int(1)
    range: integer
    required: false

```
</details>

### Induced

<details>
```yaml
name: Shape
description: A shape
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
abstract: true
attributes:
  label:
    name: label
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: label
    owner: Shape
    domain_of:
    - ROI
    - Shape
    range: string
    required: false
  z:
    name: z
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: z
    owner: Shape
    domain_of:
    - Image5D
    - Shape
    range: float
    required: false
  c:
    name: c
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: c
    owner: Shape
    domain_of:
    - Image5D
    - Shape
    range: integer
    required: false
  t:
    name: t
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: t
    owner: Shape
    domain_of:
    - Image5D
    - Shape
    range: integer
    required: false
  fill_color:
    name: fill_color
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: fill_color
    owner: Shape
    domain_of:
    - Shape
    range: Color
    required: false
  stroke_color:
    name: stroke_color
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: stroke_color
    owner: Shape
    domain_of:
    - Shape
    range: Color
    required: false
  stroke_width:
    name: stroke_width
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    ifabsent: int(1)
    alias: stroke_width
    owner: Shape
    domain_of:
    - Shape
    range: integer
    required: false

```
</details>