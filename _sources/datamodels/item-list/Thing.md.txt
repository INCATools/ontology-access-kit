

# Class: Thing



URI: [schema:Thing](http://schema.org/Thing)






```{mermaid}
 classDiagram
    class Thing
    click Thing href "../Thing"
      Thing : description
        
      Thing : id
        
      Thing : identifiers
        
      Thing : name
        
      Thing : type
        
      Thing : url
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | The identifier of the item | direct |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of the item | direct |
| [url](url.md) | 0..1 <br/> [Uri](Uri.md) | A URL for the item | direct |
| [identifiers](identifiers.md) | * <br/> [Uriorcurie](Uriorcurie.md) | A list of identifiers for the item | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) | A description of the item | direct |
| [type](type.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of the item | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ListItem](ListItem.md) | [item](item.md) | range | [Thing](Thing.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | schema:Thing |
| native | itemList:Thing |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Thing
from_schema: https://w3id.org/oak/item-list
attributes:
  id:
    name: id
    description: The identifier of the item. Note this can be a 'proper' CURIE ID
      or any other unique field, for example symbol
    from_schema: https://w3id.org/oak/item-list
    slot_uri: schema:identifier
    identifier: true
    domain_of:
    - ItemList
    - Thing
    range: uriorcurie
    required: true
  name:
    name: name
    description: The name of the item
    from_schema: https://w3id.org/oak/item-list
    slot_uri: rdfs:label
    domain_of:
    - ItemList
    - Thing
    range: string
  url:
    name: url
    description: A URL for the item
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    domain_of:
    - Thing
    range: uri
  identifiers:
    name: identifiers
    description: A list of identifiers for the item. For example, if the id is a symbol,
      this would be a list of identifiers for the item, such as HGNC, MGI, etc.
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true
  description:
    name: description
    description: A description of the item
    from_schema: https://w3id.org/oak/item-list
    domain_of:
    - ItemList
    - Thing
    range: string
  type:
    name: type
    description: The type of the item.
    examples:
    - value: biolink:Gene
    - value: schema:Person
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    domain_of:
    - Thing
    range: uriorcurie
class_uri: schema:Thing

```
</details>

### Induced

<details>
```yaml
name: Thing
from_schema: https://w3id.org/oak/item-list
attributes:
  id:
    name: id
    description: The identifier of the item. Note this can be a 'proper' CURIE ID
      or any other unique field, for example symbol
    from_schema: https://w3id.org/oak/item-list
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: Thing
    domain_of:
    - ItemList
    - Thing
    range: uriorcurie
    required: true
  name:
    name: name
    description: The name of the item
    from_schema: https://w3id.org/oak/item-list
    slot_uri: rdfs:label
    alias: name
    owner: Thing
    domain_of:
    - ItemList
    - Thing
    range: string
  url:
    name: url
    description: A URL for the item
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: url
    owner: Thing
    domain_of:
    - Thing
    range: uri
  identifiers:
    name: identifiers
    description: A list of identifiers for the item. For example, if the id is a symbol,
      this would be a list of identifiers for the item, such as HGNC, MGI, etc.
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: identifiers
    owner: Thing
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true
  description:
    name: description
    description: A description of the item
    from_schema: https://w3id.org/oak/item-list
    alias: description
    owner: Thing
    domain_of:
    - ItemList
    - Thing
    range: string
  type:
    name: type
    description: The type of the item.
    examples:
    - value: biolink:Gene
    - value: schema:Person
    from_schema: https://w3id.org/oak/item-list
    rank: 1000
    alias: type
    owner: Thing
    domain_of:
    - Thing
    range: uriorcurie
class_uri: schema:Thing

```
</details>