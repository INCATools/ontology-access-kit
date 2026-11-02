

# Class: CodeSystemProperty



URI: [fhir:CodeSystemProperty](https://build.fhir.org/CodeSystemProperty)






```{mermaid}
 classDiagram
    class CodeSystemProperty
    click CodeSystemProperty href "../CodeSystemProperty"
      CodeSystemProperty : code
        
      CodeSystemProperty : description
        
      CodeSystemProperty : type
        
      CodeSystemProperty : uri
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [code](code.md) | 1 <br/> [String](String.md) |  | direct |
| [uri](uri.md) | 0..1 <br/> [uri](uri.md) |  | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) |  | direct |
| [type](type.md) | 1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [CodeSystem](CodeSystem.md) | [property](property.md) | range | [CodeSystemProperty](CodeSystemProperty.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:CodeSystemProperty |
| native | fhir:CodeSystemProperty |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CodeSystemProperty
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
    range: string
    required: true
  uri:
    name: uri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystemProperty
    range: uri
    required: false
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
    range: string
  type:
    name: type
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystemProperty
    range: string
    required: true

```
</details>

### Induced

<details>
```yaml
name: CodeSystemProperty
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    alias: code
    owner: CodeSystemProperty
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
    range: string
    required: true
  uri:
    name: uri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: uri
    owner: CodeSystemProperty
    domain_of:
    - CodeSystemProperty
    range: uri
    required: false
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    alias: description
    owner: CodeSystemProperty
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
    range: string
  type:
    name: type
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: type
    owner: CodeSystemProperty
    domain_of:
    - CodeSystemProperty
    range: string
    required: true

```
</details>