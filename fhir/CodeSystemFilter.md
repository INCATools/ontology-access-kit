

# Class: CodeSystemFilter



URI: [fhir:CodeSystemFilter](https://build.fhir.org/CodeSystemFilter)






```{mermaid}
 classDiagram
    class CodeSystemFilter
    click CodeSystemFilter href "../CodeSystemFilter"
      CodeSystemFilter : code
        
      CodeSystemFilter : description
        
      CodeSystemFilter : operator
        
      CodeSystemFilter : value
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [code](code.md) | 1 <br/> [String](String.md) |  | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) |  | direct |
| [operator](operator.md) | * <br/> [String](String.md) |  | direct |
| [value](value.md) | 1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [CodeSystem](CodeSystem.md) | [filter](filter.md) | range | [CodeSystemFilter](CodeSystemFilter.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:CodeSystemFilter |
| native | fhir:CodeSystemFilter |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CodeSystemFilter
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
    required: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
  operator:
    name: operator
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystemFilter
    range: string
    multivalued: true
  value:
    name: value
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - ConceptDesignation
    - CodeSystemFilter
    range: string
    required: true

```
</details>

### Induced

<details>
```yaml
name: CodeSystemFilter
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    alias: code
    owner: CodeSystemFilter
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
    range: string
    required: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    alias: description
    owner: CodeSystemFilter
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
    range: string
  operator:
    name: operator
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: operator
    owner: CodeSystemFilter
    domain_of:
    - CodeSystemFilter
    range: string
    multivalued: true
  value:
    name: value
    from_schema: https://w3id.org/oak/fhir
    alias: value
    owner: CodeSystemFilter
    domain_of:
    - ConceptDesignation
    - CodeSystemFilter
    range: string
    required: true

```
</details>