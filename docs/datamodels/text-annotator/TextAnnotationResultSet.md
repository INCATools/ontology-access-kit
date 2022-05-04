# Class: TextAnnotationResultSet
_A collection of annotation results_





URI: [ann:TextAnnotationResultSet](https://w3id.org/linkml/text_annotator/TextAnnotationResultSet)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [annotations](annotations.md) | [TextAnnotation](TextAnnotation.md) | 0..* | all annotations  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotationResultSet
description: A collection of annotation results
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  annotations:
    name: annotations
    description: all annotations
    from_schema: https://w3id.org/linkml/text_annotator
    multivalued: true
    inlined: true
    range: TextAnnotation

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationResultSet
description: A collection of annotation results
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  annotations:
    name: annotations
    description: all annotations
    from_schema: https://w3id.org/linkml/text_annotator
    multivalued: true
    inlined: true
    alias: annotations
    owner: TextAnnotationResultSet
    range: TextAnnotation

```
</details>