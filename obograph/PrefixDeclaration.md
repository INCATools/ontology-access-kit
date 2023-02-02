# Class: PrefixDeclaration
_maps individual prefix to namespace_




URI: [sh:PrefixDeclaration](https://w3id.org/shacl/PrefixDeclaration)



```{mermaid}
 classDiagram
    class PrefixDeclaration
      PrefixDeclaration : namespace
      PrefixDeclaration : prefix
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [prefix](prefix.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The prefix of a prefix declaration | direct |
| [namespace](namespace.md) | 0..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | The namespace associated with a prefix in a prefix declaration | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [prefixes](prefixes.md) | range | [PrefixDeclaration](PrefixDeclaration.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:PrefixDeclaration |
| native | og:PrefixDeclaration |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PrefixDeclaration
description: maps individual prefix to namespace
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  prefix:
    name: prefix
    description: The prefix of a prefix declaration.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:prefix
    range: string
  namespace:
    name: namespace
    description: The namespace associated with a prefix in a prefix declaration.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:namespace
    range: uri
class_uri: sh:PrefixDeclaration

```
</details>

### Induced

<details>
```yaml
name: PrefixDeclaration
description: maps individual prefix to namespace
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  prefix:
    name: prefix
    description: The prefix of a prefix declaration.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:prefix
    alias: prefix
    owner: PrefixDeclaration
    domain_of:
    - PrefixDeclaration
    range: string
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