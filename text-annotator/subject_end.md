

# Slot: subject_end



URI: [ann:subject_end](https://w3id.org/linkml/text_annotator/subject_end)



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
| self | ann:subject_end |
| native | ann:subject_end |
| exact | bpa:to |




## LinkML Source

<details>
```yaml
name: subject_end
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- bpa:to
rank: 1000
alias: subject_end
owner: HasSpan
domain_of:
- HasSpan
range: Position

```
</details>