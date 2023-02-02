# Class: TransitiveProperty
_An ObjectProperty with the property of transitivity_




URI: [omoschema:TransitiveProperty](http://purl.obolibrary.org/obo/omo/schema/TransitiveProperty)



```{mermaid}
 classDiagram
    class TransitiveProperty
      ObjectProperty <|-- TransitiveProperty
      
      TransitiveProperty : alternative_term
      TransitiveProperty : broadMatch
      TransitiveProperty : category
      TransitiveProperty : closeMatch
      TransitiveProperty : comment
      TransitiveProperty : conformsTo
      TransitiveProperty : consider
      TransitiveProperty : contributor
      TransitiveProperty : created
      TransitiveProperty : created_by
      TransitiveProperty : creation_date
      TransitiveProperty : creator
      TransitiveProperty : curator_note
      TransitiveProperty : database_cross_reference
      TransitiveProperty : date
      TransitiveProperty : definition
      TransitiveProperty : definition_source
      TransitiveProperty : depicted_by
      TransitiveProperty : deprecated
      TransitiveProperty : disjointWith
      TransitiveProperty : domain
      TransitiveProperty : editor_note
      TransitiveProperty : editor_preferred_term
      TransitiveProperty : equivalentProperty
      TransitiveProperty : exactMatch
      TransitiveProperty : example_of_usage
      TransitiveProperty : excluded_from_QC_check
      TransitiveProperty : excluded_subClassOf
      TransitiveProperty : excluded_synonym
      TransitiveProperty : has_alternative_id
      TransitiveProperty : has_broad_synonym
      TransitiveProperty : has_curation_status
      TransitiveProperty : has_exact_synonym
      TransitiveProperty : has_narrow_synonym
      TransitiveProperty : has_obo_namespace
      TransitiveProperty : has_obsolescence_reason
      TransitiveProperty : has_related_synonym
      TransitiveProperty : id
      TransitiveProperty : IEDB_alternative_term
      TransitiveProperty : image
      TransitiveProperty : imported_from
      TransitiveProperty : in_subset
      TransitiveProperty : inverseOf
      TransitiveProperty : is_class_level
      TransitiveProperty : is_cyclic
      TransitiveProperty : is_metadata_tag
      TransitiveProperty : is_transitive
      TransitiveProperty : ISA_alternative_term
      TransitiveProperty : isDefinedBy
      TransitiveProperty : label
      TransitiveProperty : narrowMatch
      TransitiveProperty : OBO_foundry_unique_label
      TransitiveProperty : ontology_term_requester
      TransitiveProperty : page
      TransitiveProperty : propertyChainAxiom
      TransitiveProperty : range
      TransitiveProperty : seeAlso
      TransitiveProperty : shorthand
      TransitiveProperty : should_conform_to
      TransitiveProperty : temporal_interpretation
      TransitiveProperty : term_editor
      TransitiveProperty : term_replaced_by
      TransitiveProperty : term_tracker_item
      TransitiveProperty : type
      
```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * [Property](Property.md)
                * [ObjectProperty](ObjectProperty.md) [ [PropertyExpression](PropertyExpression.md)]
                    * **TransitiveProperty**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [temporal_interpretation](temporal_interpretation.md) | 0..1 <br/> [NamedIndividual](NamedIndividual.md) |  | [ObjectProperty](ObjectProperty.md) |
| [is_cyclic](is_cyclic.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | [ObjectProperty](ObjectProperty.md) |
| [is_transitive](is_transitive.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | [ObjectProperty](ObjectProperty.md) |
| [shorthand](shorthand.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ObjectProperty](ObjectProperty.md) |
| [equivalentProperty](equivalentProperty.md) | 0..* <br/> [Property](Property.md) |  | [ObjectProperty](ObjectProperty.md) |
| [inverseOf](inverseOf.md) | 0..1 <br/> [Property](Property.md) |  | [ObjectProperty](ObjectProperty.md) |
| [propertyChainAxiom](propertyChainAxiom.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ObjectProperty](ObjectProperty.md) |
| [disjointWith](disjointWith.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [PropertyExpression](PropertyExpression.md) |
| [domain](domain.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [Property](Property.md) |
| [range](range.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [Property](Property.md) |
| [is_class_level](is_class_level.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | [Property](Property.md) |
| [is_metadata_tag](is_metadata_tag.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | [Property](Property.md) |
| [has_exact_synonym](has_exact_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_narrow_synonym](has_narrow_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_broad_synonym](has_broad_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [has_related_synonym](has_related_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | [HasSynonyms](HasSynonyms.md) |
| [alternative_term](alternative_term.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasSynonyms](HasSynonyms.md) |
| [ISA_alternative_term](ISA_alternative_term.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasSynonyms](HasSynonyms.md) |
| [IEDB_alternative_term](IEDB_alternative_term.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasSynonyms](HasSynonyms.md) |
| [editor_preferred_term](editor_preferred_term.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasSynonyms](HasSynonyms.md) |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasSynonyms](HasSynonyms.md) |
| [deprecated](deprecated.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_obsolescence_reason](has_obsolescence_reason.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasLifeCycle](HasLifeCycle.md) |
| [term_replaced_by](term_replaced_by.md) | 0..1 <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [consider](consider.md) | 0..* <br/> [Any](Any.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [has_alternative_id](has_alternative_id.md) | 0..* <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | Relates a live term to a deprecated ID that was merged in | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_from_QC_check](excluded_from_QC_check.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_subClassOf](excluded_subClassOf.md) | 0..* <br/> [Class](Class.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [excluded_synonym](excluded_synonym.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasLifeCycle](HasLifeCycle.md) |
| [should_conform_to](should_conform_to.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasLifeCycle](HasLifeCycle.md) |
| [created_by](created_by.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [creation_date](creation_date.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [contributor](contributor.md) | 0..* <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [creator](creator.md) | 0..* <br/> [Agent](Agent.md) |  | [HasProvenance](HasProvenance.md) |
| [created](created.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | when the term came into being | [HasProvenance](HasProvenance.md) |
| [date](date.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | when the term was updated | [HasProvenance](HasProvenance.md) |
| [isDefinedBy](isDefinedBy.md) | 0..1 <br/> [Ontology](Ontology.md) |  | [HasProvenance](HasProvenance.md) |
| [editor_note](editor_note.md) | 0..* <br/> [NarrativeText](NarrativeText.md) |  | [HasProvenance](HasProvenance.md) |
| [term_editor](term_editor.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [definition_source](definition_source.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [ontology_term_requester](ontology_term_requester.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [imported_from](imported_from.md) | 0..* <br/> [NamedIndividual](NamedIndividual.md) |  | [HasProvenance](HasProvenance.md) |
| [term_tracker_item](term_tracker_item.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasProvenance](HasProvenance.md) |
| [broadMatch](broadMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [closeMatch](closeMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [exactMatch](exactMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [narrowMatch](narrowMatch.md) | 0..* <br/> [Property](Property.md) |  | [HasMappings](HasMappings.md) |
| [database_cross_reference](database_cross_reference.md) | 0..* <br/> [CURIELiteral](CURIELiteral.md) |  | [HasMappings](HasMappings.md) |
| [has_obo_namespace](has_obo_namespace.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasCategory](HasCategory.md) |
| [category](category.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasCategory](HasCategory.md) |
| [in_subset](in_subset.md) | 0..* <br/> [Subset](Subset.md) | Maps an ontology element to a subset it belongs to | [HasCategory](HasCategory.md) |
| [conformsTo](conformsTo.md) | 0..* <br/> [Thing](Thing.md) |  | [HasCategory](HasCategory.md) |
| [comment](comment.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasUserInformation](HasUserInformation.md) |
| [seeAlso](seeAlso.md) | 0..* <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [image](image.md) | 0..1 <br/> [Thing](Thing.md) |  | [HasUserInformation](HasUserInformation.md) |
| [example_of_usage](example_of_usage.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasUserInformation](HasUserInformation.md) |
| [curator_note](curator_note.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasUserInformation](HasUserInformation.md) |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasUserInformation](HasUserInformation.md) |
| [depicted_by](depicted_by.md) | 0..* <br/> [Image](Image.md) |  | [HasUserInformation](HasUserInformation.md) |
| [page](page.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [HasUserInformation](HasUserInformation.md) |
| [label](label.md) | 0..1 _recommended_ <br/> [LabelType](LabelType.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [definition](definition.md) | 0..* _recommended_ <br/> [NarrativeText](NarrativeText.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [id](id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [type](type.md) | 0..* <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |  | [Thing](Thing.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:TransitiveProperty |
| native | omoschema:TransitiveProperty |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TransitiveProperty
description: An ObjectProperty with the property of transitivity
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: ObjectProperty

```
</details>

### Induced

<details>
```yaml
name: TransitiveProperty
description: An ObjectProperty with the property of transitivity
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: ObjectProperty
attributes:
  temporal_interpretation:
    name: temporal_interpretation
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: RO:0001900
    alias: temporal_interpretation
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: NamedIndividual
  is_cyclic:
    name: is_cyclic
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:is_cyclic
    alias: is_cyclic
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: boolean
  is_transitive:
    name: is_transitive
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: TransitiveProperty
    rank: 1000
    slot_uri: oio:is_transitive
    alias: is_transitive
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: boolean
  shorthand:
    name: shorthand
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:shorthand
    multivalued: true
    alias: shorthand
    owner: TransitiveProperty
    domain_of:
    - AnnotationProperty
    - ObjectProperty
    range: string
  equivalentProperty:
    name: equivalentProperty
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentProperty
    multivalued: true
    alias: equivalentProperty
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: Property
  inverseOf:
    name: inverseOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:inverseOf
    alias: inverseOf
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: Property
  propertyChainAxiom:
    name: propertyChainAxiom
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:propertyChainAxiom
    multivalued: true
    alias: propertyChainAxiom
    owner: TransitiveProperty
    domain_of:
    - ObjectProperty
    range: string
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: TransitiveProperty
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
  domain:
    name: domain
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:domain
    multivalued: true
    alias: domain
    owner: TransitiveProperty
    domain_of:
    - Property
    range: string
  range:
    name: range
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:range
    multivalued: true
    alias: range
    owner: TransitiveProperty
    domain_of:
    - Property
    range: string
  is_class_level:
    name: is_class_level
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:is_class_level
    alias: is_class_level
    owner: TransitiveProperty
    domain_of:
    - Property
    range: boolean
  is_metadata_tag:
    name: is_metadata_tag
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:is_metadata_tag
    alias: is_metadata_tag
    owner: TransitiveProperty
    domain_of:
    - Property
    range: boolean
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - HasProvenance
    range: Agent
    structured_pattern:
      syntax: '{orcid_regex}'
      interpolated: true
      partial_match: false
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
    owner: TransitiveProperty
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
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:createdOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:created
    multivalued: false
    alias: created
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: TransitiveProperty
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: TransitiveProperty
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: TransitiveProperty
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - HasUserInformation
    range: Image
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: TransitiveProperty
    domain_of:
    - HasUserInformation
    range: string
  label:
    name: label
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: TransitiveProperty
    domain_of:
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    range: label type
    recommended: true
  definition:
    name: definition
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: TransitiveProperty
    domain_of:
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    range: narrative text
    recommended: true
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: TransitiveProperty
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
    owner: TransitiveProperty
    domain_of:
    - Thing
    range: uriorcurie

```
</details>