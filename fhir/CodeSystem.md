

# Class: CodeSystem


_Declares the existence of and describes a packages system or packages system supplement_





URI: [fhir:codesystem](https://build.fhir.org/codesystem)






```{mermaid}
 classDiagram
    class CodeSystem
    click CodeSystem href "../CodeSystem"
      CodeSystem : concept
        
          
    
    
    CodeSystem --> "*" Concept : concept
    click Concept href "../Concept"

        
      CodeSystem : contact
        
      CodeSystem : date
        
      CodeSystem : description
        
      CodeSystem : experimental
        
      CodeSystem : filter
        
          
    
    
    CodeSystem --> "*" CodeSystemFilter : filter
    click CodeSystemFilter href "../CodeSystemFilter"

        
      CodeSystem : id
        
      CodeSystem : identifier
        
      CodeSystem : name
        
      CodeSystem : property
        
          
    
    
    CodeSystem --> "*" CodeSystemProperty : property
    click CodeSystemProperty href "../CodeSystemProperty"

        
      CodeSystem : publisher
        
      CodeSystem : resourceType
        
      CodeSystem : status
        
      CodeSystem : title
        
      CodeSystem : url
        
      CodeSystem : version
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [resourceType](resourceType.md) | 0..1 <br/> [String](String.md) |  | direct |
| [url](url.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [identifier](identifier.md) | * <br/> [String](String.md) |  | direct |
| [version](version.md) | 0..1 <br/> [String](String.md) |  | direct |
| [name](name.md) | 0..1 <br/> [String](String.md) | Name for this packages system (computer friendly) | direct |
| [title](title.md) | 0..1 <br/> [String](String.md) |  | direct |
| [status](status.md) | 0..1 <br/> [String](String.md) |  | direct |
| [experimental](experimental.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [date](date.md) | 0..1 <br/> [Datetime](Datetime.md) |  | direct |
| [publisher](publisher.md) | 0..1 <br/> [String](String.md) |  | direct |
| [contact](contact.md) | * <br/> [String](String.md) |  | direct |
| [description](description.md) | 0..1 <br/> [String](String.md) |  | direct |
| [filter](filter.md) | * <br/> [CodeSystemFilter](CodeSystemFilter.md) |  | direct |
| [property](property.md) | * <br/> [CodeSystemProperty](CodeSystemProperty.md) |  | direct |
| [concept](concept.md) | * <br/> [Concept](Concept.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:codesystem |
| native | fhir:CodeSystem |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: CodeSystem
description: Declares the existence of and describes a packages system or packages
  system supplement
from_schema: https://w3id.org/oak/fhir
attributes:
  id:
    name: id
    comments:
    - not formally defined in FHIR schema, but present in pyrophen
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  resourceType:
    name: resourceType
    comments:
    - not formally part of FHIR schema but used in JSON serialization as type designation
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    designates_type: true
    domain_of:
    - CodeSystem
    - ConceptMap
  url:
    name: url
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
    range: uriorcurie
  identifier:
    name: identifier
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    identifier: false
    domain_of:
    - CodeSystem
    - ConceptMap
    multivalued: true
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
  name:
    name: name
    description: Name for this packages system (computer friendly)
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
  title:
    name: title
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
  status:
    name: status
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
  experimental:
    name: experimental
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
    range: boolean
  date:
    name: date
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
    range: datetime
  publisher:
    name: publisher
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
  contact:
    name: contact
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - ConceptMap
    multivalued: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
  filter:
    name: filter
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    range: CodeSystemFilter
    multivalued: true
    inlined: true
    inlined_as_list: true
  property:
    name: property
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - Concept
    range: CodeSystemProperty
    multivalued: true
    inlined: true
    inlined_as_list: true
  concept:
    name: concept
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - CodeSystem
    - Concept
    range: Concept
    multivalued: true
    inlined: true
    inlined_as_list: true
class_uri: fhir:codesystem

```
</details>

### Induced

<details>
```yaml
name: CodeSystem
description: Declares the existence of and describes a packages system or packages
  system supplement
from_schema: https://w3id.org/oak/fhir
attributes:
  id:
    name: id
    comments:
    - not formally defined in FHIR schema, but present in pyrophen
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: id
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  resourceType:
    name: resourceType
    comments:
    - not formally part of FHIR schema but used in JSON serialization as type designation
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    designates_type: true
    alias: resourceType
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  url:
    name: url
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: url
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: uriorcurie
  identifier:
    name: identifier
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    identifier: false
    alias: identifier
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
    multivalued: true
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: version
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
    range: string
  name:
    name: name
    description: Name for this packages system (computer friendly)
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: name
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  title:
    name: title
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: title
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  status:
    name: status
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: status
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  experimental:
    name: experimental
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: experimental
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: boolean
  date:
    name: date
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: date
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: datetime
  publisher:
    name: publisher
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: publisher
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  contact:
    name: contact
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: contact
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
    multivalued: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: description
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
    range: string
  filter:
    name: filter
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: filter
    owner: CodeSystem
    domain_of:
    - CodeSystem
    range: CodeSystemFilter
    multivalued: true
    inlined: true
    inlined_as_list: true
  property:
    name: property
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: property
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - Concept
    range: CodeSystemProperty
    multivalued: true
    inlined: true
    inlined_as_list: true
  concept:
    name: concept
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: concept
    owner: CodeSystem
    domain_of:
    - CodeSystem
    - Concept
    range: Concept
    multivalued: true
    inlined: true
    inlined_as_list: true
class_uri: fhir:codesystem

```
</details>