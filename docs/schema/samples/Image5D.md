# Class: Image5D


_A 5D image in TZYXC order_





URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Image5D](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Image5D)




```mermaid
 classDiagram
    class Image5D
      ImageInline <|-- Image5D
      
      Image5D : c
        
          Image5D --|> ChannelSeries : c
        
      Image5D : data
        
      Image5D : description
        
      Image5D : image_url
        
      Image5D : name
        
      Image5D : source_image_url
        
      Image5D : t
        
          Image5D --|> TimeSeries : t
        
      Image5D : x
        
          Image5D --|> PixelSeries : x
        
      Image5D : y
        
          Image5D --|> PixelSeries : y
        
      Image5D : z
        
          Image5D --|> PixelSeries : z
        
      
```





## Inheritance
* [NamedObject](NamedObject.md)
    * [MetricsObject](MetricsObject.md)
        * [Image](Image.md)
            * [ImageInline](ImageInline.md)
                * **Image5D**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [t](t.md) | 1..1 <br/> [TimeSeries](TimeSeries.md) |  | direct |
| [z](z.md) | 1..1 <br/> [PixelSeries](PixelSeries.md) |  | direct |
| [y](y.md) | 1..1 <br/> [PixelSeries](PixelSeries.md) |  | direct |
| [x](x.md) | 1..1 <br/> [PixelSeries](PixelSeries.md) |  | direct |
| [c](c.md) | 1..1 <br/> [ChannelSeries](ChannelSeries.md) |  | direct |
| [data](data.md) | 1..* <br/> [Float](Float.md) |  | direct |
| [image_url](image_url.md) | 1..1 <br/> [String](String.md) | An URL linking to the image | [Image](Image.md) |
| [source_image_url](source_image_url.md) | 0..* <br/> [String](String.md) | A list of URLs linking to the images that were used as a source | [Image](Image.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of an entity | [NamedObject](NamedObject.md) |
| [description](description.md) | 0..1 <br/> [String](String.md) | A description of an entity | [NamedObject](NamedObject.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Image5D |
| native | https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:Image5D |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Image5D
implements:
- linkml:FiveDimensionalArray
- linkml:RowOrderedArray
description: A 5D image in TZYXC order
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: ImageInline
attributes:
  t:
    name: t
    implements:
    - linkml:axis0
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: TimeSeries
    required: true
  z:
    name: z
    implements:
    - linkml:axis1
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: PixelSeries
    required: true
  y:
    name: y
    implements:
    - linkml:axis2
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: PixelSeries
    required: true
  x:
    name: x
    implements:
    - linkml:axis3
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    range: PixelSeries
    required: true
  c:
    name: c
    implements:
    - linkml:axis4
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    range: ChannelSeries
    required: true
  data:
    name: data
    implements:
    - linkml:elements
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    multivalued: true
    range: float
    required: true

```
</details>

### Induced

<details>
```yaml
name: Image5D
implements:
- linkml:FiveDimensionalArray
- linkml:RowOrderedArray
description: A 5D image in TZYXC order
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
is_a: ImageInline
attributes:
  t:
    name: t
    implements:
    - linkml:axis0
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: t
    owner: Image5D
    domain_of:
    - Image5D
    - Shape
    range: TimeSeries
    required: true
  z:
    name: z
    implements:
    - linkml:axis1
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: z
    owner: Image5D
    domain_of:
    - Image5D
    - Shape
    range: PixelSeries
    required: true
  y:
    name: y
    implements:
    - linkml:axis2
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: y
    owner: Image5D
    domain_of:
    - ImageMask
    - Image2D
    - Image5D
    - Point
    - Rectangle
    - Ellipse
    - Vertex
    - Mask
    range: PixelSeries
    required: true
  x:
    name: x
    implements:
    - linkml:axis3
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    alias: x
    owner: Image5D
    domain_of:
    - ImageMask
    - Image2D
    - Image5D
    - Point
    - Rectangle
    - Ellipse
    - Vertex
    - Mask
    range: PixelSeries
    required: true
  c:
    name: c
    implements:
    - linkml:axis4
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    rank: 1000
    alias: c
    owner: Image5D
    domain_of:
    - Image5D
    - Shape
    range: ChannelSeries
    required: true
  data:
    name: data
    implements:
    - linkml:elements
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/core_schema.yaml
    multivalued: true
    alias: data
    owner: Image5D
    domain_of:
    - ImageAsNumpy
    - ImageMask
    - Image2D
    - Image5D
    range: float
    required: true
  image_url:
    name: image_url
    description: An URL linking to the image
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    identifier: true
    alias: image_url
    owner: Image5D
    domain_of:
    - Image
    range: string
    required: true
  source_image_url:
    name: source_image_url
    description: A list of URLs linking to the images that were used as a source
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: true
    alias: source_image_url
    owner: Image5D
    domain_of:
    - Image
    range: string
    required: false
  name:
    name: name
    description: The name of an entity
    from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
    rank: 1000
    multivalued: false
    alias: name
    owner: Image5D
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
    owner: Image5D
    domain_of:
    - NamedObject
    - Roi
    - Tag
    range: string

```
</details>