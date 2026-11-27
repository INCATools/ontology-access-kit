

# Slot: subject_label


_The portion of the subject text that is matched, ranging from subject_start to subject_end_





URI: [ann:subject_label](https://w3id.org/linkml/text_annotator/subject_label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [HasSpan](HasSpan.md) |  |  no  |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:subject_label |
| native | ann:subject_label |
| exact | bpa:text |




## LinkML Source

<details>
```yaml
name: subject_label
description: The portion of the subject text that is matched, ranging from subject_start
  to subject_end
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- bpa:text
rank: 1000
alias: subject_label
owner: HasSpan
domain_of:
- HasSpan
range: string

```
</details>