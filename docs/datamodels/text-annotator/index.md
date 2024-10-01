# Text Annotator Datamodel

A datamodel for representing the results of textual named entity recognition annotation results. This draws upon both SSSOM and https://www.w3.org/TR/annotation-model/

URI: https://w3id.org/oak/text_annotator

Name: text-annotator



## Classes

| Class | Description |
| --- | --- |
| [HasSpan](HasSpan.md) | None |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |
| [TextAnnotationConfiguration](TextAnnotationConfiguration.md) | configuration for search |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | A collection of annotation results |
| [TextualElement](TextualElement.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [annotations](annotations.md) | all annotations |
| [categories](categories.md) | A list of named entity categories to include |
| [confidence](confidence.md) |  |
| [id](id.md) |  |
| [include_aliases](include_aliases.md) | If true, then the aliases (synonyms) of the matched entity are included in th... |
| [info](info.md) |  |
| [is_longest_match](is_longest_match.md) |  |
| [limit](limit.md) | The maximum number of annotations to return |
| [match_string](match_string.md) |  |
| [match_type](match_type.md) |  |
| [matches_whole_text](matches_whole_text.md) | If true, then only grounding is performed, and the entire text is used as the... |
| [model](model.md) | The name of the model to use for annotation |
| [object_aliases](object_aliases.md) |  |
| [object_categories](object_categories.md) |  |
| [object_id](object_id.md) |  |
| [object_label](object_label.md) |  |
| [object_source](object_source.md) |  |
| [parent_document](parent_document.md) |  |
| [predicate_id](predicate_id.md) |  |
| [source_text](source_text.md) |  |
| [sources](sources.md) |  |
| [subject_end](subject_end.md) |  |
| [subject_label](subject_label.md) | The portion of the subject text that is matched, ranging from subject_start t... |
| [subject_source](subject_source.md) |  |
| [subject_start](subject_start.md) |  |
| [subject_text_id](subject_text_id.md) |  |
| [text](text.md) |  |
| [token_exclusion_list](token_exclusion_list.md) | A list of tokens to exclude from the annotation process |


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
| [Position](Position.md) |  |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
