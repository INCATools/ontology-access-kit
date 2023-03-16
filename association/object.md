# Slot: object
_An ontology entity that is associated with the subject._


URI: [rdf:object](rdf:object)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Association](Association.md) | A generic association between a thing (subject) and another thing (object)
[NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object)
[PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association






## Properties

* Range: [Uriorcurie](Uriorcurie.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: object
description: An ontology entity that is associated with the subject.
from_schema: https://w3id.org/oak/association
exact_mappings:
- oa:hasTarget
rank: 1000
slot_uri: rdf:object
alias: object
domain_of:
- Association
- NegatedAssociation
- PropertyValue
range: uriorcurie

```
</details>