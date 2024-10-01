

# Slot: diff_slot


_A mixin for any paired slot that pertains to an association diff_





URI: [ontoassoc:diff_slot](https://w3id.org/oak/association/diff_slot)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [old_date](old_date.md) | The date of the old association | None | AssociationChange |
| [new_date](new_date.md) | The date of the new association | None | AssociationChange |
| [publication_is_added](publication_is_added.md) | True if the publication was not present in the old association set (and prese... | boolean | AssociationChange |
| [publication_is_deleted](publication_is_deleted.md) | True if the publication is not present in the new association set (and presen... | boolean | AssociationChange |
| [old_predicate](old_predicate.md) | If the association diff is a change in predicate, this is the predicate on th... | None | AssociationChange |
| [new_predicate](new_predicate.md) | If the association diff is a change in predicate, this is the predicate on th... | None | AssociationChange |
| [old_object](old_object.md) | The object (e | None | AssociationChange |
| [new_object](new_object.md) | The object (e | None | AssociationChange |
| [old_object_obsolete](old_object_obsolete.md) | if the object (e | boolean | AssociationChange |
| [is_migration](is_migration.md) | if the object (e | boolean | AssociationChange |
| [is_generalization](is_generalization.md) | True if the association was inferred to become more general (based on closure... | boolean | AssociationChange |
| [is_specialization](is_specialization.md) | True if the association was inferred to become more specific (based on closur... | boolean | AssociationChange |
| [is_creation](is_creation.md) |  | boolean | AssociationChange |
| [is_deletion](is_deletion.md) |  | boolean | AssociationChange |



## Properties

* Range: [String](String.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:diff_slot |
| native | ontoassoc:diff_slot |




## LinkML Source

<details>
```yaml
name: diff_slot
description: A mixin for any paired slot that pertains to an association diff
from_schema: https://w3id.org/oak/association
rank: 1000
mixin: true
alias: diff_slot
range: string

```
</details>