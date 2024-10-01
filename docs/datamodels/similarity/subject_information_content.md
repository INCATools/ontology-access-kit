

# Slot: subject_information_content


_The IC of the subject_





URI: [sim:subject_information_content](https://w3id.org/linkml/similarity/subject_information_content)




## Inheritance

* [score](score.md)
    * [information_content](information_content.md)
        * **subject_information_content**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [NegativeLogValue](NegativeLogValue.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:subject_information_content |
| native | sim:subject_information_content |




## LinkML Source

<details>
```yaml
name: subject_information_content
description: The IC of the subject
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: information_content
alias: subject_information_content
domain_of:
- TermPairwiseSimilarity
range: NegativeLogValue

```
</details>