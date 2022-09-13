# Slot: comment

URI: [http://www.w3.org/2000/01/rdf-schema#comment](http://www.w3.org/2000/01/rdf-schema#comment)




## Inheritance

* [informative_property](informative_property.md)
    * **comment**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Comments

* in obo format, a term cannot have more than one comment

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: comment
comments:
- in obo format, a term cannot have more than one comment
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: informative_property
slot_uri: rdfs:comment
multivalued: true
alias: comment
domain_of:
- HasUserInformation
- Ontology
- Axiom
range: string

```
</details>