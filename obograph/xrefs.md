

# Slot: xrefs


_A list of cross references to other entities represented in other ontologies, vocabularies, databases, or websites. The semantics of xrefs are intentionally weak, and most closely align with rdfs:seeAlso_





URI: [obographs:xrefs](https://github.com/geneontology/obographs/xrefs)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |  no  |
| [Meta](Meta.md) | A collection of annotations on an entity or ontology or edge or axiom |  yes  |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |  no  |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |  no  |
| [XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |  no  |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |  yes  |







## Properties

* Range: [XrefString](XrefString.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:xrefs |
| native | obographs:xrefs |
| exact | oio:hasDbXref |
| close | rdfs:seeAlso |




## LinkML Source

<details>
```yaml
name: xrefs
description: A list of cross references to other entities represented in other ontologies,
  vocabularies, databases, or websites. The semantics of xrefs are intentionally weak,
  and most closely align with rdfs:seeAlso
from_schema: https://github.com/geneontology/obographs
exact_mappings:
- oio:hasDbXref
close_mappings:
- rdfs:seeAlso
rank: 1000
alias: xrefs
domain_of:
- Meta
- PropertyValue
range: XrefString
multivalued: true

```
</details>