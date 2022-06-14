# Class: Subset
_A collection of terms grouped for some purpose_





URI: [oio:Subset](http://www.geneontology.org/formats/oboInOwl#Subset)




```{mermaid}
 classDiagram
      AnnotationProperty <|-- Subset
      
      Subset : alternative_term
      Subset : broadMatch
      Subset : category
      Subset : closeMatch
      Subset : comment
      Subset : conformsTo
      Subset : consider
      Subset : contributor
      Subset : created
      Subset : created_by
      Subset : creation_date
      Subset : creator
      Subset : curator_note
      Subset : database_cross_reference
      Subset : date
      Subset : definition
      Subset : definition_source
      Subset : depicted_by
      Subset : deprecated
      Subset : domain
      Subset : editor_note
      Subset : editor_preferred_term
      Subset : exactMatch
      Subset : example_of_usage
      Subset : excluded_from_QC_check
      Subset : excluded_subClassOf
      Subset : excluded_synonym
      Subset : has_alternative_id
      Subset : has_broad_synonym
      Subset : has_curation_status
      Subset : has_exact_synonym
      Subset : has_narrow_synonym
      Subset : has_obo_namespace
      Subset : has_obsolescence_reason
      Subset : has_related_synonym
      Subset : id
      Subset : IEDB_alternative_term
      Subset : image
      Subset : imported_from
      Subset : in_subset
      Subset : is_class_level
      Subset : is_metadata_tag
      Subset : ISA_alternative_term
      Subset : isDefinedBy
      Subset : label
      Subset : narrowMatch
      Subset : OBO_foundry_unique_label
      Subset : ontology_term_requester
      Subset : page
      Subset : range
      Subset : seeAlso
      Subset : shorthand
      Subset : should_conform_to
      Subset : term_editor
      Subset : term_replaced_by
      Subset : term_tracker_item
      Subset : type
      

```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ HasSynonyms HasLifeCycle HasProvenance HasMappings HasCategory HasUserInformation HasMinimalMetadata]
            * [Property](Property.md)
                * [AnnotationProperty](AnnotationProperty.md)
                    * **Subset**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [shorthand](shorthand.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [domain](domain.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [range](range.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [is_class_level](is_class_level.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [is_metadata_tag](is_metadata_tag.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [has_exact_synonym](has_exact_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_narrow_synonym](has_narrow_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_broad_synonym](has_broad_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_related_synonym](has_related_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [alternative_term](alternative_term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [ISA_alternative_term](ISA_alternative_term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [IEDB_alternative_term](IEDB_alternative_term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [editor_preferred_term](editor_preferred_term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [deprecated](deprecated.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [has_obsolescence_reason](has_obsolescence_reason.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [term_replaced_by](term_replaced_by.md) | [Any](Any.md) | 0..1 | None  | . |
| [consider](consider.md) | [Any](Any.md) | 0..* | None  | . |
| [has_alternative_id](has_alternative_id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..* | None  | . |
| [excluded_from_QC_check](excluded_from_QC_check.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [excluded_subClassOf](excluded_subClassOf.md) | [Class](Class.md) | 0..* | None  | . |
| [excluded_synonym](excluded_synonym.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [should_conform_to](should_conform_to.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [created_by](created_by.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [creation_date](creation_date.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [contributor](contributor.md) | [Thing](Thing.md) | 0..* | None  | . |
| [creator](creator.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [created](created.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | when the term came into being  | . |
| [date](date.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | when the term was updated  | . |
| [isDefinedBy](isDefinedBy.md) | [Ontology](Ontology.md) | 0..1 | None  | . |
| [editor_note](editor_note.md) | [narrative_text](narrative_text.md) | 0..* | None  | . |
| [term_editor](term_editor.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [definition_source](definition_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [ontology_term_requester](ontology_term_requester.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [imported_from](imported_from.md) | [NamedIndividual](NamedIndividual.md) | 0..* | None  | . |
| [term_tracker_item](term_tracker_item.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [broadMatch](broadMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [closeMatch](closeMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [exactMatch](exactMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [narrowMatch](narrowMatch.md) | [Property](Property.md) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | None  | . |
| [has_obo_namespace](has_obo_namespace.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [category](category.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [in_subset](in_subset.md) | [Subset](Subset.md) | 0..* | Maps an ontology element to a subset it belongs to  | . |
| [conformsTo](conformsTo.md) | [Thing](Thing.md) | 0..* | None  | . |
| [comment](comment.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [seeAlso](seeAlso.md) | [Thing](Thing.md) | 0..* | None  | . |
| [image](image.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [example_of_usage](example_of_usage.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [curator_note](curator_note.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [has_curation_status](has_curation_status.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [depicted_by](depicted_by.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [page](page.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [label](label.md) | [label_type](label_type.md) | 0..1 _recommended_ | None  | . |
| [definition](definition.md) | [narrative_text](narrative_text.md) | 0..* _recommended_ | None  | . |
| [id](id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | this maps to the URI in RDF  | . |
| [type](type.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasCategory](HasCategory.md) | [in_subset](in_subset.md) | range | Subset |
| [Term](Term.md) | [in_subset](in_subset.md) | range | Subset |
| [Class](Class.md) | [in_subset](in_subset.md) | range | Subset |
| [Property](Property.md) | [in_subset](in_subset.md) | range | Subset |
| [AnnotationProperty](AnnotationProperty.md) | [in_subset](in_subset.md) | range | Subset |
| [ObjectProperty](ObjectProperty.md) | [in_subset](in_subset.md) | range | Subset |
| [TransitiveProperty](TransitiveProperty.md) | [in_subset](in_subset.md) | range | Subset |
| [NamedIndividual](NamedIndividual.md) | [in_subset](in_subset.md) | range | Subset |
| [Subset](Subset.md) | [in_subset](in_subset.md) | range | Subset |



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['oio:Subset'] |
| native | ['omoschema:Subset'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Subset
description: A collection of terms grouped for some purpose
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationProperty
class_uri: oio:Subset

```
</details>

### Induced

<details>
```yaml
name: Subset
description: A collection of terms grouped for some purpose
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationProperty
attributes:
  shorthand:
    name: shorthand
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:shorthand
    multivalued: true
    alias: shorthand
    owner: Subset
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
    owner: Subset
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
    owner: Subset
    range: string
  is_class_level:
    name: is_class_level
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_class_level
    alias: is_class_level
    owner: Subset
    range: boolean
  is_metadata_tag:
    name: is_metadata_tag
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_metadata_tag
    alias: is_metadata_tag
    owner: Subset
    range: boolean
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: Subset
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
    owner: Subset
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: Subset
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: Subset
    range: label type
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:altLabel
    slot_uri: IAO:0000118
    multivalued: true
    alias: alternative_term
    owner: Subset
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: Subset
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: Subset
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
    owner: Subset
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
    owner: Subset
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
    is_a: obsoletion_related_property
    slot_uri: owl:deprecated
    alias: deprecated
    owner: Subset
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
    owner: Subset
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
    is_a: obsoletion_related_property
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: Subset
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
    owner: Subset
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
    owner: Subset
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: Subset
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: Subset
    range: Class
  excluded_synonym:
    name: excluded_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:hiddenSynonym
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: Subset
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: should_conform_to
    owner: Subset
    range: Thing
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: creator
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: Subset
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
    owner: Subset
    range: string
  contributor:
    name: contributor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - prov:wasAttributedTo
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: Subset
    range: Thing
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - prov:wasAttributedTo
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: Subset
    range: string
  created:
    name: created
    description: when the term came into being
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:createdOn
    is_a: provenance_property
    slot_uri: dcterms:created
    multivalued: false
    alias: created
    owner: Subset
    range: string
  date:
    name: date
    description: when the term was updated
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:authoredOn
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: Subset
    range: string
  isDefinedBy:
    name: isDefinedBy
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: Subset
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: Subset
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: Subset
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
    owner: Subset
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: Subset
    range: string
  imported_from:
    name: imported_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: Subset
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
    owner: Subset
    range: string
  broadMatch:
    name: broadMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: Subset
    range: Property
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: Subset
    range: Property
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: Subset
    range: Property
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: Subset
    range: Property
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: Subset
    range: CURIELiteral
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: Subset
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: Subset
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: Subset
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: Subset
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
    owner: Subset
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: Subset
    range: Thing
  image:
    name: image
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: Subset
    range: Thing
  example_of_usage:
    name: example_of_usage
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:example
    is_a: informative_property
    slot_uri: IAO:0000112
    multivalued: true
    alias: example_of_usage
    owner: Subset
    range: string
  curator_note:
    name: curator_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: Subset
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: Subset
    range: string
  depicted_by:
    name: depicted_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: Subset
    range: string
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: Subset
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
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: Subset
    range: label type
    recommended: true
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
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: Subset
    range: narrative text
    recommended: true
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: Subset
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
    owner: Subset
    range: uriorcurie
class_uri: oio:Subset

```
</details>