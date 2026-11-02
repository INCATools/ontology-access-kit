

# Class: ConceptDesignation



URI: [fhir:ConceptDesignation](https://build.fhir.org/ConceptDesignation)






```{mermaid}
 classDiagram
    class ConceptDesignation
    click ConceptDesignation href "../ConceptDesignation"
      ConceptDesignation : language
        
      ConceptDesignation : use
        
          
    
    
    ConceptDesignation --> "0..1" Coding : use
    click Coding href "../Coding"

        
      ConceptDesignation : value
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [language](language.md) | 0..1 <br/> [String](String.md) |  | direct |
| [use](use.md) | 0..1 <br/> [Coding](Coding.md) |  | direct |
| [value](value.md) | 0..1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Concept](Concept.md) | [designation](designation.md) | range | [ConceptDesignation](ConceptDesignation.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:ConceptDesignation |
| native | fhir:ConceptDesignation |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ConceptDesignation
from_schema: https://w3id.org/oak/fhir
attributes:
  language:
    name: language
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptDesignation
  use:
    name: use
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptDesignation
    range: Coding
  value:
    name: value
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptDesignation
    - CodeSystemFilter

```
</details>

### Induced

<details>
```yaml
name: ConceptDesignation
from_schema: https://w3id.org/oak/fhir
attributes:
  language:
    name: language
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: language
    owner: ConceptDesignation
    domain_of:
    - ConceptDesignation
    range: string
  use:
    name: use
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: use
    owner: ConceptDesignation
    domain_of:
    - ConceptDesignation
    range: Coding
  value:
    name: value
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: value
    owner: ConceptDesignation
    domain_of:
    - ConceptDesignation
    - CodeSystemFilter
    range: string

```
</details>