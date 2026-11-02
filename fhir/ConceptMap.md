

# Class: ConceptMap



URI: [fhir:ConceptMap](https://build.fhir.org/ConceptMap)






```{mermaid}
 classDiagram
    class ConceptMap
    click ConceptMap href "../ConceptMap"
      ConceptMap : contact
        
      ConceptMap : date
        
      ConceptMap : description
        
      ConceptMap : experimental
        
      ConceptMap : group
        
          
    
    
    ConceptMap --> "*" ConceptMapGroup : group
    click ConceptMapGroup href "../ConceptMapGroup"

        
      ConceptMap : id
        
      ConceptMap : identifier
        
      ConceptMap : name
        
      ConceptMap : publisher
        
      ConceptMap : resourceType
        
      ConceptMap : sourceCanonical
        
      ConceptMap : sourceUri
        
      ConceptMap : status
        
      ConceptMap : targetCanonical
        
      ConceptMap : targetUri
        
      ConceptMap : title
        
      ConceptMap : url
        
      ConceptMap : version
        
      
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
| [sourceUri](sourceUri.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [sourceCanonical](sourceCanonical.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [targetUri](targetUri.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [targetCanonical](targetCanonical.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [group](group.md) | * <br/> [ConceptMapGroup](ConceptMapGroup.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:ConceptMap |
| native | fhir:ConceptMap |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ConceptMap
from_schema: https://w3id.org/oak/fhir
attributes:
  id:
    name: id
    comments:
    - not formally defined in FHIR schema, but present in pyrophen
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  resourceType:
    name: resourceType
    comments:
    - not formally part of FHIR schema but used in JSON serialization as type designation
    from_schema: https://w3id.org/oak/fhir
    designates_type: true
    domain_of:
    - CodeSystem
    - ConceptMap
  url:
    name: url
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
    range: uriorcurie
  identifier:
    name: identifier
    from_schema: https://w3id.org/oak/fhir
    identifier: false
    domain_of:
    - CodeSystem
    - ConceptMap
    multivalued: true
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
  name:
    name: name
    description: Name for this packages system (computer friendly)
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
  title:
    name: title
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
  status:
    name: status
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
  experimental:
    name: experimental
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
    range: boolean
  date:
    name: date
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
    range: datetime
  publisher:
    name: publisher
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
  contact:
    name: contact
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - ConceptMap
    multivalued: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
  sourceUri:
    name: sourceUri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMap
    range: uriorcurie
  sourceCanonical:
    name: sourceCanonical
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMap
    range: uriorcurie
  targetUri:
    name: targetUri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMap
    range: uriorcurie
  targetCanonical:
    name: targetCanonical
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMap
    range: uriorcurie
  group:
    name: group
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMap
    range: ConceptMapGroup
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: ConceptMap
from_schema: https://w3id.org/oak/fhir
attributes:
  id:
    name: id
    comments:
    - not formally defined in FHIR schema, but present in pyrophen
    from_schema: https://w3id.org/oak/fhir
    alias: id
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  resourceType:
    name: resourceType
    comments:
    - not formally part of FHIR schema but used in JSON serialization as type designation
    from_schema: https://w3id.org/oak/fhir
    designates_type: true
    alias: resourceType
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  url:
    name: url
    from_schema: https://w3id.org/oak/fhir
    alias: url
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: uriorcurie
  identifier:
    name: identifier
    from_schema: https://w3id.org/oak/fhir
    identifier: false
    alias: identifier
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
    multivalued: true
  version:
    name: version
    from_schema: https://w3id.org/oak/fhir
    alias: version
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - Coding
    - ConceptMap
    range: string
  name:
    name: name
    description: Name for this packages system (computer friendly)
    from_schema: https://w3id.org/oak/fhir
    alias: name
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  title:
    name: title
    from_schema: https://w3id.org/oak/fhir
    alias: title
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  status:
    name: status
    from_schema: https://w3id.org/oak/fhir
    alias: status
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  experimental:
    name: experimental
    from_schema: https://w3id.org/oak/fhir
    alias: experimental
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: boolean
  date:
    name: date
    from_schema: https://w3id.org/oak/fhir
    alias: date
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: datetime
  publisher:
    name: publisher
    from_schema: https://w3id.org/oak/fhir
    alias: publisher
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
  contact:
    name: contact
    from_schema: https://w3id.org/oak/fhir
    alias: contact
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - ConceptMap
    range: string
    multivalued: true
  description:
    name: description
    from_schema: https://w3id.org/oak/fhir
    alias: description
    owner: ConceptMap
    domain_of:
    - CodeSystem
    - CodeSystemFilter
    - CodeSystemProperty
    - ConceptMap
    range: string
  sourceUri:
    name: sourceUri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: sourceUri
    owner: ConceptMap
    domain_of:
    - ConceptMap
    range: uriorcurie
  sourceCanonical:
    name: sourceCanonical
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: sourceCanonical
    owner: ConceptMap
    domain_of:
    - ConceptMap
    range: uriorcurie
  targetUri:
    name: targetUri
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: targetUri
    owner: ConceptMap
    domain_of:
    - ConceptMap
    range: uriorcurie
  targetCanonical:
    name: targetCanonical
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: targetCanonical
    owner: ConceptMap
    domain_of:
    - ConceptMap
    range: uriorcurie
  group:
    name: group
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: group
    owner: ConceptMap
    domain_of:
    - ConceptMap
    range: ConceptMapGroup
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>