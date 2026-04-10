

# Slot: prefixes


_A collection of mappings between prefixes and namespaces, used to map CURIEs (e.g. GO:0008150) to IRIs (e.g. http://purl.obolibrary.org/obo/GO_0008150)_





URI: [sh:declare](https://w3id.org/shacl/declare)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |  no  |
| [GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes th... |  no  |







## Properties

* Range: [PrefixDeclaration](PrefixDeclaration.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:declare |
| native | obographs:prefixes |




## LinkML Source

<details>
```yaml
name: prefixes
description: A collection of mappings between prefixes and namespaces, used to map
  CURIEs (e.g. GO:0008150) to IRIs (e.g. http://purl.obolibrary.org/obo/GO_0008150)
from_schema: https://github.com/geneontology/obographs
rank: 1000
slot_uri: sh:declare
alias: prefixes
domain_of:
- GraphDocument
- Graph
range: PrefixDeclaration
multivalued: true
inlined: true

```
</details>