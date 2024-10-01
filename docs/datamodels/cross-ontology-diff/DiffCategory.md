# Enum: DiffCategory




_Category of the cross-ontology diff, from the perspective of the left-hand edge_



URI: [DiffCategory](DiffCategory.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Identical | None | there is a direct analogous direct asserted edge on the right side with the i... |
| MoreSpecificPredicateOnRight | None | there is an analogous edge on the right side with a more specific but non-ide... |
| LessSpecificPredicateOnRight | None | there is an analogous edge on the right side with a less specific but non-ide... |
| LeftEntailedByRight | None | there is an analogous edge on the right side, where that edge is different fr... |
| RightEntailedByLeft | None | there is an analogous edge on the right side, where that edge is different fr... |
| IndirectFormOfEdgeOnRight | None | there is no direct analogous right side edge but an analogous edge can be ent... |
| RightNodesAreIdentical | None | a special case where both the left subject and left object map to the same no... |
| NonEntailedRelationship | None | there is an analogous edge on the right side with a different predicate that ... |
| NoRelationship | None | there is no relationship between the right object and right subject |
| MissingMapping | None | one or both mappings are missing |
| MissingSubjectMapping | None | there is no mapping for the subject |
| MissingObjectMapping | None | there is no mapping for the object |




## Slots

| Name | Description |
| ---  | --- |
| [category](category.md) | Each match (or lack of match) is placed into exactly one category |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff






## LinkML Source

<details>
```yaml
name: DiffCategory
description: Category of the cross-ontology diff, from the perspective of the left-hand
  edge
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
permissible_values:
  Identical:
    text: Identical
    description: there is a direct analogous direct asserted edge on the right side
      with the identical predicate
    rank: 1
  MoreSpecificPredicateOnRight:
    text: MoreSpecificPredicateOnRight
    description: there is an analogous edge on the right side with a more specific
      but non-identical predicate
    is_a: LeftEntailedByRight
    rank: 2
  LessSpecificPredicateOnRight:
    text: LessSpecificPredicateOnRight
    description: there is an analogous edge on the right side with a less specific
      but non-identical predicate
    is_a: RightEntailedByLeft
    rank: 2
  LeftEntailedByRight:
    text: LeftEntailedByRight
    description: there is an analogous edge on the right side, where that edge is
      different from but entailed by the one on the right
    rank: 3
  RightEntailedByLeft:
    text: RightEntailedByLeft
    description: there is an analogous edge on the right side, where that edge is
      different from but entails the one on the right
    rank: 3
  IndirectFormOfEdgeOnRight:
    text: IndirectFormOfEdgeOnRight
    description: there is no direct analogous right side edge but an analogous edge
      can be entailed
    is_a: LeftEntailedByRight
    rank: 3
  RightNodesAreIdentical:
    text: RightNodesAreIdentical
    description: a special case where both the left subject and left object map to
      the same node on the right
    rank: 5
  NonEntailedRelationship:
    text: NonEntailedRelationship
    description: there is an analogous edge on the right side with a different predicate
      that is neither more specific nor less specific
    rank: 10
  NoRelationship:
    text: NoRelationship
    description: there is no relationship between the right object and right subject
    rank: 20
  MissingMapping:
    text: MissingMapping
    description: one or both mappings are missing
    rank: 99
  MissingSubjectMapping:
    text: MissingSubjectMapping
    description: there is no mapping for the subject
    is_a: MissingMapping
    rank: 99
  MissingObjectMapping:
    text: MissingObjectMapping
    description: there is no mapping for the object
    is_a: MissingMapping
    rank: 99

```
</details>
