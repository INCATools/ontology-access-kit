

# Slot: token_exclusion_list


_A list of tokens to exclude from the annotation process_





URI: [ann:token_exclusion_list](https://w3id.org/linkml/text_annotator/token_exclusion_list)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TextAnnotationConfiguration](TextAnnotationConfiguration.md) | configuration for search |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:token_exclusion_list |
| native | ann:token_exclusion_list |




## LinkML Source

<details>
```yaml
name: token_exclusion_list
description: A list of tokens to exclude from the annotation process
from_schema: https://w3id.org/oak/text_annotator
rank: 1000
alias: token_exclusion_list
owner: TextAnnotationConfiguration
domain_of:
- TextAnnotationConfiguration
range: string
multivalued: true

```
</details>