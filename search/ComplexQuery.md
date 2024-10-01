

# Class: ComplexQuery



URI: [ontosearch:ComplexQuery](https://w3id.org/oak/search-datamodel/ComplexQuery)






```{mermaid}
 classDiagram
    class ComplexQuery
    click ComplexQuery href "../ComplexQuery"
      ComplexQuery : all_of
        
          
    
    
    ComplexQuery --> "*" ComplexQuery : all_of
    click ComplexQuery href "../ComplexQuery"

        
      ComplexQuery : any_of
        
          
    
    
    ComplexQuery --> "*" ComplexQuery : any_of
    click ComplexQuery href "../ComplexQuery"

        
      ComplexQuery : atom
        
          
    
    
    ComplexQuery --> "0..1" SearchBaseConfiguration : atom
    click SearchBaseConfiguration href "../SearchBaseConfiguration"

        
      ComplexQuery : none_of
        
          
    
    
    ComplexQuery --> "*" ComplexQuery : none_of
    click ComplexQuery href "../ComplexQuery"

        
      ComplexQuery : path_to
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [all_of](all_of.md) | * <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
| [any_of](any_of.md) | * <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
| [none_of](none_of.md) | * <br/> [ComplexQuery](ComplexQuery.md) |  | direct |
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
attributes:
  all_of:
    name: all_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
  any_of:
    name: any_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
  none_of:
    name: none_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
  path_to:
    name: path_to
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - ComplexQuery
  atom:
    name: atom
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - ComplexQuery
    range: SearchBaseConfiguration

```
</details>

### Induced

<details>
```yaml
name: ComplexQuery
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  all_of:
    name: all_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: all_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
  any_of:
    name: any_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: any_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
  none_of:
    name: none_of
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: none_of
    owner: ComplexQuery
    domain_of:
    - ComplexQuery
    range: ComplexQuery
    multivalued: true
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