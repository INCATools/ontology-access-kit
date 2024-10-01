

# Class: PredicateTerm


_A term that represents a relationship type_





URI: [tc:PredicateTerm](https://w3id.org/linkml/taxon_constraints/PredicateTerm)






```{mermaid}
 classDiagram
    class PredicateTerm
    click PredicateTerm href "../PredicateTerm"
      Term <|-- PredicateTerm
        click Term href "../Term"
      
      PredicateTerm : id
        
      PredicateTerm : label
        
      
```





## Inheritance
* [Term](Term.md)
    * **PredicateTerm**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the OBO CURIE for the term | [Term](Term.md) |
| [label](label.md) | 0..1 <br/> [String](String.md) | the human readable name or label of the term | [Term](Term.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | [predicate](predicate.md) | range | [PredicateTerm](PredicateTerm.md) |
| [TaxonConstraint](TaxonConstraint.md) | [predicates](predicates.md) | range | [PredicateTerm](PredicateTerm.md) |






## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* RO








### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




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
id_prefixes:
- RO
description: A term that represents a relationship type
from_schema: https://w3id.org/oak/taxon_constraints
is_a: Term

```
</details>

### Induced

<details>
```yaml
name: PredicateTerm
id_prefixes:
- RO
description: A term that represents a relationship type
from_schema: https://w3id.org/oak/taxon_constraints
is_a: Term
attributes:
  id:
    name: id
    description: the OBO CURIE for the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: PredicateTerm
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
    owner: PredicateTerm
    domain_of:
    - Term
    range: string

```
</details>