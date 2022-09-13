# Slot: anonymous_individual_count

URI: [https://w3id.org/linkml/reportanonymous_individual_count](https://w3id.org/linkml/reportanonymous_individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **anonymous_individual_count**





## Properties

* Range: [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Specification

<details>
```yaml
name: anonymous_individual_count
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: anonymous_individual_count
domain_of:
- SummaryStatisticCollection
slot_group: individual_statistic_group
range: integer
equals_expression: '{named_individual_count} - {individual_count}'

```
</details>