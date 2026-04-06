

# Slot: subject_start



URI: [ann:subject_start](https://w3id.org/linkml/text_annotator/subject_start)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [HasSpan](HasSpan.md) |  |  no  |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |  no  |







## Properties

* Range: [Position](Position.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:subject_start |
| native | ann:subject_start |
| exact | bpa:from |




## LinkML Source

<details>
```yaml
name: subject_start
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- bpa:from
rank: 1000
alias: subject_start
owner: HasSpan
domain_of:
- HasSpan
range: Position

```
</details>