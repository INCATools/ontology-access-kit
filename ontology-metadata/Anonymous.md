# Class: Anonymous
_Abstract root class for all anonymous (non-named; lacking an identifier) expressions_



* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [omoschema:Anonymous](http://purl.obolibrary.org/obo/schema/Anonymous)


```{mermaid}
 classDiagram
    class Anonymous
      Anonymous <|-- AnonymousClassExpression
      
      
```




## Inheritance
* **Anonymous**
    * [AnonymousClassExpression](AnonymousClassExpression.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





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
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
abstract: true

```
</details>

### Induced

<details>
```yaml
name: Anonymous
description: Abstract root class for all anonymous (non-named; lacking an identifier)
  expressions
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
abstract: true

```
</details>