# Summary Statistics Datamodel

A datamodel for reports on data

URI: https://w3id.org/oak/summary_statistics

Name: summary-statistics



## Classes

| Class | Description |
| --- | --- |
| [Agent](Agent.md) | An agent |
| [ChangeTypeStatistic](ChangeTypeStatistic.md) | statistics for a particular kind of diff |
| [ContributorRole](ContributorRole.md) | A role that a contributor can have |
| [ContributorStatistics](ContributorStatistics.md) | Statistics for a contributor |
| [FacetedCount](FacetedCount.md) | Counts broken down by a facet |
| [Ontology](Ontology.md) | An ontology |
| [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | An activity that calculates summary statistics for an ontology |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | abstract base class for all summary statistics reports |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GroupedStatistics](GroupedStatistics.md) | summary statistics for the entire resource |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |



## Slots

| Slot | Description |
| --- | --- |
| [acted_on_behalf_of](acted_on_behalf_of.md) | the agent that the activity acted on behalf of |
| [agents](agents.md) | Agents that contributed to the report |
| [annotation_property_count](annotation_property_count.md) | Number of annotation properties (metadata properties) in the ontology or subs... |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | Number of anonymous class expressions in the ontology or subset |
| [anonymous_individual_count](anonymous_individual_count.md) | Number of anonymous individuals in the ontology or subset |
| [change_summary](change_summary.md) | Summary of changes between two versions of an ontology |
| [class_count](class_count.md) | Number of classes in the ontology or subset |
| [class_count_by_category](class_count_by_category.md) | Number of classes grouped by category in the ontology or subset |
| [class_count_by_subset](class_count_by_subset.md) | Number of classes grouped by subset (slim, value set) in the ontology or subs... |
| [class_count_with_text_definitions](class_count_with_text_definitions.md) | Number of classes with text definitions in the ontology or subset |
| [class_count_without_text_definitions](class_count_without_text_definitions.md) | Number of classes without text definitions in the ontology or subset |
| [class_statistic_group](class_statistic_group.md) |  |
| [compared_with](compared_with.md) | For diffs, the ontologies being compared against |
| [contributor_id](contributor_id.md) | the contributor |
| [contributor_name](contributor_name.md) | the name of the contributor |
| [contributor_summary](contributor_summary.md) |  |
| [count_statistic](count_statistic.md) |  |
| [datatype_property_count](datatype_property_count.md) | Number of datatype properties in the ontology or subset |
| [deprecated_class_count](deprecated_class_count.md) | Number of deprecated (obsoleted) classes in the ontology or subset |
| [deprecated_object_property_count](deprecated_object_property_count.md) | Number of deprecated (obsoleted) object properties in the ontology or subset |
| [description](description.md) | a description of the resource |
| [description_logic_profile](description_logic_profile.md) | Description logic profile (e |
| [distinct_synonym_count](distinct_synonym_count.md) | Number of distinct synonym strings in the ontology or subset |
| [edge_count_by_predicate](edge_count_by_predicate.md) | Number of edges grouped by predicate in the ontology or subset |
| [ended_at_time](ended_at_time.md) | the time at which the activity ended |
| [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | Number of entailed (includes indirect) edges grouped by predicate in the onto... |
| [equivalent_classes_axiom_count](equivalent_classes_axiom_count.md) | Number of equivalent classes axioms in the ontology or subset |
| [facet](facet.md) | the facet used to group the counts |
| [filtered_count](filtered_count.md) | the number of items in the facet |
| [id](id.md) | Unique handle for this report |
| [individual_count](individual_count.md) | Number of individuals (named and anonymous) in the ontology or subset |
| [individual_statistic_group](individual_statistic_group.md) |  |
| [label](label.md) | the label for the agent |
| [mapping_count](mapping_count.md) | Number of mappings (including xrefs) in the ontology or subset |
| [mapping_statement_count_by_object_source](mapping_statement_count_by_object_source.md) | Number of mappings grouped by object_source (prefix of external vocabulary) i... |
| [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | Number of mappings grouped by predicate (e |
| [mapping_statement_count_subject_by_object_source](mapping_statement_count_subject_by_object_source.md) | Number of distinct subject entities grouped by object_source (prefix of exter... |
| [merged_class_count](merged_class_count.md) | Number of merged classes (obsoletions with merge reason) in the ontology or s... |
| [metadata_statistic_group](metadata_statistic_group.md) |  |
| [named_individual_count](named_individual_count.md) | Number of named individuals in the ontology or subset |
| [non_deprecated_class_count](non_deprecated_class_count.md) | Number of non-deprecated (non-obsoleted) classes in the ontology or subset |
| [non_deprecated_object_property_count](non_deprecated_object_property_count.md) | Number of non-deprecated (non-obsoleted) object properties in the ontology or... |
| [normalization_comments](normalization_comments.md) | if contributor name normalization was applied, provide details here |
| [object_property_count](object_property_count.md) | Number of object properties (relations) in the ontology or subset |
| [ontologies](ontologies.md) | Ontology for which the statistics are computed |
| [ontology_count](ontology_count.md) | Number of ontologies (including imports) for the ontology or subset |
| [owl_axiom_count](owl_axiom_count.md) | Number of OWL axioms in the ontology or subset |
| [owl_statistic_group](owl_statistic_group.md) |  |
| [partitions](partitions.md) | statistics grouped by a particular property |
| [prefix](prefix.md) | the prefix for the ontology |
| [property_count](property_count.md) | Number of properties in the ontology or subset |
| [property_statistic_group](property_statistic_group.md) |  |
| [rdf_triple_count](rdf_triple_count.md) | Number of RDF triples in the ontology or subset |
| [role_counts](role_counts.md) |  |
| [started_at_time](started_at_time.md) | the time at which the activity started |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | Number of subclass axioms in the ontology or subset |
| [subset_count](subset_count.md) | Number of distinct subsets (slims, value sets) in the ontology or subset |
| [synonym_statement_count](synonym_statement_count.md) | Number of synonym statements (assertions) in the ontology or subset |
| [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | Number of synonym statements (assertions) grouped by predicate (scope) in the... |
| [title](title.md) | the title of the resource |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | Number of unsatisfiable classes in the ontology or subset |
| [untyped_entity_count](untyped_entity_count.md) | Number of entities whose type could not be determined in the ontology or subs... |
| [version](version.md) | the version of the resource |
| [version_info](version_info.md) | the version info of the resource |
| [was_associated_with](was_associated_with.md) | the agent that was associated with the activity |
| [was_generated_by](was_generated_by.md) | The process that generated the report |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
