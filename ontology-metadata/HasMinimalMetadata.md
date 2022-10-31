# Class: HasMinimalMetadata
_Absolute minimum metadata model_




* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:HasMinimalMetadata](http://purl.obolibrary.org/obo/schema/HasMinimalMetadata)


```{mermaid}
 classDiagram
    class HasMinimalMetadata
      AnnotationPropertyMixin <|-- HasMinimalMetadata
      
      HasMinimalMetadata : definition
      HasMinimalMetadata : label
      

      HasMinimalMetadata <|-- Term
      
      HasMinimalMetadata : definition
      HasMinimalMetadata : label
      
```




## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasMinimalMetadata**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [label](label.md) | 0..1 <br/> [LabelType](LabelType.md) | None  | direct |
| [definition](definition.md) | 0..* <br/> [NarrativeText](NarrativeText.md) | None  | direct |




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:HasMinimalMetadata']|join(', ') |
| native | ['omoschema:HasMinimalMetadata']|join(', ') |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasMinimalMetadata
description: Absolute minimum metadata model
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
slots:
- label
- definition

```
</details>

### Induced

<details>
```yaml
name: HasMinimalMetadata
description: Absolute minimum metadata model
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  label:
    name: label
    comments:
    - SHOULD follow OBO label guidelines
    - MUST be unique within an ontology
    - SHOULD be unique across OBO
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    is_a: core_property
    slot_uri: rdfs:label
    multivalued: false
    alias: label
    owner: HasMinimalMetadata
    domain_of:
    - HasMinimalMetadata
    - Axiom
    range: label type
  definition:
    name: definition
    comments:
    - SHOULD be in Aristotelian (genus-differentia) form
    in_subset:
    - allotrope required profile
    - go required profile
    - obi required profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:definition
    rank: 1000
    is_a: core_property
    slot_uri: IAO:0000115
    multivalued: true
    alias: definition
    owner: HasMinimalMetadata
    domain_of:
    - HasMinimalMetadata
    range: narrative text

```
</details>