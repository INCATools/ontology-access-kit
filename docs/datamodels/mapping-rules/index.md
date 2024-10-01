# Mapping Rules Datamodel

A datamodel for specifying lexical mapping rules. Rules consist of *preconditions* which are used to match elements to match on, and *postconditions* which are used to generate new elements. Each rule can be assigned a *weight*, these weights are summed and then a logit function applied to obtain an SSSOM-compatible confidence score.

URI: https://w3id.org/oak/mapping-rules-datamodel

Name: mapping-rules-datamodel



## Classes

| Class | Description |
| --- | --- |
| [Activity](Activity.md) | Generic grouping for any lexical operation |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transformed string |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fashion |
| [Any](Any.md) | None |
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term |
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit |
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are applied |
| [MappingRuleCollection](MappingRuleCollection.md) | A collection of mapping rules |
| [Postcondition](Postcondition.md) | None |
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping |
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term |
| [RuleSet](RuleSet.md) | A set of rules for generating synonyms or alternate lexical elements. |
| [Synonymizer](Synonymizer.md) | Specification of a rule for generating a synonym or alternate lexical element. |
| [Test](Test.md) | A unit test for a rule, specifies an intended output for an input |



## Slots

| Slot | Description |
| --- | --- |
| [description](description.md) |  |
| [element](element.md) |  |
| [element_term](element_term.md) | the original term used in the element |
| [groupings](groupings.md) | all groupings |
| [in_place](in_place.md) | Whether the rule is applied in place or not |
| [input](input.md) | Input string for the rule |
| [mapping_source_one_of](mapping_source_one_of.md) | The source of the mapping to be matched |
| [match](match.md) | Reg-ex rule to match substrings in labels |
| [match_scope](match_scope.md) | Synonym scope of the reg-ex rule, e |
| [minimum_confidence](minimum_confidence.md) |  |
| [name](name.md) |  |
| [object_match_field_one_of](object_match_field_one_of.md) | The field in the object to be matched |
| [object_source_one_of](object_source_one_of.md) | The source of the object to be matched |
| [oneway](oneway.md) | if true then subject and object can be switched and predicate inverted |
| [output](output.md) | Output based on the rule |
| [params](params.md) | Any parameters to be applied to the transformation algorithm |
| [pipeline](pipeline.md) |  |
| [pipelines](pipelines.md) | all pipelines used to build the index |
| [postconditions](postconditions.md) | conditions that apply if preconditions match |
| [preconditions](preconditions.md) | all of the criteria that must be true before a rule is fired |
| [predicate](predicate.md) |  |
| [predicate_id](predicate_id.md) | The predicate that is inferred |
| [predicate_id_one_of](predicate_id_one_of.md) | The predicate to be matched |
| [prefix](prefix.md) | The prefix that qualifies for the rule |
| [qualifier](qualifier.md) | Type of match for the new synonym generated |
| [relationships](relationships.md) | All ontology elements grouped and their relationship to the normalized term |
| [replacement](replacement.md) | Reg-ex rule to replace substrings in labels |
| [rules](rules.md) | all rules |
| [source](source.md) |  |
| [subject_match_field_one_of](subject_match_field_one_of.md) | The field in the subject to be matched |
| [subject_source_one_of](subject_source_one_of.md) | The source of the subject to be matched |
| [synonymized](synonymized.md) |  |
| [synonymizer](synonymizer.md) | Normalizing rules to labels |
| [term](term.md) | A normalized term that groups ontology elements |
| [tests](tests.md) | Unit tests for each rules |
| [transformations](transformations.md) |  |
| [transformations_included_in](transformations_included_in.md) |  |
| [type](type.md) | The type of transformation |
| [weight](weight.md) | Weighting of the rule |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to |


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
| [RegularExpressionString](RegularExpressionString.md) |  |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
