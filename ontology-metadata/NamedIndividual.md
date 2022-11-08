# Class: NamedIndividual
_An instance that has a IRI_




URI: [owl:NamedIndividual](http://www.w3.org/2002/07/owl#NamedIndividual)


```{mermaid}
 classDiagram
    class NamedIndividual
      Term <|-- NamedIndividual
      
      NamedIndividual : alternative_term
      NamedIndividual : broadMatch
      NamedIndividual : category
      NamedIndividual : closeMatch
      NamedIndividual : comment
      NamedIndividual : conformsTo
      NamedIndividual : consider
      NamedIndividual : contributor
      NamedIndividual : created
      NamedIndividual : created_by
      NamedIndividual : creation_date
      NamedIndividual : creator
      NamedIndividual : curator_note
      NamedIndividual : database_cross_reference
      NamedIndividual : date
      NamedIndividual : definition
      NamedIndividual : definition_source
      NamedIndividual : depicted_by
      NamedIndividual : deprecated
      NamedIndividual : editor_note
      NamedIndividual : editor_preferred_term
      NamedIndividual : exactMatch
      NamedIndividual : example_of_usage
      NamedIndividual : excluded_from_QC_check
      NamedIndividual : excluded_subClassOf
      NamedIndividual : excluded_synonym
      NamedIndividual : has_alternative_id
      NamedIndividual : has_broad_synonym
      NamedIndividual : has_curation_status
      NamedIndividual : has_exact_synonym
      NamedIndividual : has_narrow_synonym
      NamedIndividual : has_obo_namespace
      NamedIndividual : has_obsolescence_reason
      NamedIndividual : has_related_synonym
      NamedIndividual : id
      NamedIndividual : IEDB_alternative_term
      NamedIndividual : image
      NamedIndividual : imported_from
      NamedIndividual : in_subset
      NamedIndividual : ISA_alternative_term
      NamedIndividual : isDefinedBy
      NamedIndividual : label
      NamedIndividual : narrowMatch
      NamedIndividual : OBO_foundry_unique_label
      NamedIndividual : ontology_term_requester
      NamedIndividual : page
      NamedIndividual : seeAlso
      NamedIndividual : should_conform_to
      NamedIndividual : term_editor
      NamedIndividual : term_replaced_by
      NamedIndividual : term_tracker_item
      NamedIndividual : type
      
```




## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * **NamedIndividual**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- || [has_related_synonym](has_related_synonym.md) | 0..* <br/> label type | None | [HasSynonyms](HasSynonyms.md) |
| [broadMatch](broadMatch.md) | 0..* <br/> Thing | None | [HasMappings](HasMappings.md) |
| [alternative_term](alternative_term.md) | 0..* <br/> None | None | [HasSynonyms](HasSynonyms.md) |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | 0..1 <br/> None | None | [HasSynonyms](HasSynonyms.md) |
| [conformsTo](conformsTo.md) | 0..* <br/> Thing | None | [HasCategory](HasCategory.md) |
| [in_subset](in_subset.md) | 0..* <br/> Subset | Maps an ontology element to a subset it belongs to | [HasCategory](HasCategory.md) |
| [has_broad_synonym](has_broad_synonym.md) | 0..* <br/> label type | None | [HasSynonyms](HasSynonyms.md) |
| [should_conform_to](should_conform_to.md) | 0..1 <br/> Thing | None | [HasLifeCycle](HasLifeCycle.md) |
| [id](id.md) | 1..1 <br/> uriorcurie | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [has_exact_synonym](has_exact_synonym.md) | 0..* <br/> label type | None | [HasSynonyms](HasSynonyms.md) |
| [excluded_from_QC_check](excluded_from_QC_check.md) | 0..1 <br/> Thing | None | [HasLifeCycle](HasLifeCycle.md) |
| [consider](consider.md) | 0..* <br/> Any | None | [HasLifeCycle](HasLifeCycle.md) |
| [term_editor](term_editor.md) | 0..* <br/> None | None | [HasProvenance](HasProvenance.md) |
| [imported_from](imported_from.md) | 0..* <br/> NamedIndividual | None | [HasProvenance](HasProvenance.md) |
| [term_tracker_item](term_tracker_item.md) | 0..* <br/> None | None | [HasProvenance](HasProvenance.md) |
| [comment](comment.md) | 0..* <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [definition_source](definition_source.md) | 0..* <br/> None | None | [HasProvenance](HasProvenance.md) |
| [created](created.md) | 0..1 <br/> None | when the term came into being | [HasProvenance](HasProvenance.md) |
| [isDefinedBy](isDefinedBy.md) | 0..1 <br/> Ontology | None | [HasProvenance](HasProvenance.md) |
| [exactMatch](exactMatch.md) | 0..* <br/> Thing | None | [HasMappings](HasMappings.md) |
| [contributor](contributor.md) | 0..* <br/> Thing | None | [HasProvenance](HasProvenance.md) |
| [database_cross_reference](database_cross_reference.md) | 0..* <br/> CURIELiteral | None | [HasMappings](HasMappings.md) |
| [created_by](created_by.md) | 0..1 <br/> None | None | [HasProvenance](HasProvenance.md) |
| [deprecated](deprecated.md) | 0..1 <br/> boolean | None | [HasLifeCycle](HasLifeCycle.md) |
| [editor_preferred_term](editor_preferred_term.md) | 0..* <br/> None | None | [HasSynonyms](HasSynonyms.md) |
| [IEDB_alternative_term](IEDB_alternative_term.md) | 0..1 <br/> None | None | [HasSynonyms](HasSynonyms.md) |
| [ontology_term_requester](ontology_term_requester.md) | 0..1 <br/> None | None | [HasProvenance](HasProvenance.md) |
| [term_replaced_by](term_replaced_by.md) | 0..1 <br/> Any | None | [HasLifeCycle](HasLifeCycle.md) |
| [has_narrow_synonym](has_narrow_synonym.md) | 0..* <br/> label type | None | [HasSynonyms](HasSynonyms.md) |
| [definition](definition.md) | 0..* <br/> narrative text | None | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [category](category.md) | 0..1 <br/> None | None | [HasCategory](HasCategory.md) |
| [has_obsolescence_reason](has_obsolescence_reason.md) | 0..1 <br/> None | None | [HasLifeCycle](HasLifeCycle.md) |
| [creation_date](creation_date.md) | 0..* <br/> None | None | [HasProvenance](HasProvenance.md) |
| [seeAlso](seeAlso.md) | 0..* <br/> Thing | None | [HasUserInformation](HasUserInformation.md) |
| [page](page.md) | 0..* <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [date](date.md) | 0..* <br/> None | when the term was updated | [HasProvenance](HasProvenance.md) |
| [type](type.md) | 0..* <br/> uriorcurie | None | [Thing](Thing.md) |
| [excluded_subClassOf](excluded_subClassOf.md) | 0..* <br/> Class | None | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_synonym](excluded_synonym.md) | 0..* <br/> None | None | [HasLifeCycle](HasLifeCycle.md) |
| [has_obo_namespace](has_obo_namespace.md) | 0..* <br/> None | None | [HasCategory](HasCategory.md) |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [label](label.md) | 0..1 <br/> label type | None | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [ISA_alternative_term](ISA_alternative_term.md) | 0..1 <br/> None | None | [HasSynonyms](HasSynonyms.md) |
| [curator_note](curator_note.md) | 0..* <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [creator](creator.md) | 0..* <br/> None | None | [HasProvenance](HasProvenance.md) |
| [depicted_by](depicted_by.md) | 0..* <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [example_of_usage](example_of_usage.md) | 0..* <br/> None | None | [HasUserInformation](HasUserInformation.md) |
| [image](image.md) | 0..1 <br/> Thing | None | [HasUserInformation](HasUserInformation.md) |
| [closeMatch](closeMatch.md) | 0..* <br/> Thing | None | [HasMappings](HasMappings.md) |
| [has_alternative_id](has_alternative_id.md) | 0..* <br/> uriorcurie | Relates a live term to a deprecated ID that was merged in | [HasLifeCycle](HasLifeCycle.md) |
| [editor_note](editor_note.md) | 0..* <br/> narrative text | None | [HasProvenance](HasProvenance.md) |
| [narrowMatch](narrowMatch.md) | 0..* <br/> Thing | None | [HasMappings](HasMappings.md) |



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







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:NamedIndividual |
| native | omoschema:NamedIndividual |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedIndividual
description: An instance that has a IRI
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Term
class_uri: owl:NamedIndividual

