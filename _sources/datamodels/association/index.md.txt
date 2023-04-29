# OAK Association Data Model

A datamodel for representing generic associations.

The core datamodel is broad, encompassing the W3 Open Annotation data model as well
as common ontology annotation data models using in the biosciences.

URI: https://w3id.org/oak/association
Name: association



## Classes

| Class | Description |
| --- | --- |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |
| [AssociationChange](AssociationChange.md) |  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |
| [ParserConfiguration](ParserConfiguration.md) |  |
| [PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association |
| [RollupGroup](RollupGroup.md) |  |


## Slots

| Slot | Description |
| --- | --- |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | The knowledge source that aggregated the association |
| [associations](associations.md) |  |
| [closure_predicates](closure_predicates.md) |  |
| [creation_date](creation_date.md) |  |
| [date](date.md) |  |
| [denormalized_slot](denormalized_slot.md) | denormalized slots are for models that follow a denormalized data model |
| [group_object](group_object.md) | An ontology entity that is the ancestor of the objects in the group's  |
| [include_association_attributes](include_association_attributes.md) | If true, then the parser will include non S/P/O properties as additional attr... |
| [is_creation](is_creation.md) |  |
| [is_deletion](is_deletion.md) |  |
| [is_generalization](is_generalization.md) |  |
| [is_migration](is_migration.md) |  |
| [is_specialization](is_specialization.md) |  |
| [modification_date](modification_date.md) |  |
| [new_date](new_date.md) |  |
| [new_object](new_object.md) |  |
| [new_predicate](new_predicate.md) |  |
| [object](object.md) | An ontology entity that is associated with the subject |
| [object_label](object_label.md) | The label of the ontology entity that is associated with the subject |
| [old_date](old_date.md) |  |
| [old_object](old_object.md) |  |
| [old_object_obsolete](old_object_obsolete.md) |  |
| [old_predicate](old_predicate.md) |  |
| [original_object](original_object.md) | The original object of the association prior to normalization |
| [original_predicate](original_predicate.md) | The original subject of the association prior to normalization |
| [original_subject](original_subject.md) | The original subject of the association prior to normalization |
| [predicate](predicate.md) | The type of relationship between the subject and object |
| [predicate_label](predicate_label.md) | The label of the type of relationship between the subject and object |
| [preserve_negated_associations](preserve_negated_associations.md) | If true, then the parser will keep negated associations in the output |
| [primary_knowledge_source](primary_knowledge_source.md) | The primary knowledge source for the association |
| [property_values](property_values.md) |  |
| [publication_is_added](publication_is_added.md) |  |
| [publication_is_deleted](publication_is_deleted.md) |  |
| [publications](publications.md) | The publications that support the association |
| [sub_groups](sub_groups.md) | Container for groups within a rollup group |
| [subject](subject.md) | The thing which the association is about |
| [subject_label](subject_label.md) | The label of the thing which the association is about |
| [summary_group](summary_group.md) |  |


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
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
