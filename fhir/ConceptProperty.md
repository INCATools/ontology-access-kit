

# Class: ConceptProperty



URI: [fhir:ConceptProperty](https://build.fhir.org/ConceptProperty)






```{mermaid}
 classDiagram
    class ConceptProperty
    click ConceptProperty href "../ConceptProperty"
      ConceptProperty : code
        
      ConceptProperty : valueBoolean
        
      ConceptProperty : valueCode
        
      ConceptProperty : valueCoding
        
      ConceptProperty : valueDateTime
        
      ConceptProperty : valueDecimal
        
      ConceptProperty : valueInteger
        
      ConceptProperty : valueString
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [code](code.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueCode](valueCode.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueCoding](valueCoding.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueString](valueString.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueInteger](valueInteger.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueBoolean](valueBoolean.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueDateTime](valueDateTime.md) | 0..1 <br/> [String](String.md) |  | direct |
| [valueDecimal](valueDecimal.md) | 0..1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Concept](Concept.md) | [property](property.md) | range | [ConceptProperty](ConceptProperty.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:ConceptProperty |
| native | fhir:ConceptProperty |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ConceptProperty
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
  valueCode:
    name: valueCode
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueCoding:
    name: valueCoding
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueString:
    name: valueString
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueInteger:
    name: valueInteger
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueBoolean:
    name: valueBoolean
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueDateTime:
    name: valueDateTime
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty
  valueDecimal:
    name: valueDecimal
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptProperty

```
</details>

### Induced

<details>
```yaml
name: ConceptProperty
from_schema: https://w3id.org/oak/fhir
attributes:
  code:
    name: code
    from_schema: https://w3id.org/oak/fhir
    alias: code
    owner: ConceptProperty
    domain_of:
    - Concept
    - ConceptProperty
    - CodeSystemFilter
    - CodeSystemProperty
    - Coding
    range: string
  valueCode:
    name: valueCode
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueCode
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueCoding:
    name: valueCoding
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueCoding
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueString:
    name: valueString
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueString
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueInteger:
    name: valueInteger
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueInteger
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueBoolean:
    name: valueBoolean
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueBoolean
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueDateTime:
    name: valueDateTime
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueDateTime
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string
  valueDecimal:
    name: valueDecimal
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: valueDecimal
    owner: ConceptProperty
    domain_of:
    - ConceptProperty
    range: string

```
</details>