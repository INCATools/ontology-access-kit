

# Slot: versionInfo



URI: [owl:versionInfo](http://www.w3.org/2002/07/owl#versionInfo)




## Inheritance

* [version_property](version_property.md)
    * **versionInfo**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Ontology](Ontology.md) | An OWL ontology |  yes  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:versionInfo |
| native | omoschema:versionInfo |
| close | pav:version |




## LinkML Source

<details>
```yaml
name: versionInfo
from_schema: https://w3id.org/oak/ontology-metadata
close_mappings:
- pav:version
rank: 1000
is_a: version_property
slot_uri: owl:versionInfo
alias: versionInfo
domain_of:
- Ontology
range: string

```
</details>