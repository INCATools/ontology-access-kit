# Slot: definition

URI: [http://purl.obolibrary.org/obo/IAO_0000115](http://purl.obolibrary.org/obo/IAO_0000115)




## Inheritance

* [core_property](core_property.md)
    * **definition**





## Properties

* Range: [NarrativeText](NarrativeText.md)
* Multivalued: True







## Comments

* SHOULD be in Aristotelian (genus-differentia) form

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: definition
comments:
- SHOULD be in Aristotelian (genus-differentia) form
in_subset:
- allotrope required profile
- go required profile
- obi required profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- skos:definition
rank: 1000
is_a: core_property
slot_uri: IAO:0000115
multivalued: true
alias: definition
domain_of:
- HasMinimalMetadata
range: narrative text

```
</details>