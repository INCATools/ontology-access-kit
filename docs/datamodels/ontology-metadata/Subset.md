

# Class: Subset


_A collection of terms grouped for some purpose_





URI: [oio:Subset](http://www.geneontology.org/formats/oboInOwl#Subset)






```{mermaid}
 classDiagram
    class Subset
    click Subset href "../Subset"
      AnnotationProperty <|-- Subset
        click AnnotationProperty href "../AnnotationProperty"
      
      Subset : alternative_term
        
      Subset : broadMatch
        
          
    
    
    Subset --> "*" Property : broadMatch
    click Property href "../Property"

        
      Subset : category
        
      Subset : closeMatch
        
          
    
    
    Subset --> "*" Property : closeMatch
    click Property href "../Property"

        
      Subset : comment
        
      Subset : conformsTo
        
          
    
    
    Subset --> "*" Thing : conformsTo
    click Thing href "../Thing"

        
      Subset : consider
        
          
    
    
    Subset --> "*" Any : consider
    click Any href "../Any"

        
      Subset : contributor
        
          
    
    
    Subset --> "*" Agent : contributor
    click Agent href "../Agent"

        
      Subset : created
        
      Subset : created_by
        
      Subset : creation_date
        
      Subset : creator
        
          
    
    
    Subset --> "*" Agent : creator
    click Agent href "../Agent"

        
      Subset : curator_note
        
      Subset : database_cross_reference
        
      Subset : date
        
      Subset : definition
        
      Subset : definition_source
        
      Subset : depicted_by
        
          
    
    
    Subset --> "*" Image : depicted_by
    click Image href "../Image"

        
      Subset : deprecated
        
      Subset : domain
        
      Subset : editor_note
        
      Subset : editor_preferred_term
        
      Subset : exactMatch
        
          
    
    
    Subset --> "*" Property : exactMatch
    click Property href "../Property"

        
      Subset : example_of_usage
        
      Subset : excluded_from_QC_check
        
          
    
    
    Subset --> "0..1" Thing : excluded_from_QC_check
    click Thing href "../Thing"

        
      Subset : excluded_subClassOf
        
          
    
    
    Subset --> "*" Class : excluded_subClassOf
    click Class href "../Class"

        
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
        
          
    
    
    Subset --> "0..1" Thing : image
    click Thing href "../Thing"

        
      Subset : imported_from
        
          
    
    
    Subset --> "*" NamedIndividual : imported_from
    click NamedIndividual href "../NamedIndividual"

        
      Subset : in_subset
        
          
    
    
    Subset --> "*" Subset : in_subset
    click Subset href "../Subset"

        
      Subset : is_class_level
        
      Subset : is_metadata_tag
        
      Subset : ISA_alternative_term
        
      Subset : isDefinedBy
        
          
    
    
    Subset --> "0..1" Ontology : isDefinedBy
    click Ontology href "../Ontology"

        
      Subset : label
        
      Subset : narrowMatch
        
          
    
    
    Subset --> "*" Property : narrowMatch
    click Property href "../Property"

        
      Subset : OBO_foundry_unique_label
        
      Subset : ontology_term_requester
        
      Subset : page
        
      Subset : range
        
      Subset : seeAlso
        
          
    
    
    Subset --> "*" Thing : seeAlso
    click Thing href "../Thing"

        
      Subset : shorthand
        
      Subset : should_conform_to
        
          
    
    
    Subset --> "0..1" Thing : should_conform_to
    click Thing href "../Thing"

        
      Subset : term_editor
        
      Subset : term_replaced_by
        
          
    
    
    Subset --> "0..1" Any : term_replaced_by
    click Any href "../Any"

        
      Subset : term_tracker_item
        
      Subset : type
        
      
```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * [Property](Property.md)
                * [AnnotationProperty](AnnotationProperty.md)
                    * **Subset**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [shorthand](shorthand.md) | * <br/> [String](String.md) |  | [AnnotationProperty](AnnotationProperty.md) |
| [domain](domain.md) | * <br/> [String](String.md) |  | [Property](Property.md) |
| [range](range.md) | * <br/> [String](String.md) |  | [Property](Property.md) |
| [is_class_level](is_class_level.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [Property](Property.md) |
| [is_metadata_tag](is_metadata_tag.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [Property](Property.md) |
| [has_exact_synonym](has_exact_synonym.md) | * <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_narrow_synonym](has_narrow_synonym.md) | * <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_broad_synonym](has_broad_synonym.md) | * <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_related_synonym](has_related_synonym.md) | * <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [alternative_term](alternative_term.md) | * <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [ISA_alternative_term](ISA_alternative_term.md) | * <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [IEDB_alternative_term](IEDB_alternative_term.md) | * <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [editor_preferred_term](editor_preferred_term.md) | * <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | * <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [deprecated](deprecated.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_obsolescence_reason](has_obsolescence_reason.md) | 0..1 <br/> [String](String.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [term_replaced_by](term_replaced_by.md) | 0..1 <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [consider](consider.md) | * <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_alternative_id](has_alternative_id.md) | * <br/> [Uriorcurie](Uriorcurie.md) | Relates a live term to a deprecated ID that was merged in | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_from_QC_check](excluded_from_QC_check.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_subClassOf](excluded_subClassOf.md) | * <br/> [Class](Class.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_synonym](excluded_synonym.md) | * <br/> [String](String.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [should_conform_to](should_conform_to.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [created_by](created_by.md) | 0..1 <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [creation_date](creation_date.md) | * <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [contributor](contributor.md) | * <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [creator](creator.md) | * <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [created](created.md) | 0..1 <br/> [String](String.md) | when the term came into being | [HasProvenance](HasProvenance.md) |
| [date](date.md) | * <br/> [String](String.md) | when the term was updated | [HasProvenance](HasProvenance.md) |
| [isDefinedBy](isDefinedBy.md) | 0..1 <br/> [Ontology](Ontology.md) |  | [HasProvenance](HasProvenance.md) |
| [editor_note](editor_note.md) | * <br/> [NarrativeText](NarrativeText.md) |  | [HasProvenance](HasProvenance.md) |
| [term_editor](term_editor.md) | * <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [definition_source](definition_source.md) | * <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [ontology_term_requester](ontology_term_requester.md) | 0..1 <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [imported_from](imported_from.md) | * <br/> [NamedIndividual](NamedIndividual.md) |  | [HasProvenance](HasProvenance.md) |
| [term_tracker_item](term_tracker_item.md) | * <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [broadMatch](broadMatch.md) | * <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [closeMatch](closeMatch.md) | * <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [exactMatch](exactMatch.md) | * <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [narrowMatch](narrowMatch.md) | * <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [database_cross_reference](database_cross_reference.md) | * <br/> [CURIELiteral](CURIELiteral.md) |  | [HasMappings](HasMappings.md) |
| [has_obo_namespace](has_obo_namespace.md) | * <br/> [String](String.md) |  | [HasCategory](HasCategory.md) |
| [category](category.md) | 0..1 <br/> [String](String.md) |  | [HasCategory](HasCategory.md) |
| [in_subset](in_subset.md) | * <br/> [Subset](Subset.md) | Maps an ontology element to a subset it belongs to | [HasCategory](HasCategory.md) |
| [conformsTo](conformsTo.md) | * <br/> [Thing](Thing.md) |  | [HasCategory](HasCategory.md) |
| [comment](comment.md) | * <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [seeAlso](seeAlso.md) | * <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [image](image.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [example_of_usage](example_of_usage.md) | * <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [curator_note](curator_note.md) | * <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [depicted_by](depicted_by.md) | * <br/> [Image](Image.md) |  | [HasUserInformation](HasUserInformation.md) |
| [page](page.md) | * <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [label](label.md) | 0..1 _recommended_ <br/> [LabelType](LabelType.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [definition](definition.md) | * _recommended_ <br/> [NarrativeText](NarrativeText.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [type](type.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasCategory](HasCategory.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Term](Term.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Class](Class.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Property](Property.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [AnnotationProperty](AnnotationProperty.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [ObjectProperty](ObjectProperty.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [TransitiveProperty](TransitiveProperty.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [NamedIndividual](NamedIndividual.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [HomoSapiens](HomoSapiens.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Agent](Agent.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Image](Image.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |
| [Subset](Subset.md) | [in_subset](in_subset.md) | range | [Subset](Subset.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:Subset |
| native | omoschema:Subset |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Subset
description: A collection of terms grouped for some purpose
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationProperty
class_uri: oio:Subset

```
</details>

### Induced

<details>
```yaml
name: Subset
description: A collection of terms grouped for some purpose
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationProperty
attributes:
  shorthand:
    name: shorthand
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:shorthand
    alias: shorthand
    owner: Subset
    domain_of:
    - AnnotationProperty
    - ObjectProperty
    range: string
    multivalued: true
  domain:
    name: domain
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:domain
    alias: domain
    owner: Subset
    domain_of:
    - Property
    range: string
    multivalued: true
  range:
    name: range
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:range
    alias: range
    owner: Subset
    domain_of:
    - Property
    range: string
    multivalued: true
  is_class_level:
    name: is_class_level
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:is_class_level
    alias: is_class_level
    owner: Subset
    domain_of:
    - Property
    range: boolean
  is_metadata_tag:
    name: is_metadata_tag
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:is_metadata_tag
    alias: is_metadata_tag
    owner: Subset
    domain_of:
    - Property
    range: boolean
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    alias: has_exact_synonym
    owner: Subset
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
    multivalued: true
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    alias: has_narrow_synonym
    owner: Subset
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    alias: has_broad_synonym
    owner: Subset
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  has_related_synonym:
    name: has_related_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasRelatedSynonym
    alias: has_related_synonym
    owner: Subset
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:altLabel
    rank: 1000
    slot_uri: IAO:0000118
    alias: alternative_term
    owner: Subset
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:0001847
    alias: ISA_alternative_term
    owner: Subset
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:9991118
    alias: IEDB_alternative_term
    owner: Subset
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000111
    alias: editor_preferred_term
    owner: Subset
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000589
    alias: OBO_foundry_unique_label
    owner: Subset
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  deprecated:
    name: deprecated
    in_subset:
    - allotrope permitted profile
    - go permitted profile
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    aliases:
    - is obsolete
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: owl:deprecated
    alias: deprecated
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: boolean
  has_obsolescence_reason:
    name: has_obsolescence_reason
    todos:
    - restrict range
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0000231
    alias: has_obsolescence_reason
    owner: Subset
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
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - dcterms:isReplacedBy
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: Any
  consider:
    name: consider
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: oio:consider
    alias: consider
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: Any
    multivalued: true
  has_alternative_id:
    name: has_alternative_id
    description: Relates a live term to a deprecated ID that was merged in
    deprecated: This is deprecated as it is redundant with the inverse replaced_by
      triple
    comments:
    - '{''RULE'': ''object must NOT be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    see_also:
    - https://github.com/owlcs/owlapi/issues/317
    rank: 1000
    is_a: obsoletion_related_property
    domain: NotObsoleteAspect
    slot_uri: oio:hasAlternativeId
    alias: has_alternative_id
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: uriorcurie
    multivalued: true
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_subClassOf
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: Class
    multivalued: true
  excluded_synonym:
    name: excluded_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:hiddenSynonym
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_synonym
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: string
    multivalued: true
  should_conform_to:
    name: should_conform_to
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: Subset
    domain_of:
    - HasLifeCycle
    range: Thing
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: creator
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: Subset
    domain_of:
    - HasProvenance
    - Axiom
    range: string
  creation_date:
    name: creation_date
    deprecated: proposed obsoleted by OMO group 2022-04-12
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: created
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:creation_date
    alias: creation_date
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  contributor:
    name: contributor
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:contributor
    alias: contributor
    owner: Subset
    domain_of:
    - HasProvenance
    range: Agent
    multivalued: true
    structured_pattern:
      syntax: '{orcid_regex}'
      interpolated: true
      partial_match: false
  creator:
    name: creator
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:creator
    alias: creator
    owner: Subset
    domain_of:
    - HasProvenance
    - Ontology
    range: Agent
    multivalued: true
    structured_pattern:
      syntax: '{orcid_regex}'
      interpolated: true
      partial_match: false
  created:
    name: created
    description: when the term came into being
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:createdOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:created
    alias: created
    owner: Subset
    domain_of:
    - HasProvenance
    - Ontology
    range: string
    multivalued: false
  date:
    name: date
    description: when the term was updated
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:authoredOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:date
    alias: date
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  isDefinedBy:
    name: isDefinedBy
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    rank: 1000
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: Subset
    domain_of:
    - HasProvenance
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000116
    alias: editor_note
    owner: Subset
    domain_of:
    - HasProvenance
    range: narrative text
    multivalued: true
  term_editor:
    name: term_editor
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000117
    alias: term_editor
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  definition_source:
    name: definition_source
    todos:
    - restrict range
    in_subset:
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000119
    alias: definition_source
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
  imported_from:
    name: imported_from
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000412
    alias: imported_from
    owner: Subset
    domain_of:
    - HasProvenance
    range: NamedIndividual
    multivalued: true
  term_tracker_item:
    name: term_tracker_item
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000233
    alias: term_tracker_item
    owner: Subset
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  broadMatch:
    name: broadMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:broadMatch
    alias: broadMatch
    owner: Subset
    domain_of:
    - HasMappings
    range: Property
    multivalued: true
  closeMatch:
    name: closeMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    alias: closeMatch
    owner: Subset
    domain_of:
    - HasMappings
    range: Property
    multivalued: true
  exactMatch:
    name: exactMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    alias: exactMatch
    owner: Subset
    domain_of:
    - HasMappings
    range: Property
    multivalued: true
  narrowMatch:
    name: narrowMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    alias: narrowMatch
    owner: Subset
    domain_of:
    - HasMappings
    range: Property
    multivalued: true
  database_cross_reference:
    name: database_cross_reference
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    alias: database_cross_reference
    owner: Subset
    domain_of:
    - HasMappings
    - Axiom
    range: CURIELiteral
    multivalued: true
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasOBONamespace
    alias: has_obo_namespace
    owner: Subset
    domain_of:
    - HasCategory
    range: string
    multivalued: true
  category:
    name: category
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: Subset
    domain_of:
    - HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:inSubset
    alias: in_subset
    owner: Subset
    domain_of:
    - HasCategory
    range: Subset
    multivalued: true
  conformsTo:
    name: conformsTo
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    alias: conformsTo
    owner: Subset
    domain_of:
    - HasCategory
    range: Thing
    multivalued: true
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    alias: comment
    owner: Subset
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
    multivalued: true
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: rdfs:seeAlso
    alias: seeAlso
    owner: Subset
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
    multivalued: true
  image:
    name: image
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: Subset
    domain_of:
    - HasUserInformation
    range: Thing
  example_of_usage:
    name: example_of_usage
    in_subset:
    - allotrope permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:example
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000112
    alias: example_of_usage
    owner: Subset
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true
  curator_note:
    name: curator_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000232
    alias: curator_note
    owner: Subset
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true
  has_curation_status:
    name: has_curation_status
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: Subset
    domain_of:
    - HasUserInformation
    range: string
  depicted_by:
    name: depicted_by
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:depicted_by
    alias: depicted_by
    owner: Subset
    domain_of:
    - HasUserInformation
    range: Image
    multivalued: true
  page:
    name: page
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    alias: page
    owner: Subset
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true
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
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    alias: label
    owner: Subset
    domain_of:
    - HasMinimalMetadata
    - Axiom
    range: label type
    recommended: true
    multivalued: false
  definition:
    name: definition
    comments:
    - SHOULD be in Aristotelian (genus-differentia) form
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:definition
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    alias: definition
    owner: Subset
    domain_of:
    - HasMinimalMetadata
    range: narrative text
    recommended: true
    multivalued: true
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: Subset
    domain_of:
    - NamedObject
    range: uriorcurie
    required: true
  type:
    name: type
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    designates_type: true
    alias: type
    owner: Subset
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true
class_uri: oio:Subset

```
</details>