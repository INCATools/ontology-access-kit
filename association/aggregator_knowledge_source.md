

# Slot: aggregator_knowledge_source


_The knowledge source that aggregated the association_





URI: [biolink:aggregator_knowledge_source](https://w3id.org/biolink/vocab/aggregator_knowledge_source)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ParserConfiguration](ParserConfiguration.md) | Settings that determine behavior when parsing associations |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | biolink:aggregator_knowledge_source |
| native | ontoassoc:aggregator_knowledge_source |




## LinkML Source

<details>
```yaml
name: aggregator_knowledge_source
description: The knowledge source that aggregated the association
from_schema: https://w3id.org/oak/association
rank: 1000
slot_uri: biolink:aggregator_knowledge_source
alias: aggregator_knowledge_source
domain_of:
- PositiveOrNegativeAssociation
- ParserConfiguration
- AssociationChange
range: uriorcurie

```
</details>