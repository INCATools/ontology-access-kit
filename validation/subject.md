# Slot: subject
_The instance which the result is about_


URI: [http://www.w3.org/ns/shacl#focusNode](http://www.w3.org/ns/shacl#focusNode)



<!-- no inheritance hierarchy -->




## Properties

* Range: [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)
* Multivalued: None



* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## LinkML Specification

<details>
```yaml
name: subject
description: The instance which the result is about
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:focusNode
alias: subject
domain_of:
- ValidationResult
range: uriorcurie
required: true

```
</details>