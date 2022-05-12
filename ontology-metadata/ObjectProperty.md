# Class: ObjectProperty




URI: [owl:ObjectProperty](http://www.w3.org/2002/07/owl#ObjectProperty)




## Inheritance

* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ HasSynonyms HasLifeCycle HasProvenance HasMappings HasCategory HasUserInformation HasMinimalMetadata]
            * [Property](Property.md)
                * **ObjectProperty** [ PropertyExpression]
                    * [TransitiveProperty](TransitiveProperty.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [temporal_interpretation](temporal_interpretation.md) | [NamedIndividual](NamedIndividual.md) | 0..1 | None  | . |
| [is_cyclic](is_cyclic.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [is_transitive](is_transitive.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [shorthand](shorthand.md) | [string](string.md) | 0..* | None  | . |
| [equivalentProperty](equivalentProperty.md) | [Property](Property.md) | 0..* | None  | . |
| [inverseOf](inverseOf.md) | [Property](Property.md) | 0..1 | None  | . |
| [propertyChainAxiom](propertyChainAxiom.md) | [string](string.md) | 0..* | None  | . |
| [disjointWith](disjointWith.md) | [string](string.md) | 0..* | None  | . |
| [domain](domain.md) | [string](string.md) | 0..* | None  | . |
| [range](range.md) | [string](string.md) | 0..* | None  | . |
| [is_class_level](is_class_level.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [is_metadata_tag](is_metadata_tag.md) | [boolean](boolean.md) | 0..1 | None  | . |
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
| [term_replaced_by](term_replaced_by.md) | [Any](Any.md) | 0..1 | None  | . |
| [consider](consider.md) | [Any](Any.md) | 0..* | None  | . |
| [has_alternative_id](has_alternative_id.md) | [uriorcurie](uriorcurie.md) | 0..* | None  | . |
| [excluded_from_QC_check](excluded_from_QC_check.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [excluded_subClassOf](excluded_subClassOf.md) | [Class](Class.md) | 0..* | None  | . |
| [excluded_synonym](excluded_synonym.md) | [string](string.md) | 0..* | None  | . |
| [should_conform_to](should_conform_to.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [created_by](created_by.md) | [string](string.md) | 0..1 | None  | . |
| [creation_date](creation_date.md) | [string](string.md) | 0..* | None  | . |
| [contributor](contributor.md) | [Thing](Thing.md) | 0..* | None  | . |
| [creator](creator.md) | [string](string.md) | 0..* | None  | . |
| [created](created.md) | [string](string.md) | 0..1 | when the term came into being  | . |
| [date](date.md) | [string](string.md) | 0..* | when the term was updated  | . |
| [isDefinedBy](isDefinedBy.md) | [Ontology](Ontology.md) | 0..1 | None  | . |
| [editor_note](editor_note.md) | [narrative_text](narrative_text.md) | 0..* | None  | . |
| [term_editor](term_editor.md) | [string](string.md) | 0..* | None  | . |
| [definition_source](definition_source.md) | [string](string.md) | 0..* | None  | . |
| [ontology_term_requester](ontology_term_requester.md) | [string](string.md) | 0..1 | None  | . |
| [imported_from](imported_from.md) | [NamedIndividual](NamedIndividual.md) | 0..* | None  | . |
| [term_tracker_item](term_tracker_item.md) | [string](string.md) | 0..* | None  | . |
| [broadMatch](broadMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [closeMatch](closeMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [exactMatch](exactMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [narrowMatch](narrowMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | None  | . |
| [has_obo_namespace](has_obo_namespace.md) | [string](string.md) | 0..* | None  | . |
| [category](category.md) | [string](string.md) | 0..1 | None  | . |
| [in_subset](in_subset.md) | [Subset](Subset.md) | 0..* | Maps an ontology element to a subset it belongs to  | . |
| [conformsTo](conformsTo.md) | [Thing](Thing.md) | 0..* | None  | . |
| [comment](comment.md) | [string](string.md) | 0..* | None  | . |
| [seeAlso](seeAlso.md) | [Thing](Thing.md) | 0..* | None  | . |
| [image](image.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [example_of_usage](example_of_usage.md) | [string](string.md) | 0..* | None  | . |
| [curator_note](curator_note.md) | [string](string.md) | 0..* | None  | . |
| [has_curation_status](has_curation_status.md) | [string](string.md) | 0..1 | None  | . |
| [depicted_by](depicted_by.md) | [string](string.md) | 0..* | None  | . |
| [page](page.md) | [string](string.md) | 0..* | None  | . |
| [label](label.md) | [label_type](label_type.md) | 0..1 _recommended_ | None  | . |
| [definition](definition.md) | [narrative_text](narrative_text.md) | 0..* _recommended_ | None  | . |
| [id](id.md) | [uriorcurie](uriorcurie.md) | 1..1 | this maps to the URI in RDF  | . |
| [type](type.md) | [uriorcurie](uriorcurie.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ObjectProperty
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Property
mixins:
- PropertyExpression
slots:
- temporal_interpretation
- is_cyclic
- is_transitive
- shorthand
- equivalentProperty
- inverseOf
- propertyChainAxiom
class_uri: owl:ObjectProperty

```
</details>

### Induced

<details>
```yaml
name: ObjectProperty
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Property
mixins:
- PropertyExpression
attributes:
  temporal_interpretation:
    name: temporal_interpretation
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: RO:0001900
    alias: temporal_interpretation
    owner: ObjectProperty
    range: NamedIndividual
  is_cyclic:
    name: is_cyclic
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_cyclic
    alias: is_cyclic
    owner: ObjectProperty
    range: boolean
  is_transitive:
    name: is_transitive
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: TransitiveProperty
    slot_uri: oio:is_transitive
    alias: is_transitive
    owner: ObjectProperty
    range: boolean
  shorthand:
    name: shorthand
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:shorthand
    multivalued: true
    alias: shorthand
    owner: ObjectProperty
    range: string
  equivalentProperty:
    name: equivalentProperty
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentProperty
    multivalued: true
    alias: equivalentProperty
    owner: ObjectProperty
    range: Property
  inverseOf:
    name: inverseOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:inverseOf
    alias: inverseOf
    owner: ObjectProperty
    range: Property
  propertyChainAxiom:
    name: propertyChainAxiom
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:propertyChainAxiom
    multivalued: true
    alias: propertyChainAxiom
    owner: ObjectProperty
    range: string
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: ObjectProperty
    range: string
  domain:
    name: domain
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdfs:domain
    multivalued: true
    alias: domain
    owner: ObjectProperty
    range: string
  range:
    name: range
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdfs:range
    multivalued: true
    alias: range
    owner: ObjectProperty
    range: string
  is_class_level:
    name: is_class_level
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_class_level
    alias: is_class_level
    owner: ObjectProperty
    range: boolean
  is_metadata_tag:
    name: is_metadata_tag
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_metadata_tag
    alias: is_metadata_tag
    owner: ObjectProperty
    range: boolean
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: ObjectProperty
    disjoint_with:
    - label
    range: label type
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    multivalued: true
    alias: has_narrow_synonym
    owner: ObjectProperty
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: ObjectProperty
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: ObjectProperty
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: Any
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
    owner: ObjectProperty
    range: Any
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
    owner: ObjectProperty
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: ObjectProperty
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: ObjectProperty
    range: Class
  excluded_synonym:
    name: excluded_synonym
    exact_mappings:
    - skos:hiddenSynonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: ObjectProperty
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: should_conform_to
    owner: ObjectProperty
    range: Thing
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: creator
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: ObjectProperty
    range: string
  creation_date:
    name: creation_date
    deprecated: proposed obsoleted by OMO group 2022-04-12
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: created
    is_a: provenance_property
    slot_uri: oio:creation_date
    multivalued: true
    alias: creation_date
    owner: ObjectProperty
    range: string
  contributor:
    name: contributor
    close_mappings:
    - prov:wasAttributedTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: ObjectProperty
    range: Thing
  creator:
    name: creator
    close_mappings:
    - prov:wasAttributedTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: ObjectProperty
    range: string
  created:
    name: created
    close_mappings:
    - pav:createdOn
    description: when the term came into being
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:created
    multivalued: false
    alias: created
    owner: ObjectProperty
    range: string
  date:
    name: date
    close_mappings:
    - pav:authoredOn
    description: when the term was updated
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: ObjectProperty
    range: string
  isDefinedBy:
    name: isDefinedBy
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: ObjectProperty
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: ObjectProperty
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: ObjectProperty
    range: string
  imported_from:
    name: imported_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: string
  broadMatch:
    name: broadMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: ObjectProperty
    range: Property
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: ObjectProperty
    range: Property
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: ObjectProperty
    range: Property
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: ObjectProperty
    range: Property
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: ObjectProperty
    range: CURIELiteral
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: ObjectProperty
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: ObjectProperty
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: ObjectProperty
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: ObjectProperty
    range: Thing
  image:
    name: image
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: ObjectProperty
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
    owner: ObjectProperty
    range: string
  curator_note:
    name: curator_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: ObjectProperty
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: ObjectProperty
    range: string
  depicted_by:
    name: depicted_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: ObjectProperty
    range: string
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: ObjectProperty
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
    multivalued: false
    alias: label
    owner: ObjectProperty
    range: label type
    recommended: true
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
    owner: ObjectProperty
    range: narrative text
    recommended: true
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: ObjectProperty
    range: uriorcurie
    required: true
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    designates_type: true
    alias: type
    owner: ObjectProperty
    range: uriorcurie
class_uri: owl:ObjectProperty

```
</details>