# Slot: excluded_synonym

URI: [http://purl.obolibrary.org/obo/schema/excluded_synonym](http://purl.obolibrary.org/obo/schema/excluded_synonym)




## Inheritance

* [excluded_axiom](excluded_axiom.md)
    * **excluded_synonym**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: excluded_synonym
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- skos:hiddenSynonym
rank: 1000
is_a: excluded_axiom
multivalued: true
alias: excluded_synonym
domain_of:
- HasLifeCycle
range: string

```
</details>