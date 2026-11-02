

# Class: Resolver


_A mechanism for resolving using an ontology_





URI: [vsconf:Resolver](https://w3id.org/linkml/value-set-configuration/Resolver)






```{mermaid}
 classDiagram
    class Resolver
    click Resolver href "../Resolver"
      Resolver <|-- NamedResolver
        click NamedResolver href "../NamedResolver"
      
      Resolver : method
        
          
    
    
    Resolver --> "0..1" ResolverMethod : method
    click ResolverMethod href "../ResolverMethod"

        
      Resolver : name
        
      Resolver : shorthand
        
      Resolver : shorthand_prefix
        
      Resolver : url
        
      
```





## Inheritance
* **Resolver**
    * [NamedResolver](NamedResolver.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of the resource or prefix | direct |
| [shorthand_prefix](shorthand_prefix.md) | 0..1 <br/> [String](String.md) |  | direct |
| [shorthand](shorthand.md) | 0..1 <br/> [String](String.md) | A shorthand for the resolver, using the OAK shorthand syntax, for example, 'o... | direct |
| [method](method.md) | 0..1 <br/> [ResolverMethod](ResolverMethod.md) | The method used to resolve the value set | direct |
| [url](url.md) | 0..1 <br/> [Uri](Uri.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValueSetConfiguration](ValueSetConfiguration.md) | [default_resolver](default_resolver.md) | range | [Resolver](Resolver.md) |
| [ValueSetConfiguration](ValueSetConfiguration.md) | [resource_resolvers](resource_resolvers.md) | range | [Resolver](Resolver.md) |
| [ValueSetConfiguration](ValueSetConfiguration.md) | [prefix_resolvers](prefix_resolvers.md) | range | [Resolver](Resolver.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/value-set-configuration




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vsconf:Resolver |
| native | vsconf:Resolver |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Resolver
description: A mechanism for resolving using an ontology
from_schema: https://w3id.org/linkml/value-set-configuration
attributes:
  name:
    name: name
    description: The name of the resource or prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    key: true
    domain_of:
    - Resolver
    - NamedResolver
    range: string
    required: true
  shorthand_prefix:
    name: shorthand_prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - Resolver
  shorthand:
    name: shorthand
    description: A shorthand for the resolver, using the OAK shorthand syntax, for
      example, 'obo:sqlite:cl'
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - Resolver
  method:
    name: method
    description: The method used to resolve the value set.
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - Resolver
    range: ResolverMethod
  url:
    name: url
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    domain_of:
    - Resolver
    range: uri

```
</details>

### Induced

<details>
```yaml
name: Resolver
description: A mechanism for resolving using an ontology
from_schema: https://w3id.org/linkml/value-set-configuration
attributes:
  name:
    name: name
    description: The name of the resource or prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    key: true
    alias: name
    owner: Resolver
    domain_of:
    - Resolver
    - NamedResolver
    range: string
    required: true
  shorthand_prefix:
    name: shorthand_prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: shorthand_prefix
    owner: Resolver
    domain_of:
    - Resolver
    range: string
  shorthand:
    name: shorthand
    description: A shorthand for the resolver, using the OAK shorthand syntax, for
      example, 'obo:sqlite:cl'
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: shorthand
    owner: Resolver
    domain_of:
    - Resolver
    range: string
  method:
    name: method
    description: The method used to resolve the value set.
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: method
    owner: Resolver
    domain_of:
    - Resolver
    range: ResolverMethod
  url:
    name: url
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: url
    owner: Resolver
    domain_of:
    - Resolver
    range: uri

```
</details>