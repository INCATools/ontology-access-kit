

# Class: Concept



URI: [fhir:Concept](https://build.fhir.org/Concept)






```{mermaid}
 classDiagram
    class Concept
    click Concept href "../Concept"
      Concept : code
        
      Concept : concept
        
          
    
    
    Concept --> "*" Concept : concept
    click Concept href "../Concept"

        
      Concept : definition
        
      Concept : designation
        
          
    
    
    Concept --> "*" ConceptDesignation : designation
    click ConceptDesignation href "../ConceptDesignation"

        
      Concept : display
        
      Concept : property
        
          
    
    
    Concept --> "*" ConceptProperty : property
    click ConceptProperty href "../ConceptProperty"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [code](code.md) | 0..1 <br/> [String](String.md) |  | direct |
| [display](display.md) | 0..1 <br/> [String](String.md) |  | direct |
| [definition](definition.md) | 0..1 <br/> [String](String.md) |  | direct |
| [designation](designation.md) | * <br/> [ConceptDesignation](ConceptDesignation.md) |  | direct |
| [property](property.md) | * <br/> [ConceptProperty](ConceptProperty.md) |  | direct |
| [concept](concept.md) | * <br/> [Concept](Concept.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [CodeSystem](CodeSystem.md) | [concept](concept.md) | range | [Concept](Concept.md) |
| [Concept](Concept.md) | [concept](concept.md) | range | [Concept](Concept.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:Concept |
| native | fhir:Concept |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Concept
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
  display:
    name: display
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Concept
    - Coding
  definition:
    name: definition
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Concept
  designation:
    name: designation
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - Concept
    range: ConceptDesignation
    multivalued: true
  property:
    name: property
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - Concept
    range: ConceptProperty
    multivalued: true
  concept:
    name: concept
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - Concept
    range: Concept
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: Concept
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: code
    owner: Concept
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
    rank: 1000
    alias: display
    owner: Concept
    domain_of:
    - Concept
    - Coding
    range: string
  definition:
    name: definition
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: definition
    owner: Concept
    domain_of:
    - Concept
    range: string
  designation:
    name: designation
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: designation
    owner: Concept
    domain_of:
    - Concept
    range: ConceptDesignation
    multivalued: true
  property:
    name: property
    from_schema: https://w3id.org/oak/fhir
    alias: property
    owner: Concept
    domain_of:
    - CodeSystem
    - Concept
    range: ConceptProperty
    multivalued: true
  concept:
    name: concept
    from_schema: https://w3id.org/oak/fhir
    alias: concept
    owner: Concept
    domain_of:
    - CodeSystem
    - Concept
    range: Concept
    multivalued: true

```
</details>