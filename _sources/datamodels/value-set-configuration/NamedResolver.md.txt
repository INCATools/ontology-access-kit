

# Class: NamedResolver


_A resolver that is associated with a named resource or prefix_





URI: [vsconf:NamedResolver](https://w3id.org/linkml/value-set-configuration/NamedResolver)






```{mermaid}
 classDiagram
    class NamedResolver
    click NamedResolver href "../NamedResolver"
      Resolver <|-- NamedResolver
        click Resolver href "../Resolver"
      
      NamedResolver : method
        
          
    
    
    NamedResolver --> "0..1" ResolverMethod : method
    click ResolverMethod href "../ResolverMethod"

        
      NamedResolver : name
        
      NamedResolver : shorthand
        
      NamedResolver : shorthand_prefix
        
      NamedResolver : url
        
      
```





## Inheritance
* [Resolver](Resolver.md)
    * **NamedResolver**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 0..1 <br/> [String](String.md) | The name of the resource or prefix | direct |
| [shorthand_prefix](shorthand_prefix.md) | 0..1 <br/> [String](String.md) |  | [Resolver](Resolver.md) |
| [shorthand](shorthand.md) | 0..1 <br/> [String](String.md) | A shorthand for the resolver, using the OAK shorthand syntax, for example, 'o... | [Resolver](Resolver.md) |
| [method](method.md) | 0..1 <br/> [ResolverMethod](ResolverMethod.md) | The method used to resolve the value set | [Resolver](Resolver.md) |
| [url](url.md) | 0..1 <br/> [Uri](Uri.md) |  | [Resolver](Resolver.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/value-set-configuration




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vsconf:NamedResolver |
| native | vsconf:NamedResolver |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedResolver
description: A resolver that is associated with a named resource or prefix
from_schema: https://w3id.org/linkml/value-set-configuration
is_a: Resolver
attributes:
  name:
    name: name
    description: The name of the resource or prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    key: true
    domain_of:
    - Resolver
    - NamedResolver
    range: string
    required: true

```
</details>

### Induced

<details>
```yaml
name: NamedResolver
description: A resolver that is associated with a named resource or prefix
from_schema: https://w3id.org/linkml/value-set-configuration
is_a: Resolver
attributes:
  name:
    name: name
    description: The name of the resource or prefix
    from_schema: https://w3id.org/linkml/value-set-configuration
    key: true
    alias: name
    owner: NamedResolver
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
    owner: NamedResolver
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
    owner: NamedResolver
    domain_of:
    - Resolver
    range: string
  method:
    name: method
    description: The method used to resolve the value set.
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: method
    owner: NamedResolver
    domain_of:
    - Resolver
    range: ResolverMethod
  url:
    name: url
    from_schema: https://w3id.org/linkml/value-set-configuration
    rank: 1000
    alias: url
    owner: NamedResolver
    domain_of:
    - Resolver
    range: uri

```
</details>