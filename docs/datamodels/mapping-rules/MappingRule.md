# Class: MappingRule
_An individual mapping rule, if preconditions match the postconditions are applied_





URI: [mrules:MappingRule](https://w3id.org/linkml/mapping_rules_datamodel/MappingRule)




```{mermaid}
 classDiagram
    class MappingRule
      MappingRule : description
      MappingRule : oneway
      MappingRule : postconditions
      MappingRule : preconditions
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [description](description.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [oneway](oneway.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | if true then subject and object can be switched and predicate inverted  | . |
| [preconditions](preconditions.md) | [Precondition](Precondition.md) | 0..1 | all of the criteria that must be true before a rule is fired  | . |
| [postconditions](postconditions.md) | [Postcondition](Postcondition.md) | 0..1 | conditions that apply if preconditions match  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRuleCollection](MappingRuleCollection.md) | [rules](rules.md) | range | MappingRule |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['mrules:MappingRule'] |
| native | ['mrules:MappingRule'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    ifabsent: 'False'
    range: boolean
  preconditions:
    name: preconditions
    description: all of the criteria that must be true before a rule is fired
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    slot_uri: sh:condition
    range: Precondition
  postconditions:
    name: postconditions
    description: conditions that apply if preconditions match
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    range: Postcondition

```
</details>

### Induced

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    alias: description
    owner: MappingRule
    range: string
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    ifabsent: 'False'
    alias: oneway
    owner: MappingRule
    range: boolean
  preconditions:
    name: preconditions
    description: all of the criteria that must be true before a rule is fired
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    slot_uri: sh:condition
    alias: preconditions
    owner: MappingRule
    range: Precondition
  postconditions:
    name: postconditions
    description: conditions that apply if preconditions match
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    alias: postconditions
    owner: MappingRule
    range: Postcondition

```
</details>