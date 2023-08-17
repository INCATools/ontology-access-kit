# Slot: primary_knowledge_source


_The primary knowledge source for the association_



URI: [biolink:primary_knowledge_source](https://w3id.org/biolink/vocab/primary_knowledge_source)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
[AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |
[Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
[NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
[ParserConfiguration](ParserConfiguration.md) | Settings that determine behavior when parsing associations |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: primary_knowledge_source
description: The primary knowledge source for the association
from_schema: https://w3id.org/oak/association
rank: 1000
slot_uri: biolink:primary_knowledge_source
alias: primary_knowledge_source
domain_of:
- PositiveOrNegativeAssociation
- ParserConfiguration
- AssociationChange
range: uriorcurie

```
</details>