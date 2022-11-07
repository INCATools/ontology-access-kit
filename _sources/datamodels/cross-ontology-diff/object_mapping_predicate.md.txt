# Slot: object_mapping_predicate
_The mapping predicate that holds between left_object_id and right_object_id_


URI: [ann:object_mapping_predicate](https://w3id.org/linkml/text_annotator/object_mapping_predicate)




## Inheritance

* **object_mapping_predicate** [ [subject](subject.md) [predicate](predicate.md)]





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

* Range: [EntityReference](EntityReference.md)






## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: object_mapping_predicate
description: The mapping predicate that holds between left_object_id and right_object_id
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- subject
- predicate
alias: object_mapping_predicate
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>