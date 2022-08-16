# Semantic Similarity

A datamodel for representing semantic similarity between terms or lists of terms.

URI: https://w3id.org/linkml/similarity
Name: similarity

## Classes

| Class | Description |
| --- | --- |
| [PairwiseSimilarity](PairwiseSimilarity.md) | Abstract grouping for representing individual pairwise similarities |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |
| [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | A simple pairwise similarity between two sets of concepts/terms |


## Slots

| Slot | Description |
| --- | --- |
| [ancestor_id](ancestor_id.md) | the most recent common ancestor of the two compared entities. If there are multiple MRCAs then the most informative one is selected |
| [ancestor_information_content](ancestor_information_content.md) | The IC of the object |
| [ancestor_label](ancestor_label.md) | the name or label of the ancestor concept |
| [ancestor_source](ancestor_source.md) | None |
| [dice_similarity](dice_similarity.md) | None |
| [information_content](information_content.md) | The IC is the negative log of the probability of the concept |
| [intersection_count](intersection_count.md) | None |
| [jaccard_similarity](jaccard_similarity.md) | The number of concepts in the intersection divided by the number in the union |
| [object_id](object_id.md) | The second of the two entities being compared |
| [object_information_content](object_information_content.md) | The IC of the object |
| [object_label](object_label.md) | the label or name for the second entity |
| [object_source](object_source.md) | the source for the second entity |
| [overlap_coefficient](overlap_coefficient.md) | None |
| [phenodigm_score](phenodigm_score.md) | the geometric mean of the jaccard similarity and the information content |
| [score](score.md) | Abstract base slot for different kinds of scores |
| [subject_id](subject_id.md) | The first of the two entities being compared |
| [subject_information_content](subject_information_content.md) | The IC of the subject |
| [subject_label](subject_label.md) | the label or name for the first entity |
| [subject_source](subject_source.md) | the source for the first entity |
| [subsumed_by_score](subsumed_by_score.md) | None |
| [subsumes_score](subsumes_score.md) | None |
| [union_count](union_count.md) | None |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
