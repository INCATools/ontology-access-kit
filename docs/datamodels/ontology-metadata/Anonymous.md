

# Class: Anonymous


_Abstract root class for all anonymous (non-named; lacking an identifier) expressions_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [omoschema:Anonymous](https://w3id.org/oak/ontology-metadata/Anonymous)






```{mermaid}
 classDiagram
    class Anonymous
    click Anonymous href "../Anonymous"
      Anonymous <|-- AnonymousClassExpression
        click AnonymousClassExpression href "../AnonymousClassExpression"
      
      
```





## Inheritance
* **Anonymous**
    * [AnonymousClassExpression](AnonymousClassExpression.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:Anonymous |
| native | omoschema:Anonymous |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Anonymous
description: Abstract root class for all anonymous (non-named; lacking an identifier)
  expressions
from_schema: https://w3id.org/oak/ontology-metadata
abstract: true

```
</details>

### Induced

<details>
```yaml
name: Anonymous
description: Abstract root class for all anonymous (non-named; lacking an identifier)
  expressions
from_schema: https://w3id.org/oak/ontology-metadata
abstract: true

```
</details>