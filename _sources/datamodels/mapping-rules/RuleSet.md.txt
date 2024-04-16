

# Class: RuleSet


_A set of rules for generating synonyms or alternate lexical elements._





URI: [mappingrules:RuleSet](https://w3id.org/oak/mapping-rules-datamodel/RuleSet)




```{mermaid}
 classDiagram
    class RuleSet
      RuleSet : prefix
        
      RuleSet : rules
        
          RuleSet --> Synonymizer : rules
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [rules](rules.md) | 0..* <br/> [Synonymizer](Synonymizer.md) | A list of rules for generating synonyms or alternate lexical elements | direct |
| [prefix](prefix.md) | 0..1 <br/> [String](String.md) | The prefix that qualifies for the rule | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:RuleSet |
| native | mappingrules:RuleSet |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RuleSet
description: A set of rules for generating synonyms or alternate lexical elements.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  rules:
    name: rules
    description: A list of rules for generating synonyms or alternate lexical elements.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    multivalued: true
    domain_of:
    - MappingRuleCollection
    - RuleSet
    range: Synonymizer
  prefix:
    name: prefix
    description: The prefix that qualifies for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    domain_of:
    - Synonymizer
    - Test
    - RuleSet
    range: string

```
</details>

### Induced

<details>
```yaml
name: RuleSet
description: A set of rules for generating synonyms or alternate lexical elements.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  rules:
    name: rules
    description: A list of rules for generating synonyms or alternate lexical elements.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    multivalued: true
    alias: rules
    owner: RuleSet
    domain_of:
    - MappingRuleCollection
    - RuleSet
    range: Synonymizer
  prefix:
    name: prefix
    description: The prefix that qualifies for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    alias: prefix
    owner: RuleSet
    domain_of:
    - Synonymizer
    - Test
    - RuleSet
    range: string

```
</details>