# mapping-rules

A datamodel for specifying lexical mapping rules. NOTE -- this may move to another package

URI: https://w3id.org/linkml/mapping_rules_datamodel

## Classes

| Class | Description |
| --- | --- |
| [MappingRuleCollection](MappingRuleCollection.md) | A collection of mapping rules | 
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are applied | 
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping | 
| [Postcondition](Postcondition.md) | None | 
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit | 
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term | 
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term | 
| [Activity](Activity.md) | Generic grouping for any lexical operation | 
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fashion | 
| [LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transformed string | 


## Slots

| Slot | Description |
| --- | --- |
| [rules](rules.md) | all rules | 
| [minimum_confidence](minimum_confidence.md) | None | 
| [description](description.md) | None | 
| [oneway](oneway.md) | if true then subject and object can be switched and predicate inverted | 
| [preconditions](preconditions.md) | all of the criteria that must be true before a rule is fired | 
| [postconditions](postconditions.md) | conditions that apply if preconditions match | 
| [subject_source_one_of](subject_source_one_of.md) | None | 
| [object_source_one_of](object_source_one_of.md) | None | 
| [mapping_source_one_of](mapping_source_one_of.md) | None | 
| [subject_match_field_one_of](subject_match_field_one_of.md) | None | 
| [object_match_field_one_of](object_match_field_one_of.md) | None | 
| [transformations_included_in](transformations_included_in.md) | None | 
| [predicate_id](predicate_id.md) | None | 
| [weight](weight.md) | Weighting of the rule, positive increases the confidence, negative decreases | 
| [groupings](groupings.md) | all groupings | 
| [pipelines](pipelines.md) | all pipelines used to build the index | 
| [term](term.md) | A normalized term that groups ontology elements | 
| [relationships](relationships.md) | All ontology elements grouped and their relationship to the normalized term | 
| [predicate](predicate.md) | None | 
| [element](element.md) | None | 
| [element_term](element_term.md) | the original term used in the element | 
| [source](source.md) | None | 
| [pipeline](pipeline.md) | None | 
| [name](name.md) | None | 
| [transformations](transformations.md) | None | 
| [type](type.md) | The type of transformation | 
| [params](params.md) | Any parameters to be applied to the transformation algorithm | 


## Enums

| Enums | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to | 

