

# Class: ItemListCollection


_a set of item lists_





URI: [itemList:ItemListCollection](https://w3id.org/linkml/item-list/ItemListCollection)




```{mermaid}
 classDiagram
    class ItemListCollection
      ItemListCollection : itemLists
        
          ItemListCollection --> ItemList : itemLists
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [itemLists](itemLists.md) | 0..* <br/> [ItemList](ItemList.md) |  | direct |







## Aliases


* item list catalog



## Comments

* this is used for when you wish to pass around multiple lists.

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | itemList:ItemListCollection |
| native | itemList:ItemListCollection |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ItemListCollection
description: a set of item lists
comments:
- this is used for when you wish to pass around multiple lists.
from_schema: https://w3id.org/oak/item-list
aliases:
- item list catalog
attributes:
  itemLists:
    name: itemLists
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    multivalued: true
    domain_of:
    - ItemListCollection
    range: ItemList
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: ItemListCollection
description: a set of item lists
comments:
- this is used for when you wish to pass around multiple lists.
from_schema: https://w3id.org/oak/item-list
aliases:
- item list catalog
attributes:
  itemLists:
    name: itemLists
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    multivalued: true
    alias: itemLists
    owner: ItemListCollection
    domain_of:
    - ItemListCollection
    range: ItemList
    inlined: true

```
</details>