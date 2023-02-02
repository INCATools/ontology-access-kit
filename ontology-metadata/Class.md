# Class: Class



URI: [owl:Class](http://www.w3.org/2002/07/owl#Class)



```{mermaid}
 classDiagram
    class Class
      ClassExpression <|-- Class
      Term <|-- Class
      
      Class : alternative_term
      Class : broadMatch
      Class : cardinality
      Class : category
      Class : closeMatch
      Class : comment
      Class : complementOf
      Class : conformsTo
      Class : consider
      Class : contributor
      Class : created
      Class : created_by
      Class : creation_date
      Class : creator
      Class : curator_note
      Class : database_cross_reference
      Class : date
      Class : definition
      Class : definition_source
      Class : depicted_by
      Class : deprecated
      Class : disconnected_from
      Class : disjointWith
      Class : editor_note
      Class : editor_preferred_term
      Class : equivalentClass
      Class : exactMatch
      Class : example_of_usage
      Class : excluded_from_QC_check
      Class : excluded_subClassOf
      Class : excluded_synonym
      Class : has_alternative_id
      Class : has_broad_synonym
      Class : has_curation_status
      Class : has_exact_synonym
      Class : has_narrow_synonym
      Class : has_obo_namespace
      Class : has_obsolescence_reason
      Class : has_rank
      Class : has_related_synonym
      Class : id
      Class : IEDB_alternative_term
      Class : image
      Class : imported_from
      Class : in_subset
      Class : intersectionOf
      Class : ISA_alternative_term
      Class : isDefinedBy
      Class : label
      Class : narrowMatch
      Class : never_in_taxon
      Class : OBO_foundry_unique_label
      Class : oneOf
      Class : ontology_term_requester
      Class : page
      Class : seeAlso
      Class : should_conform_to
      Class : subClassOf
      Class : term_editor
      Class : term_replaced_by
      Class : term_tracker_item
      Class : type
      Class : unionOf
      
```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]
            * **Class** [ [ClassExpression](ClassExpression.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [never_in_taxon](never_in_taxon.md) | 0..* <br/> [Class](Class.md) |  | direct |
| [disconnected_from](disconnected_from.md) | 0..1 <br/> [Class](Class.md) |  | direct |
| [has_rank](has_rank.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |
| [disjointWith](disjointWith.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ClassExpression](ClassExpression.md) |
| [equivalentClass](equivalentClass.md) | 0..* <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [intersectionOf](intersectionOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [subClassOf](subClassOf.md) | 0..* <br/> [Class](Class.md) |  | [ClassExpression](ClassExpression.md) |
| [cardinality](cardinality.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ClassExpression](ClassExpression.md) |
| [complementOf](complementOf.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ClassExpression](ClassExpression.md) |
| [oneOf](oneOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [unionOf](unionOf.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [ClassExpression](ClassExpression.md) |
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
| [broadMatch](broadMatch.md) | 0..* <br/> [Class](Class.md) |  | [HasMappings](HasMappings.md) |
| [closeMatch](closeMatch.md) | 0..* <br/> [Class](Class.md) |  | [HasMappings](HasMappings.md) |
| [exactMatch](exactMatch.md) | 0..* <br/> [Class](Class.md) |  | [HasMappings](HasMappings.md) |
| [narrowMatch](narrowMatch.md) | 0..* <br/> [Class](Class.md) |  | [HasMappings](HasMappings.md) |
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
| [label](label.md) | 1..1 <br/> [LabelType](LabelType.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [definition](definition.md) | 0..* _recommended_ <br/> [NarrativeText](NarrativeText.md) |  | [HasMinimalMetadata](HasMinimalMetadata.md) |
| [id](id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [type](type.md) | 0..* <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |  | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasLifeCycle](HasLifeCycle.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Ontology](Ontology.md) | [has_ontology_root_term](has_ontology_root_term.md) | range | [Class](Class.md) |
| [Term](Term.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Class](Class.md) | [never_in_taxon](never_in_taxon.md) | range | [Class](Class.md) |
| [Class](Class.md) | [disconnected_from](disconnected_from.md) | range | [Class](Class.md) |
| [Class](Class.md) | [subClassOf](subClassOf.md) | range | [Class](Class.md) |
| [Class](Class.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Class](Class.md) | [broadMatch](broadMatch.md) | range | [Class](Class.md) |
| [Class](Class.md) | [closeMatch](closeMatch.md) | range | [Class](Class.md) |
| [Class](Class.md) | [exactMatch](exactMatch.md) | range | [Class](Class.md) |
| [Class](Class.md) | [narrowMatch](narrowMatch.md) | range | [Class](Class.md) |
| [Property](Property.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [AnnotationProperty](AnnotationProperty.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [ObjectProperty](ObjectProperty.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [TransitiveProperty](TransitiveProperty.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [NamedIndividual](NamedIndividual.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [HomoSapiens](HomoSapiens.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Agent](Agent.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Image](Image.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |
| [Subset](Subset.md) | [excluded_subClassOf](excluded_subClassOf.md) | range | [Class](Class.md) |




## Aliases


* term
* concept



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Class |
| native | omoschema:Class |
| close | skos:Concept |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Class
from_schema: http://purl.obolibrary.org/obo/omo/schema
aliases:
- term
- concept
close_mappings:
- skos:Concept
rank: 1000
is_a: Term
mixins:
- ClassExpression
slots:
- never_in_taxon
- disconnected_from
- has_rank
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
    required: true
  definition:
    name: definition
    domain_of:
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
    range: Class
  exactMatch:
    name: exactMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  narrowMatch:
    name: narrowMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  closeMatch:
    name: closeMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  subClassOf:
    name: subClassOf
    domain_of:
    - ClassExpression
    - ClassExpression
    - ClassExpression
    range: Class
class_uri: owl:Class

```
</details>

### Induced

<details>
```yaml
name: Class
from_schema: http://purl.obolibrary.org/obo/omo/schema
aliases:
- term
- concept
close_mappings:
- skos:Concept
rank: 1000
is_a: Term
mixins:
- ClassExpression
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
    required: true
  definition:
    name: definition
    domain_of:
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
    range: Class
  exactMatch:
    name: exactMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  narrowMatch:
    name: narrowMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  closeMatch:
    name: closeMatch
    domain_of:
    - HasMappings
    - HasMappings
    - HasMappings
    range: Class
  subClassOf:
    name: subClassOf
    domain_of:
    - ClassExpression
    - ClassExpression
    - ClassExpression
    range: Class
attributes:
  never_in_taxon:
    name: never_in_taxon
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: RO:0002161
    multivalued: true
    alias: never_in_taxon
    owner: Class
    domain_of:
    - Class
    range: Class
  disconnected_from:
    name: disconnected_from
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: shortcut_annotation_property
    alias: disconnected_from
    owner: Class
    domain_of:
    - Class
    range: Class
  has_rank:
    name: has_rank
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - obo:ncbitaxon/subsets/taxslim#has_rank
    rank: 1000
    alias: has_rank
    owner: Class
    domain_of:
    - Class
    range: Thing
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
    owner: Class
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
  equivalentClass:
    name: equivalentClass
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentClass
    multivalued: true
    alias: equivalentClass
    owner: Class
    domain_of:
    - ClassExpression
    range: ClassExpression
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:intersectionOf
    alias: intersectionOf
    owner: Class
    domain_of:
    - ClassExpression
    range: ClassExpression
  subClassOf:
    name: subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    multivalued: true
    alias: subClassOf
    owner: Class
    domain_of:
    - ClassExpression
    - ClassExpression
    range: Class
  cardinality:
    name: cardinality
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:cardinality
    alias: cardinality
    owner: Class
    domain_of:
    - ClassExpression
    range: string
  complementOf:
    name: complementOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:complementOf
    alias: complementOf
    owner: Class
    domain_of:
    - ClassExpression
    range: string
  oneOf:
    name: oneOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:oneOf
    alias: oneOf
    owner: Class
    domain_of:
    - ClassExpression
    range: ClassExpression
  unionOf:
    name: unionOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:unionOf
    alias: unionOf
    owner: Class
    domain_of:
    - ClassExpression
    range: string
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: Class
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
    owner: Class
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
    owner: Class
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
    domain_of:
    - HasMappings
    - HasMappings
    range: Class
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: Class
    domain_of:
    - HasMappings
    - HasMappings
    range: Class
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: Class
    domain_of:
    - HasMappings
    - HasMappings
    range: Class
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: Class
    domain_of:
    - HasMappings
    - HasMappings
    range: Class
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
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
    owner: Class
    domain_of:
    - HasMinimalMetadata
    - Axiom
    - HasMinimalMetadata
    - Axiom
    range: label type
    required: true
  definition:
    name: definition
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: Class
    domain_of:
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
    owner: Class
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
    owner: Class
    domain_of:
    - Thing
    range: uriorcurie
class_uri: owl:Class

```
</details>