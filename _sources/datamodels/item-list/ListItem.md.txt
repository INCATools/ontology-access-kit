

# Class: ListItem


_an item in an item list_





URI: [schema:ListItem](http://schema.org/ListItem)






```{mermaid}
 classDiagram
    class ListItem
    click ListItem href "../ListItem"
      ListItem : elementId
        
      ListItem : idType
        
      ListItem : item
        
          
    
    
    ListItem --> "0..1" Thing : item
    click Thing href "../Thing"

        
      ListItem : position
        
      ListItem : previousItem
        
          
    
    
    ListItem --> "0..1" ListItem : previousItem
    click ListItem href "../ListItem"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [elementId](elementId.md) | 0..1 <br/> [String](String.md) | The identifier of the item | direct |
| [idType](idType.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of the identifier | direct |
| [item](item.md) | 0..1 <br/> [Thing](Thing.md) | The item represented by the list item | direct |
| [position](position.md) | 0..1 <br/> [Integer](Integer.md) | The position of the item in the list | direct |
| [previousItem](previousItem.md) | 0..1 <br/> [ListItem](ListItem.md) | The previous item in the list | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ItemList](ItemList.md) | [itemListElements](itemListElements.md) | range | [ListItem](ListItem.md) |
| [ItemList](ItemList.md) | [itemMetadataMap](itemMetadataMap.md) | range | [ListItem](ListItem.md) |
| [ListItem](ListItem.md) | [previousItem](previousItem.md) | range | [ListItem](ListItem.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | schema:ListItem |
| native | itemList:ListItem |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ListItem
description: an item in an item list
from_schema: https://w3id.org/oak/item-list
attributes:
  elementId:
    name: elementId
    description: 'The identifier of the item. Note this can be a ''proper'' CURIE
      ID or any other unique field, for example symbol

      '
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    key: true
    domain_of:
    - ListItem
    range: string
    required: true
  idType:
    name: idType
    description: The type of the identifier. For example, if the id is a symbol, this
      would be 'symbol'
    examples:
    - value: biolink:symbol
    - value: skos:prefLabel
    - value: schema:identifier
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    domain_of:
    - ListItem
    range: uriorcurie
  item:
    name: item
    description: The item represented by the list item
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:item
    domain_of:
    - ListItem
    range: Thing
    inlined: true
  position:
    name: position
    description: The position of the item in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:position
    domain_of:
    - ListItem
    range: integer
  previousItem:
    name: previousItem
    description: The previous item in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:previousItem
    domain_of:
    - ListItem
    range: ListItem
class_uri: schema:ListItem

```
</details>

### Induced

<details>
```yaml
name: ListItem
description: an item in an item list
from_schema: https://w3id.org/oak/item-list
attributes:
  elementId:
    name: elementId
    description: 'The identifier of the item. Note this can be a ''proper'' CURIE
      ID or any other unique field, for example symbol

      '
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    key: true
    alias: elementId
    owner: ListItem
    domain_of:
    - ListItem
    range: string
    required: true
  idType:
    name: idType
    description: The type of the identifier. For example, if the id is a symbol, this
      would be 'symbol'
    examples:
    - value: biolink:symbol
    - value: skos:prefLabel
    - value: schema:identifier
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: idType
    owner: ListItem
    domain_of:
    - ListItem
    range: uriorcurie
  item:
    name: item
    description: The item represented by the list item
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:item
    alias: item
    owner: ListItem
    domain_of:
    - ListItem
    range: Thing
    inlined: true
  position:
    name: position
    description: The position of the item in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:position
    alias: position
    owner: ListItem
    domain_of:
    - ListItem
    range: integer
  previousItem:
    name: previousItem
    description: The previous item in the list
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    slot_uri: schema:previousItem
    alias: previousItem
    owner: ListItem
    domain_of:
    - ListItem
    range: ListItem
class_uri: schema:ListItem

```
</details>