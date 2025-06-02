

# Class: PositiveOrNegativeAssociation


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [ontoassoc:PositiveOrNegativeAssociation](https://w3id.org/oak/association/PositiveOrNegativeAssociation)






```{mermaid}
 classDiagram
    class PositiveOrNegativeAssociation
    click PositiveOrNegativeAssociation href "../PositiveOrNegativeAssociation"
      PositiveOrNegativeAssociation <|-- Association
        click Association href "../Association"
      PositiveOrNegativeAssociation <|-- NegatedAssociation
        click NegatedAssociation href "../NegatedAssociation"
      
      PositiveOrNegativeAssociation : aggregator_knowledge_source
        
      PositiveOrNegativeAssociation : comments
        
      PositiveOrNegativeAssociation : evidence_type
        
      PositiveOrNegativeAssociation : negated
        
      PositiveOrNegativeAssociation : object
        
      PositiveOrNegativeAssociation : object_closure
        
      PositiveOrNegativeAssociation : object_closure_label
        
      PositiveOrNegativeAssociation : object_label
        
      PositiveOrNegativeAssociation : predicate
        
      PositiveOrNegativeAssociation : predicate_label
        
      PositiveOrNegativeAssociation : primary_knowledge_source
        
      PositiveOrNegativeAssociation : property_values
        
          
    
    
    PositiveOrNegativeAssociation --> "*" PropertyValue : property_values
    click PropertyValue href "../PropertyValue"

        
      PositiveOrNegativeAssociation : publications
        
      PositiveOrNegativeAssociation : subject
        
      PositiveOrNegativeAssociation : subject_closure
        
      PositiveOrNegativeAssociation : subject_closure_label
        
      PositiveOrNegativeAssociation : subject_label
        
      PositiveOrNegativeAssociation : supporting_objects
        
      
```





## Inheritance
* **PositiveOrNegativeAssociation**
    * [Association](Association.md)
    * [NegatedAssociation](NegatedAssociation.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | direct |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | direct |
| [object](object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is associated with the subject | direct |
| [property_values](property_values.md) | * <br/> [PropertyValue](PropertyValue.md) | Arbitrary key-value pairs with additional information about the association | direct |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | The label of the thing which the association is about | direct |
| [predicate_label](predicate_label.md) | 0..1 <br/> [String](String.md) | The label of the type of relationship between the subject and object | direct |
| [object_label](object_label.md) | 0..1 <br/> [String](String.md) | The label of the ontology entity that is associated with the subject | direct |
| [negated](negated.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the association is negated - i | direct |
| [publications](publications.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The publications that support the association | direct |
| [evidence_type](evidence_type.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of evidence supporting the association | direct |
| [supporting_objects](supporting_objects.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The objects that support the association | direct |
| [primary_knowledge_source](primary_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The primary knowledge source for the association | direct |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The knowledge source that aggregated the association | direct |
| [subject_closure](subject_closure.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The set of subjects that are related to the subject of the association via th... | direct |
| [subject_closure_label](subject_closure_label.md) | * <br/> [String](String.md) | The set of subjects that are related to the subject of the association via th... | direct |
| [object_closure](object_closure.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The set of objects that are related to the object of the association via the ... | direct |
| [object_closure_label](object_closure_label.md) | * <br/> [String](String.md) | The set of objects that are related to the object of the association via the ... | direct |
| [comments](comments.md) | * <br/> [String](String.md) | Comments about the association | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:PositiveOrNegativeAssociation |
| native | ontoassoc:PositiveOrNegativeAssociation |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PositiveOrNegativeAssociation
from_schema: https://w3id.org/oak/association
abstract: true
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
- evidence_type
- supporting_objects
- primary_knowledge_source
- aggregator_knowledge_source
- subject_closure
- subject_closure_label
- object_closure
- object_closure_label
- comments

```
</details>

### Induced

<details>
```yaml
name: PositiveOrNegativeAssociation
from_schema: https://w3id.org/oak/association
abstract: true
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    slot_group: core_triple
    range: uriorcurie
  property_values:
    name: property_values
    description: Arbitrary key-value pairs with additional information about the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: property_values
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: PropertyValue
    multivalued: true
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
  negated:
    name: negated
    description: True if the association is negated - i.e the core triple is not true.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: negated
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: boolean
  publications:
    name: publications
    description: The publications that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:publications
    alias: publications
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    - AssociationChange
    range: uriorcurie
    multivalued: true
  evidence_type:
    name: evidence_type
    description: The type of evidence supporting the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: evidence_type
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: uriorcurie
  supporting_objects:
    name: supporting_objects
    description: The objects that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: supporting_objects
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: uriorcurie
    multivalued: true
  primary_knowledge_source:
    name: primary_knowledge_source
    description: The primary knowledge source for the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:primary_knowledge_source
    alias: primary_knowledge_source
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
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
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie
  subject_closure:
    name: subject_closure
    description: The set of subjects that are related to the subject of the association
      via the closure predicates
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: subject_closure
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: uriorcurie
    multivalued: true
  subject_closure_label:
    name: subject_closure_label
    description: The set of subjects that are related to the subject of the association
      via the closure predicates
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: subject_closure_label
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
    multivalued: true
  object_closure:
    name: object_closure
    description: The set of objects that are related to the object of the association
      via the closure predicates
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: object_closure
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: uriorcurie
    multivalued: true
  object_closure_label:
    name: object_closure_label
    description: The set of objects that are related to the object of the association
      via the closure predicates
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: object_closure_label
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
    multivalued: true
  comments:
    name: comments
    description: Comments about the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdfs:comment
    alias: comments
    owner: PositiveOrNegativeAssociation
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
    multivalued: true

```
</details>