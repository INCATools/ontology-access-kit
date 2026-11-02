

# Class: Coding



URI: [fhir:Coding](https://build.fhir.org/Coding)






```{mermaid}
 classDiagram
    class Coding
    click Coding href "../Coding"
      Coding : code
        
      Coding : display
        
      Coding : system
        
      Coding : userSelected
        
      Coding : version
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [system](system.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [version](version.md) | 0..1 <br/> [String](String.md) |  | direct |
| [code](code.md) | 0..1 <br/> [String](String.md) |  | direct |
| [display](display.md) | 0..1 <br/> [String](String.md) |  | direct |
| [userSelected](userSelected.md) | 0..1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ConceptDesignation](ConceptDesignation.md) | [use](use.md) | range | [Coding](Coding.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:Coding |
| native | fhir:Coding |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Coding
from_schema: https://w3id.org/oak/fhir
attributes:
  system:
    name: system
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Coding
    range: uriorcurie
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
  display:
    name: display
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - Concept
    - Coding
  userSelected:
    name: userSelected
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Coding

```
</details>

### Induced

<details>
```yaml
name: Coding
from_schema: https://w3id.org/oak/fhir
attributes:
  system:
    name: system
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: system
    owner: Coding
    domain_of:
    - Coding
    range: uriorcurie
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    alias: version
    owner: Coding
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
    range: string
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    alias: code
    owner: Coding
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
    range: string
  display:
    name: display
    from_schema: https://w3id.org/oak/fhir
    alias: display
    owner: Coding
    domain_of:
    - Concept
    - Coding
    range: string
  userSelected:
    name: userSelected
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: userSelected
    owner: Coding
    domain_of:
    - Coding
    range: string

```
</details>