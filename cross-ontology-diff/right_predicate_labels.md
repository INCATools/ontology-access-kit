# Slot: right_predicate_labels
_The names corresponding to the right_predicate_ids_


URI: [ann:right_predicate_labels](https://w3id.org/linkml/text_annotator/right_predicate_labels)




## Inheritance

* **right_predicate_labels** [ [right_side](right_side.md) [predicate](predicate.md) [label](label.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a...






## Properties

* Range: [Label](Label.md)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: right_predicate_labels
description: The names corresponding to the right_predicate_ids
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- right_side
- predicate
- label
multivalued: true
alias: right_predicate_labels
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>