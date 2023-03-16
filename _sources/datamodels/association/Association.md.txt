# Class: Association
_A generic association between a thing (subject) and another thing (object)._




URI: [oa:Annotation](http://www.w3.org/ns/oa#Annotation)



```{mermaid}
 classDiagram
    class Association
      Association : object
        
      Association : predicate
        
      Association : property_values
        
          Association ..> PropertyValue : property_values
        
      Association : subject
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | direct |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | direct |
| [object](object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is associated with the subject | direct |
| [property_values](property_values.md) | 0..* <br/> [PropertyValue](PropertyValue.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RollupGroup](RollupGroup.md) | [associations](associations.md) | range | [Association](Association.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oa:Annotation |
| native | ontoassoc:Association |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Association
description: A generic association between a thing (subject) and another thing (object).
from_schema: https://w3id.org/oak/association
rank: 1000
slots:
- subject
- predicate
- object
- property_values
class_uri: oa:Annotation

```
</details>

### Induced

<details>
```yaml
name: Association
description: A generic association between a thing (subject) and another thing (object).
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  subject:
    name: subject
    description: The thing which the association is about.
    from_schema: https://w3id.org/oak/association
    exact_mappings:
    - oa:hasBody
    rank: 1000
    slot_uri: rdf:subject
    alias: subject
    owner: Association
    domain_of:
    - Association
    - NegatedAssociation
    range: uriorcurie
  predicate:
    name: predicate
    description: The type of relationship between the subject and object.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdf:predicate
    alias: predicate
    owner: Association
    domain_of:
    - Association
    - NegatedAssociation
    - PropertyValue
    range: uriorcurie
  object:
    name: object
    description: An ontology entity that is associated with the subject.
    from_schema: https://w3id.org/oak/association
    exact_mappings:
    - oa:hasTarget
    rank: 1000
    slot_uri: rdf:object
    alias: object
    owner: Association
    domain_of:
    - Association
    - NegatedAssociation
    - PropertyValue
    range: uriorcurie
  property_values:
    name: property_values
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: property_values
    owner: Association
    domain_of:
    - Association
    - NegatedAssociation
    range: PropertyValue
    inlined: true
class_uri: oa:Annotation

```
</details>