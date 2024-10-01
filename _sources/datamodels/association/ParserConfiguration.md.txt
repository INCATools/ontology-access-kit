

# Class: ParserConfiguration


_Settings that determine behavior when parsing associations._





URI: [ontoassoc:ParserConfiguration](https://w3id.org/oak/association/ParserConfiguration)






```{mermaid}
 classDiagram
    class ParserConfiguration
    click ParserConfiguration href "../ParserConfiguration"
      ParserConfiguration : aggregator_knowledge_source
        
      ParserConfiguration : include_association_attributes
        
      ParserConfiguration : preserve_negated_associations
        
      ParserConfiguration : primary_knowledge_source
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [preserve_negated_associations](preserve_negated_associations.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then the parser will keep negated associations in the output | direct |
| [include_association_attributes](include_association_attributes.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then the parser will include non S/P/O properties as additional attr... | direct |
| [primary_knowledge_source](primary_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The default primary knowledge source for all associations in this resource | direct |
| [aggregator_knowledge_source](aggregator_knowledge_source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The default aggregator knowledge source for all associations in this resource | direct |









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
description: Settings that determine behavior when parsing associations.
from_schema: https://w3id.org/oak/association
attributes:
  preserve_negated_associations:
    name: preserve_negated_associations
    description: 'If true, then the parser will keep negated associations in the output.

      If false, then the parser will remove negated associations from the output.'
    comments:
    - Note that to be defensive most applications should leave the default as false
    from_schema: https://w3id.org/oak/association
    rank: 1000
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
    domain_of:
    - ParserConfiguration
    range: boolean
  primary_knowledge_source:
    name: primary_knowledge_source
    description: The default primary knowledge source for all associations in this
      resource.
    from_schema: https://w3id.org/oak/association
    slot_uri: biolink:primary_knowledge_source
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie
  aggregator_knowledge_source:
    name: aggregator_knowledge_source
    description: The default aggregator knowledge source for all associations in this
      resource.
    from_schema: https://w3id.org/oak/association
    slot_uri: biolink:aggregator_knowledge_source
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie

```
</details>

### Induced

<details>
```yaml
name: ParserConfiguration
description: Settings that determine behavior when parsing associations.
from_schema: https://w3id.org/oak/association
attributes:
  preserve_negated_associations:
    name: preserve_negated_associations
    description: 'If true, then the parser will keep negated associations in the output.

      If false, then the parser will remove negated associations from the output.'
    comments:
    - Note that to be defensive most applications should leave the default as false
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
  primary_knowledge_source:
    name: primary_knowledge_source
    description: The default primary knowledge source for all associations in this
      resource.
    from_schema: https://w3id.org/oak/association
    slot_uri: biolink:primary_knowledge_source
    alias: primary_knowledge_source
    owner: ParserConfiguration
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie
  aggregator_knowledge_source:
    name: aggregator_knowledge_source
    description: The default aggregator knowledge source for all associations in this
      resource.
    from_schema: https://w3id.org/oak/association
    slot_uri: biolink:aggregator_knowledge_source
    alias: aggregator_knowledge_source
    owner: ParserConfiguration
    domain_of:
    - PositiveOrNegativeAssociation
    - ParserConfiguration
    - AssociationChange
    range: uriorcurie

```
</details>