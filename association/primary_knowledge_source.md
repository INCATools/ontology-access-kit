

# Slot: primary_knowledge_source


_The primary knowledge source for the association_





URI: [biolink:primary_knowledge_source](https://w3id.org/biolink/vocab/primary_knowledge_source)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ParserConfiguration](ParserConfiguration.md) | Settings that determine behavior when parsing associations |  no  |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | biolink:primary_knowledge_source |
| native | ontoassoc:primary_knowledge_source |




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