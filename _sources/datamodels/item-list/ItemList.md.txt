# Class: ItemList
_a list of entities plus metadata_




URI: [schema:ItemList](http://schema.org/ItemList)



```{mermaid}
 classDiagram
    class ItemList
      ItemList : additionalType
        
      ItemList : categories
        
      ItemList : description
        
      ItemList : id
        
      ItemList : itemListElements
        
          ItemList ..> ListItem : itemListElements
        
      ItemList : itemMetadataMap
        
          ItemList ..> ListItem : itemMetadataMap
        
      ItemList : keywords
        
      ItemList : name
        
      ItemList : numberOfItems
        
          ItemList ..> ItemListOrderType : numberOfItems
        
      ItemList : wasGeneratedBy
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [name](name.md) | 0..1 <br/> [String](String.md) |  | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) |  | direct |
| [itemListElements](itemListElements.md) | 0..* <br/> [ListItem](ListItem.md) | The entities in the list, represented as a simple list | direct |
| [numberOfItems](numberOfItems.md) | 0..1 <br/> [ItemListOrderType](ItemListOrderType.md) | The order of the items in the list | direct |
| [itemMetadataMap](itemMetadataMap.md) | 0..* <br/> [ListItem](ListItem.md) | The entities in the list, represented as a map keyed by item id | direct |
| [categories](categories.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | Controlled terms used to categorize an element | direct |
| [keywords](keywords.md) | 0..* <br/> [String](String.md) | Keywords or tags used to describe the element | direct |
| [additionalType](additionalType.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | An additional type for the item, typically used for adding more specific type... | direct |
| [wasGeneratedBy](wasGeneratedBy.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | The provenance of the list, for example a script that generated the list | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ItemListCollection](ItemListCollection.md) | [itemLists](itemLists.md) | range | [ItemList](ItemList.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | schema:ItemList |
| native | itemList:ItemList |
| close | rdf:List |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ItemList
description: a list of entities plus metadata
from_schema: https://w3id.org/oak/item-list
close_mappings:
- rdf:List
rank: 1000
attributes:
  id:
    name: id
    description: The identifier of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    range: uriorcurie
  name:
    name: name
    description: The name of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    range: string
  description:
    name: description
    description: A description of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    range: string
  itemListElements:
    name: itemListElements
    description: The entities in the list, represented as a simple list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: itemListElement
    slot_uri: schema:itemListElement
    multivalued: true
    range: ListItem
    inlined: false
  numberOfItems:
    name: numberOfItems
    description: The order of the items in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:numberOfItems
    range: ItemListOrderType
  itemMetadataMap:
    name: itemMetadataMap
    description: The entities in the list, represented as a map keyed by item id
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    multivalued: true
    range: ListItem
    inlined: true
  categories:
    name: categories
    description: Controlled terms used to categorize an element.
    comments:
    - if you wish to use uncontrolled terms or terms that lack identifiers then use
      the keywords element
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: category
    slot_uri: dcterms:subject
    multivalued: true
    range: uriorcurie
  keywords:
    name: keywords
    description: Keywords or tags used to describe the element
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: keyword
    slot_uri: schema:keywords
    multivalued: true
    range: string
  additionalType:
    name: additionalType
    description: An additional type for the item, typically used for adding more specific
      types from external vocabularies in microdata syntax. This is a relationship
      between something and a class that the thing is in. In RDFa syntax, it is better
      to use the native RDFa syntax - the 'typeof' attribute - for multiple types.
      Schema.org tools may have only weaker understanding of extra types, in particular
      those defined externally.
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:additionalType
    multivalued: true
    range: uriorcurie
  wasGeneratedBy:
    name: wasGeneratedBy
    description: The provenance of the list, for example a script that generated the
      list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: prov:wasGeneratedBy
    multivalued: true
    range: uriorcurie
class_uri: schema:ItemList

```
</details>

### Induced

<details>
```yaml
name: ItemList
description: a list of entities plus metadata
from_schema: https://w3id.org/oak/item-list
close_mappings:
- rdf:List
rank: 1000
attributes:
  id:
    name: id
    description: The identifier of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: id
    owner: ItemList
    domain_of:
    - ItemList
    - ListItem
    range: uriorcurie
  name:
    name: name
    description: The name of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: name
    owner: ItemList
    domain_of:
    - ItemList
    - Thing
    range: string
  description:
    name: description
    description: A description of the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: description
    owner: ItemList
    domain_of:
    - ItemList
    - Thing
    range: string
  itemListElements:
    name: itemListElements
    description: The entities in the list, represented as a simple list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: itemListElement
    slot_uri: schema:itemListElement
    multivalued: true
    alias: itemListElements
    owner: ItemList
    domain_of:
    - ItemList
    range: ListItem
    inlined: false
  numberOfItems:
    name: numberOfItems
    description: The order of the items in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:numberOfItems
    alias: numberOfItems
    owner: ItemList
    domain_of:
    - ItemList
    range: ItemListOrderType
  itemMetadataMap:
    name: itemMetadataMap
    description: The entities in the list, represented as a map keyed by item id
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    multivalued: true
    alias: itemMetadataMap
    owner: ItemList
    domain_of:
    - ItemList
    range: ListItem
    inlined: true
  categories:
    name: categories
    description: Controlled terms used to categorize an element.
    comments:
    - if you wish to use uncontrolled terms or terms that lack identifiers then use
      the keywords element
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: category
    slot_uri: dcterms:subject
    multivalued: true
    alias: categories
    owner: ItemList
    domain_of:
    - ItemList
    range: uriorcurie
  keywords:
    name: keywords
    description: Keywords or tags used to describe the element
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    singular_name: keyword
    slot_uri: schema:keywords
    multivalued: true
    alias: keywords
    owner: ItemList
    domain_of:
    - ItemList
    range: string
  additionalType:
    name: additionalType
    description: An additional type for the item, typically used for adding more specific
      types from external vocabularies in microdata syntax. This is a relationship
      between something and a class that the thing is in. In RDFa syntax, it is better
      to use the native RDFa syntax - the 'typeof' attribute - for multiple types.
      Schema.org tools may have only weaker understanding of extra types, in particular
      those defined externally.
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:additionalType
    multivalued: true
    alias: additionalType
    owner: ItemList
    domain_of:
    - ItemList
    range: uriorcurie
  wasGeneratedBy:
    name: wasGeneratedBy
    description: The provenance of the list, for example a script that generated the
      list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: prov:wasGeneratedBy
    multivalued: true
    alias: wasGeneratedBy
    owner: ItemList
    domain_of:
    - ItemList
    range: uriorcurie
class_uri: schema:ItemList

```
</details>