

# Class: Postcondition



URI: [mappingrules:Postcondition](https://w3id.org/oak/mapping-rules-datamodel/Postcondition)




```{mermaid}
 classDiagram
    class Postcondition
      Postcondition : predicate_id
        
      Postcondition : weight
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate_id](predicate_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [weight](weight.md) | 0..1 <br/> [Float](Float.md) | Weighting of the rule, positive increases the confidence, negative decreases | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [postconditions](postconditions.md) | range | [Postcondition](Postcondition.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:Postcondition |
| native | mappingrules:Postcondition |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Postcondition
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  predicate_id:
    name: predicate_id
    comments:
    - if the rule is invertible, then the predicate is inverted, e.g. skos broad becomes
      narrow
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Postcondition
  weight:
    name: weight
    description: Weighting of the rule, positive increases the confidence, negative
      decreases
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    see_also:
    - https://en.wikipedia.org/wiki/Logit
    - https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png
    rank: 1000
    domain_of:
    - Postcondition
    range: float

```
</details>

### Induced

<details>
```yaml
name: Postcondition
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  predicate_id:
    name: predicate_id
    comments:
    - if the rule is invertible, then the predicate is inverted, e.g. skos broad becomes
      narrow
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: predicate_id
    owner: Postcondition
    domain_of:
    - Postcondition
    range: string
  weight:
    name: weight
    description: Weighting of the rule, positive increases the confidence, negative
      decreases
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    see_also:
    - https://en.wikipedia.org/wiki/Logit
    - https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png
    rank: 1000
    alias: weight
    owner: Postcondition
    domain_of:
    - Postcondition
    range: float

```
</details>