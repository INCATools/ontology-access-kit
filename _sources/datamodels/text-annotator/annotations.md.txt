

# Slot: annotations


_all annotations_





URI: [ann:annotations](https://w3id.org/linkml/text_annotator/annotations)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | A collection of annotation results |  no  |







## Properties

* Range: [TextAnnotation](TextAnnotation.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:annotations |
| native | ann:annotations |




## LinkML Source

<details>
```yaml
name: annotations
description: all annotations
from_schema: https://w3id.org/oak/text_annotator
rank: 1000
alias: annotations
owner: TextAnnotationResultSet
domain_of:
- TextAnnotationResultSet
range: TextAnnotation
multivalued: true
inlined: true

```
</details>