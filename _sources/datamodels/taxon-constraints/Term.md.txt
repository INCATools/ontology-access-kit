

# Class: Term


_An ontology term. In this model this is either the SubjectTerm of a taxon constraint, or an actual taxon_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [owl:Class](http://www.w3.org/2002/07/owl#Class)






```{mermaid}
 classDiagram
    class Term
    click Term href "../Term"
      Term <|-- SubjectTerm
        click SubjectTerm href "../SubjectTerm"
      Term <|-- Taxon
        click Taxon href "../Taxon"
      Term <|-- PredicateTerm
        click PredicateTerm href "../PredicateTerm"
      
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
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the OBO CURIE for the term | direct |
| [label](label.md) | 0..1 <br/> [String](String.md) | the human readable name or label of the term | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




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
from_schema: https://w3id.org/oak/taxon_constraints
abstract: true
attributes:
  id:
    name: id
    description: the OBO CURIE for the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    identifier: true
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
    domain_of:
    - Term
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
from_schema: https://w3id.org/oak/taxon_constraints
abstract: true
attributes:
  id:
    name: id
    description: the OBO CURIE for the term
    from_schema: https://w3id.org/oak/taxon_constraints
    rank: 1000
    identifier: true
    alias: id
    owner: Term
    domain_of:
    - Term
    range: uriorcurie
  label:
    name: label
    description: the human readable name or label of the term
    from_schema: https://w3id.org/oak/taxon_constraints
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