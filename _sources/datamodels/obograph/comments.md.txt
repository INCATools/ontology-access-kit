

# Slot: comments


_A list of comments about the entity_





URI: [rdfs:comment](http://www.w3.org/2000/01/rdf-schema#comment)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Meta](Meta.md) | A collection of annotations on an entity or ontology or edge or axiom |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Comments

* for historic reasons obo format only supports a single comment per entity. This limitation is not carried over here, but users should be aware that multiple comments will not be supported in converting back to obo format.

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:comment |
| native | obographs:comments |




## LinkML Source

<details>
```yaml
name: comments
description: A list of comments about the entity
comments:
- for historic reasons obo format only supports a single comment per entity. This
  limitation is not carried over here, but users should be aware that multiple comments
  will not be supported in converting back to obo format.
from_schema: https://github.com/geneontology/obographs
rank: 1000
slot_uri: rdfs:comment
alias: comments
domain_of:
- Meta
range: string
multivalued: true

```
</details>