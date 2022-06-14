# Class: Axiom




URI: [owl:Axiom](http://www.w3.org/2002/07/owl#Axiom)




```{mermaid}
 classDiagram
    class Axiom
      Axiom : annotatedProperty
      Axiom : annotatedSource
      Axiom : annotatedTarget
      Axiom : annotations
      Axiom : comment
      Axiom : created_by
      Axiom : database_cross_reference
      Axiom : date_retrieved
      Axiom : evidence
      Axiom : external_ontology
      Axiom : has_axiom_label
      Axiom : has_exact_synonym
      Axiom : has_synonym_type
      Axiom : is_a_defining_property_chain_axiom
      Axiom : is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
      Axiom : is_inferred
      Axiom : label
      Axiom : notes
      Axiom : seeAlso
      Axiom : source
      Axiom : url
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [annotatedProperty](annotatedProperty.md) | [AnnotationProperty](AnnotationProperty.md) | 0..1 | None  | . |
| [annotatedSource](annotatedSource.md) | [NamedObject](NamedObject.md) | 0..1 | None  | . |
| [annotatedTarget](annotatedTarget.md) | [Any](Any.md) | 0..1 | None  | . |
| [annotations](annotations.md) | [Annotation](Annotation.md) | 0..* | None  | . |
| [source](source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [is_inferred](is_inferred.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [notes](notes.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [url](url.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [has_axiom_label](has_axiom_label.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [created_by](created_by.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [date_retrieved](date_retrieved.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [evidence](evidence.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [external_ontology](external_ontology.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | Uses to indicate the source of an axiom  | . |
| [has_exact_synonym](has_exact_synonym.md) | [label_type](label_type.md) | 0..* | None  | . |
| [has_synonym_type](has_synonym_type.md) | [AnnotationProperty](AnnotationProperty.md) | 0..* | None  | . |
| [comment](comment.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [label](label.md) | [label_type](label_type.md) | 0..1 | None  | . |
| [seeAlso](seeAlso.md) | [Thing](Thing.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['owl:Axiom'] |
| native | ['omoschema:Axiom'] |
| exact | ['rdf:Statement'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Axiom
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- rdf:Statement
slots:
- annotatedProperty
- annotatedSource
- annotatedTarget
- annotations
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
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
    exact_mappings:
    - dcterms:source
class_uri: owl:Axiom
represents_relationship: true

```
</details>

### Induced

<details>
```yaml
name: Axiom
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- rdf:Statement
slot_usage:
  database_cross_reference:
    name: database_cross_reference
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
    exact_mappings:
    - dcterms:source
attributes:
  annotatedProperty:
    name: annotatedProperty
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - rdf:predicate
    is_a: reification_predicate
    slot_uri: owl:annotatedProperty
    alias: annotatedProperty
    owner: Axiom
    relational_role: PREDICATE
    range: AnnotationProperty
  annotatedSource:
    name: annotatedSource
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - rdf:subject
    is_a: reification_predicate
    slot_uri: owl:annotatedSource
    alias: annotatedSource
    owner: Axiom
    relational_role: SUBJECT
    range: NamedObject
  annotatedTarget:
    name: annotatedTarget
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - rdf:object
    is_a: reification_predicate
    slot_uri: owl:annotatedTarget
    alias: annotatedTarget
    owner: Axiom
    relational_role: OBJECT
    range: Any
  annotations:
    name: annotations
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    multivalued: true
    alias: annotations
    owner: Axiom
    range: Annotation
  source:
    name: source
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
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
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - dcterms:source
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
represents_relationship: true

```
</details>