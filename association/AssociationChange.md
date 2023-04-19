# Class: AssociationChange



URI: [ontoassoc:AssociationChange](https://w3id.org/oak/association/AssociationChange)



```{mermaid}
 classDiagram
    class AssociationChange
      AssociationChange : closure_predicates
        
      AssociationChange : is_creation
        
      AssociationChange : is_deletion
        
      AssociationChange : is_generalization
        
      AssociationChange : is_migration
        
      AssociationChange : is_specialization
        
      AssociationChange : new_object
        
      AssociationChange : new_predicate
        
      AssociationChange : old_object
        
      AssociationChange : old_object_obsolete
        
      AssociationChange : old_predicate
        
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
| [summary_group](summary_group.md) | 0..1 <br/> [String](String.md) |  | direct |
| [publications](publications.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | The publications that support the association | direct |
| [publication_is_added](publication_is_added.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [publication_is_deleted](publication_is_deleted.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [subject](subject.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The thing which the association is about | direct |
| [old_predicate](old_predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [new_predicate](new_predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [old_object](old_object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [new_object](new_object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [old_object_obsolete](old_object_obsolete.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_migration](is_migration.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_generalization](is_generalization.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_specialization](is_specialization.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_creation](is_creation.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_deletion](is_deletion.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [closure_predicates](closure_predicates.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) |  | direct |









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
from_schema: https://w3id.org/oak/association
rank: 1000
slots:
- summary_group
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

```
</details>

### Induced

<details>
```yaml
name: AssociationChange
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  summary_group:
    name: summary_group
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: summary_group
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: string
  publications:
    name: publications
    description: The publications that support the association
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: biolink:publications
    multivalued: true
    alias: publications
    owner: AssociationChange
    domain_of:
    - Association
    - NegatedAssociation
    - AssociationChange
    range: uriorcurie
  publication_is_added:
    name: publication_is_added
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: publication_is_added
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  publication_is_deleted:
    name: publication_is_deleted
    from_schema: https://w3id.org/oak/association
    rank: 1000
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
    - Association
    - NegatedAssociation
    - AssociationChange
    range: uriorcurie
  old_predicate:
    name: old_predicate
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: predicate
    alias: old_predicate
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  new_predicate:
    name: new_predicate
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: predicate
    alias: new_predicate
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  old_object:
    name: old_object
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    alias: old_object
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  new_object:
    name: new_object
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    alias: new_object
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie
  old_object_obsolete:
    name: old_object_obsolete
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: old_object_obsolete
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_migration:
    name: is_migration
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: is_migration
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_generalization:
    name: is_generalization
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: is_generalization
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_specialization:
    name: is_specialization
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: is_specialization
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_creation:
    name: is_creation
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: is_creation
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  is_deletion:
    name: is_deletion
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: is_deletion
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: boolean
  closure_predicates:
    name: closure_predicates
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: closure_predicates
    owner: AssociationChange
    domain_of:
    - AssociationChange
    range: uriorcurie

```
</details>