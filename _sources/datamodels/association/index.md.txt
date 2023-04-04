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
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |
| [ParserConfiguration](ParserConfiguration.md) |  |
| [PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association |
| [RollupGroup](RollupGroup.md) |  |


## Slots

| Slot | Description |
| --- | --- |
| [associations](associations.md) |  |
| [group_object](group_object.md) | An ontology entity that is the ancestor of the objects in the group's  |
| [include_association_attributes](include_association_attributes.md) | If true, then the parser will include non S/P/O properties as additional attr... |
| [object](object.md) | An ontology entity that is associated with the subject |
| [predicate](predicate.md) | The type of relationship between the subject and object |
| [preserve_negated_associations](preserve_negated_associations.md) | If true, then the parser will keep negated associations in the output |
| [property_values](property_values.md) |  |
| [sub_groups](sub_groups.md) | Container for groups within a rollup group |
| [subject](subject.md) | The thing which the association is about |


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
