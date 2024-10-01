

# Class: RepairConfiguration


_Configuration parameters for execution of validation repairs_





URI: [vm:RepairConfiguration](https://w3id.org/linkml/validation-model/RepairConfiguration)






```{mermaid}
 classDiagram
    class RepairConfiguration
    click RepairConfiguration href "../RepairConfiguration"
      RepairConfiguration : dry_run
        
      RepairConfiguration : validation_configuration
        
          
    
    
    RepairConfiguration --> "0..1" ValidationConfiguration : validation_configuration
    click ValidationConfiguration href "../ValidationConfiguration"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [validation_configuration](validation_configuration.md) | 0..1 <br/> [ValidationConfiguration](ValidationConfiguration.md) | repair configurations include validation configurations | direct |
| [dry_run](dry_run.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:RepairConfiguration |
| native | vm:RepairConfiguration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RepairConfiguration
description: Configuration parameters for execution of validation repairs
from_schema: https://w3id.org/linkml/validation_results
attributes:
  validation_configuration:
    name: validation_configuration
    description: repair configurations include validation configurations
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - RepairConfiguration
    range: ValidationConfiguration
  dry_run:
    name: dry_run
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - RepairConfiguration
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: RepairConfiguration
description: Configuration parameters for execution of validation repairs
from_schema: https://w3id.org/linkml/validation_results
attributes:
  validation_configuration:
    name: validation_configuration
    description: repair configurations include validation configurations
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: validation_configuration
    owner: RepairConfiguration
    domain_of:
    - RepairConfiguration
    range: ValidationConfiguration
  dry_run:
    name: dry_run
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: dry_run
    owner: RepairConfiguration
    domain_of:
    - RepairConfiguration
    range: boolean

```
</details>