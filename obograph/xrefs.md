# Slot: xrefs
_A list of cross references to other entities represented in other ontologies, vocabularies, databases, or websites. The semantics of xrefs are intentionally weak, and most closely align with rdfs:seeAlso_


URI: [og:xrefs](https://github.com/geneontology/obographs/xrefs)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Meta](Meta.md) | A collection of annotations on an entity or ontology or axiom
[PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec...
[DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of...
[BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d...
[XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ...
[SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity






## Properties

* Range: [XrefString](XrefString.md)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: xrefs
description: A list of cross references to other entities represented in other ontologies,
  vocabularies, databases, or websites. The semantics of xrefs are intentionally weak,
  and most closely align with rdfs:seeAlso
from_schema: https://github.com/geneontology/obographs
close_mappings:
- rdfs:seeAlso
rank: 1000
multivalued: true
alias: xrefs
domain_of:
- Meta
- PropertyValue
range: XrefString

```
</details>