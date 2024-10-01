

# Class: PairwiseSimilarity


_Abstract grouping for representing individual pairwise similarities_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [sim:PairwiseSimilarity](https://w3id.org/linkml/similarity/PairwiseSimilarity)






```{mermaid}
 classDiagram
    class PairwiseSimilarity
    click PairwiseSimilarity href "../PairwiseSimilarity"
      PairwiseSimilarity <|-- TermPairwiseSimilarity
        click TermPairwiseSimilarity href "../TermPairwiseSimilarity"
      PairwiseSimilarity <|-- TermSetPairwiseSimilarity
        click TermSetPairwiseSimilarity href "../TermSetPairwiseSimilarity"
      
      
```





## Inheritance
* **PairwiseSimilarity**
    * [TermPairwiseSimilarity](TermPairwiseSimilarity.md)
    * [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:PairwiseSimilarity |
| native | sim:PairwiseSimilarity |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PairwiseSimilarity
description: Abstract grouping for representing individual pairwise similarities
from_schema: https://w3id.org/oak/similarity
abstract: true

```
</details>

### Induced

<details>
```yaml
name: PairwiseSimilarity
description: Abstract grouping for representing individual pairwise similarities
from_schema: https://w3id.org/oak/similarity
abstract: true

```
</details>