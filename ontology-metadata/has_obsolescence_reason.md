# Slot: has_obsolescence_reason

URI: [http://purl.obolibrary.org/obo/IAO_0000231](http://purl.obolibrary.org/obo/IAO_0000231)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_obsolescence_reason**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None







## Comments

* {'RULE': 'subject must be deprecated'}

## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: has_obsolescence_reason
todos:
- restrict range
comments:
- '{''RULE'': ''subject must be deprecated''}'
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: IAO:0000231
alias: has_obsolescence_reason
domain_of:
- HasLifeCycle
range: string

```
</details>