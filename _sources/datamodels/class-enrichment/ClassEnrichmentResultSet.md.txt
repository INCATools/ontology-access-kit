

# Class: ClassEnrichmentResultSet


_A collection of enrichemt results_





URI: [ontoenrich:ClassEnrichmentResultSet](https://w3id.org/oak/class-enrichment/ClassEnrichmentResultSet)






```{mermaid}
 classDiagram
    class ClassEnrichmentResultSet
    click ClassEnrichmentResultSet href "../ClassEnrichmentResultSet"
      ClassEnrichmentResultSet : results
        
          
    
    
    ClassEnrichmentResultSet --> "*" ClassEnrichmentResult : results
    click ClassEnrichmentResult href "../ClassEnrichmentResult"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | * <br/> [ClassEnrichmentResult](ClassEnrichmentResult.md) | The enrichment results | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/class-enrichment




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoenrich:ClassEnrichmentResultSet |
| native | ontoenrich:ClassEnrichmentResultSet |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ClassEnrichmentResultSet
description: A collection of enrichemt results
from_schema: https://w3id.org/oak/class-enrichment
attributes:
  results:
    name: results
    description: The enrichment results
    from_schema: https://w3id.org/oak/class-enrichment
    rank: 1000
    domain_of:
    - ClassEnrichmentResultSet
    range: ClassEnrichmentResult
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: ClassEnrichmentResultSet
description: A collection of enrichemt results
from_schema: https://w3id.org/oak/class-enrichment
attributes:
  results:
    name: results
    description: The enrichment results
    from_schema: https://w3id.org/oak/class-enrichment
    rank: 1000
    alias: results
    owner: ClassEnrichmentResultSet
    domain_of:
    - ClassEnrichmentResultSet
    range: ClassEnrichmentResult
    multivalued: true

```
</details>