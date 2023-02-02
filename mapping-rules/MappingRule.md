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
      MappingRule : synonymizer
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [description](description.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [oneway](oneway.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | if true then subject and object can be switched and predicate inverted | direct |
| [preconditions](preconditions.md) | 0..1 <br/> [Precondition](Precondition.md) | all of the criteria that must be true before a rule is fired | direct |
| [postconditions](postconditions.md) | 0..1 <br/> [Postcondition](Postcondition.md) | conditions that apply if preconditions match | direct |
| [synonymizer](synonymizer.md) | 0..1 <br/> [Synonymizer](Synonymizer.md) | Normalizing rules to labels | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRuleCollection](MappingRuleCollection.md) | [rules](rules.md) | range | [MappingRule](MappingRule.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mrules:MappingRule |
| native | mrules:MappingRule |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
rank: 1000
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    ifabsent: 'False'
    range: boolean
  preconditions:
    name: preconditions
    description: all of the criteria that must be true before a rule is fired
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    slot_uri: sh:condition
    range: Precondition
  postconditions:
    name: postconditions
    description: conditions that apply if preconditions match
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: Postcondition
  synonymizer:
    name: synonymizer
    description: Normalizing rules to labels.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: Synonymizer

```
</details>

### Induced

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
rank: 1000
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: description
    owner: MappingRule
    domain_of:
    - MappingRule
    range: string
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    ifabsent: 'False'
    alias: oneway
    owner: MappingRule
    domain_of:
    - MappingRule
    range: boolean
  preconditions:
    name: preconditions
    description: all of the criteria that must be true before a rule is fired
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    slot_uri: sh:condition
    alias: preconditions
    owner: MappingRule
    domain_of:
    - MappingRule
    range: Precondition
  postconditions:
    name: postconditions
    description: conditions that apply if preconditions match
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: postconditions
    owner: MappingRule
    domain_of:
    - MappingRule
    range: Postcondition
  synonymizer:
    name: synonymizer
    description: Normalizing rules to labels.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: synonymizer
    owner: MappingRule
    domain_of:
    - MappingRule
    range: Synonymizer

```
</details>