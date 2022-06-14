# Class: Postcondition




URI: [mrules:Postcondition](https://w3id.org/linkml/mapping_rules_datamodel/Postcondition)




```{mermaid}
 classDiagram
    class Postcondition
      Postcondition : predicate_id
      Postcondition : weight
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [predicate_id](predicate_id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [weight](weight.md) | [xsd:float](http://www.w3.org/2001/XMLSchema#float) | 0..1 | Weighting of the rule, positive increases the confidence, negative decreases  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [postconditions](postconditions.md) | range | Postcondition |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['mrules:Postcondition'] |
| native | ['mrules:Postcondition'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Postcondition
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  predicate_id:
    name: predicate_id
    comments:
    - if the rule is invertible, then the predicate is inverted, e.g. skos broad becomes
      narrow
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
  weight:
    name: weight
    description: Weighting of the rule, positive increases the confidence, negative
      decreases
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    see_also:
    - https://en.wikipedia.org/wiki/Logit
    - https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png
    range: float

```
</details>

### Induced

<details>
```yaml
name: Postcondition
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  predicate_id:
    name: predicate_id
    comments:
    - if the rule is invertible, then the predicate is inverted, e.g. skos broad becomes
      narrow
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    alias: predicate_id
    owner: Postcondition
    range: string
  weight:
    name: weight
    description: Weighting of the rule, positive increases the confidence, negative
      decreases
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    see_also:
    - https://en.wikipedia.org/wiki/Logit
    - https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png
    alias: weight
    owner: Postcondition
    range: float

```
</details>