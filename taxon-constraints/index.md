# Taxon Constraints Reporting Datamodel

A datamodel for representing inferred and asserted taxon constraints.

URI: https://w3id.org/linkml/taxon_constraints
Name: taxon-constraints



## Classes

| Class | Description |
| --- | --- |
| [PredicateTerm](PredicateTerm.md) | A term that represents a relationship type |
| [SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint |
| [Taxon](Taxon.md) | A term that represents a taxonomic group, may be at species level of a higher... |
| [TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint |
| [Term](Term.md) | An ontology term |


## Slots

| Slot | Description |
| --- | --- |
| [asserted](asserted.md) | holds if the constraint is asserted in the source ontology, rather than infer... |
| [comments](comments.md) |  |
| [contradicted_by](contradicted_by.md) | If the taxon constraint conflicts with another,  then this is the set of taxo... |
| [description](description.md) | A description of the term |
| [evolutionary](evolutionary.md) | holds if the constraint is an evolutionary statement |
| [id](id.md) |  |
| [label](label.md) |  |
| [never_in](never_in.md) | The term AND its descendants MUST NOT be in the specified taxon, or a descend... |
| [only_in](only_in.md) | The term AND its descendants MUST be in the specified taxon, or a descendant ... |
| [predicate](predicate.md) | The relationship type for the contraint (e |
| [predicates](predicates.md) | The predicates that connect the subject term to the via_terms |
| [present_in](present_in.md) | The term MAY be in the specified taxon, or a descendant of that taxon |
| [present_in_ancestor_of](present_in_ancestor_of.md) |  |
| [redundant](redundant.md) | True if this is redundant within the set of constraints of the same type (nev... |
| [redundant_with](redundant_with.md) | If the taxon constraint is redundant, then this is the set of taxon constrain... |
| [redundant_with_only_in](redundant_with_only_in.md) | True for never in constraints that are subsumed by an only in |
| [sources](sources.md) |  |
| [subject](subject.md) | The term to which the constraint applies |
| [taxon](taxon.md) | The taxon which this constraint is about |
| [unsatisfiable](unsatisfiable.md) | If true then some combination of taxon constraints plus ontology lead to cont... |
| [via_terms](via_terms.md) | For inferred taxon constraints, this is the term or terms that have the taxon... |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | A binary (true or false) value |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | a compact URI |
| [xsd:date](http://www.w3.org/2001/XMLSchema#date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | The combination of a date and time |
| [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](http://www.w3.org/2001/XMLSchema#double) | A real number that conforms to the xsd:double specification |
| [xsd:float](http://www.w3.org/2001/XMLSchema#float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | An integer |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
