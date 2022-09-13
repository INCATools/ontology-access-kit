# Slot: named_individual_count

URI: [https://w3id.org/linkml/reportnamed_individual_count](https://w3id.org/linkml/reportnamed_individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **named_individual_count**





## Properties

* Range: [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)
* Multivalued: None







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| _if_missing |  |
| count_of | owl:NamedIndividual |




### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Specification

<details>
```yaml
name: named_individual_count
annotations:
  count_of:
    tag: count_of
    value: owl:NamedIndividual
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: named_individual_count
domain_of:
- SummaryStatisticCollection
slot_group: individual_statistic_group
range: integer

```
</details>