

# Class: NotObsoleteAspect


_Auto-classifies anything that is not obsolete_





URI: [omoschema:NotObsoleteAspect](https://w3id.org/oak/ontology-metadata/NotObsoleteAspect)






```{mermaid}
 classDiagram
    class NotObsoleteAspect
    click NotObsoleteAspect href "../NotObsoleteAspect"
      
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
| [HasLifeCycle](HasLifeCycle.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Term](Term.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Class](Class.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Property](Property.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [AnnotationProperty](AnnotationProperty.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [ObjectProperty](ObjectProperty.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [TransitiveProperty](TransitiveProperty.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [NamedIndividual](NamedIndividual.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [HomoSapiens](HomoSapiens.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Agent](Agent.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Image](Image.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |
| [Subset](Subset.md) | [has_alternative_id](has_alternative_id.md) | domain | [NotObsoleteAspect](NotObsoleteAspect.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:NotObsoleteAspect |
| native | omoschema:NotObsoleteAspect |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NotObsoleteAspect
description: Auto-classifies anything that is not obsolete
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
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