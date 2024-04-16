

# Class: Axiom


_A logical or non-logical statement_





URI: [owl:Axiom](http://www.w3.org/2002/07/owl#Axiom)




```{mermaid}
 classDiagram
    class Axiom
      Axiom : annotatedProperty
        
          Axiom --> AnnotationProperty : annotatedProperty
        
      Axiom : annotatedSource
        
          Axiom --> NamedObject : annotatedSource
        
      Axiom : annotatedTarget
        
          Axiom --> Any : annotatedTarget
        
      Axiom : annotations
        
          Axiom --> Annotation : annotations
        
      Axiom : comment
        
      Axiom : created_by
        
      Axiom : database_cross_reference
        
      Axiom : date_retrieved
        
      Axiom : evidence
        
      Axiom : external_ontology
        
      Axiom : has_axiom_label
        
          Axiom --> Thing : has_axiom_label
        
      Axiom : has_exact_synonym
        
      Axiom : has_synonym_type
        
          Axiom --> AnnotationProperty : has_synonym_type
        
      Axiom : is_a_defining_property_chain_axiom
        
      Axiom : is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
        
      Axiom : is_inferred
        
      Axiom : label
        
      Axiom : notes
        
      Axiom : seeAlso
        
          Axiom --> Thing : seeAlso
        
      Axiom : source
        
      Axiom : url
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [annotatedProperty](annotatedProperty.md) | 0..1 <br/> [AnnotationProperty](AnnotationProperty.md) |  | direct |
| [annotatedSource](annotatedSource.md) | 0..1 <br/> [NamedObject](NamedObject.md) |  | direct |
| [annotatedTarget](annotatedTarget.md) | 0..1 <br/> [Any](Any.md) |  | direct |
| [annotations](annotations.md) | 0..* <br/> [Annotation](Annotation.md) |  | direct |
| [source](source.md) | 0..* <br/> [String](String.md) |  | direct |
| [is_inferred](is_inferred.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [notes](notes.md) | 0..* <br/> [String](String.md) |  | direct |
| [url](url.md) | 0..1 <br/> [String](String.md) |  | direct |
| [has_axiom_label](has_axiom_label.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) | 0..1 <br/> [String](String.md) |  | direct |
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) | 0..1 <br/> [String](String.md) |  | direct |
| [created_by](created_by.md) | 0..1 <br/> [String](String.md) |  | direct |
| [date_retrieved](date_retrieved.md) | 0..1 <br/> [String](String.md) |  | direct |
| [evidence](evidence.md) | 0..1 <br/> [String](String.md) |  | direct |
| [external_ontology](external_ontology.md) | 0..* <br/> [String](String.md) |  | direct |
| [database_cross_reference](database_cross_reference.md) | 0..* <br/> [CURIELiteral](CURIELiteral.md) | Uses to indicate the source of an axiom | direct |
| [has_exact_synonym](has_exact_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | direct |
| [has_synonym_type](has_synonym_type.md) | 0..* <br/> [AnnotationProperty](AnnotationProperty.md) |  | direct |
| [comment](comment.md) | 0..* <br/> [String](String.md) |  | direct |
| [label](label.md) | 0..1 <br/> [LabelType](LabelType.md) |  | direct |
| [seeAlso](seeAlso.md) | 0..* <br/> [Thing](Thing.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Axiom |
| native | omoschema:Axiom |
| exact | rdf:Statement |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Axiom
description: A logical or non-logical statement
from_schema: https://w3id.org/oak/ontology-metadata
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
    domain_of:
    - HasMappings
    - Axiom
class_uri: owl:Axiom
represents_relationship: true

```
</details>

### Induced

<details>
```yaml
name: Axiom
description: A logical or non-logical statement
from_schema: https://w3id.org/oak/ontology-metadata
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
    domain_of:
    - HasMappings
    - Axiom
attributes:
  annotatedProperty:
    name: annotatedProperty
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - rdf:predicate
    rank: 1000
    is_a: reification_predicate
    slot_uri: owl:annotatedProperty
    alias: annotatedProperty
    owner: Axiom
    domain_of:
    - Axiom
    relational_role: PREDICATE
    range: AnnotationProperty
  annotatedSource:
    name: annotatedSource
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - rdf:subject
    rank: 1000
    is_a: reification_predicate
    slot_uri: owl:annotatedSource
    alias: annotatedSource
    owner: Axiom
    domain_of:
    - Axiom
    relational_role: SUBJECT
    range: NamedObject
  annotatedTarget:
    name: annotatedTarget
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - rdf:object
    rank: 1000
    is_a: reification_predicate
    slot_uri: owl:annotatedTarget
    alias: annotatedTarget
    owner: Axiom
    domain_of:
    - Axiom
    relational_role: OBJECT
    range: Any
  annotations:
    name: annotations
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    multivalued: true
    alias: annotations
    owner: Axiom
    domain_of:
    - Axiom
    range: Annotation
  source:
    name: source
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:source
    multivalued: true
    alias: source
    owner: Axiom
    domain_of:
    - Ontology
    - Axiom
    range: string
  is_inferred:
    name: is_inferred
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:is_inferred
    alias: is_inferred
    owner: Axiom
    domain_of:
    - Axiom
    range: boolean
  notes:
    name: notes
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:notes
    multivalued: true
    alias: notes
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  url:
    name: url
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:url
    alias: url
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  has_axiom_label:
    name: has_axiom_label
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0010000
    alias: has_axiom_label
    owner: Axiom
    domain_of:
    - Axiom
    range: Thing
  is_a_defining_property_chain_axiom:
    name: is_a_defining_property_chain_axiom
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: RO:0002581
    alias: is_a_defining_property_chain_axiom
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  is_a_defining_property_chain_axiom_where_second_argument_is_reflexive:
    name: is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: RO:0002582
    alias: is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: creator
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: Axiom
    domain_of:
    - HasProvenance
    - Axiom
    range: string
  date_retrieved:
    name: date_retrieved
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:date_retrieved
    alias: date_retrieved
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  evidence:
    name: evidence
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:evidence
    alias: evidence
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  external_ontology:
    name: external_ontology
    deprecated: deprecated oboInOwl property
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:external_ontology
    multivalued: true
    alias: external_ontology
    owner: Axiom
    domain_of:
    - Axiom
    range: string
  database_cross_reference:
    name: database_cross_reference
    description: Uses to indicate the source of an axiom
    in_subset:
    - go permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - dcterms:source
    rank: 1000
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: Axiom
    domain_of:
    - HasMappings
    - Axiom
    range: CURIELiteral
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: Axiom
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
  has_synonym_type:
    name: has_synonym_type
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasSynonymType
    multivalued: true
    alias: has_synonym_type
    owner: Axiom
    domain_of:
    - Axiom
    range: AnnotationProperty
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
    owner: Axiom
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
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
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: Axiom
    domain_of:
    - HasMinimalMetadata
    - Axiom
    range: label type
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: Axiom
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
class_uri: owl:Axiom
represents_relationship: true

```
</details>