# Slot: has_exact_synonym

URI: [http://www.geneontology.org/formats/oboInOwl#hasExactSynonym](http://www.geneontology.org/formats/oboInOwl#hasExactSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * [synonym](synonym.md)
        * **has_exact_synonym**





## Properties

* Range: [LabelType](LabelType.md)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: has_exact_synonym
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: synonym
slot_uri: oio:hasExactSynonym
multivalued: true
alias: has_exact_synonym
domain_of:
- HasSynonyms
- Axiom
disjoint_with:
- label
range: label type

```
</details>