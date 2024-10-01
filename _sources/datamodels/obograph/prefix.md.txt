

# Slot: prefix


_The prefix of a prefix declaration._





URI: [sh:prefix](https://w3id.org/shacl/prefix)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PrefixDeclaration](PrefixDeclaration.md) | A mapping between an individual prefix (e |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Comments

* It is strongly recommended that the prefix is a valid NCName

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:prefix |
| native | obographs:prefix |




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
key: true
alias: prefix
owner: PrefixDeclaration
domain_of:
- PrefixDeclaration
range: string
required: true

```
</details>