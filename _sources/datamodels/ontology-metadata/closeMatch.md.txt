

# Slot: closeMatch

URI: [skos:closeMatch](http://www.w3.org/2004/02/skos/core#closeMatch)




## Inheritance

* [match](match.md) [ [match_aspect](match_aspect.md)]
    * **closeMatch**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Class](Class.md) |  |  yes  |
| [Image](Image.md) |  |  no  |
| [HasMappings](HasMappings.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Property](Property.md) |  |  yes  |
| [Agent](Agent.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: closeMatch
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: match
slot_uri: skos:closeMatch
multivalued: true
alias: closeMatch
domain_of:
- HasMappings
range: Thing

```
</details>