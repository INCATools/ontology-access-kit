# Slot: type
_The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID_


URI: [http://www.w3.org/ns/shacl#sourceConstraintComponent](http://www.w3.org/ns/shacl#sourceConstraintComponent)



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
name: type
description: The type of validation result. SHACL validation vocabulary is recommended
  for checks against a datamodel. For principle checks use the corresponding rule
  or principle, e.g. GO RULE ID, OBO Principle ID
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:sourceConstraintComponent
alias: type
domain_of:
- TypeSeverityKeyValue
- ValidationResult
range: uriorcurie
required: true

```
</details>