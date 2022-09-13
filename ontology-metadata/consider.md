# Slot: consider

URI: [http://www.geneontology.org/formats/oboInOwl#consider](http://www.geneontology.org/formats/oboInOwl#consider)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **consider**





## Properties

* Range: [Any](Any.md)
* Multivalued: True







## Comments

* {'RULE': 'subject must be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: consider
comments:
- '{''RULE'': ''subject must be deprecated''}'
in_subset:
- go permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: oio:consider
multivalued: true
alias: consider
domain_of:
- HasLifeCycle
range: Any

```
</details>