

# Class: TaxonConstraint


_An individual taxon constraint_





URI: [rdf:Statement](http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement)






```{mermaid}
 classDiagram
    class TaxonConstraint
    click TaxonConstraint href "../TaxonConstraint"
      TaxonConstraint : asserted
        
      TaxonConstraint : candidate
        
      TaxonConstraint : comments
        
      TaxonConstraint : contradicted_by
        
          
    
    
    TaxonConstraint --> "*" TaxonConstraint : contradicted_by
    click TaxonConstraint href "../TaxonConstraint"

        
      TaxonConstraint : evolutionary
        
      TaxonConstraint : predicate
        
          
    
    
    TaxonConstraint --> "0..1" PredicateTerm : predicate
    click PredicateTerm href "../PredicateTerm"

        
      TaxonConstraint : predicates
        
          
    
    
    TaxonConstraint --> "*" PredicateTerm : predicates
    click PredicateTerm href "../PredicateTerm"

        
      TaxonConstraint : redundant
        
      TaxonConstraint : redundant_with
        
          
    
    
    TaxonConstraint --> "*" TaxonConstraint : redundant_with
    click TaxonConstraint href "../TaxonConstraint"

        
      TaxonConstraint : redundant_with_only_in
        
      TaxonConstraint : sources
        
      TaxonConstraint : subject
        
          
    
    
    TaxonConstraint --> "0..1" SubjectTerm : subject
    click SubjectTerm href "../SubjectTerm"

        
      TaxonConstraint : taxon
        
          
    
    
    TaxonConstraint --> "0..1" Taxon : taxon
    click Taxon href "../Taxon"

        
      TaxonConstraint : via_terms
        
          
    
    
    TaxonConstraint --> "*" SubjectTerm : via_terms
    click SubjectTerm href "../SubjectTerm"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject](subject.md) | 0..1 <br/> [SubjectTerm](SubjectTerm.md) | The term to which the constraint applies | direct |
| [predicate](predicate.md) | 0..1 <br/> [PredicateTerm](PredicateTerm.md) | The relationship type for the constraint (e | direct |
| [asserted](asserted.md) | 0..1 <br/> [Boolean](Boolean.md) | holds if the constraint is asserted in the source ontology, rather than infer... | direct |
| [evolutionary](evolutionary.md) | 0..1 <br/> [Boolean](Boolean.md) | holds if the constraint is an evolutionary statement | direct |
| [redundant](redundant.md) | 0..1 <br/> [Boolean](Boolean.md) | True if this is redundant within the set of constraints of the same type (nev... | direct |
| [redundant_with_only_in](redundant_with_only_in.md) | 0..1 <br/> [Boolean](Boolean.md) | True for never in constraints that are subsumed by an only in | direct |
| [taxon](taxon.md) | 0..1 <br/> [Taxon](Taxon.md) | The taxon which this constraint is about | direct |
| [redundant_with](redundant_with.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) | If the taxon constraint is redundant, then this is the set of taxon constrain... | direct |
| [contradicted_by](contradicted_by.md) | * <br/> [TaxonConstraint](TaxonConstraint.md) | If the taxon constraint conflicts with another,  then this is the set of taxo... | direct |
| [via_terms](via_terms.md) | * <br/> [SubjectTerm](SubjectTerm.md) | For inferred taxon constraints, this is the term or terms that have the taxon... | direct |
| [predicates](predicates.md) | * <br/> [PredicateTerm](PredicateTerm.md) | The predicates that connect the subject term to the via_terms | direct |
| [sources](sources.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [comments](comments.md) | * <br/> [String](String.md) |  | direct |
| [candidate](candidate.md) | 0..1 <br/> [Boolean](Boolean.md) | true if this is a proposed candidate constraint | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SubjectTerm](SubjectTerm.md) | [only_in](only_in.md) | range | [TaxonConstraint](TaxonConstraint.md) |
| [SubjectTerm](SubjectTerm.md) | [never_in](never_in.md) | range | [TaxonConstraint](TaxonConstraint.md) |
| [SubjectTerm](SubjectTerm.md) | [present_in](present_in.md) | range | [TaxonConstraint](TaxonConstraint.md) |
| [SubjectTerm](SubjectTerm.md) | [present_in_ancestor_of](present_in_ancestor_of.md) | range | [TaxonConstraint](TaxonConstraint.md) |
| [TaxonConstraint](TaxonConstraint.md) | [redundant_with](redundant_with.md) | range | [TaxonConstraint](TaxonConstraint.md) |
| [TaxonConstraint](TaxonConstraint.md) | [contradicted_by](contradicted_by.md) | range | [TaxonConstraint](TaxonConstraint.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:Statement |
| native | tc:TaxonConstraint |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TaxonConstraint
description: An individual taxon constraint
from_schema: https://w3id.org/oak/taxon_constraints
attributes:
  subject:
    name: subject
    description: The term to which the constraint applies
    comments:
    - this is a reciprocal slot and will be the same as the containing SubjectTerm
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:subject
    domain_of:
    - TaxonConstraint
    range: SubjectTerm
  predicate:
    name: predicate
    description: The relationship type for the constraint (e.g. in_taxon, never_in
      taxon)
    todos:
    - define a value set of this
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:predicate
    domain_of:
    - TaxonConstraint
    range: PredicateTerm
  asserted:
    name: asserted
    description: holds if the constraint is asserted in the source ontology, rather
      than inferred by rules or reasoning
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: boolean
  evolutionary:
    name: evolutionary
    description: holds if the constraint is an evolutionary statement
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: boolean
  redundant:
    name: redundant
    description: True if this is redundant within the set of constraints of the same
      type (never vs only)
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: boolean
  redundant_with_only_in:
    name: redundant_with_only_in
    description: True for never in constraints that are subsumed by an only in
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: boolean
  taxon:
    name: taxon
    description: The taxon which this constraint is about. May be species or a more
      general class.
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:object
    domain_of:
    - TaxonConstraint
    range: Taxon
    inlined: true
  redundant_with:
    name: redundant_with
    description: If the taxon constraint is redundant, then this is the set of taxon
      constraints that it is redundant with
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: TaxonConstraint
    multivalued: true
  contradicted_by:
    name: contradicted_by
    description: If the taxon constraint conflicts with another,  then this is the
      set of taxon constraints that it is redundant with
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: TaxonConstraint
    multivalued: true
  via_terms:
    name: via_terms
    description: For inferred taxon constraints, this is the term or terms that have
      the taxon constraint asserted
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: SubjectTerm
    multivalued: true
    inlined: true
    inlined_as_list: true
  predicates:
    name: predicates
    description: The predicates that connect the subject term to the via_terms.
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: PredicateTerm
    multivalued: true
  sources:
    name: sources
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: uriorcurie
    multivalued: true
  comments:
    name: comments
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: string
    multivalued: true
  candidate:
    name: candidate
    description: true if this is a proposed candidate constraint
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    domain_of:
    - TaxonConstraint
    range: boolean
class_uri: rdf:Statement

```
</details>

