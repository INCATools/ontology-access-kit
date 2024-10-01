

# Slot: object_id



URI: [sssom:object_id](http://w3id.org/sssom/object_id)



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
| self | sssom:object_id |
| native | ann:object_id |
| exact | bpa:annotatedClass.id |




## LinkML Source

<details>
```yaml
name: object_id
from_schema: https://w3id.org/oak/text_annotator
exact_mappings:
- bpa:annotatedClass.id
rank: 1000
slot_uri: sssom:object_id
alias: object_id
owner: TextAnnotation
domain_of:
- TextAnnotation
range: string

```
</details>