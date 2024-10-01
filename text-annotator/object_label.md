

# Slot: object_label



URI: [sssom:object_label](http://w3id.org/sssom/object_label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sssom:object_label |
| native | ann:object_label |
| exact | bpa:annotatedClass.prefLabel |




## LinkML Source

<details>
```yaml
name: object_label
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- bpa:annotatedClass.prefLabel
rank: 1000
slot_uri: sssom:object_label
alias: object_label
owner: TextAnnotation
domain_of:
- TextAnnotation
range: string

```
</details>