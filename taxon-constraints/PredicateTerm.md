# Class: PredicateTerm
_A term that represents a relationship type_




URI: [tc:PredicateTerm](https://w3id.org/linkml/taxon_constraints/PredicateTerm)



```{mermaid}
 classDiagram
    class PredicateTerm
      Term <|-- PredicateTerm
      
      PredicateTerm : id
      PredicateTerm : label
      
```





## Inheritance
* [Term](Term.md)
    * **PredicateTerm**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |  | [Term](Term.md) |
| [label](label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [Term](Term.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | [predicate](predicate.md) | range | [PredicateTerm](PredicateTerm.md) |
| [TaxonConstraint](TaxonConstraint.md) | [predicates](predicates.md) | range | [PredicateTerm](PredicateTerm.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/taxon_constraints





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | tc:PredicateTerm |
| native | tc:PredicateTerm |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PredicateTerm
description: A term that represents a relationship type
from_schema: https://w3id.org/linkml/taxon_constraints
rank: 1000
is_a: Term

```
</details>

### Induced

<details>
```yaml
name: PredicateTerm
description: A term that represents a relationship type
from_schema: https://w3id.org/linkml/taxon_constraints
rank: 1000
is_a: Term
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: PredicateTerm
    domain_of:
    - Term
    range: uriorcurie
  label:
    name: label
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    slot_uri: rdfs:label
    alias: label
    owner: PredicateTerm
    domain_of:
    - Term
    range: string

```
</details>