# Slot: left_subject_label
_The name of the subject (child) of the source/left edge_


URI: [ann:left_subject_label](https://w3id.org/linkml/text_annotator/left_subject_label)




## Inheritance

* **left_subject_label** [ [left_side](left_side.md) [subject](subject.md) [label](label.md)]





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
name: left_subject_label
description: The name of the subject (child) of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- subject
- label
alias: left_subject_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>