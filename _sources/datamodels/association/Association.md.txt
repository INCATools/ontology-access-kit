

# Class: Association


_A generic association between a thing (subject) and another thing (object)._





URI: [oa:Annotation](http://www.w3.org/ns/oa#Annotation)






```{mermaid}
 classDiagram
    class Association
    click Association href "../Association"
      PositiveOrNegativeAssociation <|-- Association
        click PositiveOrNegativeAssociation href "../PositiveOrNegativeAssociation"
      
      Association : aggregator_knowledge_source
        
      Association : comments
        
      Association : evidence_type
        
      Association : negated
        
      Association : object
        
      Association : object_closure
        
      Association : object_closure_label
        
      Association : object_label
        
      Association : predicate
        
      Association : predicate_label
        
      Association : primary_knowledge_source
        
      Association : property_values
        
          
    
    
    Association --> "*" PropertyValue : property_values
    click PropertyValue href "../PropertyValue"

        
      Association : publications
        
      Association : subject
        
      Association : subject_closure
        
      Association : subject_closure_label
        
      Association : subject_label
        
      Association : supporting_objects
        
      
```





## Inheritance
* [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md)
    * **Association**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [object](object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is associated with the subject | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [property_values](property_values.md) | * <br/> [PropertyValue](PropertyValue.md) | Arbitrary key-value pairs with additional information about the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | The label of the thing which the association is about | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [predicate_label](predicate_label.md) | 0..1 <br/> [String](String.md) | The label of the type of relationship between the subject and object | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [object_label](object_label.md) | 0..1 <br/> [String](String.md) | The label of the ontology entity that is associated with the subject | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [negated](negated.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the association is negated - i | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [publications](publications.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The publications that support the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [evidence_type](evidence_type.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of evidence supporting the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [supporting_objects](supporting_objects.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The objects that support the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [primary_knowledge_source](primary_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The primary knowledge source for the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The knowledge source that aggregated the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [subject_closure](subject_closure.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The set of subjects that are related to the subject of the association via th... | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [subject_closure_label](subject_closure_label.md) | * <br/> [String](String.md) | The set of subjects that are related to the subject of the association via th... | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [object_closure](object_closure.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The set of objects that are related to the object of the association via the ... | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [object_closure_label](object_closure_label.md) | * <br/> [String](String.md) | The set of objects that are related to the object of the association via the ... | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |
| [comments](comments.md) | * <br/> [String](String.md) | Comments about the association | [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RollupGroup](RollupGroup.md) | [associations](associations.md) | range | [Association](Association.md) |
| [PairwiseCoAssociation](PairwiseCoAssociation.md) | [associations_for_subjects_in_common](associations_for_subjects_in_common.md) | range | [Association](Association.md) |






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
is_a: PositiveOrNegativeAssociation
slot_usage:
  negated:
    name: negated
    equals_expression: 'False'
class_uri: oa:Annotation

```
</details>

### Induced

<details>
```yaml
name: Association
description: A generic association between a thing (subject) and another thing (object).
from_schema: https://w3id.org/oak/association
is_a: PositiveOrNegativeAssociation
slot_usage:
  negated:
    name: negated
    equals_expression: 'False'
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
  negated:
    name: negated
    description: True if the association is negated - i.e the core triple is not true.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: negated
    owner: Association
    domain_of:
    - PositiveOrNegativeAssociation
    range: boolean
    equals_expression: 'False'
  publications:
    name: publications
    description: The publications that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:publications
    alias: publications
    owner: Association
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
    owner: Association
    domain_of:
    - PositiveOrNegativeAssociation
    range: uriorcurie
  supporting_objects:
    name: supporting_objects
    description: The objects that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: supporting_objects
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
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
    owner: Association
    domain_of:
    - PositiveOrNegativeAssociation
    range: string
    multivalued: true
class_uri: oa:Annotation

```
</details>