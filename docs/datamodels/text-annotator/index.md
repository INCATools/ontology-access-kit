# Text Annotator Datamodel

A datamodel for representing the results of textual named entity recognition annotation results. This draws upon both SSSOM and https://www.w3.org/TR/annotation-model/

URI: https://w3id.org/linkml/text_annotator
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
| [confidence](confidence.md) | None |
| [id](id.md) | None |
| [info](info.md) | None |
| [is_longest_match](is_longest_match.md) | None |
| [limit](limit.md) | None |
| [match_string](match_string.md) | None |
| [match_type](match_type.md) | None |
| [matches_whole_text](matches_whole_text.md) | None |
| [object_id](object_id.md) | None |
| [object_label](object_label.md) | None |
| [object_source](object_source.md) | None |
| [parent_document](parent_document.md) | None |
| [predicate_id](predicate_id.md) | None |
| [source_text](source_text.md) | None |
| [sources](sources.md) | None |
| [subject_end](subject_end.md) | None |
| [subject_label](subject_label.md) | The portion of the subject text that is matched, ranging from subject_start to subject_end |
| [subject_source](subject_source.md) | None |
| [subject_start](subject_start.md) | None |
| [subject_text_id](subject_text_id.md) | None |
| [text](text.md) | None |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [TransformationType](TransformationType.md) | A controlled datamodels of the types of transformation that can be applied to |


## Subsets

| Subset | Description |
| --- | --- |
