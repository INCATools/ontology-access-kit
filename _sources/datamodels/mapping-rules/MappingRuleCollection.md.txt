# Class: MappingRuleCollection
_A collection of mapping rules_





URI: [mrules:MappingRuleCollection](https://w3id.org/linkml/mapping_rules_datamodel/MappingRuleCollection)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [rules](rules.md) | [MappingRule](MappingRule.md) | 0..* | all rules  | . |
| [minimum_confidence](minimum_confidence.md) | [float](float.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingRuleCollection
description: A collection of mapping rules
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  rules:
    name: rules
    description: all rules
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    inlined: true
    range: MappingRule
  minimum_confidence:
    name: minimum_confidence
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    range: float
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: MappingRuleCollection
description: A collection of mapping rules
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  rules:
    name: rules
    description: all rules
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    inlined: true
    alias: rules
    owner: MappingRuleCollection
    range: MappingRule
  minimum_confidence:
    name: minimum_confidence
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    alias: minimum_confidence
    owner: MappingRuleCollection
    range: float
tree_root: true

```
</details>