# Class: Term
_An ontology term. In this model this is either the SubjectTerm of a taxon constraint, or an actual taxon_



* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [owl:Class](http://www.w3.org/2002/07/owl#Class)



```{mermaid}
 classDiagram
    class Term
      Term <|-- SubjectTerm
      Term <|-- Taxon
      Term <|-- PredicateTerm
      
      Term : id
      Term : label
      
```





## Inheritance
* **Term**
    * [SubjectTerm](SubjectTerm.md)
    * [Taxon](Taxon.md)
    * [PredicateTerm](PredicateTerm.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |  | direct |
| [label](label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/taxon_constraints





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Class |
| native | tc:Term |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Term
description: An ontology term. In this model this is either the SubjectTerm of a taxon
  constraint, or an actual taxon
from_schema: https://w3id.org/linkml/taxon_constraints
rank: 1000
abstract: true
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    identifier: true
    range: uriorcurie
  label:
    name: label
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    slot_uri: rdfs:label
    range: string
class_uri: owl:Class

```
</details>

### Induced

<details>
```yaml
name: Term
description: An ontology term. In this model this is either the SubjectTerm of a taxon
  constraint, or an actual taxon
from_schema: https://w3id.org/linkml/taxon_constraints
rank: 1000
abstract: true
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: Term
    domain_of:
    - Term
    range: uriorcurie
  label:
    name: label
    from_schema: https://w3id.org/linkml/taxon_constraints
    rank: 1000
    slot_uri: rdfs:label
    alias: label
    owner: Term
    domain_of:
    - Term
    range: string
class_uri: owl:Class

```
</details>