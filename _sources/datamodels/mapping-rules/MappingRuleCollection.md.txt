# Class: MappingRuleCollection
_A collection of mapping rules_





URI: [mrules:MappingRuleCollection](https://w3id.org/linkml/mapping_rules_datamodel/MappingRuleCollection)




```{mermaid}
 classDiagram
    class MappingRuleCollection
      MappingRuleCollection : minimum_confidence
      MappingRuleCollection : rules
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [rules](rules.md) | [MappingRule](MappingRule.md) | 0..* | all rules  | . |
| [minimum_confidence](minimum_confidence.md) | [xsd:float](http://www.w3.org/2001/XMLSchema#float) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['mrules:MappingRuleCollection'] |
| native | ['mrules:MappingRuleCollection'] |


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
    range: MappingRule
    inlined: true
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
    alias: rules
    owner: MappingRuleCollection
    range: MappingRule
    inlined: true
  minimum_confidence:
    name: minimum_confidence
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    alias: minimum_confidence
    owner: MappingRuleCollection
    range: float
tree_root: true

```
</details>