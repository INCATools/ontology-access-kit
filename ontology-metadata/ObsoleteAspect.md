# Class: ObsoleteAspect
_Auto-classifies anything that is obsolete_




URI: [omoschema:ObsoleteAspect](http://purl.obolibrary.org/obo/schema/ObsoleteAspect)


```{mermaid}
 classDiagram
    class ObsoleteAspect
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
## Mixin Usage

| mixed into | description |
| --- | --- |




## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasLifeCycle](HasLifeCycle.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [HasLifeCycle](HasLifeCycle.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [HasLifeCycle](HasLifeCycle.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [HasLifeCycle](HasLifeCycle.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [Term](Term.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [Term](Term.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [Term](Term.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [Term](Term.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [Class](Class.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [Class](Class.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [Class](Class.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [Class](Class.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [Property](Property.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [Property](Property.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [Property](Property.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [Property](Property.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [AnnotationProperty](AnnotationProperty.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [AnnotationProperty](AnnotationProperty.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [AnnotationProperty](AnnotationProperty.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [AnnotationProperty](AnnotationProperty.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [ObjectProperty](ObjectProperty.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [ObjectProperty](ObjectProperty.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [ObjectProperty](ObjectProperty.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [ObjectProperty](ObjectProperty.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [TransitiveProperty](TransitiveProperty.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [TransitiveProperty](TransitiveProperty.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [TransitiveProperty](TransitiveProperty.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [TransitiveProperty](TransitiveProperty.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [NamedIndividual](NamedIndividual.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [NamedIndividual](NamedIndividual.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [NamedIndividual](NamedIndividual.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [NamedIndividual](NamedIndividual.md) | [consider](consider.md) | domain | ObsoleteAspect |
| [Subset](Subset.md) | [deprecated](deprecated.md) | domain | ObsoleteAspect |
| [Subset](Subset.md) | [has_obsolescence_reason](has_obsolescence_reason.md) | domain | ObsoleteAspect |
| [Subset](Subset.md) | [term_replaced_by](term_replaced_by.md) | domain | ObsoleteAspect |
| [Subset](Subset.md) | [consider](consider.md) | domain | ObsoleteAspect |







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:ObsoleteAspect |
| native | omoschema:ObsoleteAspect |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ObsoleteAspect
description: Auto-classifies anything that is obsolete
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
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
rank: 1000
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