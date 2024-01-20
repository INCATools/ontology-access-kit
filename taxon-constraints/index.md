# Taxon Constraints Reporting Datamodel

A datamodel for representing inferred and asserted taxon constraints.

URI: https://w3id.org/oak/taxon_constraints

Name: taxon-constraints



## Classes

| Class | Description |
| --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint |
| [Term](Term.md) | An ontology term. In this model this is either the SubjectTerm of a taxon constraint, or an actual taxon |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PredicateTerm](PredicateTerm.md) | A term that represents a relationship type |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint. Typically comes from ontologies like GO, UBERON, CL, ... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Taxon](Taxon.md) | A term that represents a taxonomic group, may be at species level of a higher level |



## Slots

| Slot | Description |
| --- | --- |
| [asserted](asserted.md) | holds if the constraint is asserted in the source ontology, rather than infer... |
| [candidate](candidate.md) | true if this is a proposed candidate constraint |
| [comments](comments.md) |  |
| [contradicted_by](contradicted_by.md) | If the taxon constraint conflicts with another,  then this is the set of taxo... |
| [description](description.md) | A description of the term |
| [evolutionary](evolutionary.md) | holds if the constraint is an evolutionary statement |
| [id](id.md) | the OBO CURIE for the term |
| [label](label.md) | the human readable name or label of the term |
| [never_in](never_in.md) | Points to a taxon constraint that states the SubjectTerm is NEVER found in a ... |
| [only_in](only_in.md) | Points to a taxon constraint that states the SubjectTerm is ONLY found in a t... |
| [predicate](predicate.md) | The relationship type for the constraint (e |
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
| [ConfigurationOption](ConfigurationOption.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
