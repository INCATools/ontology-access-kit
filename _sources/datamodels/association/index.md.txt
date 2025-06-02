# OAK Association Data Model

A data model for representing generic associations and changes of these associations.

The core data model is broad, encompassing the W3 Open Annotation data model as well
as common ontology annotation data models using in the biosciences, such as the GAF
data model used by the Gene Ontology, and the HPOA association model used by the Human Phenotype
Ontology.

The core elements of the data model are the *subject* (the entity being described) and the *object*
(the term, descriptor, or other entity that describes some aspect of the subject).

A subject might be a biological entity such as gene, drug, disease, person, or chemical. The object is typically
a class from an ontology such as a term from GO.

URI: https://w3id.org/oak/association

Name: association



## Classes

| Class | Description |
| --- | --- |
| [Any](Any.md) | None |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations. |
| [PairwiseCoAssociation](PairwiseCoAssociation.md) | A collection of subjects co-associated with two objects |
| [ParserConfiguration](ParserConfiguration.md) | Settings that determine behavior when parsing associations. |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Association](Association.md) | A generic association between a thing (subject) and another thing (object). |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object). |
| [PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association. |
| [RollupGroup](RollupGroup.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | The knowledge source that aggregated the association |
| [associations](associations.md) | A collection of associations |
| [associations_for_subjects_in_common](associations_for_subjects_in_common.md) |  |
| [closure_delta](closure_delta.md) |  |
| [closure_information_content_delta](closure_information_content_delta.md) |  |
| [closure_predicates](closure_predicates.md) | The set of predicates used to determine if the new association object is a sp... |
| [comments](comments.md) | Comments about the association |
| [core_triple](core_triple.md) | A grouping slot for the core subject-predicate-object triple |
| [creation_date](creation_date.md) | The date the association was created |
| [date](date.md) | The date the association was created or last updated |
| [denormalized_slot](denormalized_slot.md) | denormalized slots are for models that follow a denormalized data model |
| [diff_slot](diff_slot.md) | A mixin for any paired slot that pertains to an association diff |
| [evidence_type](evidence_type.md) | The type of evidence supporting the association |
| [group_object](group_object.md) | An ontology entity that is the ancestor of the objects in the group's  |
| [include_association_attributes](include_association_attributes.md) | If true, then the parser will include non S/P/O properties as additional attr... |
| [is_creation](is_creation.md) |  |
| [is_deletion](is_deletion.md) |  |
| [is_generalization](is_generalization.md) | True if the association was inferred to become more general (based on closure... |
| [is_migration](is_migration.md) | if the object (e |
| [is_specialization](is_specialization.md) | True if the association was inferred to become more specific (based on closur... |
| [modification_date](modification_date.md) | The date the association was last modified |
| [negated](negated.md) | True if the association is negated - i |
| [new_date](new_date.md) | The date of the new association |
| [new_object](new_object.md) | The object (e |
| [new_predicate](new_predicate.md) | If the association diff is a change in predicate, this is the predicate on th... |
| [number_subject_unique_to_entity1](number_subject_unique_to_entity1.md) |  |
| [number_subject_unique_to_entity2](number_subject_unique_to_entity2.md) |  |
| [number_subjects_in_common](number_subjects_in_common.md) |  |
| [number_subjects_in_union](number_subjects_in_union.md) |  |
| [object](object.md) | An ontology entity that is associated with the subject |
| [object1](object1.md) |  |
| [object1_label](object1_label.md) |  |
| [object2](object2.md) |  |
| [object2_label](object2_label.md) |  |
| [object_closure](object_closure.md) | The set of objects that are related to the object of the association via the ... |
| [object_closure_label](object_closure_label.md) | The set of objects that are related to the object of the association via the ... |
| [object_label](object_label.md) | The label of the ontology entity that is associated with the subject |
| [old_date](old_date.md) | The date of the old association |
| [old_object](old_object.md) | The object (e |
| [old_object_obsolete](old_object_obsolete.md) | if the object (e |
| [old_predicate](old_predicate.md) | If the association diff is a change in predicate, this is the predicate on th... |
| [original_object](original_object.md) | The original object of the association prior to normalization |
| [original_predicate](original_predicate.md) | The original subject of the association prior to normalization |
| [original_subject](original_subject.md) | The original subject of the association prior to normalization |
| [predicate](predicate.md) | The type of relationship between the subject and object |
| [predicate_label](predicate_label.md) | The label of the type of relationship between the subject and object |
| [preserve_negated_associations](preserve_negated_associations.md) | If true, then the parser will keep negated associations in the output |
| [primary_knowledge_source](primary_knowledge_source.md) | The primary knowledge source for the association |
| [property_values](property_values.md) | Arbitrary key-value pairs with additional information about the association |
| [proportion_entity1_subjects_in_entity2](proportion_entity1_subjects_in_entity2.md) |  |
| [proportion_entity2_subjects_in_entity1](proportion_entity2_subjects_in_entity1.md) |  |
| [proportion_subjects_in_common](proportion_subjects_in_common.md) |  |
| [publication_is_added](publication_is_added.md) | True if the publication was not present in the old association set (and prese... |
| [publication_is_deleted](publication_is_deleted.md) | True if the publication is not present in the new association set (and presen... |
| [publications](publications.md) | The publications that support the association |
| [sub_groups](sub_groups.md) | Container for groups within a rollup group |
| [subject](subject.md) | The thing which the association is about |
| [subject_closure](subject_closure.md) | The set of subjects that are related to the subject of the association via th... |
| [subject_closure_label](subject_closure_label.md) | The set of subjects that are related to the subject of the association via th... |
| [subject_label](subject_label.md) | The label of the thing which the association is about |
| [subjects_in_common](subjects_in_common.md) |  |
| [summary_group](summary_group.md) | The field used to group an association diff summary |
| [supporting_objects](supporting_objects.md) | The objects that support the association |
| [value_or_object](value_or_object.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
