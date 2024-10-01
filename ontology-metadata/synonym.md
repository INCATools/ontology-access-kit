

# Slot: synonym


* __NOTE__: this is an abstract slot and should not be populated directly


URI: [OIO:hasSynonym](http://www.geneontology.org/formats/oboInOwl#hasSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * **synonym**
        * [has_exact_synonym](has_exact_synonym.md)
        * [has_narrow_synonym](has_narrow_synonym.md)
        * [has_broad_synonym](has_broad_synonym.md)









## Properties

* Range: [LabelType](LabelType.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | OIO:hasSynonym |
| native | omoschema:synonym |




## LinkML Source

<details>
```yaml
name: synonym
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: alternative_term
abstract: true
slot_uri: OIO:hasSynonym
alias: synonym
range: label type
multivalued: true

```
</details>