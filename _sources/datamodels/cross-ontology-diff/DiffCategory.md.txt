# DiffCategory

Category of the cross-ontology diff, from the perspective of the left-hand edge

URI: DiffCategory

## Permissible Values

| Value | Meaning | Description | Info |
| --- | --- | --- | --- |
| Identical | None | there is a direct analogous direct asserted edge on the right side with the identical predicate | |
| MoreSpecificPredicateOnRight | None | there is an analogous edge on the right side with a more specific but non-identical predicate | |
| LessSpecificPredicateOnRight | None | there is an analogous edge on the right side with a less specific but non-identical predicate | |
| LeftEntailedByRight | None | there is an analogous edge on the right side, where that edge is different from but entailed by the one on the right | |
| RightEntailedByLeft | None | there is an analogous edge on the right side, where that edge is different from but entails the one on the right | |
| IndirectFormOfEdgeOnRight | None | there is no direct analogous right side edge but an analogous edge can be entailed | |
| RightNodesAreIdentical | None | a special case where both the left subject and left object map to the same node on the right | |
| NonEntailedRelationship | None | there is an analogous edge on the right side with a different predicate that is neither more specific nor less specific | |
| NoRelationship | None | there is no relationship between the right object and right subject | |
| MissingMapping | None | one or both mappings are missing | |
| MissingSubjectMapping | None | there is no mapping for the subject | |
| MissingObjectMapping | None | there is no mapping for the object | |


## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff



