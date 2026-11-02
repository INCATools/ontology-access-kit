

# Class: ValueSetConfiguration


_configuration for value set expansion_





URI: [vsconf:ValueSetConfiguration](https://w3id.org/linkml/value-set-configuration/ValueSetConfiguration)






```{mermaid}
 classDiagram
    class ValueSetConfiguration
    click ValueSetConfiguration href "../ValueSetConfiguration"
      ValueSetConfiguration : default_resolver
        
          
    
    
    ValueSetConfiguration --> "0..1" Resolver : default_resolver
    click Resolver href "../Resolver"

        
      ValueSetConfiguration : prefix_resolvers
        
          
    
    
    ValueSetConfiguration --> "*" Resolver : prefix_resolvers
    click Resolver href "../Resolver"

        
      ValueSetConfiguration : resource_resolvers
        
          
    
    
    ValueSetConfiguration --> "*" Resolver : resource_resolvers
    click Resolver href "../Resolver"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [default_resolver](default_resolver.md) | 0..1 <br/> [Resolver](Resolver.md) | The default resolver to use for value set expansion | direct |
| [resource_resolvers](resource_resolvers.md) | * <br/> [Resolver](Resolver.md) |  | direct |
| [prefix_resolvers](prefix_resolvers.md) | * <br/> [Resolver](Resolver.md) | Mapping of prefixes to resolvers | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/value-set-configuration




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vsconf:ValueSetConfiguration |
| native | vsconf:ValueSetConfiguration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValueSetConfiguration
description: configuration for value set expansion
from_schema: https://w3id.org/linkml/value-set-configuration
attributes:
  default_resolver:
    name: default_resolver
    description: The default resolver to use for value set expansion
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    inlined: true
  resource_resolvers:
    name: resource_resolvers
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    multivalued: true
    inlined: true
  prefix_resolvers:
    name: prefix_resolvers
    description: Mapping of prefixes to resolvers
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    multivalued: true
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: ValueSetConfiguration
description: configuration for value set expansion
from_schema: https://w3id.org/linkml/value-set-configuration
attributes:
  default_resolver:
    name: default_resolver
    description: The default resolver to use for value set expansion
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: default_resolver
    owner: ValueSetConfiguration
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    inlined: true
  resource_resolvers:
    name: resource_resolvers
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: resource_resolvers
    owner: ValueSetConfiguration
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    multivalued: true
    inlined: true
  prefix_resolvers:
    name: prefix_resolvers
    description: Mapping of prefixes to resolvers
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: prefix_resolvers
    owner: ValueSetConfiguration
    domain_of:
    - ValueSetConfiguration
    range: Resolver
    multivalued: true
    inlined: true

```
</details>