# Class: HasProvenance



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:HasProvenance](http://purl.obolibrary.org/obo/schema/HasProvenance)




## Inheritance

* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasProvenance**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [created_by](created_by.md) | [string](string.md) | 0..1 | None  | . |
| [creation_date](creation_date.md) | [string](string.md) | 0..* | None  | . |
| [contributor](contributor.md) | [Thing](Thing.md) | 0..* | None  | . |
| [creator](creator.md) | [string](string.md) | 0..* | None  | . |
| [editor_note](editor_note.md) | [narrative_text](narrative_text.md) | 0..* | None  | . |
| [term_editor](term_editor.md) | [string](string.md) | 0..* | None  | . |
| [definition_source](definition_source.md) | [string](string.md) | 0..* | None  | . |
| [ontology_term_requester](ontology_term_requester.md) | [string](string.md) | 0..1 | None  | . |
| [date](date.md) | [string](string.md) | 0..* | None  | . |
| [isDefinedBy](isDefinedBy.md) | [Ontology](Ontology.md) | 0..1 | None  | . |
| [imported_from](imported_from.md) | [NamedIndividual](NamedIndividual.md) | 0..* | None  | . |
| [term_tracker_item](term_tracker_item.md) | [string](string.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasProvenance
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
slots:
- created_by
- creation_date
- contributor
- creator
- editor_note
- term_editor
- definition_source
- ontology_term_requester
- date
- isDefinedBy
- imported_from
- term_tracker_item

```
</details>

### Induced

<details>
```yaml
name: HasProvenance
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  created_by:
    name: created_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: HasProvenance
    range: string
  creation_date:
    name: creation_date
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: oio:creation_date
    multivalued: true
    alias: creation_date
    owner: HasProvenance
    range: string
  contributor:
    name: contributor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: HasProvenance
    range: Thing
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: HasProvenance
    range: string
  editor_note:
    name: editor_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: HasProvenance
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: HasProvenance
    range: string
  definition_source:
    name: definition_source
    todos:
    - restrict range
    in_subset:
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000119
    multivalued: true
    alias: definition_source
    owner: HasProvenance
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: HasProvenance
    range: string
  date:
    name: date
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: HasProvenance
    range: string
  isDefinedBy:
    name: isDefinedBy
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: HasProvenance
    range: Ontology
  imported_from:
    name: imported_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: HasProvenance
    range: NamedIndividual
  term_tracker_item:
    name: term_tracker_item
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000233
    multivalued: true
    alias: term_tracker_item
    owner: HasProvenance
    range: string

```
</details>