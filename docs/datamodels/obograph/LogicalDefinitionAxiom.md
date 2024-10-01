

# Class: LogicalDefinitionAxiom


_An axiom that defines a class in terms of a genus or set of genus classes and a set of differentia_





URI: [obographs:LogicalDefinitionAxiom](https://github.com/geneontology/obographs/LogicalDefinitionAxiom)






```{mermaid}
 classDiagram
    class LogicalDefinitionAxiom
    click LogicalDefinitionAxiom href "../LogicalDefinitionAxiom"
      Axiom <|-- LogicalDefinitionAxiom
        click Axiom href "../Axiom"
      
      LogicalDefinitionAxiom : definedClassId
        
      LogicalDefinitionAxiom : genusIds
        
      LogicalDefinitionAxiom : meta
        
          
    
    
    LogicalDefinitionAxiom --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      LogicalDefinitionAxiom : restrictions
        
          
    
    
    LogicalDefinitionAxiom --> "* _recommended_" ExistentialRestrictionExpression : restrictions
    click ExistentialRestrictionExpression href "../ExistentialRestrictionExpression"

        
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **LogicalDefinitionAxiom**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [definedClassId](definedClassId.md) | 1 <br/> [OboIdentifierString](OboIdentifierString.md) | The class that is defined by this axiom | direct |
| [genusIds](genusIds.md) | * _recommended_ <br/> [OboIdentifierString](OboIdentifierString.md) | The set of classes that are the genus of the defined class | direct |
| [restrictions](restrictions.md) | * _recommended_ <br/> [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | The set of restrictions that are the differentiating features of the defined ... | direct |
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
| self | obographs:LogicalDefinitionAxiom |
| native | obographs:LogicalDefinitionAxiom |







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
is_a: Axiom
attributes:
  definedClassId:
    name: definedClassId
    description: The class that is defined by this axiom
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    domain_of:
    - LogicalDefinitionAxiom
    range: OboIdentifierString
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
    domain_of:
    - LogicalDefinitionAxiom
    range: OboIdentifierString
    recommended: true
    multivalued: true
  restrictions:
    name: restrictions
    description: The set of restrictions that are the differentiating features of
      the defined class
    comments:
    - typically this will always be present.
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    aliases:
    - differentia
    rank: 1000
    slot_uri: owl:someValuesFrom
    domain_of:
    - LogicalDefinitionAxiom
    range: ExistentialRestrictionExpression
    recommended: true
    multivalued: true

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
    range: OboIdentifierString
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
    alias: genusIds
    owner: LogicalDefinitionAxiom
    domain_of:
    - LogicalDefinitionAxiom
    range: OboIdentifierString
    recommended: true
    multivalued: true
  restrictions:
    name: restrictions
    description: The set of restrictions that are the differentiating features of
      the defined class
    comments:
    - typically this will always be present.
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://github.com/geneontology/obographs/issues/89
    aliases:
    - differentia
    rank: 1000
    slot_uri: owl:someValuesFrom
    alias: restrictions
    owner: LogicalDefinitionAxiom
    domain_of:
    - LogicalDefinitionAxiom
    range: ExistentialRestrictionExpression
    recommended: true
    multivalued: true
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