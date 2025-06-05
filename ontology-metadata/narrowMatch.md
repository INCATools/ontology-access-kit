

# Slot: narrowMatch



URI: [skos:narrowMatch](http://www.w3.org/2004/02/skos/core#narrowMatch)




## Inheritance

* [match](match.md) [ [match_aspect](match_aspect.md)]
    * **narrowMatch**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Property](Property.md) |  |  yes  |
| [HasMappings](HasMappings.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Class](Class.md) |  |  yes  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | skos:narrowMatch |
| native | omoschema:narrowMatch |




## LinkML Source

<details>
```yaml
name: narrowMatch
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: match
slot_uri: skos:narrowMatch
alias: narrowMatch
domain_of:
- HasMappings
range: Thing
multivalued: true

```
</details>