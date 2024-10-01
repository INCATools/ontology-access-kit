

# Class: NamedResource



URI: [vm:NamedResource](https://w3id.org/linkml/validation-model/NamedResource)






```{mermaid}
 classDiagram
    class NamedResource
    click NamedResource href "../NamedResource"
      NamedResource <|-- ConstraintComponent
        click ConstraintComponent href "../ConstraintComponent"
      NamedResource <|-- Node
        click Node href "../Node"
      
      NamedResource : id
        
      
```





## Inheritance
* **NamedResource**
    * [ConstraintComponent](ConstraintComponent.md)
    * [Node](Node.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:NamedResource |
| native | vm:NamedResource |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedResource
from_schema: https://w3id.org/linkml/validation_results
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    identifier: true
    domain_of:
    - NamedResource
    range: uriorcurie
    required: true

```
</details>

### Induced

<details>
```yaml
name: NamedResource
from_schema: https://w3id.org/linkml/validation_results
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    identifier: true
    alias: id
    owner: NamedResource
    domain_of:
    - NamedResource
    range: uriorcurie

```
</details>