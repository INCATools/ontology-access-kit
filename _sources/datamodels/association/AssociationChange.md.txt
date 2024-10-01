

# Class: AssociationChange


_A change object describing a change between two associations._





URI: [ontoassoc:AssociationChange](https://w3id.org/oak/association/AssociationChange)






```{mermaid}
 classDiagram
    class AssociationChange
    click AssociationChange href "../AssociationChange"
      AssociationChange : aggregator_knowledge_source
        
      AssociationChange : closure_delta
        
      AssociationChange : closure_predicates
        
      AssociationChange : is_creation
        
      AssociationChange : is_deletion
        
      AssociationChange : is_generalization
        
      AssociationChange : is_migration
        
      AssociationChange : is_specialization
        
      AssociationChange : new_date
        
      AssociationChange : new_object
        
      AssociationChange : new_predicate
        
      AssociationChange : old_date
        
      AssociationChange : old_object
        
      AssociationChange : old_object_obsolete
        
      AssociationChange : old_predicate
        
      AssociationChange : primary_knowledge_source
        
      AssociationChange : publication_is_added
        
      AssociationChange : publication_is_deleted
        
      AssociationChange : publications
        
      AssociationChange : subject
        
      AssociationChange : summary_group
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [summary_group](summary_group.md) | 0..1 <br/> [String](String.md) | The field used to group an association diff summary | direct |
| [old_date](old_date.md) | 0..1 <br/> [String](String.md) | The date of the old association | direct |
| [new_date](new_date.md) | 0..1 <br/> [String](String.md) | The date of the new association | direct |
| [primary_knowledge_source](primary_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The primary knowledge source for the association | direct |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The knowledge source that aggregated the association | direct |
| [publications](publications.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The publications that support the association | direct |
| [publication_is_added](publication_is_added.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the publication was not present in the old association set (and prese... | direct |
| [publication_is_deleted](publication_is_deleted.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the publication is not present in the new association set (and presen... | direct |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | direct |
| [old_predicate](old_predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | If the association diff is a change in predicate, this is the predicate on th... | direct |
| [new_predicate](new_predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | If the association diff is a change in predicate, this is the predicate on th... | direct |
| [old_object](old_object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The object (e | direct |
| [new_object](new_object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The object (e | direct |
| [old_object_obsolete](old_object_obsolete.md) | 0..1 <br/> [Boolean](Boolean.md) | if the object (e | direct |
| [is_migration](is_migration.md) | 0..1 <br/> [Boolean](Boolean.md) | if the object (e | direct |
| [is_generalization](is_generalization.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the association was inferred to become more general (based on closure... | direct |
| [is_specialization](is_specialization.md) | 0..1 <br/> [Boolean](Boolean.md) | True if the association was inferred to become more specific (based on closur... | direct |
| [is_creation](is_creation.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_deletion](is_deletion.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [closure_predicates](closure_predicates.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The set of predicates used to determine if the new association object is a sp... | direct |
| [closure_delta](closure_delta.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |









## Comments

* the change may be between associations in the same set at different times, or associations from different sources.

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:AssociationChange |
| native | ontoassoc:AssociationChange |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: AssociationChange
description: A change object describing a change between two associations.
comments:
- the change may be between associations in the same set at different times, or associations
  from different sources.
from_schema: https://w3id.org/oak/association
slots:
- summary_group
- old_date
- new_date
- primary_knowledge_source
- aggregator_knowledge_source
- publications
- publication_is_added
- publication_is_deleted
- subject
- old_predicate
- new_predicate
- old_object
- new_object
- old_object_obsolete
- is_migration
- is_generalization
- is_specialization
- is_creation
- is_deletion
- closure_predicates
- closure_delta

```
</details>

### Induced

<details>
```yaml
name: AssociationChange
description: A change object describing a change between two associations.
comments:
- the change may be between associations in the same set at different times, or associations
  from different sources.
from_schema: https://w3id.org/oak/association
attributes:
  summary_group:
    name: summary_group
    description: The field used to group an association diff summary
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: summary_group
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: string
  old_date:
    name: old_date
    description: The date of the old association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: date
    mixins:
    - diff_slot
    alias: old_date
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: string
  new_date:
    name: new_date
    description: The date of the new association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: date
    mixins:
    - diff_slot
    alias: new_date
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: string
  primary_knowledge_source:
    name: primary_knowledge_source
    description: The primary knowledge source for the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:primary_knowledge_source
    alias: primary_knowledge_source
    owner: AssociationChange
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
    owner: AssociationChange
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie
  publications:
    name: publications
    description: The publications that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:publications
    alias: publications
    owner: AssociationChange
    domain_of:
    - PositiveOrNegativeAssociation
    - AssociationChange
    range: uriorcurie
    multivalued: true
  publication_is_added:
    name: publication_is_added
    description: True if the publication was not present in the old association set
      (and present in the new)
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: publication_is_added
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  publication_is_deleted:
    name: publication_is_deleted
    description: True if the publication is not present in the new association set
      (and present in the old)
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: publication_is_deleted
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
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
    owner: AssociationChange
    domain_of:
    - PositiveOrNegativeAssociation
    - AssociationChange
    slot_group: core_triple
    range: uriorcurie
  old_predicate:
    name: old_predicate
    description: If the association diff is a change in predicate, this is the predicate
      on the old association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: predicate
    mixins:
    - diff_slot
    alias: old_predicate
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  new_predicate:
    name: new_predicate
    description: If the association diff is a change in predicate, this is the predicate
      on the new association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: predicate
    mixins:
    - diff_slot
    alias: new_predicate
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  old_object:
    name: old_object
    description: The object (e.g. term) on the old association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    mixins:
    - diff_slot
    alias: old_object
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  new_object:
    name: new_object
    description: The object (e.g. term) on the new association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    mixins:
    - diff_slot
    alias: new_object
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  old_object_obsolete:
    name: old_object_obsolete
    description: if the object (e.g. term) of the old object has been obsoleted, this
      is true
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: old_object_obsolete
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_migration:
    name: is_migration
    description: if the object (e.g. term) of the old object has been obsoleted, and
      the object has been migrated (either automatically or manually) to a new object
      based on obsoletion migration metadata, this is True
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: is_migration
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_generalization:
    name: is_generalization
    description: True if the association was inferred to become more general (based
      on closure predicates). Note that depending on the tool, this may be inferred,
      if there is no explicit association-level migration information.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: is_generalization
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_specialization:
    name: is_specialization
    description: True if the association was inferred to become more specific (based
      on closure predicates). Note that depending on the tool, this may be inferred,
      if there is no explicit association-level migration information.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: is_specialization
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_creation:
    name: is_creation
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: is_creation
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_deletion:
    name: is_deletion
    from_schema: https://w3id.org/oak/association
    rank: 1000
    mixins:
    - diff_slot
    alias: is_deletion
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  closure_predicates:
    name: closure_predicates
    description: The set of predicates used to determine if the new association object
      is a specialization or generalization of the old one.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: closure_predicates
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
    multivalued: true
  closure_delta:
    name: closure_delta
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: closure_delta
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: integer

```
</details>