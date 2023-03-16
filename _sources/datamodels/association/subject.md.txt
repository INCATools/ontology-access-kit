# Slot: subject
_The thing which the association is about._


URI: [rdf:subject](rdf:subject)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Association](Association.md) | A generic association between a thing (subject) and another thing (object)
[NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object)






## Properties

* Range: [Uriorcurie](Uriorcurie.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: subject
description: The thing which the association is about.
from_schema: https://w3id.org/oak/association
exact_mappings:
- oa:hasBody
rank: 1000
slot_uri: rdf:subject
alias: subject
domain_of:
- Association
- NegatedAssociation
range: uriorcurie

```
</details>