# Class: PropertyValue
_A generic tag-value that can be associated with an association._




URI: [ontoassoc:PropertyValue](https://w3id.org/oak/association/PropertyValue)



```{mermaid}
 classDiagram
    class PropertyValue
      PropertyValue : object
        
      PropertyValue : predicate
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | direct |
| [object](object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is associated with the subject | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Association](Association.md) | [property_values](property_values.md) | range | [PropertyValue](PropertyValue.md) |
| [NegatedAssociation](NegatedAssociation.md) | [property_values](property_values.md) | range | [PropertyValue](PropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:PropertyValue |
| native | ontoassoc:PropertyValue |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyValue
description: A generic tag-value that can be associated with an association.
from_schema: https://w3id.org/oak/association
rank: 1000
slots:
- predicate
- object

```
</details>

### Induced

<details>
```yaml
name: PropertyValue
description: A generic tag-value that can be associated with an association.
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  predicate:
    name: predicate
    description: The type of relationship between the subject and object.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdf:predicate
    alias: predicate
    owner: PropertyValue
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
    owner: PropertyValue
    domain_of:
    - Association
    - NegatedAssociation
    - PropertyValue
    range: uriorcurie

```
</details>