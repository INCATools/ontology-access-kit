# Class: ParserConfiguration



URI: [ontoassoc:ParserConfiguration](https://w3id.org/oak/association/ParserConfiguration)



```{mermaid}
 classDiagram
    class ParserConfiguration
      ParserConfiguration : include_association_attributes
        
      ParserConfiguration : preserve_negated_associations
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [preserve_negated_associations](preserve_negated_associations.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then the parser will keep negated associations in the output | direct |
| [include_association_attributes](include_association_attributes.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then the parser will include non S/P/O properties as additional attr... | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:ParserConfiguration |
| native | ontoassoc:ParserConfiguration |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ParserConfiguration
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  preserve_negated_associations:
    name: preserve_negated_associations
    description: 'If true, then the parser will keep negated associations in the output.

      If false, then the parser will remove negated associations from the output.'
    from_schema: https://w3id.org/oak/association
    rank: 1000
    range: boolean
  include_association_attributes:
    name: include_association_attributes
    description: 'If true, then the parser will include non S/P/O properties as additional
      attributes.

      This may result in slower parsing'
    from_schema: https://w3id.org/oak/association
    rank: 1000
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: ParserConfiguration
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  preserve_negated_associations:
    name: preserve_negated_associations
    description: 'If true, then the parser will keep negated associations in the output.

      If false, then the parser will remove negated associations from the output.'
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: preserve_negated_associations
    owner: ParserConfiguration
    domain_of:
    - ParserConfiguration
    range: boolean
  include_association_attributes:
    name: include_association_attributes
    description: 'If true, then the parser will include non S/P/O properties as additional
      attributes.

      This may result in slower parsing'
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: include_association_attributes
    owner: ParserConfiguration
    domain_of:
    - ParserConfiguration
    range: boolean

```
</details>