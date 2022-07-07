# Lexical Index

A datamodel for representing a lexical index of an ontology. A lexical index is keyed by optionally normalized terms.

URI: https://w3id.org/linkml/lexical_index
Name: lexical-index

## Classes

| Class | Description |
| --- | --- |
| [Activity](Activity.md) | Generic grouping for any lexical operation |
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term |
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit |
| [LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transformed string |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fashion |
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term |


## Slots

| Slot | Description |
| --- | --- |
| [element](element.md) | None |
| [element_term](element_term.md) | the original term used in the element |
| [groupings](groupings.md) | all groupings |
| [name](name.md) | None |
| [params](params.md) | Any parameters to be applied to the transformation algorithm |
| [pipeline](pipeline.md) | None |
| [pipelines](pipelines.md) | all pipelines used to build the index |
| [predicate](predicate.md) | None |
| [relationships](relationships.md) | All ontology elements grouped and their relationship to the normalized term |
| [source](source.md) | None |
| [term](term.md) | A normalized term that groups ontology elements |
| [transformations](transformations.md) | None |
| [type](type.md) | The type of transformation |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to |


## Subsets

| Subset | Description |
| --- | --- |
