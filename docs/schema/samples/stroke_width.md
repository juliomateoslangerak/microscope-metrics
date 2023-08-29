# Slot: stroke_width


_The stroke width of the shape_



URI: [https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:stroke_width](https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml/:stroke_width)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Shape](Shape.md) | A shape |  no  |
[Point](Point.md) | A point as defined by x and y coordinates |  no  |
[Line](Line.md) | A line as defined by x1, y1, x2, y2 coordinates |  no  |
[Rectangle](Rectangle.md) | A rectangle as defined by x, y coordinates and width, height |  no  |
[Ellipse](Ellipse.md) | An ellipse as defined by x, y coordinates and x and y radii |  no  |
[Polygon](Polygon.md) | A polygon as defined by a series of vertexes and a boolean to indicate if clo... |  no  |
[Mask](Mask.md) | A mask as defined by a boolean image |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml




## LinkML Source

<details>
```yaml
name: stroke_width
description: The stroke width of the shape
from_schema: https://github.com/MontpellierRessourcesImagerie/microscope-metrics/blob/main/src/microscopemetrics/data_schema/samples/argolight_schema.yaml
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