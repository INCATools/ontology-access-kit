

# Slot: object_match_field_one_of


_The field in the object to be matched. Multiple values can be provided, it must match at least one._





URI: [mappingrules:object_match_field_one_of](https://w3id.org/oak/mapping-rules-datamodel/object_match_field_one_of)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:object_match_field_one_of |
| native | mappingrules:object_match_field_one_of |




## LinkML Source

<details>
```yaml
name: object_match_field_one_of
description: The field in the object to be matched. Multiple values can be provided,
  it must match at least one.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
alias: object_match_field_one_of
owner: Precondition
domain_of:
- Precondition
range: string
multivalued: true

```
</details>