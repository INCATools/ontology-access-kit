

# Class: StructureDiffResultSet


_A collection of relational diff results_





URI: [xodiff:StructureDiffResultSet](https://w3id.org/oak/cross-ontology-diff/StructureDiffResultSet)






```{mermaid}
 classDiagram
    class StructureDiffResultSet
    click StructureDiffResultSet href "../StructureDiffResultSet"
      StructureDiffResultSet : left_source
        
      StructureDiffResultSet : results
        
          
    
    
    StructureDiffResultSet --> "*" RelationalDiff : results
    click RelationalDiff href "../RelationalDiff"

        
      StructureDiffResultSet : right_source
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | * <br/> [RelationalDiff](RelationalDiff.md) | all differences between a pair of ontologies | direct |
| [left_source](left_source.md) | 0..1 <br/> [Source](Source.md) | Ontology source for left entities | direct |
| [right_source](right_source.md) | 0..1 <br/> [Source](Source.md) | Ontology source for right entities | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:StructureDiffResultSet |
| native | xodiff:StructureDiffResultSet |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results
from_schema: https://w3id.org/oak/cross-ontology-diff
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    domain_of:
    - StructureDiffResultSet
    range: RelationalDiff
    multivalued: true
    inlined: true
  left_source:
    name: left_source
    description: Ontology source for left entities
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    domain_of:
    - StructureDiffResultSet
    range: Source
  right_source:
    name: right_source
    description: Ontology source for right entities
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    domain_of:
    - StructureDiffResultSet
    range: Source

```
</details>

### Induced

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results
from_schema: https://w3id.org/oak/cross-ontology-diff
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    alias: results
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: RelationalDiff
    multivalued: true
    inlined: true
  left_source:
    name: left_source
    description: Ontology source for left entities
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    alias: left_source
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: Source
  right_source:
    name: right_source
    description: Ontology source for right entities
    from_schema: https://w3id.org/oak/cross-ontology-diff
    rank: 1000
    alias: right_source
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: Source

```
</details>