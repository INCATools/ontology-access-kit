# Class: ObsoleteAspect
_Auto-classifies anything that is obsolete_




* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:ObsoleteAspect](http://purl.obolibrary.org/obo/schema/ObsoleteAspect)




```{mermaid}
 classDiagram
    class ObsoleteAspect
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Rules



## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:ObsoleteAspect'] |
| native | ['omoschema:ObsoleteAspect'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ObsoleteAspect
description: Auto-classifies anything that is obsolete
from_schema: http://purl.obolibrary.org/obo/omo/schema
mixin: true
slot_usage:
  label:
    name: label
    pattern: ^obsolete
classification_rules:
- slot_conditions:
    deprecated:
      name: deprecated
      equals_expression: 'true'

```
</details>

### Induced

<details>
```yaml
name: ObsoleteAspect
description: Auto-classifies anything that is obsolete
from_schema: http://purl.obolibrary.org/obo/omo/schema
mixin: true
slot_usage:
  label:
    name: label
    pattern: ^obsolete
classification_rules:
- slot_conditions:
    deprecated:
      name: deprecated
      equals_expression: 'true'

```
</details>