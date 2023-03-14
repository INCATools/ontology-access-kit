# Class: ComplexQuery



URI: [ontosearch:ComplexQuery](https://w3id.org/oak/search-datamodel/ComplexQuery)



```{mermaid}
 classDiagram
    class ComplexQuery
      ComplexQuery : all_of
        
          ComplexQuery ..> ComplexQuery : all_of
        
      ComplexQuery : any_of
        
          ComplexQuery ..> ComplexQuery : any_of
        
      ComplexQuery : atom
        
          ComplexQuery ..> SearchBaseConfiguration : atom
        
      ComplexQuery : none_of
        
          ComplexQuery ..> ComplexQuery : none_of
        
      ComplexQuery : path_to
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [all_of](all_of.md) | 0..* <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
| [any_of](any_of.md) | 0..* <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
| [none_of](none_of.md) | 0..* <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
| [path_to](path_to.md) | 0..1 <br/> [String](String.md) |  | direct |
| [atom](atom.md) | 0..1 <br/> [SearchBaseConfiguration](SearchBaseConfiguration.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ComplexQuery](ComplexQuery.md) | [all_of](all_of.md) | range | [ComplexQuery](ComplexQuery.md) |
| [ComplexQuery](ComplexQuery.md) | [any_of](any_of.md) | range | [ComplexQuery](ComplexQuery.md) |
| [ComplexQuery](ComplexQuery.md) | [none_of](none_of.md) | range | [ComplexQuery](ComplexQuery.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:ComplexQuery |
| native | ontosearch:ComplexQuery |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ComplexQuery
from_schema: https://w3id.org/oak/search-datamodel
rank: 1000
attributes:
  all_of:
    name: all_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    range: ComplexQuery
  any_of:
    name: any_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    range: ComplexQuery
  none_of:
    name: none_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    range: ComplexQuery
  path_to:
    name: path_to
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
  atom:
    name: atom
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    range: SearchBaseConfiguration

```
</details>

### Induced

<details>
```yaml
name: ComplexQuery
from_schema: https://w3id.org/oak/search-datamodel
rank: 1000
attributes:
  all_of:
    name: all_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    alias: all_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
  any_of:
    name: any_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    alias: any_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
  none_of:
    name: none_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    alias: none_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
  path_to:
    name: path_to
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: path_to
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: string
  atom:
    name: atom
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: atom
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: SearchBaseConfiguration

```
</details>