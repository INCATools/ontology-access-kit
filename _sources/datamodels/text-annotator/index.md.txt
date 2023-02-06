# Text Annotator Datamodel

A datamodel for representing the results of textual named entity recognition annotation results. This draws upon both SSSOM and https://www.w3.org/TR/annotation-model/

URI: https://w3id.org/linkml/text_annotator
Name: text-annotator



## Classes

| Class | Description |
| --- | --- |
| [HasSpan](HasSpan.md) |  |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |
| [TextAnnotationConfiguration](TextAnnotationConfiguration.md) | configuration for search |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | A collection of annotation results |
| [TextualElement](TextualElement.md) |  |


## Slots

| Slot | Description |
| --- | --- |
| [annotations](annotations.md) | all annotations |
| [confidence](confidence.md) |  |
| [id](id.md) |  |
| [include_aliases](include_aliases.md) |  |
| [info](info.md) |  |
| [is_longest_match](is_longest_match.md) |  |
| [limit](limit.md) |  |
| [match_string](match_string.md) |  |
| [match_type](match_type.md) |  |
| [matches_whole_text](matches_whole_text.md) |  |
| [model](model.md) |  |
| [object_aliases](object_aliases.md) |  |
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
| [token_exclusion_list](token_exclusion_list.md) |  |


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
| [Position](Position.md) |  |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
