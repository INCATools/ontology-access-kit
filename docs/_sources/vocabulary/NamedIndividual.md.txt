# Class: NamedIndividual




URI: [owl:NamedIndividual](http://www.w3.org/2002/07/owl#NamedIndividual)




## Inheritance

* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ HasSynonyms HasLifeCycle HasProvenance HasMappings HasCategory HasUserInformation HasMinimalMetadata]
            * **NamedIndividual**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [ClassExpression](ClassExpression.md) | 0..* | None  | . |
| [has_exact_synonym](has_exact_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_narrow_synonym](has_narrow_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_broad_synonym](has_broad_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_related_synonym](has_related_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [alternative_term](alternative_term.md) | [string](string.md) | 0..* | None  | . |
| [ISA_alternative_term](ISA_alternative_term.md) | [string](string.md) | 0..* | None  | . |
| [IEDB_alternative_term](IEDB_alternative_term.md) | [string](string.md) | 0..* | None  | . |
| [editor_preferred_term](editor_preferred_term.md) | [string](string.md) | 0..* | None  | . |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | [string](string.md) | 0..* | None  | . |
| [deprecated](deprecated.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [has_obsolescence_reason](has_obsolescence_reason.md) | [string](string.md) | 0..1 | None  | . |
| [term_replaced_by](term_replaced_by.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [consider](consider.md) | [string](string.md) | 0..* | None  | . |
| [has_alternative_id](has_alternative_id.md) | [uriorcurie](uriorcurie.md) | 0..* | None  | . |
| [excluded_from_QC_check](excluded_from_QC_check.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [excluded_subClassOf](excluded_subClassOf.md) | [Class](Class.md) | 0..* | None  | . |
| [excluded_synonym](excluded_synonym.md) | [string](string.md) | 0..* | None  | . |
| [should_conform_to](should_conform_to.md) | [Thing](Thing.md) | 0..1 | None  | . |
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
| [broadMatch](broadMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [closeMatch](closeMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [exactMatch](exactMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [narrowMatch](narrowMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | None  | . |
| [has_obo_namespace](has_obo_namespace.md) | [string](string.md) | 0..* | None  | . |
| [category](category.md) | [string](string.md) | 0..1 | None  | . |
| [in_subset](in_subset.md) | [Subset](Subset.md) | 0..* | Maps an ontology element to a subset it belongs to  | . |
| [conformsTo](conformsTo.md) | [Thing](Thing.md) | 0..* | None  | . |
| [comment](comment.md) | [string](string.md) | 0..* | None  | . |
| [seeAlso](seeAlso.md) | [string](string.md) | 0..* | None  | . |
| [image](image.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [example_of_usage](example_of_usage.md) | [string](string.md) | 0..* | None  | . |
| [curator_note](curator_note.md) | [string](string.md) | 0..* | None  | . |
| [has_curation_status](has_curation_status.md) | [string](string.md) | 0..1 | None  | . |
| [depicted_by](depicted_by.md) | [string](string.md) | 0..* | None  | . |
| [page](page.md) | [string](string.md) | 0..* | None  | . |
| [label](label.md) | [label_type](label_type.md) | 0..* | None  | . |
| [definition](definition.md) | [narrative_text](narrative_text.md) | 0..* | None  | . |
| [id](id.md) | [uriorcurie](uriorcurie.md) | 1..1 | this maps to the URI in RDF  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasProvenance](HasProvenance.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [Term](Term.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [Class](Class.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [Property](Property.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [AnnotationProperty](AnnotationProperty.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [ObjectProperty](ObjectProperty.md) | [temporal_interpretation](temporal_interpretation.md) | range | NamedIndividual |
| [ObjectProperty](ObjectProperty.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [TransitiveProperty](TransitiveProperty.md) | [temporal_interpretation](temporal_interpretation.md) | range | NamedIndividual |
| [TransitiveProperty](TransitiveProperty.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [NamedIndividual](NamedIndividual.md) | [imported_from](imported_from.md) | range | NamedIndividual |
| [Subset](Subset.md) | [imported_from](imported_from.md) | range | NamedIndividual |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedIndividual
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Term
slots:
- type
class_uri: owl:NamedIndividual

```
</details>

### Induced

<details>
```yaml
name: NamedIndividual
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Term
attributes:
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    alias: type
    owner: NamedIndividual
    range: ClassExpression
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: NamedIndividual
    range: label type
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    multivalued: true
    alias: has_narrow_synonym
    owner: NamedIndividual
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: NamedIndividual
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: NamedIndividual
    range: label type
  alternative_term:
    name: alternative_term
    exact_mappings:
    - skos:altLabel
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: IAO:0000118
    multivalued: true
    alias: alternative_term
    owner: NamedIndividual
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: NamedIndividual
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: NamedIndividual
    range: string
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: IAO:0000111
    multivalued: true
    alias: editor_preferred_term
    owner: NamedIndividual
    range: string
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: IAO:0000589
    multivalued: true
    alias: OBO_foundry_unique_label
    owner: NamedIndividual
    range: string
  deprecated:
    name: deprecated
    aliases:
    - is obsolete
    in_subset:
    - allotrope permitted profile
    - go permitted profile
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    slot_uri: owl:deprecated
    alias: deprecated
    owner: NamedIndividual
    range: boolean
  has_obsolescence_reason:
    name: has_obsolescence_reason
    todos:
    - restrict range
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    slot_uri: IAO:0000231
    alias: has_obsolescence_reason
    owner: NamedIndividual
    range: string
  term_replaced_by:
    name: term_replaced_by
    exact_mappings:
    - dcterms:isReplacedBy
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    - obi permitted profile
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: NamedIndividual
    range: Thing
  consider:
    name: consider
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    slot_uri: oio:consider
    multivalued: true
    alias: consider
    owner: NamedIndividual
    range: string
  has_alternative_id:
    name: has_alternative_id
    comments:
    - '{''RULE'': ''object must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    slot_uri: oio:hasAlternativeId
    multivalued: true
    alias: has_alternative_id
    owner: NamedIndividual
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: NamedIndividual
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: NamedIndividual
    range: Class
  excluded_synonym:
    name: excluded_synonym
    exact_mappings:
    - skos:hiddenSynonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: NamedIndividual
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: should_conform_to
    owner: NamedIndividual
    range: Thing
  created_by:
    name: created_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: NamedIndividual
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
    owner: NamedIndividual
    range: string
  contributor:
    name: contributor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: NamedIndividual
    range: Thing
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: NamedIndividual
    range: string
  editor_note:
    name: editor_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: NamedIndividual
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: NamedIndividual
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
    owner: NamedIndividual
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: NamedIndividual
    range: string
  date:
    name: date
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: NamedIndividual
    range: string
  isDefinedBy:
    name: isDefinedBy
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: NamedIndividual
    range: Ontology
  imported_from:
    name: imported_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: NamedIndividual
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
    owner: NamedIndividual
    range: string
  broadMatch:
    name: broadMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: NamedIndividual
    range: Thing
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: NamedIndividual
    range: Thing
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: NamedIndividual
    range: Thing
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: NamedIndividual
    range: Thing
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: NamedIndividual
    range: CURIELiteral
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: NamedIndividual
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: NamedIndividual
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: NamedIndividual
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: NamedIndividual
    range: Thing
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: NamedIndividual
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: NamedIndividual
    range: string
  image:
    name: image
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: NamedIndividual
    range: Thing
  example_of_usage:
    name: example_of_usage
    exact_mappings:
    - skos:example
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: IAO:0000112
    multivalued: true
    alias: example_of_usage
    owner: NamedIndividual
    range: string
  curator_note:
    name: curator_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: NamedIndividual
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: NamedIndividual
    range: string
  depicted_by:
    name: depicted_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: NamedIndividual
    range: string
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: NamedIndividual
    range: string
  label:
    name: label
    exact_mappings:
    - skos:prefLabel
    comments:
    - SHOULD follow OBO label guidelines
    - MUST be unique within an ontology
    - SHOULD be unique across OBO
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: true
    alias: label
    owner: NamedIndividual
    range: label type
  definition:
    name: definition
    exact_mappings:
    - skos:definition
    comments:
    - SHOULD be in Aristotelian (genus-differentia) form
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: NamedIndividual
    range: narrative text
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: NamedIndividual
    range: uriorcurie
    required: true
class_uri: owl:NamedIndividual

```
</details>