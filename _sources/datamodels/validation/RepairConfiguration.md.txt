# Class: RepairConfiguration
_Configuration parameters for execution of validation repairs_





URI: [vm:RepairConfiguration](https://w3id.org/linkml/validation-model/RepairConfiguration)




```{mermaid}
 classDiagram
    class RepairConfiguration
      RepairConfiguration : dry_run
      RepairConfiguration : validation_configuration
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [validation_configuration](validation_configuration.md) | [ValidationConfiguration](ValidationConfiguration.md) | 0..1 | repair configurations include validation configurations  | . |
| [dry_run](dry_run.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:RepairConfiguration'] |
| native | ['vm:RepairConfiguration'] |


## LinkML Specification

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
    range: ValidationConfiguration
  dry_run:
    name: dry_run
    from_schema: https://w3id.org/linkml/validation_results
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
    alias: validation_configuration
    owner: RepairConfiguration
    range: ValidationConfiguration
  dry_run:
    name: dry_run
    from_schema: https://w3id.org/linkml/validation_results
    alias: dry_run
    owner: RepairConfiguration
    range: boolean

```
</details>