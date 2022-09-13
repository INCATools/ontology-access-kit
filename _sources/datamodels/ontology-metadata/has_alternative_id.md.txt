# Slot: has_alternative_id
_Relates a live term to a deprecated ID that was merged in_


URI: [http://www.geneontology.org/formats/oboInOwl#hasAlternativeId](http://www.geneontology.org/formats/oboInOwl#hasAlternativeId)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_alternative_id**





## Properties

* Range: [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)
* Multivalued: True







## Comments

* {'RULE': 'object must NOT be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: has_alternative_id
description: Relates a live term to a deprecated ID that was merged in
deprecated: This is deprecated as it is redundant with the inverse replaced_by triple
comments:
- '{''RULE'': ''object must NOT be deprecated''}'
in_subset:
- go permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
see_also:
- https://github.com/owlcs/owlapi/issues/317
rank: 1000
is_a: obsoletion_related_property
domain: NotObsoleteAspect
slot_uri: oio:hasAlternativeId
multivalued: true
alias: has_alternative_id
domain_of:
- HasLifeCycle
range: uriorcurie

```
</details>