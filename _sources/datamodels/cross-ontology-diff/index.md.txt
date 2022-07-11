# Cross-Ontology Diff

A datamodel for representing the results of relational diffs across a pair of ontologies connected by mappings

URI: https://w3id.org/linkml/cross_ontology_diff
Name: cross-ontology-diff

## Classes

| Class | Description |
| --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in
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
of the left edge. |
| [StructureDiffResultSet](StructureDiffResultSet.md) | A collection of relational diff results results |


## Slots

| Slot | Description |
| --- | --- |
| [category](category.md) | Each match (or lack of match) is placed into exactly one category |
| [is_functional](is_functional.md) | None |
| [label](label.md) | None |
| [left_object_id](left_object_id.md) | The object (parent) of the source/left edge |
| [left_object_is_functional](left_object_is_functional.md) | True if an object mapping is present, and maps uniquely within the same ontology |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge |
| [left_predicate_id](left_predicate_id.md) | The predicate (relation) of the source/left edge |
| [left_predicate_label](left_predicate_label.md) | The name of the predicate of the source/left edge |
| [left_side](left_side.md) | None |
| [left_source](left_source.md) | None |
| [left_subject_id](left_subject_id.md) | The subject (child) of the source/left edge |
| [left_subject_is_functional](left_subject_is_functional.md) | True if a subject mapping is present, and maps uniquely within the same ontology |
| [left_subject_label](left_subject_label.md) | The name of the subject (child) of the source/left edge |
| [object](object.md) | None |
| [object_mapping_cardinality](object_mapping_cardinality.md) | The mapping cardinality of the object pair |
| [object_mapping_predicate](object_mapping_predicate.md) | The mapping predicate that holds between left_object_id and right_object_id |
| [predicate](predicate.md) | None |
| [results](results.md) | all differences between a pair of ontologies |
| [right_intermediate_ids](right_intermediate_ids.md) | None |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable |
| [right_predicate_ids](right_predicate_ids.md) | * If the match type is consistent, then all consistent predicates.
* If the match type is identical, then the identical predicate.
* If the match type is OtherRelationship, then all predicates that form a path between right subject and object |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids |
| [right_side](right_side.md) | None |
| [right_source](right_source.md) | None |
| [right_subject_id](right_subject_id.md) | The subject (child) of the matched/right edge, if matchable |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable |
| [side](side.md) | None |
| [subject](subject.md) | None |
| [subject_mapping_cardinality](subject_mapping_cardinality.md) | The mapping cardinality of the subject pair |
| [subject_mapping_predicate](subject_mapping_predicate.md) | The mapping predicate that holds between left_subject_id and right_subject_id |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [DiffCategory](DiffCategory.md) | Category of the cross-ontology diff, from the perspective of the left-hand edge |
| [MappingCardinalityEnum](MappingCardinalityEnum.md) | None |


## Subsets

| Subset | Description |
| --- | --- |
