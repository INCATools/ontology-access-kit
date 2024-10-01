

# Class: Taxon


_A term that represents a taxonomic group, may be at species level of a higher level_





URI: [tc:Taxon](https://w3id.org/linkml/taxon_constraints/Taxon)






```{mermaid}
 classDiagram
    class Taxon
    click Taxon href "../Taxon"
      Term <|-- Taxon
        click Term href "../Term"
      
      Taxon : id
        
      Taxon : label
        
      
```





## Inheritance
* [Term](Term.md)
    * **Taxon**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the OBO CURIE for the term | [Term](Term.md) |
| [label](label.md) | 0..1 <br/> [String](String.md) | the human readable name or label of the term | [Term](Term.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | [taxon](taxon.md) | range | [Taxon](Taxon.md) |






## Identifier and Mapping Information


### Valid ID Prefixes

Instances of this class *should* have identifiers with one of the following prefixes:

* NCBITaxon

* NCBITaxon_Union








### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | tc:Taxon |
| native | tc:Taxon |
| exact | NCBITaxon:1 |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Taxon
id_prefixes:
- NCBITaxon
- NCBITaxon_Union
description: A term that represents a taxonomic group, may be at species level of
  a higher level
from_schema: https://w3id.org/oak/taxon_constraints
exact_mappings:
- NCBITaxon:1
is_a: Term

```
</details>

### Induced

<details>
```yaml
name: Taxon
id_prefixes:
- NCBITaxon
- NCBITaxon_Union
description: A term that represents a taxonomic group, may be at species level of
  a higher level
from_schema: https://w3id.org/oak/taxon_constraints
exact_mappings:
- NCBITaxon:1
is_a: Term
attributes:
  id:
    name: id
    description: the OBO CURIE for the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: Taxon
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
    owner: Taxon
    domain_of:
    - Term
    range: string

```
</details>