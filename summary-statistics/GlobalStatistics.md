# Class: GlobalStatistics
_summary statistics for the entire resource_




URI: [reporting:GlobalStatistics](https://w3id.org/linkml/reportGlobalStatistics)


```{mermaid}
 classDiagram
    class GlobalStatistics
      SummaryStatisticCollection <|-- GlobalStatistics
      
      GlobalStatistics : annotation_property_count
      GlobalStatistics : anonymous_class_expression_count
      GlobalStatistics : anonymous_individual_count
      GlobalStatistics : by_category
      GlobalStatistics : by_ontology
      GlobalStatistics : by_subset
      GlobalStatistics : by_taxon
      GlobalStatistics : class_count
      GlobalStatistics : class_count_by_category
      GlobalStatistics : class_count_with_text_definitions
      GlobalStatistics : class_count_without_text_definitions
      GlobalStatistics : datatype_property_count
      GlobalStatistics : deprecated_class_count
      GlobalStatistics : deprecated_object_property_count
      GlobalStatistics : description_logic_profile
      GlobalStatistics : distinct_synonym_count
      GlobalStatistics : edge_count_by_predicate
      GlobalStatistics : entailed_edge_count_by_predicate
      GlobalStatistics : equivalent_classes_axiom_count
      GlobalStatistics : individual_count
      GlobalStatistics : mapping_count
      GlobalStatistics : mapping_statement_count_by_predicate
      GlobalStatistics : named_individual_count
      GlobalStatistics : non_deprecated_class_count
      GlobalStatistics : non_deprecated_object_property_count
      GlobalStatistics : object_property_count
      GlobalStatistics : ontology_count
      GlobalStatistics : owl_axiom_count
      GlobalStatistics : property_count
      GlobalStatistics : rdf_triple_count
      GlobalStatistics : subclass_of_axiom_count
      GlobalStatistics : synonym_statement_count
      GlobalStatistics : synonym_statement_count_by_predicate
      GlobalStatistics : unsatisfiable_class_count
      GlobalStatistics : untyped_entity_count
      
```




## Inheritance
* [SummaryStatisticCollection](SummaryStatisticCollection.md)
    * **GlobalStatistics**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [by_category](by_category.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md) | statistics keyed by category | direct |
| [by_taxon](by_taxon.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md) | statistics keyed by organism taxon | direct |
| [by_ontology](by_ontology.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md) | statistics keyed by ontology | direct |
| [by_subset](by_subset.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md) | statistics keyed by ontology subset | direct |
| [deprecated_object_property_count](deprecated_object_property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [description_logic_profile](description_logic_profile.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [non_deprecated_class_count](non_deprecated_class_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [anonymous_individual_count](anonymous_individual_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | 0..* <br/> [FacetedCount](FacetedCount.md) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [class_count_with_text_definitions](class_count_with_text_definitions.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [class_count_by_category](class_count_by_category.md) | 0..* <br/> [FacetedCount](FacetedCount.md) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [object_property_count](object_property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [owl_axiom_count](owl_axiom_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [named_individual_count](named_individual_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [untyped_entity_count](untyped_entity_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [edge_count_by_predicate](edge_count_by_predicate.md) | 0..* <br/> [FacetedCount](FacetedCount.md) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [class_count_without_text_definitions](class_count_without_text_definitions.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [distinct_synonym_count](distinct_synonym_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [property_count](property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [equivalent_classes_axiom_count](equivalent_classes_axiom_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [datatype_property_count](datatype_property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | 0..* <br/> [FacetedCount](FacetedCount.md) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [rdf_triple_count](rdf_triple_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [synonym_statement_count](synonym_statement_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [non_deprecated_object_property_count](non_deprecated_object_property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [individual_count](individual_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [class_count](class_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [ontology_count](ontology_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [annotation_property_count](annotation_property_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [mapping_count](mapping_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [deprecated_class_count](deprecated_class_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | 0..* <br/> [FacetedCount](FacetedCount.md) |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | 0..1 <br/> NONE |  | [SummaryStatisticCollection](SummaryStatisticCollection.md) |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | reporting:GlobalStatistics |
| native | reporting:GlobalStatistics |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: SummaryStatisticCollection
attributes:
  by_category:
    name: by_category
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_taxon:
    name: by_taxon
    description: statistics keyed by organism taxon
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_ontology:
    name: by_ontology
    description: statistics keyed by ontology
    comments:
    - if a large ontology collection like OntoBee is indexed then it makes sense to
      break stats into each sub-ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_subset:
    name: by_subset
    description: statistics keyed by ontology subset
    comments:
    - For example, GO metagenomics_slim
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: SummaryStatisticCollection
attributes:
  by_category:
    name: by_category
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_category
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_taxon:
    name: by_taxon
    description: statistics keyed by organism taxon
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_taxon
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_ontology:
    name: by_ontology
    description: statistics keyed by ontology
    comments:
    - if a large ontology collection like OntoBee is indexed then it makes sense to
      break stats into each sub-ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_ontology
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_subset:
    name: by_subset
    description: statistics keyed by ontology subset
    comments:
    - For example, GO metagenomics_slim
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_subset
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    range: integer
  description_logic_profile:
    name: description_logic_profile
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    alias: description_logic_profile
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
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
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    range: integer

```
</details>