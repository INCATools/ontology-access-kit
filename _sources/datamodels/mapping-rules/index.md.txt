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
| [LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transf... |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fas... |
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are app... |
| [MappingRuleCollection](MappingRuleCollection.md) | A collection of mapping rules |
| [Postcondition](Postcondition.md) |  |
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping |
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term |
| [Synonymizer](Synonymizer.md) |  |


## Slots

| Slot | Description |
| --- | --- |
| [description](description.md) |  |
| [element](element.md) |  |
| [element_term](element_term.md) | the original term used in the element |
| [groupings](groupings.md) | all groupings |
| [mapping_source_one_of](mapping_source_one_of.md) |  |
| [match](match.md) | Reg-ex rule to match substrings in labels |
| [match_scope](match_scope.md) | Scope of the reg-ex rule |
| [minimum_confidence](minimum_confidence.md) |  |
| [name](name.md) |  |
| [object_match_field_one_of](object_match_field_one_of.md) |  |
| [object_source_one_of](object_source_one_of.md) |  |
| [oneway](oneway.md) | if true then subject and object can be switched and predicate inverted |
| [params](params.md) | Any parameters to be applied to the transformation algorithm |
| [pipeline](pipeline.md) |  |
| [pipelines](pipelines.md) | all pipelines used to build the index |
| [postconditions](postconditions.md) | conditions that apply if preconditions match |
| [preconditions](preconditions.md) | all of the criteria that must be true before a rule is fired |
| [predicate](predicate.md) |  |
| [predicate_id](predicate_id.md) |  |
| [qualifier](qualifier.md) | Type of match for the new synonym generated |
| [relationships](relationships.md) | All ontology elements grouped and their relationship to the normalized term |
| [replacement](replacement.md) | Reg-ex rule to replace substrings in labels |
| [rules](rules.md) | all rules |
| [source](source.md) |  |
| [subject_match_field_one_of](subject_match_field_one_of.md) |  |
| [subject_source_one_of](subject_source_one_of.md) |  |
| [synonymized](synonymized.md) |  |
| [synonymizer](synonymizer.md) | Normalizing rules to labels |
| [term](term.md) | A normalized term that groups ontology elements |
| [the_rule](the_rule.md) | Description of the rule |
| [transformations](transformations.md) |  |
| [transformations_included_in](transformations_included_in.md) |  |
| [type](type.md) | The type of transformation |
| [weight](weight.md) | Weighting of the rule, positive increases the confidence, negative decreases |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to |


## Types

| Type | Description |
| --- | --- |
| [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | A binary (true or false) value |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | a compact URI |
| [xsd:date](http://www.w3.org/2001/XMLSchema#date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | The combination of a date and time |
| [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](http://www.w3.org/2001/XMLSchema#double) | A real number that conforms to the xsd:double specification |
| [xsd:float](http://www.w3.org/2001/XMLSchema#float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | An integer |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
