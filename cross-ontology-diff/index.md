# Cross-Ontology Diff

A datamodel for representing the results of relational diffs across a pair of ontologies connected by mappings

URI: https://w3id.org/linkml/cross_ontology_diff
Name: cross-ontology-diff



## Classes

| Class | Description |
| --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |
| [StructureDiffResultSet](StructureDiffResultSet.md) | A collection of relational diff results |


## Slots

| Slot | Description |
| --- | --- |
| [category](category.md) | Each match (or lack of match) is placed into exactly one category |
| [is_functional](is_functional.md) | Maps to exactly one thing |
| [label](label.md) | human readable label |
| [left_object_id](left_object_id.md) | The object (parent) of the source/left edge |
| [left_object_is_functional](left_object_is_functional.md) | True if an object mapping is present, and maps uniquely within the same ontol... |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge |
| [left_predicate_id](left_predicate_id.md) | The predicate (relation) of the source/left edge |
| [left_predicate_label](left_predicate_label.md) | The name of the predicate of the source/left edge |
| [left_side](left_side.md) | The first ontology is arbitrarily designated the left side |
| [left_source](left_source.md) | Ontology source for left entities |
| [left_subject_id](left_subject_id.md) | The subject (child) of the source/left edge |
| [left_subject_is_functional](left_subject_is_functional.md) | True if a subject mapping is present, and maps uniquely within the same ontol... |
| [left_subject_label](left_subject_label.md) | The name of the subject (child) of the source/left edge |
| [object](object.md) | The object node on left or right side |
| [object_mapping_cardinality](object_mapping_cardinality.md) | The mapping cardinality of the object pair |
| [object_mapping_predicate](object_mapping_predicate.md) | The mapping predicate that holds between left_object_id and right_object_id |
| [predicate](predicate.md) | The relationship type between subject and object on left or right side |
| [results](results.md) | all differences between a pair of ontologies |
| [right_intermediate_ids](right_intermediate_ids.md) |  |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable |
| [right_predicate_ids](right_predicate_ids.md) | * If the match type is consistent, then all consistent predicates |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids |
| [right_side](right_side.md) | The second ontology is arbitrarily designated the right side |
| [right_source](right_source.md) | Ontology source for right entities |
| [right_subject_id](right_subject_id.md) | The subject (child) of the matched/right edge, if matchable |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable |
| [side](side.md) | left or right side |
| [subject](subject.md) | The child node on left or right side |
| [subject_mapping_cardinality](subject_mapping_cardinality.md) | The mapping cardinality of the subject pair |
| [subject_mapping_predicate](subject_mapping_predicate.md) | The mapping predicate that holds between left_subject_id and right_subject_id |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [DiffCategory](DiffCategory.md) | Category of the cross-ontology diff, from the perspective of the left-hand ed... |
| [MappingCardinalityEnum](MappingCardinalityEnum.md) |  |


## Types

| Type | Description |
| --- | --- |
| [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | A binary (true or false) value |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | a compact URI |
| [xsd:date](http://www.w3.org/2001/XMLSchema#date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | The combination of a date and time |
| [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](http://www.w3.org/2001/XMLSchema#double) | A real number that conforms to the xsd:double specification |
| [EntityReference](EntityReference.md) | A reference to a mapped entity |
| [xsd:float](http://www.w3.org/2001/XMLSchema#float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | An integer |
| [Label](Label.md) | A string that is used as a human-readable label |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [Source](Source.md) | The name of an ontology that acts as a source |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
