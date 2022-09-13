# Slot: creation_date

URI: [http://www.geneontology.org/formats/oboInOwl#creation_date](http://www.geneontology.org/formats/oboInOwl#creation_date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **creation_date**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: creation_date
deprecated: proposed obsoleted by OMO group 2022-04-12
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
deprecated_element_has_exact_replacement: created
rank: 1000
is_a: provenance_property
slot_uri: oio:creation_date
multivalued: true
alias: creation_date
domain_of:
- HasProvenance
range: string

```
</details>