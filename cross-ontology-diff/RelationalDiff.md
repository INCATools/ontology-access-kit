# Class: RelationalDiff
_A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in
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
of the left edge._




URI: [ann:RelationalDiff](https://w3id.org/linkml/text_annotator/RelationalDiff)


```{mermaid}
 classDiagram
    class RelationalDiff
      RelationalDiff : category
      RelationalDiff : left_object_id
      RelationalDiff : left_object_is_functional
      RelationalDiff : left_object_label
      RelationalDiff : left_predicate_id
      RelationalDiff : left_predicate_label
      RelationalDiff : left_subject_id
      RelationalDiff : left_subject_is_functional
      RelationalDiff : left_subject_label
      RelationalDiff : object_mapping_cardinality
      RelationalDiff : object_mapping_predicate
      RelationalDiff : right_intermediate_ids
      RelationalDiff : right_object_id
      RelationalDiff : right_object_label
      RelationalDiff : right_predicate_ids
      RelationalDiff : right_predicate_labels
      RelationalDiff : right_subject_id
      RelationalDiff : right_subject_label
      RelationalDiff : subject_mapping_cardinality
      RelationalDiff : subject_mapping_predicate
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [category](category.md) | 0..1 <br/> DiffCategory | Each match (or lack of match) is placed into exactly one category | direct |
| [left_subject_id](left_subject_id.md) | 1..1 <br/> EntityReference | The subject (child) of the source/left edge | direct |
| [left_object_id](left_object_id.md) | 1..1 <br/> EntityReference | The object (parent) of the source/left edge | direct |
| [left_predicate_id](left_predicate_id.md) | 1..1 <br/> EntityReference | The predicate (relation) of the source/left edge | direct |
| [left_subject_label](left_subject_label.md) | 0..1 <br/> Label | The name of the subject (child) of the source/left edge | direct |
| [left_object_label](left_object_label.md) | 0..1 <br/> Label | The name of the object (parent) of the source/left edge | direct |
| [left_predicate_label](left_predicate_label.md) | 0..1 <br/> Label | The name of the predicate of the source/left edge | direct |
| [right_subject_id](right_subject_id.md) | 0..1 <br/> EntityReference | The subject (child) of the matched/right edge, if matchable | direct |
| [right_object_id](right_object_id.md) | 0..1 <br/> EntityReference | The object (parent) of the matched/right edge, if matchable | direct |
| [right_predicate_ids](right_predicate_ids.md) | 0..* <br/> EntityReference | * If the match type is consistent, then all consistent predicates.
* If the match type is identical, then the identical predicate.
* If the match type is OtherRelationship, then all predicates that form a path between right subject and object | direct |
| [right_subject_label](right_subject_label.md) | 0..1 <br/> Label | The name of the subject (child) of the matched/right edge, if matchable | direct |
| [right_object_label](right_object_label.md) | 0..1 <br/> Label | The name of the object (parent) of the matched/right edge, if matchable | direct |
| [right_predicate_labels](right_predicate_labels.md) | 0..* <br/> Label | The names corresponding to the right_predicate_ids | direct |
| [left_subject_is_functional](left_subject_is_functional.md) | 0..1 <br/> None | True if a subject mapping is present, and maps uniquely within the same ontology | direct |
| [left_object_is_functional](left_object_is_functional.md) | 0..1 <br/> None | True if an object mapping is present, and maps uniquely within the same ontology | direct |
| [subject_mapping_predicate](subject_mapping_predicate.md) | 0..1 <br/> EntityReference | The mapping predicate that holds between left_subject_id and right_subject_id | direct |
| [object_mapping_predicate](object_mapping_predicate.md) | 0..1 <br/> EntityReference | The mapping predicate that holds between left_object_id and right_object_id | direct |
| [right_intermediate_ids](right_intermediate_ids.md) | 0..* <br/> EntityReference | None | direct |
| [subject_mapping_cardinality](subject_mapping_cardinality.md) | 0..1 <br/> MappingCardinalityEnum | The mapping cardinality of the subject pair | direct |
| [object_mapping_cardinality](object_mapping_cardinality.md) | 0..1 <br/> MappingCardinalityEnum | The mapping cardinality of the object pair | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [StructureDiffResultSet](StructureDiffResultSet.md) | [results](results.md) | range | RelationalDiff |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:RelationalDiff |
| native | ann:RelationalDiff |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RelationalDiff
description: "A relational diff expresses the difference between an edge in one ontology,\
  \ and an edge (or lack of edge) in\nanother ontology (or a different version of\
  \ the same ontology). The diff is from the perspective of one\nontology (the one\
  \ on the \"left\" side).\n\nFor every edge in the left ontology, the subject and\
  \ object are mapped to the right ontology.\nIf mappings cannot be found then the\
  \ diff is categorized as missing mappings.\nThe predicate is also mapped, with the\
  \ reflexivity assumption.\n\nfor every mapped subject and object pair (the \"right\"\
  \ subject and object), the entailed relationship\nis examined to determine if it\
  \ consistent with the left predicate.\n\n```\nleft_object    <--- mapped to --->\
  \ right_object\n   ^                                  ^\n   |                  \
  \                |\n   |                                  |\n   | left         \
  \                    | right\n   | predicate                        | predicate\n\
  \   |                                  |\n   |                                 \
  \ |\nleft_subject   <--- mapped to ---> right_subject\n```\n\nThe above figure gives\
  \ hows the basic structure. Classification of the edge is done from the perspective\n\
  of the left edge."
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
attributes:
  category:
    name: category
    description: Each match (or lack of match) is placed into exactly one category
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    range: DiffCategory
  left_subject_id:
    name: left_subject_id
    description: The subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - subject
    range: EntityReference
    required: true
  left_object_id:
    name: left_object_id
    description: The object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - object
    range: EntityReference
    required: true
  left_predicate_id:
    name: left_predicate_id
    description: The predicate (relation) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - predicate
    range: EntityReference
    required: true
  left_subject_label:
    name: left_subject_label
    description: The name of the subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - subject
    - label
    range: Label
  left_object_label:
    name: left_object_label
    description: The name of the object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - object
    - label
    range: Label
  left_predicate_label:
    name: left_predicate_label
    description: The name of the predicate of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - predicate
    - label
    range: Label
  right_subject_id:
    name: right_subject_id
    description: The subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - subject
    range: EntityReference
  right_object_id:
    name: right_object_id
    description: The object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - object
    range: EntityReference
  right_predicate_ids:
    name: right_predicate_ids
    description: '* If the match type is consistent, then all consistent predicates.

      * If the match type is identical, then the identical predicate.

      * If the match type is OtherRelationship, then all predicates that form a path
      between right subject and object'
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - predicate
    multivalued: true
    range: EntityReference
  right_subject_label:
    name: right_subject_label
    description: The name of the subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - subject
    - label
    range: Label
  right_object_label:
    name: right_object_label
    description: The name of the object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - object
    - label
    range: Label
  right_predicate_labels:
    name: right_predicate_labels
    description: The names corresponding to the right_predicate_ids
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - predicate
    - label
    multivalued: true
    range: Label
  left_subject_is_functional:
    name: left_subject_is_functional
    description: True if a subject mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - is_functional
  left_object_is_functional:
    name: left_object_is_functional
    description: True if an object mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - is_functional
  subject_mapping_predicate:
    name: subject_mapping_predicate
    description: The mapping predicate that holds between left_subject_id and right_subject_id
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - subject
    - predicate
    range: EntityReference
  object_mapping_predicate:
    name: object_mapping_predicate
    description: The mapping predicate that holds between left_object_id and right_object_id
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - subject
    - predicate
    range: EntityReference
  right_intermediate_ids:
    name: right_intermediate_ids
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    multivalued: true
    range: EntityReference
  subject_mapping_cardinality:
    name: subject_mapping_cardinality
    description: The mapping cardinality of the subject pair
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    range: MappingCardinalityEnum
  object_mapping_cardinality:
    name: object_mapping_cardinality
    description: The mapping cardinality of the object pair
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    range: MappingCardinalityEnum

```
</details>

### Induced

<details>
```yaml
name: RelationalDiff
description: "A relational diff expresses the difference between an edge in one ontology,\
  \ and an edge (or lack of edge) in\nanother ontology (or a different version of\
  \ the same ontology). The diff is from the perspective of one\nontology (the one\
  \ on the \"left\" side).\n\nFor every edge in the left ontology, the subject and\
  \ object are mapped to the right ontology.\nIf mappings cannot be found then the\
  \ diff is categorized as missing mappings.\nThe predicate is also mapped, with the\
  \ reflexivity assumption.\n\nfor every mapped subject and object pair (the \"right\"\
  \ subject and object), the entailed relationship\nis examined to determine if it\
  \ consistent with the left predicate.\n\n```\nleft_object    <--- mapped to --->\
  \ right_object\n   ^                                  ^\n   |                  \
  \                |\n   |                                  |\n   | left         \
  \                    | right\n   | predicate                        | predicate\n\
  \   |                                  |\n   |                                 \
  \ |\nleft_subject   <--- mapped to ---> right_subject\n```\n\nThe above figure gives\
  \ hows the basic structure. Classification of the edge is done from the perspective\n\
  of the left edge."
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
attributes:
  category:
    name: category
    description: Each match (or lack of match) is placed into exactly one category
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    alias: category
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: DiffCategory
  left_subject_id:
    name: left_subject_id
    description: The subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - subject
    alias: left_subject_id
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
    required: true
  left_object_id:
    name: left_object_id
    description: The object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - object
    alias: left_object_id
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
    required: true
  left_predicate_id:
    name: left_predicate_id
    description: The predicate (relation) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - predicate
    alias: left_predicate_id
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
    required: true
  left_subject_label:
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
  left_object_label:
    name: left_object_label
    description: The name of the object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - object
    - label
    alias: left_object_label
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: Label
  left_predicate_label:
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
  right_subject_id:
    name: right_subject_id
    description: The subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - subject
    alias: right_subject_id
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
  right_object_id:
    name: right_object_id
    description: The object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - object
    alias: right_object_id
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
  right_predicate_ids:
    name: right_predicate_ids
    description: '* If the match type is consistent, then all consistent predicates.

      * If the match type is identical, then the identical predicate.

      * If the match type is OtherRelationship, then all predicates that form a path
      between right subject and object'
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - predicate
    multivalued: true
    alias: right_predicate_ids
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
  right_subject_label:
    name: right_subject_label
    description: The name of the subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - right_side
    - subject
    - label
    alias: right_subject_label
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: Label
  right_object_label:
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
  right_predicate_labels:
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
  left_subject_is_functional:
    name: left_subject_is_functional
    description: True if a subject mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - is_functional
    alias: left_subject_is_functional
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: boolean
  left_object_is_functional:
    name: left_object_is_functional
    description: True if an object mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - left_side
    - is_functional
    alias: left_object_is_functional
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: boolean
  subject_mapping_predicate:
    name: subject_mapping_predicate
    description: The mapping predicate that holds between left_subject_id and right_subject_id
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    mixins:
    - subject
    - predicate
    alias: subject_mapping_predicate
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
  object_mapping_predicate:
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
  right_intermediate_ids:
    name: right_intermediate_ids
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    multivalued: true
    alias: right_intermediate_ids
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: EntityReference
  subject_mapping_cardinality:
    name: subject_mapping_cardinality
    description: The mapping cardinality of the subject pair
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    alias: subject_mapping_cardinality
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: MappingCardinalityEnum
  object_mapping_cardinality:
    name: object_mapping_cardinality
    description: The mapping cardinality of the object pair
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    alias: object_mapping_cardinality
    owner: RelationalDiff
    domain_of:
    - RelationalDiff
    range: MappingCardinalityEnum

```
</details>