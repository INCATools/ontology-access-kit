

# Class: SubjectTerm


_A term that is the subject of a taxon constraint. Typically comes from ontologies like GO, UBERON, CL, ..._





URI: [tc:SubjectTerm](https://w3id.org/linkml/taxon_constraints/SubjectTerm)






```{mermaid}
 classDiagram
    class SubjectTerm
    click SubjectTerm href "../SubjectTerm"
      Term <|-- SubjectTerm
        click Term href "../Term"
      
      SubjectTerm : description
        
      SubjectTerm : id
        
      SubjectTerm : label
        
      SubjectTerm : never_in
        
          
    
    
    SubjectTerm --> "*" TaxonConstraint : never_in
    click TaxonConstraint href "../TaxonConstraint"

        
      SubjectTerm : only_in
        
          
    
    
    SubjectTerm --> "*" TaxonConstraint : only_in
    click TaxonConstraint href "../TaxonConstraint"

        
      SubjectTerm : present_in
        
          
    
    
    SubjectTerm --> "*" TaxonConstraint : present_in
    click TaxonConstraint href "../TaxonConstraint"

        
      SubjectTerm : present_in_ancestor_of
        
          
    
    
    SubjectTerm --> "*" TaxonConstraint : present_in_ancestor_of
    click TaxonConstraint href "../TaxonConstraint"

        
      SubjectTerm : unsatisfiable
        
      
```





## Inheritance
* [Term](Term.md)
    * **SubjectTerm**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [description](description.md) | 0..1 <br/> [String](String.md) | A description of the term | direct |
| [unsatisfiable](unsatisfiable.md) | 0..1 <br/> [Boolean](Boolean.md) | If true then some combination of taxon constraints plus ontology lead to cont... | direct |
| [only_in](only_in.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) | Points to a taxon constraint that states the SubjectTerm is ONLY found in a t... | direct |
| [never_in](never_in.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) | Points to a taxon constraint that states the SubjectTerm is NEVER found in a ... | direct |
| [present_in](present_in.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) | The term MAY be in the specified taxon, or a descendant of that taxon | direct |
| [present_in_ancestor_of](present_in_ancestor_of.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) |  | direct |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the OBO CURIE for the term | [Term](Term.md) |
| [label](label.md) | 0..1 <br/> [String](String.md) | the human readable name or label of the term | [Term](Term.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | [subject](subject.md) | range | [SubjectTerm](SubjectTerm.md) |
| [TaxonConstraint](TaxonConstraint.md) | [via_terms](via_terms.md) | range | [SubjectTerm](SubjectTerm.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | tc:SubjectTerm |
| native | tc:SubjectTerm |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SubjectTerm
description: A term that is the subject of a taxon constraint. Typically comes from
  ontologies like GO, UBERON, CL, ...
from_schema: https://w3id.org/oak/taxon_constraints
is_a: Term
attributes:
  description:
    name: description
    description: A description of the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - SubjectTerm
  unsatisfiable:
    name: unsatisfiable
    description: If true then some combination of taxon constraints plus ontology
      lead to contradictions
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - SubjectTerm
    range: boolean
  only_in:
    name: only_in
    description: 'Points to a taxon constraint that states the SubjectTerm is ONLY
      found in a taxon or descendant. Formally, the term AND its descendants MUST
      be in the specified taxon, or a descendant of that taxon

      '
    comments:
    - Note that we conflate between the RO "only in taxon" and "in taxon" relations
      here
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002160
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  never_in:
    name: never_in
    description: 'Points to a taxon constraint that states the SubjectTerm is NEVER
      found in a taxon or descendant. Formally, the term AND its descendants MUST
      NOT be in the specified taxon, or a descendant of that taxon

      '
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002161
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  present_in:
    name: present_in
    description: 'The term MAY be in the specified taxon, or a descendant of that
      taxon

      '
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002175
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  present_in_ancestor_of:
    name: present_in_ancestor_of
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: SubjectTerm
description: A term that is the subject of a taxon constraint. Typically comes from
  ontologies like GO, UBERON, CL, ...
from_schema: https://w3id.org/oak/taxon_constraints
is_a: Term
attributes:
  description:
    name: description
    description: A description of the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: description
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: string
  unsatisfiable:
    name: unsatisfiable
    description: If true then some combination of taxon constraints plus ontology
      lead to contradictions
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: unsatisfiable
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: boolean
  only_in:
    name: only_in
    description: 'Points to a taxon constraint that states the SubjectTerm is ONLY
      found in a taxon or descendant. Formally, the term AND its descendants MUST
      be in the specified taxon, or a descendant of that taxon

      '
    comments:
    - Note that we conflate between the RO "only in taxon" and "in taxon" relations
      here
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002160
    alias: only_in
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  never_in:
    name: never_in
    description: 'Points to a taxon constraint that states the SubjectTerm is NEVER
      found in a taxon or descendant. Formally, the term AND its descendants MUST
      NOT be in the specified taxon, or a descendant of that taxon

      '
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002161
    alias: never_in
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  present_in:
    name: present_in
    description: 'The term MAY be in the specified taxon, or a descendant of that
      taxon

      '
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: RO:0002175
    alias: present_in
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  present_in_ancestor_of:
    name: present_in_ancestor_of
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: present_in_ancestor_of
    owner: SubjectTerm
    domain_of:
    - SubjectTerm
    range: TaxonConstraint
    multivalued: true
  id:
    name: id
    description: the OBO CURIE for the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: SubjectTerm
    domain_of:
    - Term
    range: uriorcurie
    required: true
  label:
    name: label
    description: the human readable name or label of the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdfs:label
    alias: label
    owner: SubjectTerm
    domain_of:
    - Term
    range: string

```
</details>