

# Class: HasMappings



URI: [omoschema:HasMappings](https://w3id.org/oak/ontology-metadata/HasMappings)






```{mermaid}
 classDiagram
    class HasMappings
    click HasMappings href "../HasMappings"
      AnnotationPropertyMixin <|-- HasMappings
        click AnnotationPropertyMixin href "../AnnotationPropertyMixin"
      

      HasMappings <|-- Term
        click Term href "../Term"
      
      
      HasMappings : broadMatch
        
          
    
    
    HasMappings --> "*" Thing : broadMatch
    click Thing href "../Thing"

        
      HasMappings : closeMatch
        
          
    
    
    HasMappings --> "*" Thing : closeMatch
    click Thing href "../Thing"

        
      HasMappings : database_cross_reference
        
      HasMappings : exactMatch
        
          
    
    
    HasMappings --> "*" Thing : exactMatch
    click Thing href "../Thing"

        
      HasMappings : narrowMatch
        
          
    
    
    HasMappings --> "*" Thing : narrowMatch
    click Thing href "../Thing"

        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasMappings**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [broadMatch](broadMatch.md) | * <br/> [Thing](Thing.md) |  | direct |
| [closeMatch](closeMatch.md) | * <br/> [Thing](Thing.md) |  | direct |
| [exactMatch](exactMatch.md) | * <br/> [Thing](Thing.md) |  | direct |
| [narrowMatch](narrowMatch.md) | * <br/> [Thing](Thing.md) |  | direct |
| [database_cross_reference](database_cross_reference.md) | * <br/> [CURIELiteral](CURIELiteral.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:HasMappings |
| native | omoschema:HasMappings |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasMappings
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
slots:
- broadMatch
- closeMatch
- exactMatch
- narrowMatch
- database_cross_reference

```
</details>

### Induced

<details>
```yaml
name: HasMappings
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  broadMatch:
    name: broadMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:broadMatch
    alias: broadMatch
    owner: HasMappings
    domain_of:
    - HasMappings
    range: Thing
    multivalued: true
  closeMatch:
    name: closeMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    alias: closeMatch
    owner: HasMappings
    domain_of:
    - HasMappings
    range: Thing
    multivalued: true
  exactMatch:
    name: exactMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    alias: exactMatch
    owner: HasMappings
    domain_of:
    - HasMappings
    range: Thing
    multivalued: true
  narrowMatch:
    name: narrowMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    alias: narrowMatch
    owner: HasMappings
    domain_of:
    - HasMappings
    range: Thing
    multivalued: true
  database_cross_reference:
    name: database_cross_reference
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    alias: database_cross_reference
    owner: HasMappings
    domain_of:
    - HasMappings
    - Axiom
    range: CURIELiteral
    multivalued: true

```
</details>