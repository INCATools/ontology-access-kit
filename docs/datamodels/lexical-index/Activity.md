

# Class: Activity


_Generic grouping for any lexical operation_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [prov:Activity](http://www.w3.org/ns/prov#Activity)






```{mermaid}
 classDiagram
    class Activity
    click Activity href "../Activity"
      Activity <|-- LexicalTransformationPipeline
        click LexicalTransformationPipeline href "../LexicalTransformationPipeline"
      Activity <|-- LexicalTransformation
        click LexicalTransformation href "../LexicalTransformation"
      
      
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


* from schema: https://w3id.org/oak/lexical-index




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:Activity |
| native | ontolexindex:Activity |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Activity
description: Generic grouping for any lexical operation
from_schema: https://w3id.org/oak/lexical-index
abstract: true
class_uri: prov:Activity

```
</details>

### Induced

<details>
```yaml
name: Activity
description: Generic grouping for any lexical operation
from_schema: https://w3id.org/oak/lexical-index
abstract: true
class_uri: prov:Activity

```
</details>