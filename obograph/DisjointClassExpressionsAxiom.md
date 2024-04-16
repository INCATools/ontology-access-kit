

# Class: DisjointClassExpressionsAxiom


_An axiom that defines a set of classes or class expressions as being mutually disjoint. Formally, there exists no instance that instantiates more that one of the union of classIds and classExpressions._





URI: [obographs:DisjointClassExpressionsAxiom](https://github.com/geneontology/obographs/DisjointClassExpressionsAxiom)




```{mermaid}
 classDiagram
    class DisjointClassExpressionsAxiom
      Axiom <|-- DisjointClassExpressionsAxiom
      
      DisjointClassExpressionsAxiom : classExpressions
        
          DisjointClassExpressionsAxiom --> ExistentialRestrictionExpression : classExpressions
        
      DisjointClassExpressionsAxiom : classIds
        
          DisjointClassExpressionsAxiom --> None : classIds
        
      DisjointClassExpressionsAxiom : meta
        
          DisjointClassExpressionsAxiom --> Meta : meta
        
      DisjointClassExpressionsAxiom : unionEquivalentTo
        
          DisjointClassExpressionsAxiom --> None : unionEquivalentTo
        
      DisjointClassExpressionsAxiom : unionEquivalentToExpression
        
          DisjointClassExpressionsAxiom --> ExistentialRestrictionExpression : unionEquivalentToExpression
        
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **DisjointClassExpressionsAxiom**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [classIds](classIds.md) | 0..* <br/> [String](String.md) | The set of named classes that are mutually disjoint | direct |
| [classExpressions](classExpressions.md) | 0..* <br/> [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | The set of class expressions that are mutually disjoint | direct |
| [unionEquivalentTo](unionEquivalentTo.md) | 0..1 <br/> [String](String.md) | If present, this equates to an OWL DisjointUnion expression | direct |
| [unionEquivalentToExpression](unionEquivalentToExpression.md) | 0..1 <br/> [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | if present, this class expression is equivalent ot the (disjoint) union of th... | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [Axiom](Axiom.md) |







## Aliases


* disjoint classes



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:DisjointClassExpressionsAxiom |
| native | obographs:DisjointClassExpressionsAxiom |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DisjointClassExpressionsAxiom
description: An axiom that defines a set of classes or class expressions as being
  mutually disjoint. Formally, there exists no instance that instantiates more that
  one of the union of classIds and classExpressions.
from_schema: https://github.com/geneontology/obographs
aliases:
- disjoint classes
is_a: Axiom
attributes:
  classIds:
    name: classIds
    description: The set of named classes that are mutually disjoint.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    domain_of:
    - DisjointClassExpressionsAxiom
  classExpressions:
    name: classExpressions
    description: The set of class expressions that are mutually disjoint.
    comments:
    - currently restricted to existential restrictions (some values from)
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    domain_of:
    - DisjointClassExpressionsAxiom
    range: ExistentialRestrictionExpression
  unionEquivalentTo:
    name: unionEquivalentTo
    description: If present, this equates to an OWL DisjointUnion expression.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    domain_of:
    - DisjointClassExpressionsAxiom
  unionEquivalentToExpression:
    name: unionEquivalentToExpression
    description: if present, this class expression is equivalent ot the (disjoint)
      union of the classIds and classExpressions.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    domain_of:
    - DisjointClassExpressionsAxiom
    range: ExistentialRestrictionExpression

```
</details>

### Induced

<details>
```yaml
name: DisjointClassExpressionsAxiom
description: An axiom that defines a set of classes or class expressions as being
  mutually disjoint. Formally, there exists no instance that instantiates more that
  one of the union of classIds and classExpressions.
from_schema: https://github.com/geneontology/obographs
aliases:
- disjoint classes
is_a: Axiom
attributes:
  classIds:
    name: classIds
    description: The set of named classes that are mutually disjoint.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: classIds
    owner: DisjointClassExpressionsAxiom
    domain_of:
    - DisjointClassExpressionsAxiom
  classExpressions:
    name: classExpressions
    description: The set of class expressions that are mutually disjoint.
    comments:
    - currently restricted to existential restrictions (some values from)
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: classExpressions
    owner: DisjointClassExpressionsAxiom
    domain_of:
    - DisjointClassExpressionsAxiom
    range: ExistentialRestrictionExpression
  unionEquivalentTo:
    name: unionEquivalentTo
    description: If present, this equates to an OWL DisjointUnion expression.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: unionEquivalentTo
    owner: DisjointClassExpressionsAxiom
    domain_of:
    - DisjointClassExpressionsAxiom
  unionEquivalentToExpression:
    name: unionEquivalentToExpression
    description: if present, this class expression is equivalent ot the (disjoint)
      union of the classIds and classExpressions.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: unionEquivalentToExpression
    owner: DisjointClassExpressionsAxiom
    domain_of:
    - DisjointClassExpressionsAxiom
    range: ExistentialRestrictionExpression
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: DisjointClassExpressionsAxiom
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