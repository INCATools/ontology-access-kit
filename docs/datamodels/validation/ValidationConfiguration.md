

# Class: ValidationConfiguration


_Configuration parameters for execution of a validation report_





URI: [vm:ValidationConfiguration](https://w3id.org/linkml/validation-model/ValidationConfiguration)






```{mermaid}
 classDiagram
    class ValidationConfiguration
    click ValidationConfiguration href "../ValidationConfiguration"
      ValidationConfiguration : documentation_objects
        
      ValidationConfiguration : lookup_references
        
      ValidationConfiguration : max_number_results_per_type
        
      ValidationConfiguration : prompt_info
        
      ValidationConfiguration : schema_path
        
      ValidationConfiguration : type_severity_map
        
          
    
    
    ValidationConfiguration --> "*" TypeSeverityKeyValue : type_severity_map
    click TypeSeverityKeyValue href "../TypeSeverityKeyValue"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [max_number_results_per_type](max_number_results_per_type.md) | 0..1 <br/> [Integer](Integer.md) | if set then truncate results such that no more than this number of results ar... | direct |
| [type_severity_map](type_severity_map.md) | * <br/> [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | Allows overriding of severity of a particular type | direct |
| [schema_path](schema_path.md) | 0..1 <br/> [String](String.md) | allows overriding the default OMO schema | direct |
| [lookup_references](lookup_references.md) | 0..1 <br/> [Boolean](Boolean.md) | if true, then look up references used as provenance (axiom annotation) | direct |
| [prompt_info](prompt_info.md) | 0..1 <br/> [String](String.md) | for AI agents, this allows passing through of additional info to the prompt | direct |
| [documentation_objects](documentation_objects.md) | * <br/> [String](String.md) | paths or URLs to files containing best practice documentation, SOPs, etc | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairConfiguration](RepairConfiguration.md) | [validation_configuration](validation_configuration.md) | range | [ValidationConfiguration](ValidationConfiguration.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:ValidationConfiguration |
| native | vm:ValidationConfiguration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: TypeSeverityKeyValue
    multivalued: true
    inlined: true
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: string
  lookup_references:
    name: lookup_references
    description: if true, then look up references used as provenance (axiom annotation).
      This may include looking up the PMID and checking if a publication is retracted.
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: boolean
  prompt_info:
    name: prompt_info
    description: for AI agents, this allows passing through of additional info to
      the prompt
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: string
  documentation_objects:
    name: documentation_objects
    description: paths or URLs to files containing best practice documentation, SOPs,
      etc. Primarily for AI agents to read when performing validation.
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ValidationConfiguration
    range: string
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: max_number_results_per_type
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: type_severity_map
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: TypeSeverityKeyValue
    multivalued: true
    inlined: true
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: schema_path
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: string
  lookup_references:
    name: lookup_references
    description: if true, then look up references used as provenance (axiom annotation).
      This may include looking up the PMID and checking if a publication is retracted.
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: lookup_references
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: boolean
  prompt_info:
    name: prompt_info
    description: for AI agents, this allows passing through of additional info to
      the prompt
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: prompt_info
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: string
  documentation_objects:
    name: documentation_objects
    description: paths or URLs to files containing best practice documentation, SOPs,
      etc. Primarily for AI agents to read when performing validation.
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: documentation_objects
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: string
    multivalued: true

```
</details>