```
</details>

### Induced

<details>
```yaml
name: NamedIndividual
description: An instance that has a IRI
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Term
attributes:
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    multivalued: true
    alias: has_narrow_synonym
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: label type
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:altLabel
    rank: 1000
    slot_uri: IAO:0000118
    multivalued: true
    alias: alternative_term
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: string
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000111
    multivalued: true
    alias: editor_preferred_term
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: string
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000589
    multivalued: true
    alias: OBO_foundry_unique_label
    owner: NamedIndividual
    domain_of:
    - HasSynonyms
    range: string
  deprecated:
    name: deprecated
    in_subset:
    - allotrope permitted profile
    - go permitted profile
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    aliases:
    - is obsolete
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: owl:deprecated
    alias: deprecated
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: boolean
  has_obsolescence_reason:
    name: has_obsolescence_reason
    todos:
    - restrict range
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0000231
    alias: has_obsolescence_reason
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: string
  term_replaced_by:
    name: term_replaced_by
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    - obi permitted profile
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - dcterms:isReplacedBy
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: Any
  consider:
    name: consider
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: oio:consider
    multivalued: true
    alias: consider
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: Any
  has_alternative_id:
    name: has_alternative_id
    description: Relates a live term to a deprecated ID that was merged in
    deprecated: This is deprecated as it is redundant with the inverse replaced_by
      triple
    comments:
    - '{''RULE'': ''object must NOT be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    see_also:
    - https://github.com/owlcs/owlapi/issues/317
    rank: 1000
    is_a: obsoletion_related_property
    domain: NotObsoleteAspect
    slot_uri: oio:hasAlternativeId
    multivalued: true
    alias: has_alternative_id
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: Class
  excluded_synonym:
    name: excluded_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:hiddenSynonym
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: NamedIndividual
    domain_of:
    - HasLifeCycle
    range: Thing
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: creator
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    - Axiom
    range: string
  creation_date:
    name: creation_date
    deprecated: proposed obsoleted by OMO group 2022-04-12
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: created
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:creation_date
    multivalued: true
    alias: creation_date
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  contributor:
    name: contributor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: Thing
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    - Ontology
    range: string
  created:
    name: created
    description: when the term came into being
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:createdOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:created
    multivalued: false
    alias: created
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    - Ontology
    range: string
  date:
    name: date
    description: when the term was updated
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:authoredOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  isDefinedBy:
    name: isDefinedBy
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    rank: 1000
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  definition_source:
    name: definition_source
    todos:
    - restrict range
    in_subset:
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000119
    multivalued: true
    alias: definition_source
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  imported_from:
    name: imported_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: NamedIndividual
  term_tracker_item:
    name: term_tracker_item
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000233
    multivalued: true
    alias: term_tracker_item
    owner: NamedIndividual
    domain_of:
    - HasProvenance
    range: string
  broadMatch:
    name: broadMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: NamedIndividual
    domain_of:
    - HasMappings
    range: Thing
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: NamedIndividual
    domain_of:
    - HasMappings
    range: Thing
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: NamedIndividual
    domain_of:
    - HasMappings
    range: Thing
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: NamedIndividual
    domain_of:
    - HasMappings
    range: Thing
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: NamedIndividual
    domain_of:
    - HasMappings
    - Axiom
    range: CURIELiteral
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: NamedIndividual
    domain_of:
    - HasCategory
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: NamedIndividual
    domain_of:
    - HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: NamedIndividual
    domain_of:
    - HasCategory
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: NamedIndividual
    domain_of:
    - HasCategory
    range: Thing
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
  image:
    name: image
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: Thing
  example_of_usage:
    name: example_of_usage
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:example
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000112
    multivalued: true
    alias: example_of_usage
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: string
  curator_note:
    name: curator_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: string
  depicted_by:
    name: depicted_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: string
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: NamedIndividual
    domain_of:
    - HasUserInformation
    range: string
  label:
    name: label
    comments:
    - SHOULD follow OBO label guidelines
    - MUST be unique within an ontology
    - SHOULD be unique across OBO
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: NamedIndividual
    domain_of:
    - HasMinimalMetadata
    - Axiom
    range: label type
  definition:
    name: definition
    comments:
    - SHOULD be in Aristotelian (genus-differentia) form
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:definition
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: NamedIndividual
    domain_of:
    - HasMinimalMetadata
    range: narrative text
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: NamedIndividual
    domain_of:
    - NamedObject
    range: uriorcurie
    required: true
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    designates_type: true
    alias: type
    owner: NamedIndividual
    domain_of:
    - Thing
    range: uriorcurie
class_uri: owl:NamedIndividual

```
</details>