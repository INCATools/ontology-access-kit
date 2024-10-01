

# Class: TextAnnotationResultSet


_A collection of annotation results_





URI: [ann:TextAnnotationResultSet](https://w3id.org/linkml/text_annotator/TextAnnotationResultSet)






```{mermaid}
 classDiagram
    class TextAnnotationResultSet
    click TextAnnotationResultSet href "../TextAnnotationResultSet"
      TextAnnotationResultSet : annotations
        
          
    
    
    TextAnnotationResultSet --> "*" TextAnnotation : annotations
    click TextAnnotation href "../TextAnnotation"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [annotations](annotations.md) | * <br/> [TextAnnotation](TextAnnotation.md) | all annotations | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:TextAnnotationResultSet |
| native | ann:TextAnnotationResultSet |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotationResultSet
description: A collection of annotation results
from_schema: https://w3id.org/oak/text_annotator
attributes:
  annotations:
    name: annotations
    description: all annotations
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationResultSet
    range: TextAnnotation
    multivalued: true
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationResultSet
description: A collection of annotation results
from_schema: https://w3id.org/oak/text_annotator
attributes:
  annotations:
    name: annotations
    description: all annotations
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: annotations
    owner: TextAnnotationResultSet
    domain_of:
    - TextAnnotationResultSet
    range: TextAnnotation
    multivalued: true
    inlined: true

```
</details>