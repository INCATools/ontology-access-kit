# Item List Data Model

A data model for representing simple lists of entities such as genes. The data model is based on the schema.org ItemList class.

URI: https://w3id.org/oak/item-list

Name: itemList



## Classes

| Class | Description |
| --- | --- |
| [ItemList](ItemList.md) | a list of entities plus metadata |
| [ItemListCollection](ItemListCollection.md) | a set of item lists |
| [ListItem](ListItem.md) | an item in an item list |
| [Thing](Thing.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [additionalType](additionalType.md) | An additional type for the item, typically used for adding more specific type... |
| [categories](categories.md) | Controlled terms used to categorize an element |
| [description](description.md) | A description of the list |
| [elementId](elementId.md) | The identifier of the item |
| [id](id.md) | The identifier of the list |
| [identifiers](identifiers.md) | A list of identifiers for the item |
| [idType](idType.md) | The type of the identifier |
| [item](item.md) | The item represented by the list item |
| [itemListElements](itemListElements.md) | The entities in the list, represented as a simple list |
| [itemLists](itemLists.md) |  |
| [itemMetadataMap](itemMetadataMap.md) | The entities in the list, represented as a map keyed by item id |
| [keywords](keywords.md) | Keywords or tags used to describe the element |
| [name](name.md) | The name of the list |
| [numberOfItems](numberOfItems.md) | The order of the items in the list |
| [position](position.md) | The position of the item in the list |
| [previousItem](previousItem.md) | The previous item in the list |
| [type](type.md) | The type of the item |
| [url](url.md) | A URL for the item |
| [wasGeneratedBy](wasGeneratedBy.md) | The provenance of the list, for example a script that generated the list |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ItemListOrderType](ItemListOrderType.md) | The order of the items in the list |


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
