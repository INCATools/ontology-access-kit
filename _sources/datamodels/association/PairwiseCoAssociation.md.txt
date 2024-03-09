# Class: PairwiseCoAssociation


_A collection of subjects co-associated with two objects_





URI: [ontoassoc:PairwiseCoAssociation](https://w3id.org/oak/association/PairwiseCoAssociation)




```{mermaid}
 classDiagram
    class PairwiseCoAssociation
      PairwiseCoAssociation : associations_for_subjects_in_common
        
          PairwiseCoAssociation --> Association : associations_for_subjects_in_common
        
      PairwiseCoAssociation : number_subject_unique_to_entity1
        
      PairwiseCoAssociation : number_subject_unique_to_entity2
        
      PairwiseCoAssociation : number_subjects_in_common
        
      PairwiseCoAssociation : object1
        
      PairwiseCoAssociation : object1_label
        
          PairwiseCoAssociation --> None : object1_label
        
      PairwiseCoAssociation : object2
        
      PairwiseCoAssociation : object2_label
        
          PairwiseCoAssociation --> None : object2_label
        
      PairwiseCoAssociation : subjects_in_common
        
          PairwiseCoAssociation --> None : subjects_in_common
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [object1](object1.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [object2](object2.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [object1_label](object1_label.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object2_label](object2_label.md) | 0..1 <br/> [String](String.md) |  | direct |
| [number_subjects_in_common](number_subjects_in_common.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [number_subject_unique_to_entity1](number_subject_unique_to_entity1.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [number_subject_unique_to_entity2](number_subject_unique_to_entity2.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [subjects_in_common](subjects_in_common.md) | 0..* <br/> [String](String.md) |  | direct |
| [associations_for_subjects_in_common](associations_for_subjects_in_common.md) | 0..* <br/> [Association](Association.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:PairwiseCoAssociation |
| native | ontoassoc:PairwiseCoAssociation |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PairwiseCoAssociation
description: A collection of subjects co-associated with two objects
from_schema: https://w3id.org/oak/association
slots:
- object1
- object2
- object1_label
- object2_label
- number_subjects_in_common
- number_subject_unique_to_entity1
- number_subject_unique_to_entity2
- subjects_in_common
- associations_for_subjects_in_common

```
</details>

### Induced

<details>
```yaml
name: PairwiseCoAssociation
description: A collection of subjects co-associated with two objects
from_schema: https://w3id.org/oak/association
attributes:
  object1:
    name: object1
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    alias: object1
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: uriorcurie
    required: true
  object2:
    name: object2
    from_schema: https://w3id.org/oak/association
    rank: 1000
    is_a: object
    alias: object2
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: uriorcurie
    required: true
  object1_label:
    name: object1_label
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: object1_label
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
  object2_label:
    name: object2_label
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: object2_label
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
  number_subjects_in_common:
    name: number_subjects_in_common
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: number_subjects_in_common
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: integer
  number_subject_unique_to_entity1:
    name: number_subject_unique_to_entity1
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: number_subject_unique_to_entity1
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: integer
  number_subject_unique_to_entity2:
    name: number_subject_unique_to_entity2
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: number_subject_unique_to_entity2
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: integer
  subjects_in_common:
    name: subjects_in_common
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: subjects_in_common
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
  associations_for_subjects_in_common:
    name: associations_for_subjects_in_common
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: associations_for_subjects_in_common
    owner: PairwiseCoAssociation
    domain_of:
    - PairwiseCoAssociation
    range: Association

```
</details>