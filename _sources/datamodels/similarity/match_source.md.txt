

# Slot: match_source



URI: [sim:match_source](https://w3id.org/linkml/similarity/match_source)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [BestMatch](BestMatch.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Comments

* note that the match_source is either the subject or the object

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:match_source |
| native | sim:match_source |




## LinkML Source

<details>
```yaml
name: match_source
comments:
- note that the match_source is either the subject or the object
from_schema: https://w3id.org/oak/similarity
rank: 1000
identifier: true
alias: match_source
owner: BestMatch
domain_of:
- BestMatch
range: string
required: true

```
</details>