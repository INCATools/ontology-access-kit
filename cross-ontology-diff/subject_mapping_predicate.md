# Slot: subject_mapping_predicate
_The mapping predicate that holds between left_subject_id and right_subject_id_


URI: [https://w3id.org/linkml/text_annotator/subject_mapping_predicate](https://w3id.org/linkml/text_annotator/subject_mapping_predicate)




## Inheritance

* **subject_mapping_predicate** [ [subject](subject.md) [predicate](predicate.md)]





## Properties

* Range: [EntityReference](EntityReference.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: subject_mapping_predicate
description: The mapping predicate that holds between left_subject_id and right_subject_id
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- subject
- predicate
alias: subject_mapping_predicate
domain_of:
- RelationalDiff
range: EntityReference

```
</details>