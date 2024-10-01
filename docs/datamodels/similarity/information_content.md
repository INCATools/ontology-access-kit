

# Slot: information_content


_The IC is the negative log of the probability of the concept_




* __NOTE__: this is an abstract slot and should not be populated directly


URI: [sim:information_content](https://w3id.org/linkml/similarity/information_content)




## Inheritance

* [score](score.md)
    * **information_content**
        * [subject_information_content](subject_information_content.md)
        * [object_information_content](object_information_content.md)
        * [ancestor_information_content](ancestor_information_content.md)









## Properties

* Range: [NegativeLogValue](NegativeLogValue.md)



## Aliases


* IC



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:information_content |
| native | sim:information_content |




## LinkML Source

<details>
```yaml
name: information_content
description: The IC is the negative log of the probability of the concept
from_schema: https://w3id.org/oak/similarity
aliases:
- IC
rank: 1000
is_a: score
abstract: true
alias: information_content
range: NegativeLogValue

```
</details>