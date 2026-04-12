

# Slot: subject_source



URI: [sssom:subject_source](http://w3id.org/sssom/subject_source)



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
| self | sssom:subject_source |
| native | ann:subject_source |
| exact | oa:hasBody |




## LinkML Source

<details>
```yaml
name: subject_source
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- oa:hasBody
rank: 1000
slot_uri: sssom:subject_source
alias: subject_source
owner: HasSpan
domain_of:
- HasSpan
range: string

```
</details>