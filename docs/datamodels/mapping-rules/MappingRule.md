

# Class: MappingRule


_An individual mapping rule, if preconditions match the postconditions are applied_





URI: [mappingrules:MappingRule](https://w3id.org/oak/mapping-rules-datamodel/MappingRule)






```{mermaid}
 classDiagram
    class MappingRule
    click MappingRule href "../MappingRule"
      MappingRule : description
        
      MappingRule : oneway
        
      MappingRule : postconditions
        
          
    
    
    MappingRule --> "0..1" Postcondition : postconditions
    click Postcondition href "../Postcondition"

        
      MappingRule : preconditions
        
          
    
    
    MappingRule --> "0..1" Precondition : preconditions
    click Precondition href "../Precondition"

        
      MappingRule : synonymizer
        
          
    
    
    MappingRule --> "0..1" Synonymizer : synonymizer
    click Synonymizer href "../Synonymizer"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [description](description.md) | 0..1 <br/> [String](String.md) |  | direct |
| [oneway](oneway.md) | 0..1 <br/> [Boolean](Boolean.md) | if true then subject and object can be switched and predicate inverted | direct |
| [preconditions](preconditions.md) | 0..1 <br/> [Precondition](Precondition.md) | all of the criteria that must be true before a rule is fired | direct |
| [postconditions](postconditions.md) | 0..1 <br/> [Postcondition](Postcondition.md) | conditions that apply if preconditions match | direct |
| [synonymizer](synonymizer.md) | 0..1 <br/> [Synonymizer](Synonymizer.md) | Normalizing rules to labels | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRuleCollection](MappingRuleCollection.md) | [rules](rules.md) | range | [MappingRule](MappingRule.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:MappingRule |
| native | mappingrules:MappingRule |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  description:
    name: description
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - MappingRule
    - Synonymizer
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    ifabsent: 'False'
    domain_of:
    - MappingRule
    range: boolean
  preconditions:
    name: preconditions
    description: all of the criteria that must be true before a rule is fired
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    slot_uri: sh:condition
    domain_of:
    - MappingRule
    range: Precondition
  postconditions:
    name: postconditions
    description: conditions that apply if preconditions match
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - MappingRule
    range: Postcondition
  synonymizer:
    name: synonymizer
    description: Normalizing rules to labels.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - MappingRule
    range: Synonymizer

```
</details>

### Induced

<details>
```yaml
name: MappingRule
description: An individual mapping rule, if preconditions match the postconditions
  are applied
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  description:
    name: description
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: description
    owner: MappingRule
    domain_of:
    - MappingRule
    - Synonymizer
    range: string
  oneway:
    name: oneway
    description: if true then subject and object can be switched and predicate inverted
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
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
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
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
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: postconditions
    owner: MappingRule
    domain_of:
    - MappingRule
    range: Postcondition
  synonymizer:
    name: synonymizer
    description: Normalizing rules to labels.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: synonymizer
    owner: MappingRule
    domain_of:
    - MappingRule
    range: Synonymizer

```
</details>