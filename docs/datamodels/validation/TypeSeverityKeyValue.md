# Class: TypeSeverityKeyValue
_key-value pair that maps a validation result type to a severity setting, for overriding default severity_





URI: [vm:TypeSeverityKeyValue](https://w3id.org/linkml/validation-model/TypeSeverityKeyValue)




```{mermaid}
 classDiagram
    class TypeSeverityKeyValue
      TypeSeverityKeyValue : severity
      TypeSeverityKeyValue : type
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | None  | . |
| [severity](severity.md) | [SeverityOptions](SeverityOptions.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | [type_severity_map](type_severity_map.md) | range | TypeSeverityKeyValue |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:TypeSeverityKeyValue'] |
| native | ['vm:TypeSeverityKeyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeSeverityKeyValue
conforms_to: wikidata:Q4818718
description: key-value pair that maps a validation result type to a severity setting,
  for overriding default severity
from_schema: https://w3id.org/linkml/validation_results
attributes:
  type:
    name: type
    from_schema: https://w3id.org/linkml/validation_results
    key: true
    range: uriorcurie
  severity:
    name: severity
    from_schema: https://w3id.org/linkml/validation_results
    range: severity_options

```
</details>

### Induced

<details>
```yaml
name: TypeSeverityKeyValue
conforms_to: wikidata:Q4818718
description: key-value pair that maps a validation result type to a severity setting,
  for overriding default severity
from_schema: https://w3id.org/linkml/validation_results
attributes:
  type:
    name: type
    from_schema: https://w3id.org/linkml/validation_results
    key: true
    alias: type
    owner: TypeSeverityKeyValue
    range: uriorcurie
    required: true
  severity:
    name: severity
    from_schema: https://w3id.org/linkml/validation_results
    alias: severity
    owner: TypeSeverityKeyValue
    range: severity_options

```
</details>