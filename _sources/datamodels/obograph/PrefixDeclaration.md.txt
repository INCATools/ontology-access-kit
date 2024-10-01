

# Class: PrefixDeclaration


_A mapping between an individual prefix (e.g. GO) and a namespace (e.g. http://purl.obolibrary.org/obo/GO_)_





URI: [sh:PrefixDeclaration](https://w3id.org/shacl/PrefixDeclaration)






```{mermaid}
 classDiagram
    class PrefixDeclaration
    click PrefixDeclaration href "../PrefixDeclaration"
      PrefixDeclaration : namespace
        
      PrefixDeclaration : prefix
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [prefix](prefix.md) | 0..1 <br/> [String](String.md) | The prefix of a prefix declaration | direct |
| [namespace](namespace.md) | 0..1 <br/> [Uri](Uri.md) | The namespace associated with a prefix in a prefix declaration | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [prefixes](prefixes.md) | range | [PrefixDeclaration](PrefixDeclaration.md) |
| [Graph](Graph.md) | [prefixes](prefixes.md) | range | [PrefixDeclaration](PrefixDeclaration.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:PrefixDeclaration |
| native | obographs:PrefixDeclaration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PrefixDeclaration
description: A mapping between an individual prefix (e.g. GO) and a namespace (e.g.
  http://purl.obolibrary.org/obo/GO_)
from_schema: https://github.com/geneontology/obographs
attributes:
  prefix:
    name: prefix
    description: The prefix of a prefix declaration.
    comments:
    - It is strongly recommended that the prefix is a valid NCName
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:prefix
    key: true
    domain_of:
    - PrefixDeclaration
    range: string
    required: true
  namespace:
    name: namespace
    description: The namespace associated with a prefix in a prefix declaration.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:namespace
    domain_of:
    - PrefixDeclaration
    range: uri
class_uri: sh:PrefixDeclaration

```
</details>

### Induced

<details>
```yaml
name: PrefixDeclaration
description: A mapping between an individual prefix (e.g. GO) and a namespace (e.g.
  http://purl.obolibrary.org/obo/GO_)
from_schema: https://github.com/geneontology/obographs
attributes:
  prefix:
    name: prefix
    description: The prefix of a prefix declaration.
    comments:
    - It is strongly recommended that the prefix is a valid NCName
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:prefix
    key: true
    alias: prefix
    owner: PrefixDeclaration
    domain_of:
    - PrefixDeclaration
    range: string
    required: true
  namespace:
    name: namespace
    description: The namespace associated with a prefix in a prefix declaration.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:namespace
    alias: namespace
    owner: PrefixDeclaration
    domain_of:
    - PrefixDeclaration
    range: uri
class_uri: sh:PrefixDeclaration

```
</details>