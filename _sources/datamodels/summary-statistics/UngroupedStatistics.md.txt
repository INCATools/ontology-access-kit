

# Class: UngroupedStatistics


_A summary statistics report object_





URI: [summary_statistics:UngroupedStatistics](https://w3id.org/oaklib/summary_statistics.UngroupedStatistics)






```{mermaid}
 classDiagram
    class UngroupedStatistics
    click UngroupedStatistics href "../UngroupedStatistics"
      SummaryStatisticsReport <|-- UngroupedStatistics
        click SummaryStatisticsReport href "../SummaryStatisticsReport"
      
      UngroupedStatistics : agents
        
          
    
    
    UngroupedStatistics --> "*" Agent : agents
    click Agent href "../Agent"

        
      UngroupedStatistics : annotation_property_count
        
      UngroupedStatistics : anonymous_class_expression_count
        
      UngroupedStatistics : anonymous_individual_count
        
      UngroupedStatistics : change_summary
        
          
    
    
    UngroupedStatistics --> "*" ChangeTypeStatistic : change_summary
    click ChangeTypeStatistic href "../ChangeTypeStatistic"

        
      UngroupedStatistics : class_count
        
      UngroupedStatistics : class_count_by_category
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : class_count_by_category
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : class_count_by_subset
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : class_count_by_subset
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : class_count_with_text_definitions
        
      UngroupedStatistics : class_count_without_text_definitions
        
      UngroupedStatistics : compared_with
        
          
    
    
    UngroupedStatistics --> "*" Ontology : compared_with
    click Ontology href "../Ontology"

        
      UngroupedStatistics : contributor_summary
        
          
    
    
    UngroupedStatistics --> "*" ContributorStatistics : contributor_summary
    click ContributorStatistics href "../ContributorStatistics"

        
      UngroupedStatistics : datatype_property_count
        
      UngroupedStatistics : deprecated_class_count
        
      UngroupedStatistics : deprecated_object_property_count
        
      UngroupedStatistics : description_logic_profile
        
      UngroupedStatistics : distinct_synonym_count
        
      UngroupedStatistics : edge_count_by_predicate
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : edge_count_by_predicate
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : entailed_edge_count_by_predicate
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : entailed_edge_count_by_predicate
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : equivalent_classes_axiom_count
        
      UngroupedStatistics : id
        
      UngroupedStatistics : individual_count
        
      UngroupedStatistics : mapping_count
        
      UngroupedStatistics : mapping_statement_count_by_object_source
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : mapping_statement_count_by_object_source
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : mapping_statement_count_by_predicate
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : mapping_statement_count_by_predicate
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : mapping_statement_count_subject_by_object_source
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : mapping_statement_count_subject_by_object_source
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : merged_class_count
        
      UngroupedStatistics : named_individual_count
        
      UngroupedStatistics : non_deprecated_class_count
        
      UngroupedStatistics : non_deprecated_object_property_count
        
      UngroupedStatistics : object_property_count
        
      UngroupedStatistics : ontologies
        
          
    
    
    UngroupedStatistics --> "*" Ontology : ontologies
    click Ontology href "../Ontology"

        
      UngroupedStatistics : ontology_count
        
      UngroupedStatistics : owl_axiom_count
        
      UngroupedStatistics : property_count
        
      UngroupedStatistics : rdf_triple_count
        
      UngroupedStatistics : subclass_of_axiom_count
        
      UngroupedStatistics : subset_count
        
      UngroupedStatistics : synonym_statement_count
        
      UngroupedStatistics : synonym_statement_count_by_predicate
        
          
    
    
    UngroupedStatistics --> "*" FacetedCount : synonym_statement_count_by_predicate
    click FacetedCount href "../FacetedCount"

        
      UngroupedStatistics : unsatisfiable_class_count
        
      UngroupedStatistics : untyped_entity_count
        
      UngroupedStatistics : was_generated_by
        
          
    
    
    UngroupedStatistics --> "0..1" SummaryStatisticsCalculationActivity : was_generated_by
    click SummaryStatisticsCalculationActivity href "../SummaryStatisticsCalculationActivity"

        
      
```





## Inheritance
* [SummaryStatisticsReport](SummaryStatisticsReport.md)
    * **UngroupedStatistics**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [class_count](class_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of classes in the ontology or subset | direct |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of anonymous class expressions in the ontology or subset | direct |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of unsatisfiable classes in the ontology or subset | direct |
| [deprecated_class_count](deprecated_class_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of deprecated (obsoleted) classes in the ontology or subset | direct |
| [non_deprecated_class_count](non_deprecated_class_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of non-deprecated (non-obsoleted) classes in the ontology or subset | direct |
| [merged_class_count](merged_class_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of merged classes (obsoletions with merge reason) in the ontology or s... | direct |
| [class_count_with_text_definitions](class_count_with_text_definitions.md) | 0..1 <br/> [Integer](Integer.md) | Number of classes with text definitions in the ontology or subset | direct |
| [class_count_without_text_definitions](class_count_without_text_definitions.md) | 0..1 <br/> [Integer](Integer.md) | Number of classes without text definitions in the ontology or subset | direct |
| [property_count](property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of properties in the ontology or subset | direct |
| [object_property_count](object_property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of object properties (relations) in the ontology or subset | direct |
| [deprecated_object_property_count](deprecated_object_property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of deprecated (obsoleted) object properties in the ontology or subset | direct |
| [non_deprecated_object_property_count](non_deprecated_object_property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of non-deprecated (non-obsoleted) object properties in the ontology or... | direct |
| [datatype_property_count](datatype_property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of datatype properties in the ontology or subset | direct |
| [annotation_property_count](annotation_property_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of annotation properties (metadata properties) in the ontology or subs... | direct |
| [individual_count](individual_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of individuals (named and anonymous) in the ontology or subset | direct |
| [named_individual_count](named_individual_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of named individuals in the ontology or subset | direct |
| [anonymous_individual_count](anonymous_individual_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of anonymous individuals in the ontology or subset | direct |
| [untyped_entity_count](untyped_entity_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of entities whose type could not be determined in the ontology or subs... | direct |
| [subset_count](subset_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of distinct subsets (slims, value sets) in the ontology or subset | direct |
| [description_logic_profile](description_logic_profile.md) | 0..1 <br/> [String](String.md) | Description logic profile (e | direct |
| [owl_axiom_count](owl_axiom_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of OWL axioms in the ontology or subset | direct |
| [rdf_triple_count](rdf_triple_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of RDF triples in the ontology or subset | direct |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of subclass axioms in the ontology or subset | direct |
| [equivalent_classes_axiom_count](equivalent_classes_axiom_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of equivalent classes axioms in the ontology or subset | direct |
| [edge_count_by_predicate](edge_count_by_predicate.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of edges grouped by predicate in the ontology or subset | direct |
| [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of entailed (includes indirect) edges grouped by predicate in the onto... | direct |
| [distinct_synonym_count](distinct_synonym_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of distinct synonym strings in the ontology or subset | direct |
| [synonym_statement_count](synonym_statement_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of synonym statements (assertions) in the ontology or subset | direct |
| [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of synonym statements (assertions) grouped by predicate (scope) in the... | direct |
| [class_count_by_subset](class_count_by_subset.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of classes grouped by subset (slim, value set) in the ontology or subs... | direct |
| [class_count_by_category](class_count_by_category.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of classes grouped by category in the ontology or subset | direct |
| [mapping_count](mapping_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of mappings (including xrefs) in the ontology or subset | direct |
| [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of mappings grouped by predicate (e | direct |
| [mapping_statement_count_by_object_source](mapping_statement_count_by_object_source.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of mappings grouped by object_source (prefix of external vocabulary) i... | direct |
| [mapping_statement_count_subject_by_object_source](mapping_statement_count_subject_by_object_source.md) | * <br/> [FacetedCount](FacetedCount.md) | Number of distinct subject entities grouped by object_source (prefix of exter... | direct |
| [ontology_count](ontology_count.md) | 0..1 <br/> [Integer](Integer.md) | Number of ontologies (including imports) for the ontology or subset | direct |
| [contributor_summary](contributor_summary.md) | * <br/> [ContributorStatistics](ContributorStatistics.md) |  | direct |
| [change_summary](change_summary.md) | * <br/> [ChangeTypeStatistic](ChangeTypeStatistic.md) | Summary of changes between two versions of an ontology | direct |
| [id](id.md) | 1 <br/> [String](String.md) | Unique handle for this report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [ontologies](ontologies.md) | * <br/> [Ontology](Ontology.md) | Ontology for which the statistics are computed | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [compared_with](compared_with.md) | * <br/> [Ontology](Ontology.md) | For diffs, the ontologies being compared against | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [was_generated_by](was_generated_by.md) | 0..1 <br/> [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | The process that generated the report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [agents](agents.md) | * <br/> [Agent](Agent.md) | Agents that contributed to the report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GroupedStatistics](GroupedStatistics.md) | [partitions](partitions.md) | range | [UngroupedStatistics](UngroupedStatistics.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:UngroupedStatistics |
| native | summary_statistics:UngroupedStatistics |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: UngroupedStatistics
description: A summary statistics report object
from_schema: https://w3id.org/oak/summary_statistics
is_a: SummaryStatisticsReport
attributes:
  class_count:
    name: class_count
    annotations:
      filter:
        tag: filter
        value: Class
    description: Number of classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    description: Number of anonymous class expressions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Unsatisfiable
    description: Number of unsatisfiable classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  deprecated_class_count:
    name: deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated
    description: Number of deprecated (obsoleted) classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  non_deprecated_class_count:
    name: non_deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, NotDeprecated
    description: Number of non-deprecated (non-obsoleted) classes in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  merged_class_count:
    name: merged_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated, Merged
    description: Number of merged classes (obsoletions with merge reason) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_with_text_definitions:
    name: class_count_with_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, HasTextDefinition
    description: Number of classes with text definitions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_without_text_definitions:
    name: class_count_without_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, NotHasTextDefinition
    description: Number of classes without text definitions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  property_count:
    name: property_count
    description: Number of properties in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  object_property_count:
    name: object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty
    description: Number of object properties (relations) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  deprecated_object_property_count:
    name: deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, Deprecated
    description: Number of deprecated (obsoleted) object properties in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  non_deprecated_object_property_count:
    name: non_deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, NotDeprecated
    description: Number of non-deprecated (non-obsoleted) object properties in the
      ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  datatype_property_count:
    name: datatype_property_count
    annotations:
      filter:
        tag: filter
        value: DatatypeProperty
    description: Number of datatype properties in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  annotation_property_count:
    name: annotation_property_count
    annotations:
      filter:
        tag: filter
        value: AnnotationProperty
    description: Number of annotation properties (metadata properties) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  individual_count:
    name: individual_count
    annotations:
      filter:
        tag: filter
        value: Individual
    description: Number of individuals (named and anonymous) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
  named_individual_count:
    name: named_individual_count
    annotations:
      filter:
        tag: filter
        value: NamedIndividual
    description: Number of named individuals in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
  anonymous_individual_count:
    name: anonymous_individual_count
    annotations:
      filter:
        tag: filter
        value: AnonymousIndividual
    description: Number of anonymous individuals in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    description: Number of entities whose type could not be determined in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    range: integer
  subset_count:
    name: subset_count
    description: Number of distinct subsets (slims, value sets) in the ontology or
      subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    range: integer
  description_logic_profile:
    name: description_logic_profile
    description: Description logic profile (e.g. OWL-EL, OWL-DL) of the ontology or
      subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    annotations:
      filter:
        tag: filter
        value: Axiom
    description: Number of OWL axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  rdf_triple_count:
    name: rdf_triple_count
    description: Number of RDF triples in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    description: Number of subclass axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  equivalent_classes_axiom_count:
    name: equivalent_classes_axiom_count
    description: Number of equivalent classes axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
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
    description: Number of edges grouped by predicate in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of entailed (includes indirect) edges grouped by predicate
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of distinct synonym strings in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count:
    name: synonym_statement_count
    annotations:
      filter:
        tag: filter
        value: Synonym
    description: Number of synonym statements (assertions) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
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
    description: Number of synonym statements (assertions) grouped by predicate (scope)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  class_count_by_subset:
    name: class_count_by_subset
    annotations:
      filter:
        tag: filter
        value: Subset
      facet:
        tag: facet
        value: Predicate
    description: Number of classes grouped by subset (slim, value set) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of classes grouped by category in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_count:
    name: mapping_count
    annotations:
      filter:
        tag: filter
        value: Mapping
    description: Number of mappings (including xrefs) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
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
    description: Number of mappings grouped by predicate (e.g. xref, skos predicate)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_statement_count_by_object_source:
    name: mapping_statement_count_by_object_source
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: ObjectSource
    description: Number of mappings grouped by object_source (prefix of external vocabulary)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_statement_count_subject_by_object_source:
    name: mapping_statement_count_subject_by_object_source
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: ObjectSource
      distinct:
        tag: distinct
        value: Subject
    description: Number of distinct subject entities grouped by object_source (prefix
      of external vocabulary) in the ontology or subset
    comments:
    - for exact or one-to-one mappings this should generally be the same as mapping_statement_count_by_object_source
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  ontology_count:
    name: ontology_count
    annotations:
      filter:
        tag: filter
        value: Ontology
    description: Number of ontologies (including imports) for the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    domain_of:
    - UngroupedStatistics
    range: integer
  contributor_summary:
    name: contributor_summary
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    range: ContributorStatistics
    multivalued: true
    inlined: true
  change_summary:
    name: change_summary
    description: Summary of changes between two versions of an ontology
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - UngroupedStatistics
    range: ChangeTypeStatistic
    multivalued: true
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: UngroupedStatistics
description: A summary statistics report object
from_schema: https://w3id.org/oak/summary_statistics
is_a: SummaryStatisticsReport
attributes:
  class_count:
    name: class_count
    annotations:
      filter:
        tag: filter
        value: Class
    description: Number of classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    description: Number of anonymous class expressions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_class_expression_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Unsatisfiable
    description: Number of unsatisfiable classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: unsatisfiable_class_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  deprecated_class_count:
    name: deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated
    description: Number of deprecated (obsoleted) classes in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: deprecated_class_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  non_deprecated_class_count:
    name: non_deprecated_class_count
    annotations:
      filter:
        tag: filter
        value: Class, NotDeprecated
    description: Number of non-deprecated (non-obsoleted) classes in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: non_deprecated_class_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  merged_class_count:
    name: merged_class_count
    annotations:
      filter:
        tag: filter
        value: Class, Deprecated, Merged
    description: Number of merged classes (obsoletions with merge reason) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: merged_class_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_with_text_definitions:
    name: class_count_with_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, HasTextDefinition
    description: Number of classes with text definitions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_with_text_definitions
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_without_text_definitions:
    name: class_count_without_text_definitions
    annotations:
      filter:
        tag: filter
        value: Class, NotHasTextDefinition
    description: Number of classes without text definitions in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_without_text_definitions
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: class_statistic_group
    range: integer
  property_count:
    name: property_count
    description: Number of properties in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  object_property_count:
    name: object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty
    description: Number of object properties (relations) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: object_property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  deprecated_object_property_count:
    name: deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, Deprecated
    description: Number of deprecated (obsoleted) object properties in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: deprecated_object_property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  non_deprecated_object_property_count:
    name: non_deprecated_object_property_count
    annotations:
      filter:
        tag: filter
        value: ObjectProperty, NotDeprecated
    description: Number of non-deprecated (non-obsoleted) object properties in the
      ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: non_deprecated_object_property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  datatype_property_count:
    name: datatype_property_count
    annotations:
      filter:
        tag: filter
        value: DatatypeProperty
    description: Number of datatype properties in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: datatype_property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  annotation_property_count:
    name: annotation_property_count
    annotations:
      filter:
        tag: filter
        value: AnnotationProperty
    description: Number of annotation properties (metadata properties) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: annotation_property_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: property_statistic_group
    range: integer
  individual_count:
    name: individual_count
    annotations:
      filter:
        tag: filter
        value: Individual
    description: Number of individuals (named and anonymous) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: individual_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
  named_individual_count:
    name: named_individual_count
    annotations:
      filter:
        tag: filter
        value: NamedIndividual
    description: Number of named individuals in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: named_individual_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
  anonymous_individual_count:
    name: anonymous_individual_count
    annotations:
      filter:
        tag: filter
        value: AnonymousIndividual
    description: Number of anonymous individuals in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_individual_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: individual_statistic_group
    range: integer
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    description: Number of entities whose type could not be determined in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: untyped_entity_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    range: integer
  subset_count:
    name: subset_count
    description: Number of distinct subsets (slims, value sets) in the ontology or
      subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: subset_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    range: integer
  description_logic_profile:
    name: description_logic_profile
    description: Description logic profile (e.g. OWL-EL, OWL-DL) of the ontology or
      subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: description_logic_profile
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    annotations:
      filter:
        tag: filter
        value: Axiom
    description: Number of OWL axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: owl_axiom_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  rdf_triple_count:
    name: rdf_triple_count
    description: Number of RDF triples in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: rdf_triple_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    description: Number of subclass axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: subclass_of_axiom_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: owl_statistic_group
    range: integer
  equivalent_classes_axiom_count:
    name: equivalent_classes_axiom_count
    description: Number of equivalent classes axioms in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: equivalent_classes_axiom_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
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
    description: Number of edges grouped by predicate in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: edge_count_by_predicate
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of entailed (includes indirect) edges grouped by predicate
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: entailed_edge_count_by_predicate
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of distinct synonym strings in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: distinct_synonym_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count:
    name: synonym_statement_count
    annotations:
      filter:
        tag: filter
        value: Synonym
    description: Number of synonym statements (assertions) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: synonym_statement_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
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
    description: Number of synonym statements (assertions) grouped by predicate (scope)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: synonym_statement_count_by_predicate
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  class_count_by_subset:
    name: class_count_by_subset
    annotations:
      filter:
        tag: filter
        value: Subset
      facet:
        tag: facet
        value: Predicate
    description: Number of classes grouped by subset (slim, value set) in the ontology
      or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: class_count_by_subset
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
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
    description: Number of classes grouped by category in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: class_count_by_category
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_count:
    name: mapping_count
    annotations:
      filter:
        tag: filter
        value: Mapping
    description: Number of mappings (including xrefs) in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: mapping_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
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
    description: Number of mappings grouped by predicate (e.g. xref, skos predicate)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: mapping_statement_count_by_predicate
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_statement_count_by_object_source:
    name: mapping_statement_count_by_object_source
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: ObjectSource
    description: Number of mappings grouped by object_source (prefix of external vocabulary)
      in the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: mapping_statement_count_by_object_source
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  mapping_statement_count_subject_by_object_source:
    name: mapping_statement_count_subject_by_object_source
    annotations:
      filter:
        tag: filter
        value: Mapping
      facet:
        tag: facet
        value: ObjectSource
      distinct:
        tag: distinct
        value: Subject
    description: Number of distinct subject entities grouped by object_source (prefix
      of external vocabulary) in the ontology or subset
    comments:
    - for exact or one-to-one mappings this should generally be the same as mapping_statement_count_by_object_source
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: mapping_statement_count_subject_by_object_source
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    slot_group: metadata_statistic_group
    range: FacetedCount
    multivalued: true
    inlined: true
  ontology_count:
    name: ontology_count
    annotations:
      filter:
        tag: filter
        value: Ontology
    description: Number of ontologies (including imports) for the ontology or subset
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: ontology_count
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    range: integer
  contributor_summary:
    name: contributor_summary
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: contributor_summary
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    range: ContributorStatistics
    multivalued: true
    inlined: true
  change_summary:
    name: change_summary
    description: Summary of changes between two versions of an ontology
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: change_summary
    owner: UngroupedStatistics
    domain_of:
    - UngroupedStatistics
    range: ChangeTypeStatistic
    multivalued: true
    inlined: true
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: id
    owner: UngroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: string
    required: true
  ontologies:
    name: ontologies
    description: Ontology for which the statistics are computed
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: ontologies
    owner: UngroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    multivalued: true
    inlined: true
    inlined_as_list: true
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: compared_with
    owner: UngroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    multivalued: true
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: was_generated_by
    owner: UngroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: SummaryStatisticsCalculationActivity
  agents:
    name: agents
    description: Agents that contributed to the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: agents
    owner: UngroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Agent
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>