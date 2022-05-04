# Class: RelationalDiff
_A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in another ontology (or a different version of the same ontology). The diff is from the perspective of one ontology (the one on the "left" side). For every edge in the left ontology, the subject and object are mapped to the right ontology. If mappings cannot be found then the diff is categorized as missing mappings. The predicate is also mapped, with the reflexivity assumption. for every mapped subject and object pair (the "right" subject and object), the entailed relationship is examined to determine if it consistent with the left predicate._





URI: [ann:RelationalDiff](https://w3id.org/linkml/text_annotator/RelationalDiff)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [category](category.md) | [DiffCategory](DiffCategory.md) | 0..1 | Each match (or lack of match) is placed into exactly one category  | . |
| [left_subject_id](left_subject_id.md) | [uriorcurie](uriorcurie.md) | 1..1 | The subject (child) of the source/left edge  | . |
| [left_object_id](left_object_id.md) | [uriorcurie](uriorcurie.md) | 1..1 | The object (parent) of the source/left edge  | . |
| [left_predicate_id](left_predicate_id.md) | [uriorcurie](uriorcurie.md) | 1..1 | The predicate (relation) of the source/left edge  | . |
| [left_subject_name](left_subject_name.md) | [string](string.md) | 0..1 | The name of the subject (child) of the source/left edge  | . |
| [left_object_name](left_object_name.md) | [string](string.md) | 0..1 | The name of the object (parent) of the source/left edge  | . |
| [left_predicate_name](left_predicate_name.md) | [string](string.md) | 0..1 | The name of the predicate of the source/left edge  | . |
| [right_subject_id](right_subject_id.md) | [uriorcurie](uriorcurie.md) | 0..1 | The subject (child) of the matched/right edge, if matchable  | . |
| [right_object_id](right_object_id.md) | [uriorcurie](uriorcurie.md) | 0..1 | The object (parent) of the matched/right edge, if matchable  | . |
| [right_predicate_ids](right_predicate_ids.md) | [uriorcurie](uriorcurie.md) | 0..* | If the match type is consistent, then all consistent predicates. If the match type is identical, then the identical predicate. If the match type is OtherRelationship, then all predicates that form a path between right subject and object  | . |
| [right_subject_name](right_subject_name.md) | [string](string.md) | 0..1 | The name of the subject (child) of the matched/right edge, if matchable  | . |
| [right_object_name](right_object_name.md) | [string](string.md) | 0..1 | The name of the object (parent) of the matched/right edge, if matchable  | . |
| [right_predicate_names](right_predicate_names.md) | [string](string.md) | 0..* | The names corresponding to the right_predicate_ids  | . |
| [left_subject_is_functional](left_subject_is_functional.md) | [boolean](boolean.md) | 0..1 | True if a subject mapping is present, and maps uniquely within the same ontology  | . |
| [left_object_is_functional](left_object_is_functional.md) | [boolean](boolean.md) | 0..1 | True if an object mapping is present, and maps uniquely within the same ontology  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [StructureDiffResultSet](StructureDiffResultSet.md) | [results](results.md) | range | RelationalDiff |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RelationalDiff
description: A relational diff expresses the difference between an edge in one ontology,
  and an edge (or lack of edge) in another ontology (or a different version of the
  same ontology). The diff is from the perspective of one ontology (the one on the
  "left" side). For every edge in the left ontology, the subject and object are mapped
  to the right ontology. If mappings cannot be found then the diff is categorized
  as missing mappings. The predicate is also mapped, with the reflexivity assumption.
  for every mapped subject and object pair (the "right" subject and object), the entailed
  relationship is examined to determine if it consistent with the left predicate.
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  category:
    name: category
    description: Each match (or lack of match) is placed into exactly one category
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: DiffCategory
  left_subject_id:
    name: left_subject_id
    description: The subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: uriorcurie
    required: true
  left_object_id:
    name: left_object_id
    description: The object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: uriorcurie
    required: true
  left_predicate_id:
    name: left_predicate_id
    description: The predicate (relation) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: uriorcurie
    required: true
  left_subject_name:
    name: left_subject_name
    description: The name of the subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  left_object_name:
    name: left_object_name
    description: The name of the object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  left_predicate_name:
    name: left_predicate_name
    description: The name of the predicate of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  right_subject_id:
    name: right_subject_id
    description: The subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: uriorcurie
  right_object_id:
    name: right_object_id
    description: The object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: uriorcurie
  right_predicate_ids:
    name: right_predicate_ids
    description: If the match type is consistent, then all consistent predicates.
      If the match type is identical, then the identical predicate. If the match type
      is OtherRelationship, then all predicates that form a path between right subject
      and object
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    range: uriorcurie
  right_subject_name:
    name: right_subject_name
    description: The name of the subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  right_object_name:
    name: right_object_name
    description: The name of the object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  right_predicate_names:
    name: right_predicate_names
    description: The names corresponding to the right_predicate_ids
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
  left_subject_is_functional:
    name: left_subject_is_functional
    description: True if a subject mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: boolean
  left_object_is_functional:
    name: left_object_is_functional
    description: True if an object mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: RelationalDiff
description: A relational diff expresses the difference between an edge in one ontology,
  and an edge (or lack of edge) in another ontology (or a different version of the
  same ontology). The diff is from the perspective of one ontology (the one on the
  "left" side). For every edge in the left ontology, the subject and object are mapped
  to the right ontology. If mappings cannot be found then the diff is categorized
  as missing mappings. The predicate is also mapped, with the reflexivity assumption.
  for every mapped subject and object pair (the "right" subject and object), the entailed
  relationship is examined to determine if it consistent with the left predicate.
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  category:
    name: category
    description: Each match (or lack of match) is placed into exactly one category
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: category
    owner: RelationalDiff
    range: DiffCategory
  left_subject_id:
    name: left_subject_id
    description: The subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_subject_id
    owner: RelationalDiff
    range: uriorcurie
    required: true
  left_object_id:
    name: left_object_id
    description: The object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_object_id
    owner: RelationalDiff
    range: uriorcurie
    required: true
  left_predicate_id:
    name: left_predicate_id
    description: The predicate (relation) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_predicate_id
    owner: RelationalDiff
    range: uriorcurie
    required: true
  left_subject_name:
    name: left_subject_name
    description: The name of the subject (child) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_subject_name
    owner: RelationalDiff
    range: string
  left_object_name:
    name: left_object_name
    description: The name of the object (parent) of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_object_name
    owner: RelationalDiff
    range: string
  left_predicate_name:
    name: left_predicate_name
    description: The name of the predicate of the source/left edge
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_predicate_name
    owner: RelationalDiff
    range: string
  right_subject_id:
    name: right_subject_id
    description: The subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: right_subject_id
    owner: RelationalDiff
    range: uriorcurie
  right_object_id:
    name: right_object_id
    description: The object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: right_object_id
    owner: RelationalDiff
    range: uriorcurie
  right_predicate_ids:
    name: right_predicate_ids
    description: If the match type is consistent, then all consistent predicates.
      If the match type is identical, then the identical predicate. If the match type
      is OtherRelationship, then all predicates that form a path between right subject
      and object
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    alias: right_predicate_ids
    owner: RelationalDiff
    range: uriorcurie
  right_subject_name:
    name: right_subject_name
    description: The name of the subject (child) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: right_subject_name
    owner: RelationalDiff
    range: string
  right_object_name:
    name: right_object_name
    description: The name of the object (parent) of the matched/right edge, if matchable
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: right_object_name
    owner: RelationalDiff
    range: string
  right_predicate_names:
    name: right_predicate_names
    description: The names corresponding to the right_predicate_ids
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    alias: right_predicate_names
    owner: RelationalDiff
    range: string
  left_subject_is_functional:
    name: left_subject_is_functional
    description: True if a subject mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_subject_is_functional
    owner: RelationalDiff
    range: boolean
  left_object_is_functional:
    name: left_object_is_functional
    description: True if an object mapping is present, and maps uniquely within the
      same ontology
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_object_is_functional
    owner: RelationalDiff
    range: boolean

```
</details>