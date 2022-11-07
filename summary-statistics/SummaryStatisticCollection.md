# Class: SummaryStatisticCollection
_A summary statistics report object_




URI: [reporting:SummaryStatisticCollection](https://w3id.org/linkml/reportSummaryStatisticCollection)


```{mermaid}
 classDiagram
    class SummaryStatisticCollection
      SummaryStatisticCollection <|-- GlobalStatistics
      SummaryStatisticCollection <|-- FacetStatistics
      
      SummaryStatisticCollection : annotation_property_count
      SummaryStatisticCollection : anonymous_class_expression_count
      SummaryStatisticCollection : anonymous_individual_count
      SummaryStatisticCollection : class_count
      SummaryStatisticCollection : class_count_by_category
      SummaryStatisticCollection : class_count_with_text_definitions
      SummaryStatisticCollection : class_count_without_text_definitions
      SummaryStatisticCollection : datatype_property_count
      SummaryStatisticCollection : deprecated_class_count
      SummaryStatisticCollection : deprecated_object_property_count
      SummaryStatisticCollection : description_logic_profile
      SummaryStatisticCollection : distinct_synonym_count
      SummaryStatisticCollection : edge_count_by_predicate
      SummaryStatisticCollection : entailed_edge_count_by_predicate
      SummaryStatisticCollection : equivalent_classes_axiom_count
      SummaryStatisticCollection : individual_count
      SummaryStatisticCollection : mapping_count
      SummaryStatisticCollection : mapping_statement_count_by_predicate
      SummaryStatisticCollection : named_individual_count
      SummaryStatisticCollection : non_deprecated_class_count
      SummaryStatisticCollection : non_deprecated_object_property_count
      SummaryStatisticCollection : object_property_count
      SummaryStatisticCollection : ontology_count
      SummaryStatisticCollection : owl_axiom_count
      SummaryStatisticCollection : property_count
      SummaryStatisticCollection : rdf_triple_count
      SummaryStatisticCollection : subclass_of_axiom_count
      SummaryStatisticCollection : synonym_statement_count
      SummaryStatisticCollection : synonym_statement_count_by_predicate
      SummaryStatisticCollection : unsatisfiable_class_count
      SummaryStatisticCollection : untyped_entity_count
      
```




## Inheritance
* **SummaryStatisticCollection**
    * [GlobalStatistics](GlobalStatistics.md)
    * [FacetStatistics](FacetStatistics.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [class_count](class_count.md) | 0..1 <br/> None | None | direct |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | 0..1 <br/> None | None | direct |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | 0..1 <br/> None | None | direct |
| [deprecated_class_count](deprecated_class_count.md) | 0..1 <br/> None | None | direct |
| [non_deprecated_class_count](non_deprecated_class_count.md) | 0..1 <br/> None | None | direct |
| [class_count_with_text_definitions](class_count_with_text_definitions.md) | 0..1 <br/> None | None | direct |
| [class_count_without_text_definitions](class_count_without_text_definitions.md) | 0..1 <br/> None | None | direct |
| [property_count](property_count.md) | 0..1 <br/> None | None | direct |
| [object_property_count](object_property_count.md) | 0..1 <br/> None | None | direct |
| [deprecated_object_property_count](deprecated_object_property_count.md) | 0..1 <br/> None | None | direct |
| [non_deprecated_object_property_count](non_deprecated_object_property_count.md) | 0..1 <br/> None | None | direct |
| [datatype_property_count](datatype_property_count.md) | 0..1 <br/> None | None | direct |
| [annotation_property_count](annotation_property_count.md) | 0..1 <br/> None | None | direct |
| [individual_count](individual_count.md) | 0..1 <br/> None | None | direct |
| [named_individual_count](named_individual_count.md) | 0..1 <br/> None | None | direct |
| [anonymous_individual_count](anonymous_individual_count.md) | 0..1 <br/> None | None | direct |
| [untyped_entity_count](untyped_entity_count.md) | 0..1 <br/> None | None | direct |
| [description_logic_profile](description_logic_profile.md) | 0..1 <br/> string | None | direct |
| [owl_axiom_count](owl_axiom_count.md) | 0..1 <br/> None | None | direct |
| [rdf_triple_count](rdf_triple_count.md) | 0..1 <br/> None | None | direct |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | 0..1 <br/> None | None | direct |
| [equivalent_classes_axiom_count](equivalent_classes_axiom_count.md) | 0..1 <br/> None | None | direct |
| [edge_count_by_predicate](edge_count_by_predicate.md) | 0..* <br/> FacetedCount | None | direct |
| [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | 0..* <br/> FacetedCount | None | direct |
| [distinct_synonym_count](distinct_synonym_count.md) | 0..1 <br/> None | None | direct |
| [synonym_statement_count](synonym_statement_count.md) | 0..1 <br/> None | None | direct |
| [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | 0..* <br/> FacetedCount | None | direct |
| [class_count_by_category](class_count_by_category.md) | 0..* <br/> FacetedCount | None | direct |
| [mapping_count](mapping_count.md) | 0..1 <br/> None | None | direct |
| [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | 0..* <br/> FacetedCount | None | direct |
| [ontology_count](ontology_count.md) | 0..1 <br/> None | None | direct |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | reporting:SummaryStatisticCollection |
| native | reporting:SummaryStatisticCollection |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SummaryStatisticCollection
description: A summary statistics report object
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  class_count:
    name: class_count
    annotations:
      filter:
        tag: filter
        value: Class
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Unsatisfiable
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  deprecated_class_count:
    name: deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  non_deprecated_class_count:
    name: non_deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, NotDeprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  class_count_with_text_definitions:
    name: class_count_with_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, HasTextDefinition
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  class_count_without_text_definitions:
    name: class_count_without_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, NotHasTextDefinition
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: class_statistic_group
  property_count:
    name: property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  object_property_count:
    name: object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  deprecated_object_property_count:
    name: deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, Deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  non_deprecated_object_property_count:
    name: non_deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, NotDeprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  datatype_property_count:
    name: datatype_property_count
    annotations:
      filter:
        tag: filter
        value: DatatypeProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  annotation_property_count:
    name: annotation_property_count
    annotations:
      filter:
        tag: filter
        value: AnnotationProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: property_statistic_group
  individual_count:
    name: individual_count
    annotations:
      filter:
        tag: filter
        value: Individual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: individual_statistic_group
  named_individual_count:
    name: named_individual_count
    annotations:
      filter:
        tag: filter
        value: NamedIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: individual_statistic_group
  anonymous_individual_count:
    name: anonymous_individual_count
    annotations:
      filter:
        tag: filter
        value: AnonymousIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: individual_statistic_group
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
  description_logic_profile:
    name: description_logic_profile
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    annotations:
      filter:
        tag: filter
        value: Axiom
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: owl_statistic_group
  rdf_triple_count:
    name: rdf_triple_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: owl_statistic_group
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: owl_statistic_group
  equivalent_classes_axiom_count:
    name: equivalent_classes_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: owl_statistic_group
  edge_count_by_predicate:
    name: edge_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Edge
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  entailed_edge_count_by_predicate:
    name: entailed_edge_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: EntailedEdge
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  distinct_synonym_count:
    name: distinct_synonym_count
    annotations:
      filter:
        tag: filter
        value: Synonym
      distinct:
        tag: distinct
        value: Value
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: metadata_statistic_group
  synonym_statement_count:
    name: synonym_statement_count
    annotations:
      filter:
        tag: filter
        value: Synonym
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: metadata_statistic_group
  synonym_statement_count_by_predicate:
    name: synonym_statement_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Synonym
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  class_count_by_category:
    name: class_count_by_category
    annotations:
      filter:
        tag: filter
        value: Class
      facet:
        tag: facet
        value: Category
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  mapping_count:
    name: mapping_count
    annotations:
      filter:
        tag: filter
        value: Mapping
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    slot_group: metadata_statistic_group
  mapping_statement_count_by_predicate:
    name: mapping_statement_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  ontology_count:
    name: ontology_count
    annotations:
      filter:
        tag: filter
        value: Ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic

```
</details>

### Induced

<details>
```yaml
name: SummaryStatisticCollection
description: A summary statistics report object
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  class_count:
    name: class_count
    annotations:
      filter:
        tag: filter
        value: Class
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_class_expression_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Unsatisfiable
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: unsatisfiable_class_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  deprecated_class_count:
    name: deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: deprecated_class_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  non_deprecated_class_count:
    name: non_deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, NotDeprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: non_deprecated_class_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  class_count_with_text_definitions:
    name: class_count_with_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, HasTextDefinition
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_with_text_definitions
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  class_count_without_text_definitions:
    name: class_count_without_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, NotHasTextDefinition
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_without_text_definitions
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  property_count:
    name: property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  object_property_count:
    name: object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: object_property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  deprecated_object_property_count:
    name: deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, Deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: deprecated_object_property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  non_deprecated_object_property_count:
    name: non_deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, NotDeprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: non_deprecated_object_property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  datatype_property_count:
    name: datatype_property_count
    annotations:
      filter:
        tag: filter
        value: DatatypeProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: datatype_property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  annotation_property_count:
    name: annotation_property_count
    annotations:
      filter:
        tag: filter
        value: AnnotationProperty
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: annotation_property_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  individual_count:
    name: individual_count
    annotations:
      filter:
        tag: filter
        value: Individual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: individual_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
  named_individual_count:
    name: named_individual_count
    annotations:
      filter:
        tag: filter
        value: NamedIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: named_individual_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
  anonymous_individual_count:
    name: anonymous_individual_count
    annotations:
      filter:
        tag: filter
        value: AnonymousIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_individual_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: untyped_entity_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    range: integer
  description_logic_profile:
    name: description_logic_profile
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    alias: description_logic_profile
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    annotations:
      filter:
        tag: filter
        value: Axiom
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: owl_axiom_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  rdf_triple_count:
    name: rdf_triple_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: rdf_triple_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: subclass_of_axiom_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  equivalent_classes_axiom_count:
    name: equivalent_classes_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: equivalent_classes_axiom_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  edge_count_by_predicate:
    name: edge_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Edge
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: edge_count_by_predicate
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  entailed_edge_count_by_predicate:
    name: entailed_edge_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: EntailedEdge
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: entailed_edge_count_by_predicate
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  distinct_synonym_count:
    name: distinct_synonym_count
    annotations:
      filter:
        tag: filter
        value: Synonym
      distinct:
        tag: distinct
        value: Value
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: distinct_synonym_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count:
    name: synonym_statement_count
    annotations:
      filter:
        tag: filter
        value: Synonym
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: synonym_statement_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count_by_predicate:
    name: synonym_statement_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Synonym
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: synonym_statement_count_by_predicate
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  class_count_by_category:
    name: class_count_by_category
    annotations:
      filter:
        tag: filter
        value: Class
      facet:
        tag: facet
        value: Category
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: class_count_by_category
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  mapping_count:
    name: mapping_count
    annotations:
      filter:
        tag: filter
        value: Mapping
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: mapping_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  mapping_statement_count_by_predicate:
    name: mapping_statement_count_by_predicate
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: Predicate
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: mapping_statement_count_by_predicate
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: FacetedCount
    inlined: true
  ontology_count:
    name: ontology_count
    annotations:
      filter:
        tag: filter
        value: Ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: ontology_count
    owner: SummaryStatisticCollection
    domain_of:
    - SummaryStatisticCollection
    range: integer

```
</details>