# Slot: severity
_the severity of the issue_


URI: [http://www.w3.org/ns/shacl#resultSeverity](http://www.w3.org/ns/shacl#resultSeverity)



<!-- no inheritance hierarchy -->




## Properties

* Range: [SeverityOptions](SeverityOptions.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## LinkML Specification

<details>
```yaml
name: severity
description: the severity of the issue
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:resultSeverity
alias: severity
domain_of:
- TypeSeverityKeyValue
- ValidationResult
range: severity_options

```
</details>