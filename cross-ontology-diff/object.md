# Slot: object

URI: [http://www.w3.org/1999/02/22-rdf-syntax-ns#object](http://www.w3.org/1999/02/22-rdf-syntax-ns#object)



<!-- no inheritance hierarchy -->



## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_object_id](left_object_id.md) | The object (parent) of the source/left edge | EntityReference |  |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge | Label |  |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable | EntityReference |  |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable | Label |  |



## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None




* Mixin: True




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: object
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixin: true
slot_uri: rdf:object
alias: object
range: string

```
</details>