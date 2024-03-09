# Class: MappingRuleCollection


_A collection of mapping rules_





URI: [mappingrules:MappingRuleCollection](https://w3id.org/oak/mapping-rules-datamodel/MappingRuleCollection)




```{mermaid}
 classDiagram
    class MappingRuleCollection
      MappingRuleCollection : minimum_confidence
        
      MappingRuleCollection : rules
        
          MappingRuleCollection --> MappingRule : rules
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [rules](rules.md) | 0..* <br/> [MappingRule](MappingRule.md) | all rules | direct |
| [minimum_confidence](minimum_confidence.md) | 0..1 <br/> [Float](Float.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:MappingRuleCollection |
| native | mappingrules:MappingRuleCollection |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingRuleCollection
description: A collection of mapping rules
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  rules:
    name: rules
    description: all rules
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    domain_of:
    - MappingRuleCollection
    range: MappingRule
    inlined: true
  minimum_confidence:
    name: minimum_confidence
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - MappingRuleCollection
    range: float
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: MappingRuleCollection
description: A collection of mapping rules
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  rules:
    name: rules
    description: all rules
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: rules
    owner: MappingRuleCollection
    domain_of:
    - MappingRuleCollection
    range: MappingRule
    inlined: true
  minimum_confidence:
    name: minimum_confidence
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: minimum_confidence
    owner: MappingRuleCollection
    domain_of:
    - MappingRuleCollection
    range: float
tree_root: true

```
</details>