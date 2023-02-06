# Class: LogicalDefinitionAxiom
_An axiom that defines a class in terms of a genus or set of genus classes and a set of differentia_




URI: [og:LogicalDefinitionAxiom](https://github.com/geneontology/obographs/LogicalDefinitionAxiom)



```{mermaid}
 classDiagram
    class LogicalDefinitionAxiom
      Axiom <|-- LogicalDefinitionAxiom
      
      LogicalDefinitionAxiom : definedClassId
      LogicalDefinitionAxiom : genusIds
      LogicalDefinitionAxiom : meta
      LogicalDefinitionAxiom : restrictions
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **LogicalDefinitionAxiom**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [definedClassId](definedClassId.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The class that is defined by this axiom | direct |
| [genusIds](genusIds.md) | 0..* _recommended_ <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The set of classes that are the genus of the defined class | direct |
| [restrictions](restrictions.md) | 0..* _recommended_ <br/> [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | The set of restrictions that are the differentia of the defined class | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [Axiom](Axiom.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | range | [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) |




## Aliases


* genus differentia definition



## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | EquivalentClasses({definedClassId} ObjectIntersectionOf({genusIds} {restrictions})) |



### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:LogicalDefinitionAxiom |
| native | og:LogicalDefinitionAxiom |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LogicalDefinitionAxiom
annotations:
  owl.fstring:
    tag: owl.fstring
    value: EquivalentClasses({definedClassId} ObjectIntersectionOf({genusIds} {restrictions}))
description: An axiom that defines a class in terms of a genus or set of genus classes
  and a set of differentia
from_schema: https://github.com/geneontology/obographs
aliases:
- genus differentia definition
rank: 1000
is_a: Axiom
attributes:
  definedClassId:
    name: definedClassId
    description: The class that is defined by this axiom
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    required: true
  genusIds:
    name: genusIds
    description: The set of classes that are the genus of the defined class
    comments:
    - typically, this will be a single class
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    rank: 1000
    multivalued: true
    recommended: true
  restrictions:
    name: restrictions
    description: The set of restrictions that are the differentia of the defined class
    comments:
    - typically this will always be present.
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    aliases:
    - differentia
    rank: 1000
    slot_uri: owl:someValuesFrom
    multivalued: true
    range: ExistentialRestrictionExpression
    recommended: true

```
</details>

### Induced

<details>
```yaml
name: LogicalDefinitionAxiom
annotations:
  owl.fstring:
    tag: owl.fstring
    value: EquivalentClasses({definedClassId} ObjectIntersectionOf({genusIds} {restrictions}))
description: An axiom that defines a class in terms of a genus or set of genus classes
  and a set of differentia
from_schema: https://github.com/geneontology/obographs
aliases:
- genus differentia definition
rank: 1000
is_a: Axiom
attributes:
  definedClassId:
    name: definedClassId
    description: The class that is defined by this axiom
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: definedClassId
    owner: LogicalDefinitionAxiom
    domain_of:
    - LogicalDefinitionAxiom
    required: true
  genusIds:
    name: genusIds
    description: The set of classes that are the genus of the defined class
    comments:
    - typically, this will be a single class
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    rank: 1000
    multivalued: true
    alias: genusIds
    owner: LogicalDefinitionAxiom
    domain_of:
    - LogicalDefinitionAxiom
    recommended: true
  restrictions:
    name: restrictions
    description: The set of restrictions that are the differentia of the defined class
    comments:
    - typically this will always be present.
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    aliases:
    - differentia
    rank: 1000
    slot_uri: owl:someValuesFrom
    multivalued: true
    alias: restrictions
    owner: LogicalDefinitionAxiom
    domain_of:
    - LogicalDefinitionAxiom
    range: ExistentialRestrictionExpression
    recommended: true
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: LogicalDefinitionAxiom
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta

```
</details>