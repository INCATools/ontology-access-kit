# Slot: right_object_label
_The name of the object (parent) of the matched/right edge, if matchable_


URI: [ann:right_object_label](https://w3id.org/linkml/text_annotator/right_object_label)




## Inheritance

* **right_object_label** [ [right_side](right_side.md) [object](object.md) [label](label.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a...






## Properties

* Range: [Label](Label.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: right_object_label
description: The name of the object (parent) of the matched/right edge, if matchable
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- right_side
- object
- label
alias: right_object_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>