### Induced

<details>
```yaml
name: TaxonConstraint
description: An individual taxon constraint
from_schema: https://w3id.org/oak/taxon_constraints
attributes:
  subject:
    name: subject
    description: The term to which the constraint applies
    comments:
    - this is a reciprocal slot and will be the same as the containing SubjectTerm
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:subject
    alias: subject
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: SubjectTerm
  predicate:
    name: predicate
    description: The relationship type for the constraint (e.g. in_taxon, never_in
      taxon)
    todos:
    - define a value set of this
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:predicate
    alias: predicate
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: PredicateTerm
  asserted:
    name: asserted
    description: holds if the constraint is asserted in the source ontology, rather
      than inferred by rules or reasoning
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: asserted
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: boolean
  evolutionary:
    name: evolutionary
    description: holds if the constraint is an evolutionary statement
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: evolutionary
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: boolean
  redundant:
    name: redundant
    description: True if this is redundant within the set of constraints of the same
      type (never vs only)
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: redundant
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: boolean
  redundant_with_only_in:
    name: redundant_with_only_in
    description: True for never in constraints that are subsumed by an only in
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: redundant_with_only_in
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: boolean
  taxon:
    name: taxon
    description: The taxon which this constraint is about. May be species or a more
      general class.
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    slot_uri: rdf:object
    alias: taxon
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: Taxon
    inlined: true
  redundant_with:
    name: redundant_with
    description: If the taxon constraint is redundant, then this is the set of taxon
      constraints that it is redundant with
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: redundant_with
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: TaxonConstraint
    multivalued: true
  contradicted_by:
    name: contradicted_by
    description: If the taxon constraint conflicts with another,  then this is the
      set of taxon constraints that it is redundant with
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: contradicted_by
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: TaxonConstraint
    multivalued: true
  via_terms:
    name: via_terms
    description: For inferred taxon constraints, this is the term or terms that have
      the taxon constraint asserted
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: via_terms
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: SubjectTerm
    multivalued: true
    inlined: true
    inlined_as_list: true
  predicates:
    name: predicates
    description: The predicates that connect the subject term to the via_terms.
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: predicates
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: PredicateTerm
    multivalued: true
  sources:
    name: sources
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: sources
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: uriorcurie
    multivalued: true
  comments:
    name: comments
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: comments
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: string
    multivalued: true
  candidate:
    name: candidate
    description: true if this is a proposed candidate constraint
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    alias: candidate
    owner: TaxonConstraint
    domain_of:
    - TaxonConstraint
    range: boolean
class_uri: rdf:Statement

```
</details>