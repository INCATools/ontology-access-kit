# Slot: left_predicate_label
_The name of the predicate of the source/left edge_


URI: [ann:left_predicate_label](https://w3id.org/linkml/text_annotator/left_predicate_label)




## Inheritance

* **left_predicate_label** [ [left_side](left_side.md) [predicate](predicate.md) [label](label.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in
another ontology (or a different version of the same ontology). The diff is from the perspective of one
ontology (the one on the "left" side).

For every edge in the left ontology, the subject and object are mapped to the right ontology.
If mappings cannot be found then the diff is categorized as missing mappings.
The predicate is also mapped, with the reflexivity assumption.

for every mapped subject and object pair (the "right" subject and object), the entailed relationship
is examined to determine if it consistent with the left predicate.

```
left_object    <--- mapped to ---> right_object
   ^                                  ^
   |                                  |
   |                                  |
   | left                             | right
   | predicate                        | predicate
   |                                  |
   |                                  |
left_subject   <--- mapped to ---> right_subject
```

The above figure gives hows the basic structure. Classification of the edge is done from the perspective
of the left edge.






## Properties

* Range: [Label](Label.md)






## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: left_predicate_label
description: The name of the predicate of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- predicate
- label
alias: left_predicate_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>