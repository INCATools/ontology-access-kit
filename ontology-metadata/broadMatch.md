

# Slot: broadMatch

URI: [skos:broadMatch](http://www.w3.org/2004/02/skos/core#broadMatch)




## Inheritance

* [match](match.md) [ [match_aspect](match_aspect.md)]
    * **broadMatch**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Property](Property.md) |  |  yes  |
| [HasMappings](HasMappings.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Class](Class.md) |  |  yes  |
| [Image](Image.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: broadMatch
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: match
slot_uri: skos:broadMatch
multivalued: true
alias: broadMatch
domain_of:
- HasMappings
range: Thing

```
</details>