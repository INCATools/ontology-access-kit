# Semantic Similarity

A datamodel for representing semantic similarity between terms or lists of terms.

URI: https://w3id.org/oak/similarity

Name: similarity



## Classes

| Class | Description |
| --- | --- |
| [BestMatch](BestMatch.md) | None |
| [PairwiseSimilarity](PairwiseSimilarity.md) | Abstract grouping for representing individual pairwise similarities |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | A simple pairwise similarity between two sets of concepts/terms |
| [TermInfo](TermInfo.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [ancestor_id](ancestor_id.md) | the most recent common ancestor of the two compared entities |
| [ancestor_information_content](ancestor_information_content.md) | The IC of the object |
| [ancestor_label](ancestor_label.md) | the name or label of the ancestor concept |
| [ancestor_source](ancestor_source.md) |  |
| [average_score](average_score.md) |  |
| [best_score](best_score.md) |  |
| [cosine_similarity](cosine_similarity.md) | the dot product of two node embeddings divided by the product of their length... |
| [dice_similarity](dice_similarity.md) |  |
| [id](id.md) |  |
| [information_content](information_content.md) | The IC is the negative log of the probability of the concept |
| [intersection_count](intersection_count.md) |  |
| [jaccard_similarity](jaccard_similarity.md) | The number of concepts in the intersection divided by the number in the union |
| [label](label.md) |  |
| [match_source](match_source.md) |  |
| [match_source_label](match_source_label.md) |  |
| [match_subsumer](match_subsumer.md) |  |
| [match_subsumer_label](match_subsumer_label.md) |  |
| [match_target](match_target.md) | the entity matches |
| [match_target_label](match_target_label.md) |  |
| [metric](metric.md) |  |
| [object_best_matches](object_best_matches.md) |  |
| [object_id](object_id.md) | The second of the two entities being compared |
| [object_information_content](object_information_content.md) | The IC of the object |
| [object_label](object_label.md) | the label or name for the second entity |
| [object_source](object_source.md) | the source for the second entity |
| [object_termset](object_termset.md) |  |
| [overlap_coefficient](overlap_coefficient.md) |  |
| [phenodigm_score](phenodigm_score.md) | the geometric mean of the jaccard similarity and the information content |
| [score](score.md) | Abstract base slot for different kinds of scores |
| [similarity](similarity.md) |  |
| [subject_best_matches](subject_best_matches.md) |  |
| [subject_id](subject_id.md) | The first of the two entities being compared |
| [subject_information_content](subject_information_content.md) | The IC of the subject |
| [subject_label](subject_label.md) | the label or name for the first entity |
| [subject_source](subject_source.md) | the source for the first entity |
| [subject_termset](subject_termset.md) |  |
| [subsumed_by_score](subsumed_by_score.md) |  |
| [subsumes_score](subsumes_score.md) |  |
| [union_count](union_count.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |


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
| [ItemCount](ItemCount.md) |  |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [NegativeLogValue](NegativeLogValue.md) |  |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [NonNegativeFloat](NonNegativeFloat.md) |  |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |
| [ZeroToOne](ZeroToOne.md) |  |


## Subsets

| Subset | Description |
| --- | --- |
