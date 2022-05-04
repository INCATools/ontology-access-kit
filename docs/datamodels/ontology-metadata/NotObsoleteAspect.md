# Class: NotObsoleteAspect
_Auto-classifies anything that is not obsolete_




* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:NotObsoleteAspect](http://purl.obolibrary.org/obo/schema/NotObsoleteAspect)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |


## Usages



## Identifier and Mapping Information









## Rules



## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NotObsoleteAspect
description: Auto-classifies anything that is not obsolete
from_schema: http://purl.obolibrary.org/obo/omo/schema
mixin: true
rules:
- postconditions:
    none_of:
    - slot_conditions:
        label:
          name: label
          pattern: ^obsolete
classification_rules:
- slot_conditions:
    none_of:
      name: none_of
      deprecated: JsonObj(equals_expression='true')

```
</details>

### Induced

<details>
```yaml
name: NotObsoleteAspect
description: Auto-classifies anything that is not obsolete
from_schema: http://purl.obolibrary.org/obo/omo/schema
mixin: true
rules:
- postconditions:
    none_of:
    - slot_conditions:
        label:
          name: label
          pattern: ^obsolete
classification_rules:
- slot_conditions:
    none_of:
      name: none_of
      deprecated: JsonObj(equals_expression='true')

```
</details>