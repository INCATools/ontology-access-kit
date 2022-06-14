# Mapping Rules Datamodel

A datamodel for specifying lexical mapping rules. NOTE -- this may move to another package

URI: https://w3id.org/linkml/mapping_rules_datamodel
Name: mapping-rules

## Classes

| Class | Description |
| --- | --- |
| [Activity](Activity.md) | Generic grouping for any lexical operation |
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term |
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit |
| [LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transformed string |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fashion |
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are applied |
| [MappingRuleCollection](MappingRuleCollection.md) | A collection of mapping rules |
| [Postcondition](Postcondition.md) | None |
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping |
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term |


## Slots

| Slot | Description |
| --- | --- |
| [description](description.md) | None |
| [element](element.md) | None |
| [element_term](element_term.md) | the original term used in the element |
| [groupings](groupings.md) | all groupings |
| [mapping_source_one_of](mapping_source_one_of.md) | None |
| [minimum_confidence](minimum_confidence.md) | None |
| [name](name.md) | None |
| [object_match_field_one_of](object_match_field_one_of.md) | None |
| [object_source_one_of](object_source_one_of.md) | None |
| [oneway](oneway.md) | if true then subject and object can be switched and predicate inverted |
| [params](params.md) | Any parameters to be applied to the transformation algorithm |
| [pipeline](pipeline.md) | None |
| [pipelines](pipelines.md) | all pipelines used to build the index |
| [postconditions](postconditions.md) | conditions that apply if preconditions match |
| [preconditions](preconditions.md) | all of the criteria that must be true before a rule is fired |
| [predicate](predicate.md) | None |
| [predicate_id](predicate_id.md) | None |
| [relationships](relationships.md) | All ontology elements grouped and their relationship to the normalized term |
| [rules](rules.md) | all rules |
| [source](source.md) | None |
| [subject_match_field_one_of](subject_match_field_one_of.md) | None |
| [subject_source_one_of](subject_source_one_of.md) | None |
| [term](term.md) | A normalized term that groups ontology elements |
| [transformations](transformations.md) | None |
| [transformations_included_in](transformations_included_in.md) | None |
| [type](type.md) | The type of transformation |
| [weight](weight.md) | Weighting of the rule, positive increases the confidence, negative decreases |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to |


## Subsets

| Subset | Description |
| --- | --- |
