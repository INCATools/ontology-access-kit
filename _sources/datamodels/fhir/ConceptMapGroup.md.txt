

# Class: ConceptMapGroup



URI: [fhir:ConceptMapGroup](https://build.fhir.org/ConceptMapGroup)






```{mermaid}
 classDiagram
    class ConceptMapGroup
    click ConceptMapGroup href "../ConceptMapGroup"
      ConceptMapGroup : element
        
      ConceptMapGroup : source
        
      ConceptMapGroup : sourceVersion
        
      ConceptMapGroup : target
        
      ConceptMapGroup : targetVersion
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [source](source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [sourceVersion](sourceVersion.md) | 0..1 <br/> [String](String.md) |  | direct |
| [target](target.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [targetVersion](targetVersion.md) | 0..1 <br/> [String](String.md) |  | direct |
| [element](element.md) | * <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ConceptMap](ConceptMap.md) | [group](group.md) | range | [ConceptMapGroup](ConceptMapGroup.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/fhir




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fhir:ConceptMapGroup |
| native | fhir:ConceptMapGroup |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ConceptMapGroup
from_schema: https://w3id.org/oak/fhir
attributes:
  source:
    name: source
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMapGroup
    range: uriorcurie
  sourceVersion:
    name: sourceVersion
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMapGroup
  target:
    name: target
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMapGroup
    range: uriorcurie
  targetVersion:
    name: targetVersion
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMapGroup
  element:
    name: element
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    domain_of:
    - ConceptMapGroup
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: ConceptMapGroup
from_schema: https://w3id.org/oak/fhir
attributes:
  source:
    name: source
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: source
    owner: ConceptMapGroup
    domain_of:
    - ConceptMapGroup
    range: uriorcurie
  sourceVersion:
    name: sourceVersion
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: sourceVersion
    owner: ConceptMapGroup
    domain_of:
    - ConceptMapGroup
    range: string
  target:
    name: target
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: target
    owner: ConceptMapGroup
    domain_of:
    - ConceptMapGroup
    range: uriorcurie
  targetVersion:
    name: targetVersion
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: targetVersion
    owner: ConceptMapGroup
    domain_of:
    - ConceptMapGroup
    range: string
  element:
    name: element
    from_schema: https://w3id.org/oak/fhir
    rank: 1000
    alias: element
    owner: ConceptMapGroup
    domain_of:
    - ConceptMapGroup
    range: string
    multivalued: true

```
</details>