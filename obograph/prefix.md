# Slot: prefix
_The prefix of a prefix declaration._


URI: [sh:prefix](https://w3id.org/shacl/prefix)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[PrefixDeclaration](PrefixDeclaration.md) | A mapping between an individual prefix (e






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Comments

* It is strongly recommended that the prefix is a valid NCName

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: prefix
description: The prefix of a prefix declaration.
comments:
- It is strongly recommended that the prefix is a valid NCName
from_schema: https://github.com/geneontology/obographs
rank: 1000
slot_uri: sh:prefix
alias: prefix
owner: PrefixDeclaration
domain_of:
- PrefixDeclaration
range: string

```
</details>