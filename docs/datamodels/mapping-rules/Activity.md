# Class: Activity
_Generic grouping for any lexical operation_



* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [prov:Activity](http://www.w3.org/ns/prov#Activity)



```{mermaid}
 classDiagram
    class Activity
      Activity <|-- LexicalTransformationPipeline
      Activity <|-- LexicalTransformation
      
      
```





## Inheritance
* **Activity**
    * [LexicalTransformationPipeline](LexicalTransformationPipeline.md)
    * [LexicalTransformation](LexicalTransformation.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:Activity |
| native | mappingrules:Activity |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Activity
description: Generic grouping for any lexical operation
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
abstract: true
class_uri: prov:Activity

```
</details>

### Induced

<details>
```yaml
name: Activity
description: Generic grouping for any lexical operation
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
abstract: true
class_uri: prov:Activity

```
</details>