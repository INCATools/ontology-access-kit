# lexical-index

A datamodel for representing a lexical index of an ontology. A lexical index is keyed by optionally normalized terms.

URI: https://w3id.org/linkml/lexical_index

## Classes

| Class | Description |
| --- | --- |
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit | 
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term | 
| [RelationshipToTerm](RelationshipToTerm.md) | A relationship of an ontology element to a lexical term | 
| [Activity](Activity.md) | Generic grouping for any lexical operation | 
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | A collection of atomic lexical transformations that are applied in serial fashion | 
| [LexicalTransformation](LexicalTransformation.md) | An atomic lexical transformation applied on a term (string) yielding a transformed string | 


## Slots

| Slot | Description |
| --- | --- |
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

