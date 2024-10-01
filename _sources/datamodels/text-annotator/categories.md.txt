

# Slot: categories


_A list of named entity categories to include._





URI: [ann:categories](https://w3id.org/linkml/text_annotator/categories)



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
| self | ann:categories |
| native | ann:categories |




## LinkML Source

<details>
```yaml
name: categories
description: A list of named entity categories to include.
from_schema: https://w3id.org/oak/text_annotator
rank: 1000
alias: categories
owner: TextAnnotationConfiguration
domain_of:
- TextAnnotationConfiguration
range: string
multivalued: true

```
</details>