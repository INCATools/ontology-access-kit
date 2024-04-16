

# Class: ObjectProperty


_A property that connects two objects in logical axioms_





URI: [owl:ObjectProperty](http://www.w3.org/2002/07/owl#ObjectProperty)




```{mermaid}
 classDiagram
    class ObjectProperty
      PropertyExpression <|-- ObjectProperty
      Property <|-- ObjectProperty
      

      ObjectProperty <|-- TransitiveProperty
      
      
      ObjectProperty : alternative_term
        
      ObjectProperty : broadMatch
        
          ObjectProperty --> Property : broadMatch
        
      ObjectProperty : category
        
      ObjectProperty : closeMatch
        
          ObjectProperty --> Property : closeMatch
        
      ObjectProperty : comment
        
      ObjectProperty : conformsTo
        
          ObjectProperty --> Thing : conformsTo
        
      ObjectProperty : consider
        
          ObjectProperty --> Any : consider
        
      ObjectProperty : contributor
        
          ObjectProperty --> Agent : contributor
        
      ObjectProperty : created
        
      ObjectProperty : created_by
        
      ObjectProperty : creation_date
        
      ObjectProperty : creator
        
          ObjectProperty --> Agent : creator
        
      ObjectProperty : curator_note
        
      ObjectProperty : database_cross_reference
        
      ObjectProperty : date
        
      ObjectProperty : definition
        
      ObjectProperty : definition_source
        
      ObjectProperty : depicted_by
        
          ObjectProperty --> Image : depicted_by
        
      ObjectProperty : deprecated
        
      ObjectProperty : disjointWith
        
      ObjectProperty : domain
        
      ObjectProperty : editor_note
        
      ObjectProperty : editor_preferred_term
        
      ObjectProperty : equivalentProperty
        
          ObjectProperty --> Property : equivalentProperty
        
      ObjectProperty : exactMatch
        
          ObjectProperty --> Property : exactMatch
        
      ObjectProperty : example_of_usage
        
      ObjectProperty : excluded_from_QC_check
        
          ObjectProperty --> Thing : excluded_from_QC_check
        
      ObjectProperty : excluded_subClassOf
        
          ObjectProperty --> Class : excluded_subClassOf
        
      ObjectProperty : excluded_synonym
        
      ObjectProperty : has_alternative_id
        
      ObjectProperty : has_broad_synonym
        
      ObjectProperty : has_curation_status
        
      ObjectProperty : has_exact_synonym
        
      ObjectProperty : has_narrow_synonym
        
      ObjectProperty : has_obo_namespace
        
      ObjectProperty : has_obsolescence_reason
        
      ObjectProperty : has_related_synonym
        
      ObjectProperty : id
        
      ObjectProperty : IEDB_alternative_term
        
      ObjectProperty : image
        
          ObjectProperty --> Thing : image
        
      ObjectProperty : imported_from
        
          ObjectProperty --> NamedIndividual : imported_from
        
      ObjectProperty : in_subset
        
          ObjectProperty --> Subset : in_subset
        
      ObjectProperty : inverseOf
        
          ObjectProperty --> Property : inverseOf
        
      ObjectProperty : is_class_level
        
      ObjectProperty : is_cyclic
        
      ObjectProperty : is_metadata_tag
        
      ObjectProperty : is_transitive
        
      ObjectProperty : ISA_alternative_term
        
      ObjectProperty : isDefinedBy
        
          ObjectProperty --> Ontology : isDefinedBy
        
      ObjectProperty : label
        
      ObjectProperty : narrowMatch
        
          ObjectProperty --> Property : narrowMatch
        
      ObjectProperty : OBO_foundry_unique_label
        
      ObjectProperty : ontology_term_requester
        
      ObjectProperty : page
        
      ObjectProperty : propertyChainAxiom
        
      ObjectProperty : range
        
      ObjectProperty : seeAlso
        
          ObjectProperty --> Thing : seeAlso
        
      ObjectProperty : shorthand
        
      ObjectProperty : should_conform_to
        
          ObjectProperty --> Thing : should_conform_to
        
      ObjectProperty : temporal_interpretation
        
          ObjectProperty --> NamedIndividual : temporal_interpretation
        
      ObjectProperty : term_editor
        
      ObjectProperty : term_replaced_by
        
          ObjectProperty --> Any : term_replaced_by
        
      ObjectProperty : term_tracker_item
        
      ObjectProperty : type
        
      
```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * [Property](Property.md)
                * **ObjectProperty** [ [PropertyExpression](PropertyExpression.md)]
                    * [TransitiveProperty](TransitiveProperty.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [temporal_interpretation](temporal_interpretation.md) | 0..1 <br/> [NamedIndividual](NamedIndividual.md) |  | direct |
| [is_cyclic](is_cyclic.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_transitive](is_transitive.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [shorthand](shorthand.md) | 0..* <br/> [String](String.md) |  | direct |
| [equivalentProperty](equivalentProperty.md) | 0..* <br/> [Property](Property.md) |  | direct |
| [inverseOf](inverseOf.md) | 0..1 <br/> [Property](Property.md) |  | direct |
| [propertyChainAxiom](propertyChainAxiom.md) | 0..* <br/> [String](String.md) |  | direct |
| [disjointWith](disjointWith.md) | 0..* <br/> [String](String.md) |  | [PropertyExpression](PropertyExpression.md) |
| [domain](domain.md) | 0..* <br/> [String](String.md) |  | [Property](Property.md) |
| [range](range.md) | 0..* <br/> [String](String.md) |  | [Property](Property.md) |
| [is_class_level](is_class_level.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [Property](Property.md) |
| [is_metadata_tag](is_metadata_tag.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [Property](Property.md) |
| [has_exact_synonym](has_exact_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_narrow_synonym](has_narrow_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_broad_synonym](has_broad_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_related_synonym](has_related_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [alternative_term](alternative_term.md) | 0..* <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [ISA_alternative_term](ISA_alternative_term.md) | 0..* <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [IEDB_alternative_term](IEDB_alternative_term.md) | 0..* <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [editor_preferred_term](editor_preferred_term.md) | 0..* <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | 0..* <br/> [String](String.md) |  | [HasSynonyms](HasSynonyms.md) |
| [deprecated](deprecated.md) | 0..1 <br/> [Boolean](Boolean.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_obsolescence_reason](has_obsolescence_reason.md) | 0..1 <br/> [String](String.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [term_replaced_by](term_replaced_by.md) | 0..1 <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [consider](consider.md) | 0..* <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_alternative_id](has_alternative_id.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | Relates a live term to a deprecated ID that was merged in | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_from_QC_check](excluded_from_QC_check.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_subClassOf](excluded_subClassOf.md) | 0..* <br/> [Class](Class.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_synonym](excluded_synonym.md) | 0..* <br/> [String](String.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [should_conform_to](should_conform_to.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [created_by](created_by.md) | 0..1 <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [creation_date](creation_date.md) | 0..* <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [contributor](contributor.md) | 0..* <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [creator](creator.md) | 0..* <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [created](created.md) | 0..1 <br/> [String](String.md) | when the term came into being | [HasProvenance](HasProvenance.md) |
| [date](date.md) | 0..* <br/> [String](String.md) | when the term was updated | [HasProvenance](HasProvenance.md) |
| [isDefinedBy](isDefinedBy.md) | 0..1 <br/> [Ontology](Ontology.md) |  | [HasProvenance](HasProvenance.md) |
| [editor_note](editor_note.md) | 0..* <br/> [NarrativeText](NarrativeText.md) |  | [HasProvenance](HasProvenance.md) |
| [term_editor](term_editor.md) | 0..* <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [definition_source](definition_source.md) | 0..* <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [ontology_term_requester](ontology_term_requester.md) | 0..1 <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [imported_from](imported_from.md) | 0..* <br/> [NamedIndividual](NamedIndividual.md) |  | [HasProvenance](HasProvenance.md) |
| [term_tracker_item](term_tracker_item.md) | 0..* <br/> [String](String.md) |  | [HasProvenance](HasProvenance.md) |
| [broadMatch](broadMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [closeMatch](closeMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [exactMatch](exactMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [narrowMatch](narrowMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [database_cross_reference](database_cross_reference.md) | 0..* <br/> [CURIELiteral](CURIELiteral.md) |  | [HasMappings](HasMappings.md) |
| [has_obo_namespace](has_obo_namespace.md) | 0..* <br/> [String](String.md) |  | [HasCategory](HasCategory.md) |
| [category](category.md) | 0..1 <br/> [String](String.md) |  | [HasCategory](HasCategory.md) |
| [in_subset](in_subset.md) | 0..* <br/> [Subset](Subset.md) | Maps an ontology element to a subset it belongs to | [HasCategory](HasCategory.md) |
| [conformsTo](conformsTo.md) | 0..* <br/> [Thing](Thing.md) |  | [HasCategory](HasCategory.md) |
| [comment](comment.md) | 0..* <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [seeAlso](seeAlso.md) | 0..* <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [image](image.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [example_of_usage](example_of_usage.md) | 0..* <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [curator_note](curator_note.md) | 0..* <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [depicted_by](depicted_by.md) | 0..* <br/> [Image](Image.md) |  | [HasUserInformation](HasUserInformation.md) |
| [page](page.md) | 0..* <br/> [String](String.md) |  | [HasUserInformation](HasUserInformation.md) |
| [label](label.md) | 0..1 _recommended_ <br/> [LabelType](LabelType.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [definition](definition.md) | 0..* _recommended_ <br/> [NarrativeText](NarrativeText.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [type](type.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) |  | [Thing](Thing.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:ObjectProperty |
| native | omoschema:ObjectProperty |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ObjectProperty
description: A property that connects two objects in logical axioms
from_schema: https://w3id.org/oak/ontology-metadata
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
description: A property that connects two objects in logical axioms
from_schema: https://w3id.org/oak/ontology-metadata
is_a: Property
mixins:
- PropertyExpression
attributes:
  temporal_interpretation:
    name: temporal_interpretation
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: RO:0001900
    alias: temporal_interpretation
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: NamedIndividual
  is_cyclic:
    name: is_cyclic
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:is_cyclic
    alias: is_cyclic
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: boolean
  is_transitive:
    name: is_transitive
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: TransitiveProperty
    rank: 1000
    slot_uri: oio:is_transitive
    alias: is_transitive
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: boolean
  shorthand:
    name: shorthand
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:shorthand
    multivalued: true
    alias: shorthand
    owner: ObjectProperty
    domain_of:
    - AnnotationProperty
    - ObjectProperty
    range: string
  equivalentProperty:
    name: equivalentProperty
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentProperty
    multivalued: true
    alias: equivalentProperty
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: Property
  inverseOf:
    name: inverseOf
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:inverseOf
    alias: inverseOf
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: Property
  propertyChainAxiom:
    name: propertyChainAxiom
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:propertyChainAxiom
    multivalued: true
    alias: propertyChainAxiom
    owner: ObjectProperty
    domain_of:
    - ObjectProperty
    range: string
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: ObjectProperty
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
  domain:
    name: domain
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:domain
    multivalued: true
    alias: domain
    owner: ObjectProperty
    domain_of:
    - Property
    range: string
  range:
    name: range
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:range
    multivalued: true
    alias: range
    owner: ObjectProperty
    domain_of:
    - Property
    range: string
  is_class_level:
    name: is_class_level
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:is_class_level
    alias: is_class_level
    owner: ObjectProperty
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
    owner: ObjectProperty
    domain_of:
    - Property
    range: boolean
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    multivalued: true
    alias: has_narrow_synonym
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: label type
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:altLabel
    rank: 1000
    slot_uri: IAO:0000118
    multivalued: true
    alias: alternative_term
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: string
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000111
    multivalued: true
    alias: editor_preferred_term
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: string
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000589
    multivalued: true
    alias: OBO_foundry_unique_label
    owner: ObjectProperty
    domain_of:
    - HasSynonyms
    range: string
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
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    multivalued: true
    alias: consider
    owner: ObjectProperty
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
    from_schema: https://w3id.org/oak/ontology-metadata
    see_also:
    - https://github.com/owlcs/owlapi/issues/317
    rank: 1000
    is_a: obsoletion_related_property
    domain: NotObsoleteAspect
    slot_uri: oio:hasAlternativeId
    multivalued: true
    alias: has_alternative_id
    owner: ObjectProperty
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: ObjectProperty
    domain_of:
    - HasLifeCycle
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: ObjectProperty
    domain_of:
    - HasLifeCycle
    range: Class
  excluded_synonym:
    name: excluded_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:hiddenSynonym
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: ObjectProperty
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: ObjectProperty
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
    owner: ObjectProperty
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
    multivalued: true
    alias: creation_date
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
  contributor:
    name: contributor
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:contributor
    multivalued: true
    alias: contributor
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: Agent
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
    multivalued: true
    alias: creator
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    - Ontology
    range: Agent
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
    multivalued: false
    alias: created
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    - Ontology
    range: string
  date:
    name: date
    description: when the term was updated
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:authoredOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:date
    multivalued: true
    alias: date
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
  isDefinedBy:
    name: isDefinedBy
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    rank: 1000
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000116
    multivalued: true
    alias: editor_note
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: narrative text
  term_editor:
    name: term_editor
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000117
    multivalued: true
    alias: term_editor
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
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
    multivalued: true
    alias: definition_source
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
  imported_from:
    name: imported_from
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000412
    multivalued: true
    alias: imported_from
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: NamedIndividual
  term_tracker_item:
    name: term_tracker_item
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000233
    multivalued: true
    alias: term_tracker_item
    owner: ObjectProperty
    domain_of:
    - HasProvenance
    range: string
  broadMatch:
    name: broadMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: ObjectProperty
    domain_of:
    - HasMappings
    range: Property
  closeMatch:
    name: closeMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: ObjectProperty
    domain_of:
    - HasMappings
    range: Property
  exactMatch:
    name: exactMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: ObjectProperty
    domain_of:
    - HasMappings
    range: Property
  narrowMatch:
    name: narrowMatch
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: ObjectProperty
    domain_of:
    - HasMappings
    range: Property
  database_cross_reference:
    name: database_cross_reference
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: ObjectProperty
    domain_of:
    - HasMappings
    - Axiom
    range: CURIELiteral
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: ObjectProperty
    domain_of:
    - HasCategory
    range: string
  category:
    name: category
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: ObjectProperty
    domain_of:
    - HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: ObjectProperty
    domain_of:
    - HasCategory
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: ObjectProperty
    domain_of:
    - HasCategory
    range: Thing
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
  image:
    name: image
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: ObjectProperty
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
    multivalued: true
    alias: example_of_usage
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    range: string
  curator_note:
    name: curator_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    range: string
  depicted_by:
    name: depicted_by
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    range: Image
  page:
    name: page
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: ObjectProperty
    domain_of:
    - HasUserInformation
    range: string
  label:
    name: label
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: ObjectProperty
    domain_of:
    - HasMinimalMetadata
    - Axiom
    range: label type
    recommended: true
  definition:
    name: definition
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: ObjectProperty
    domain_of:
    - HasMinimalMetadata
    range: narrative text
    recommended: true
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: ObjectProperty
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
    multivalued: true
    designates_type: true
    alias: type
    owner: ObjectProperty
    domain_of:
    - Thing
    range: uriorcurie
class_uri: owl:ObjectProperty

```
</details>