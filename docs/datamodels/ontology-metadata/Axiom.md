# Class: Axiom




URI: [owl:Axiom](http://www.w3.org/2002/07/owl#Axiom)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [annotatedProperty](annotatedProperty.md) | [AnnotationProperty](AnnotationProperty.md) | 0..1 | None  | . |
| [annotatedSource](annotatedSource.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [annotatedTarget](annotatedTarget.md) | [Any](Any.md) | 0..1 | None  | . |
| [source](source.md) | [string](string.md) | 0..* | None  | . |
| [is_inferred](is_inferred.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [notes](notes.md) | [string](string.md) | 0..* | None  | . |
| [url](url.md) | [string](string.md) | 0..1 | None  | . |
| [has_axiom_label](has_axiom_label.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) | [string](string.md) | 0..1 | None  | . |
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) | [string](string.md) | 0..1 | None  | . |
| [created_by](created_by.md) | [string](string.md) | 0..1 | None  | . |
| [date_retrieved](date_retrieved.md) | [string](string.md) | 0..1 | None  | . |
| [evidence](evidence.md) | [string](string.md) | 0..1 | None  | . |
| [external_ontology](external_ontology.md) | [string](string.md) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | Uses to indicate the source of an axiom  | . |
| [has_exact_synonym](has_exact_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_synonym_type](has_synonym_type.md) | [AnnotationProperty](AnnotationProperty.md) | 0..* | None  | . |
| [comment](comment.md) | [string](string.md) | 0..* | None  | . |
| [label](label.md) | [label_type](label_type.md) | 0..1 | None  | . |
| [seeAlso](seeAlso.md) | [Thing](Thing.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Axiom
exact_mappings:
- rdf:Statement
from_schema: http://purl.obolibrary.org/obo/omo/schema
slots:
- annotatedProperty
- annotatedSource
- annotatedTarget
- source
- is_inferred
- notes
- url
- has_axiom_label
- is_a_defining_property_chain_axiom
- is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
- created_by
- date_retrieved
- evidence
- external_ontology
- database_cross_reference
- has_exact_synonym
- has_synonym_type
- comment
- label
- seeAlso
slot_usage:
  database_cross_reference:
    name: database_cross_reference
    exact_mappings:
    - dcterms:source
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
class_uri: owl:Axiom

```
</details>

### Induced

<details>
```yaml
name: Axiom
exact_mappings:
- rdf:Statement
from_schema: http://purl.obolibrary.org/obo/omo/schema
slot_usage:
  database_cross_reference:
    name: database_cross_reference
    exact_mappings:
    - dcterms:source
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
attributes:
  annotatedProperty:
    name: annotatedProperty
    exact_mappings:
    - rdf:predicate
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: reification_predicate
    slot_uri: owl:annotatedProperty
    alias: annotatedProperty
    owner: Axiom
    range: AnnotationProperty
  annotatedSource:
    name: annotatedSource
    exact_mappings:
    - rdf:subject
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: reification_predicate
    slot_uri: owl:annotatedSource
    alias: annotatedSource
    owner: Axiom
    range: Thing
  annotatedTarget:
    name: annotatedTarget
    exact_mappings:
    - rdf:object
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: reification_predicate
    slot_uri: owl:annotatedTarget
    alias: annotatedTarget
    owner: Axiom
    range: Any
  source:
    name: source
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:source
    multivalued: true
    alias: source
    owner: Axiom
    range: string
  is_inferred:
    name: is_inferred
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:is_inferred
    alias: is_inferred
    owner: Axiom
    range: boolean
  notes:
    name: notes
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:notes
    multivalued: true
    alias: notes
    owner: Axiom
    range: string
  url:
    name: url
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:url
    alias: url
    owner: Axiom
    range: string
  has_axiom_label:
    name: has_axiom_label
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: IAO:0010000
    alias: has_axiom_label
    owner: Axiom
    range: Thing
  is_a_defining_property_chain_axiom:
    name: is_a_defining_property_chain_axiom
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: RO:0002581
    alias: is_a_defining_property_chain_axiom
    owner: Axiom
    range: string
  is_a_defining_property_chain_axiom_where_second_argument_is_reflexive:
    name: is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: RO:0002582
    alias: is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
    owner: Axiom
    range: string
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    deprecated_element_has_exact_replacement: creator
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: Axiom
    range: string
  date_retrieved:
    name: date_retrieved
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: oio:date_retrieved
    alias: date_retrieved
    owner: Axiom
    range: string
  evidence:
    name: evidence
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:evidence
    alias: evidence
    owner: Axiom
    range: string
  external_ontology:
    name: external_ontology
    deprecated: deprecated oboInOwl property
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:external_ontology
    multivalued: true
    alias: external_ontology
    owner: Axiom
    range: string
  database_cross_reference:
    name: database_cross_reference
    exact_mappings:
    - dcterms:source
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: Axiom
    range: CURIELiteral
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: Axiom
    disjoint_with:
    - label
    range: label type
  has_synonym_type:
    name: has_synonym_type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasSynonymType
    multivalued: true
    alias: has_synonym_type
    owner: Axiom
    range: AnnotationProperty
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: Axiom
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
    owner: Axiom
    range: label type
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: Axiom
    range: Thing
class_uri: owl:Axiom

```
</details>