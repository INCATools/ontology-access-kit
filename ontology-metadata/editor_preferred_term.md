# Slot: editor_preferred_term

URI: [http://purl.obolibrary.org/obo/IAO_0000111](http://purl.obolibrary.org/obo/IAO_0000111)




## Inheritance

* [alternative_term](alternative_term.md)
    * **editor_preferred_term**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: editor_preferred_term
in_subset:
- obi permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: alternative_term
slot_uri: IAO:0000111
multivalued: true
alias: editor_preferred_term
domain_of:
- HasSynonyms
range: string

```
</details>