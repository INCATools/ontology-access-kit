# Class: Property


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [rdf:Property](http://www.w3.org/1999/02/22-rdf-syntax-ns#Property)



```{mermaid}
 classDiagram
    class Property
      Term <|-- Property
      
      Property : alternative_term
      Property : broadMatch
      Property : category
      Property : closeMatch
      Property : comment
      Property : conformsTo
      Property : consider
      Property : contributor
      Property : created
      Property : created_by
      Property : creation_date
      Property : creator
      Property : curator_note
      Property : database_cross_reference
      Property : date
      Property : definition
      Property : definition_source
      Property : depicted_by
      Property : deprecated
      Property : domain
      Property : editor_note
      Property : editor_preferred_term
      Property : exactMatch
      Property : example_of_usage
      Property : excluded_from_QC_check
      Property : excluded_subClassOf
      Property : excluded_synonym
      Property : has_alternative_id
      Property : has_broad_synonym
      Property : has_curation_status
      Property : has_exact_synonym
      Property : has_narrow_synonym
      Property : has_obo_namespace
      Property : has_obsolescence_reason
      Property : has_related_synonym
      Property : id
      Property : IEDB_alternative_term
      Property : image
      Property : imported_from
      Property : in_subset
      Property : is_class_level
      Property : is_metadata_tag
      Property : ISA_alternative_term
      Property : isDefinedBy
      Property : label
      Property : narrowMatch
      Property : OBO_foundry_unique_label
      Property : ontology_term_requester
      Property : page
      Property : range
      Property : seeAlso
      Property : should_conform_to
      Property : term_editor
      Property : term_replaced_by
      Property : term_tracker_item
      Property : type
      

      Property <|-- AnnotationProperty
      Property <|-- ObjectProperty
      
      Property : alternative_term
      Property : broadMatch
      Property : category
      Property : closeMatch
      Property : comment
      Property : conformsTo
      Property : consider
      Property : contributor
      Property : created
      Property : created_by
      Property : creation_date
      Property : creator
      Property : curator_note
      Property : database_cross_reference
      Property : date
      Property : definition
      Property : definition_source
      Property : depicted_by
      Property : deprecated
      Property : domain
      Property : editor_note
      Property : editor_preferred_term
      Property : exactMatch
      Property : example_of_usage
      Property : excluded_from_QC_check
      Property : excluded_subClassOf
      Property : excluded_synonym
      Property : has_alternative_id
      Property : has_broad_synonym
      Property : has_curation_status
      Property : has_exact_synonym
      Property : has_narrow_synonym
      Property : has_obo_namespace
      Property : has_obsolescence_reason
      Property : has_related_synonym
      Property : id
      Property : IEDB_alternative_term
      Property : image
      Property : imported_from
      Property : in_subset
      Property : is_class_level
      Property : is_metadata_tag
      Property : ISA_alternative_term
      Property : isDefinedBy
      Property : label
      Property : narrowMatch
      Property : OBO_foundry_unique_label
      Property : ontology_term_requester
      Property : page
      Property : range
      Property : seeAlso
      Property : should_conform_to
      Property : term_editor
      Property : term_replaced_by
      Property : term_tracker_item
      Property : type
      
```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * **Property**
                * [AnnotationProperty](AnnotationProperty.md)
                * [ObjectProperty](ObjectProperty.md) [ [PropertyExpression](PropertyExpression.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [domain](domain.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [range](range.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [is_class_level](is_class_level.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | direct |
| [is_metadata_tag](is_metadata_tag.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | direct |
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





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Property](Property.md) | [broadMatch](broadMatch.md) | range | [Property](Property.md) |
| [Property](Property.md) | [closeMatch](closeMatch.md) | range | [Property](Property.md) |
| [Property](Property.md) | [exactMatch](exactMatch.md) | range | [Property](Property.md) |
| [Property](Property.md) | [narrowMatch](narrowMatch.md) | range | [Property](Property.md) |
| [AnnotationProperty](AnnotationProperty.md) | [broadMatch](broadMatch.md) | range | [Property](Property.md) |
| [AnnotationProperty](AnnotationProperty.md) | [closeMatch](closeMatch.md) | range | [Property](Property.md) |
| [AnnotationProperty](AnnotationProperty.md) | [exactMatch](exactMatch.md) | range | [Property](Property.md) |
| [AnnotationProperty](AnnotationProperty.md) | [narrowMatch](narrowMatch.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [equivalentProperty](equivalentProperty.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [inverseOf](inverseOf.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [broadMatch](broadMatch.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [closeMatch](closeMatch.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [exactMatch](exactMatch.md) | range | [Property](Property.md) |
| [ObjectProperty](ObjectProperty.md) | [narrowMatch](narrowMatch.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [equivalentProperty](equivalentProperty.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [inverseOf](inverseOf.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [broadMatch](broadMatch.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [closeMatch](closeMatch.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [exactMatch](exactMatch.md) | range | [Property](Property.md) |
| [TransitiveProperty](TransitiveProperty.md) | [narrowMatch](narrowMatch.md) | range | [Property](Property.md) |
| [Subset](Subset.md) | [broadMatch](broadMatch.md) | range | [Property](Property.md) |
| [Subset](Subset.md) | [closeMatch](closeMatch.md) | range | [Property](Property.md) |
| [Subset](Subset.md) | [exactMatch](exactMatch.md) | range | [Property](Property.md) |
| [Subset](Subset.md) | [narrowMatch](narrowMatch.md) | range | [Property](Property.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:Property |
| native | omoschema:Property |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Property
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Term
abstract: true
slots:
- domain
- range
- is_class_level
- is_metadata_tag
slot_usage:
  label:
    name: label
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
    recommended: true
  definition:
    name: definition
    domain_of:
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    recommended: true
  broadMatch:
    name: broadMatch
    domain_of:
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
    domain_of:
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
    domain_of:
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
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  subClassOf:
    name: subClassOf
    range: Property
class_uri: rdf:Property

```
</details>

### Induced

<details>
```yaml
name: Property
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Term
abstract: true
slot_usage:
  label:
    name: label
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
    recommended: true
  definition:
    name: definition
    domain_of:
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    - HasMinimalMetadata
    recommended: true
  broadMatch:
    name: broadMatch
    domain_of:
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
    domain_of:
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
    domain_of:
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
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    - HasMappings
    range: Property
  subClassOf:
    name: subClassOf
    range: Property
attributes:
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: Property
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
    owner: Property
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
    owner: Property
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
    domain_of:
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
    owner: Property
    domain_of:
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
    owner: Property
    domain_of:
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
    owner: Property
    domain_of:
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
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
    owner: Property
    domain_of:
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
    owner: Property
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
    owner: Property
    domain_of:
    - Thing
    range: uriorcurie
class_uri: rdf:Property

```
</details>