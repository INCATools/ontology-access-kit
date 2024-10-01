

# Class: Node



URI: [vm:Node](https://w3id.org/linkml/validation-model/Node)






```{mermaid}
 classDiagram
    class Node
    click Node href "../Node"
      NamedResource <|-- Node
        click NamedResource href "../NamedResource"
      
      Node : id
        
      
```





## Inheritance
* [NamedResource](NamedResource.md)
    * **Node**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) |  | [NamedResource](NamedResource.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationResult](ValidationResult.md) | [subject](subject.md) | range | [Node](Node.md) |
| [ValidationResult](ValidationResult.md) | [instantiates](instantiates.md) | range | [Node](Node.md) |
| [ValidationResult](ValidationResult.md) | [predicate](predicate.md) | range | [Node](Node.md) |
| [ValidationResult](ValidationResult.md) | [object](object.md) | range | [Node](Node.md) |
| [DefinitionValidationResult](DefinitionValidationResult.md) | [subject](subject.md) | range | [Node](Node.md) |
| [DefinitionValidationResult](DefinitionValidationResult.md) | [instantiates](instantiates.md) | range | [Node](Node.md) |
| [DefinitionValidationResult](DefinitionValidationResult.md) | [predicate](predicate.md) | range | [Node](Node.md) |
| [DefinitionValidationResult](DefinitionValidationResult.md) | [object](object.md) | range | [Node](Node.md) |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | [subject](subject.md) | range | [Node](Node.md) |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | [instantiates](instantiates.md) | range | [Node](Node.md) |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | [predicate](predicate.md) | range | [Node](Node.md) |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | [object](object.md) | range | [Node](Node.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:Node |
| native | vm:Node |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Node
from_schema: https://w3id.org/linkml/validation_results
is_a: NamedResource

```
</details>

### Induced

<details>
```yaml
name: Node
from_schema: https://w3id.org/linkml/validation_results
is_a: NamedResource
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    identifier: true
    alias: id
    owner: Node
    domain_of:
    - NamedResource
    range: uriorcurie
    required: true

```
</details>