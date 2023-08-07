# Class: NegatedAssociation


_A negated association between a thing (subject) and another thing (object)._





URI: [ontoassoc:NegatedAssociation](https://w3id.org/oak/association/NegatedAssociation)



```{mermaid}
 classDiagram
    class NegatedAssociation
      NegatedAssociation : aggregator_knowledge_source
        
      NegatedAssociation : negated
        
      NegatedAssociation : object
        
      NegatedAssociation : object_label
        
      NegatedAssociation : predicate
        
      NegatedAssociation : predicate_label
        
      NegatedAssociation : primary_knowledge_source
        
      NegatedAssociation : property_values
        
          NegatedAssociation --|> PropertyValue : property_values
        
      NegatedAssociation : publications
        
      NegatedAssociation : subject
        
      NegatedAssociation : subject_label
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | direct |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | direct |
| [object](object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is associated with the subject | direct |
| [property_values](property_values.md) | 0..* <br/> [PropertyValue](PropertyValue.md) | Arbitrary key-value pairs with additional information about the association | direct |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | The label of the thing which the association is about | direct |
| [predicate_label](predicate_label.md) | 0..1 <br/> [String](String.md) | The label of the type of relationship between the subject and object | direct |
| [object_label](object_label.md) | 0..1 <br/> [String](String.md) | The label of the ontology entity that is associated with the subject | direct |
| [negated](negated.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the association is negated - i | direct |
| [publications](publications.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | The publications that support the association | direct |
| [primary_knowledge_source](primary_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The primary knowledge source for the association | direct |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The knowledge source that aggregated the association | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:NegatedAssociation |
| native | ontoassoc:NegatedAssociation |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NegatedAssociation
description: A negated association between a thing (subject) and another thing (object).
from_schema: https://w3id.org/oak/association
slots:
- subject
- predicate
- object
- property_values
- subject_label
- predicate_label
- object_label
- negated
- publications
- primary_knowledge_source
- aggregator_knowledge_source
slot_usage:
  negated:
    name: negated
    domain_of:
    - Association
    - NegatedAssociation
    equals_expression: 'True'

```
</details>

### Induced

<details>
```yaml
name: NegatedAssociation
description: A negated association between a thing (subject) and another thing (object).
from_schema: https://w3id.org/oak/association
slot_usage:
  negated:
    name: negated
    domain_of:
    - Association
    - NegatedAssociation
    equals_expression: 'True'
attributes:
  subject:
    name: subject
    description: The thing which the association is about.
    comments:
    - it is conventional for the subject to be the "entity" and the object to be the
      ontological descriptor
    from_schema: https://w3id.org/oak/association
    exact_mappings:
    - oa:hasBody
    rank: 1000
    slot_uri: rdf:subject
    alias: subject
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - AssociationChange
    slot_group: core_triple
    range: uriorcurie
  predicate:
    name: predicate
    description: The type of relationship between the subject and object.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdf:predicate
    alias: predicate
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - PropertyValue
    slot_group: core_triple
    range: uriorcurie
  object:
    name: object
    description: An ontology entity that is associated with the subject.
    comments:
    - it is conventional for the subject to be the "entity" and the object to be the
      ontological descriptor
    from_schema: https://w3id.org/oak/association
    exact_mappings:
    - oa:hasTarget
    rank: 1000
    slot_uri: rdf:object
    alias: object
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - PropertyValue
    slot_group: core_triple
    range: uriorcurie
  property_values:
    name: property_values
    description: Arbitrary key-value pairs with additional information about the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: property_values
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    range: PropertyValue
    inlined: true
  subject_label:
    name: subject_label
    description: The label of the thing which the association is about.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - denormalized_slot
    slot_uri: sssom:subject_label
    alias: subject_label
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    range: string
  predicate_label:
    name: predicate_label
    description: The label of the type of relationship between the subject and object.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - denormalized_slot
    slot_uri: sssom:predicate_label
    alias: predicate_label
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    range: string
  object_label:
    name: object_label
    description: The label of the ontology entity that is associated with the subject.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - denormalized_slot
    slot_uri: sssom:object_label
    alias: object_label
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    range: string
  negated:
    name: negated
    description: True if the association is negated - i.e the core triple is not true.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: negated
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    range: boolean
    equals_expression: 'True'
  publications:
    name: publications
    description: The publications that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:publications
    multivalued: true
    alias: publications
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - AssociationChange
    range: uriorcurie
  primary_knowledge_source:
    name: primary_knowledge_source
    description: The primary knowledge source for the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:primary_knowledge_source
    alias: primary_knowledge_source
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie
  aggregator_knowledge_source:
    name: aggregator_knowledge_source
    description: The knowledge source that aggregated the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:aggregator_knowledge_source
    alias: aggregator_knowledge_source
    owner: NegatedAssociation
    domain_of:
    - Association
    - NegatedAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie

```
</details>