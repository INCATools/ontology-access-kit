

# Slot: background_count


_The number of items (terms or annotated entities) in the background set, i.e. N in Pr(t) = freq(t)/N_





URI: [sim:background_count](https://w3id.org/linkml/similarity/background_count)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [InformationContentMethod](InformationContentMethod.md) | Describes how information content (IC) scores were computed |  no  |







## Properties

* Range: [ItemCount](ItemCount.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:background_count |
| native | sim:background_count |




## LinkML Source

<details>
```yaml
name: background_count
description: The number of items (terms or annotated entities) in the background set,
  i.e. N in Pr(t) = freq(t)/N
from_schema: https://w3id.org/oak/similarity
rank: 1000
alias: background_count
owner: InformationContentMethod
domain_of:
- InformationContentMethod
range: ItemCount

```
</details>