

# Slot: right_object_label


_The name of the object (parent) of the matched/right edge, if matchable_





URI: [xodiff:right_object_label](https://w3id.org/oak/cross-ontology-diff/right_object_label)




## Inheritance

* **right_object_label** [ [right_side](right_side.md) [object](object.md) [label](label.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [Label](Label.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_object_label |
| native | xodiff:right_object_label |




## LinkML Source

<details>
```yaml
name: right_object_label
description: The name of the object (parent) of the matched/right edge, if matchable
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- object
- label
alias: right_object_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>