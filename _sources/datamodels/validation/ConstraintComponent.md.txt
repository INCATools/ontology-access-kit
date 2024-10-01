

# Class: ConstraintComponent



URI: [vm:ConstraintComponent](https://w3id.org/linkml/validation-model/ConstraintComponent)






```{mermaid}
 classDiagram
    class ConstraintComponent
    click ConstraintComponent href "../ConstraintComponent"
      NamedResource <|-- ConstraintComponent
        click NamedResource href "../NamedResource"
      
      ConstraintComponent : id
        
      
```





## Inheritance
* [NamedResource](NamedResource.md)
    * **ConstraintComponent**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) |  | [NamedResource](NamedResource.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationResult](ValidationResult.md) | [type](type.md) | range | [ConstraintComponent](ConstraintComponent.md) |
| [DefinitionValidationResult](DefinitionValidationResult.md) | [type](type.md) | range | [ConstraintComponent](ConstraintComponent.md) |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | [type](type.md) | range | [ConstraintComponent](ConstraintComponent.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:ConstraintComponent |
| native | vm:ConstraintComponent |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ConstraintComponent
from_schema: https://w3id.org/linkml/validation_results
is_a: NamedResource

```
</details>

### Induced

<details>
```yaml
name: ConstraintComponent
from_schema: https://w3id.org/linkml/validation_results
is_a: NamedResource
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    identifier: true
    alias: id
    owner: ConstraintComponent
    domain_of:
    - NamedResource
    range: uriorcurie
    required: true

```
</details>