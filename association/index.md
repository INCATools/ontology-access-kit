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
| [PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association |


## Slots

| Slot | Description |
| --- | --- |
| [object](object.md) | An ontology entity that is associated with the subject |
| [predicate](predicate.md) | The type of relationship between the subject and object |
| [property_values](property_values.md) |  |
| [subject](subject.md) | The thing which the association is about |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [xsd:boolean](xsd:boolean) | A binary (true or false) value |
| [xsd:string](xsd:string) | a compact URI |
| [xsd:date](xsd:date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](xsd:dateTime) | The combination of a date and time |
| [xsd:decimal](xsd:decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](xsd:double) | A real number that conforms to the xsd:double specification |
| [xsd:float](xsd:float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](xsd:integer) | An integer |
| [xsd:string](xsd:string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [xsd:string](xsd:string) | A character string |
| [xsd:dateTime](xsd:dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](xsd:anyURI) | a complete URI |
| [xsd:anyURI](xsd:anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
