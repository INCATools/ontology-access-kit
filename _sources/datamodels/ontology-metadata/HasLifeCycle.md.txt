# Class: HasLifeCycle



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:HasLifeCycle](http://purl.obolibrary.org/obo/schema/HasLifeCycle)




```{mermaid}
 classDiagram
      AnnotationPropertyMixin <|-- HasLifeCycle
      
      HasLifeCycle : consider
      HasLifeCycle : deprecated
      HasLifeCycle : excluded_from_QC_check
      HasLifeCycle : excluded_subClassOf
      HasLifeCycle : excluded_synonym
      HasLifeCycle : has_alternative_id
      HasLifeCycle : has_obsolescence_reason
      HasLifeCycle : should_conform_to
      HasLifeCycle : term_replaced_by
      

```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasLifeCycle**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [deprecated](deprecated.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [has_obsolescence_reason](has_obsolescence_reason.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [term_replaced_by](term_replaced_by.md) | [Any](Any.md) | 0..1 | None  | . |
| [consider](consider.md) | [Any](Any.md) | 0..* | None  | . |
| [has_alternative_id](has_alternative_id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..* | Relates a live term to a deprecated ID that was merged in  | . |
| [excluded_from_QC_check](excluded_from_QC_check.md) | [Thing](Thing.md) | 0..1 | None  | . |
| [excluded_subClassOf](excluded_subClassOf.md) | [Class](Class.md) | 0..* | None  | . |
| [excluded_synonym](excluded_synonym.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [should_conform_to](should_conform_to.md) | [Thing](Thing.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Rules



## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:HasLifeCycle'] |
| native | ['omoschema:HasLifeCycle'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasLifeCycle
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
slots:
- deprecated
- has_obsolescence_reason
- term_replaced_by
- consider
- has_alternative_id
- excluded_from_QC_check
- excluded_subClassOf
- excluded_synonym
- should_conform_to
rules:
- preconditions:
    slot_conditions:
      deprecated:
        name: deprecated
        equals_expression: 'true'
  postconditions:
    any_of:
    - slot_conditions:
        term_replaced_by:
          name: term_replaced_by
          required: true
    - slot_conditions:
        consider:
          name: consider
          required: true
  description: if a term is deprecated it should have either consider or replaced
    by
- preconditions:
    none_of:
    - slot_conditions:
        deprecated:
          name: deprecated
          equals_expression: 'true'
  postconditions:
    none_of:
    - slot_conditions:
        term_replaced_by:
          name: term_replaced_by
          required: true
    - slot_conditions:
        consider:
          name: consider
          required: true
  description: if a term is not deprecated it should have neither consider nor replaced
    by
- preconditions:
    slot_conditions:
      deprecated:
        name: deprecated
        equals_expression: 'true'
  postconditions:
    slot_conditions:
      label:
        name: label
        pattern: '^obsolete '
  description: if a term is deprecated its label should start with the string obsolete

```
</details>

### Induced

<details>
```yaml
name: HasLifeCycle
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  deprecated:
    name: deprecated
    in_subset:
    - allotrope permitted profile
    - go permitted profile
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    aliases:
    - is obsolete
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: owl:deprecated
    alias: deprecated
    owner: HasLifeCycle
    range: boolean
  has_obsolescence_reason:
    name: has_obsolescence_reason
    todos:
    - restrict range
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0000231
    alias: has_obsolescence_reason
    owner: HasLifeCycle
    range: string
  term_replaced_by:
    name: term_replaced_by
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    - obi permitted profile
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - dcterms:isReplacedBy
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: HasLifeCycle
    range: Any
  consider:
    name: consider
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: oio:consider
    multivalued: true
    alias: consider
    owner: HasLifeCycle
    range: Any
  has_alternative_id:
    name: has_alternative_id
    description: Relates a live term to a deprecated ID that was merged in
    deprecated: This is deprecated as it is redundant with the inverse replaced_by
      triple
    comments:
    - '{''RULE'': ''object must NOT be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    see_also:
    - https://github.com/owlcs/owlapi/issues/317
    is_a: obsoletion_related_property
    domain: NotObsoleteAspect
    slot_uri: oio:hasAlternativeId
    multivalued: true
    alias: has_alternative_id
    owner: HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: HasLifeCycle
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: HasLifeCycle
    range: Class
  excluded_synonym:
    name: excluded_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:hiddenSynonym
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: excluded_axiom
    alias: should_conform_to
    owner: HasLifeCycle
    range: Thing
rules:
- preconditions:
    slot_conditions:
      deprecated:
        name: deprecated
        equals_expression: 'true'
  postconditions:
    any_of:
    - slot_conditions:
        term_replaced_by:
          name: term_replaced_by
          required: true
    - slot_conditions:
        consider:
          name: consider
          required: true
  description: if a term is deprecated it should have either consider or replaced
    by
- preconditions:
    none_of:
    - slot_conditions:
        deprecated:
          name: deprecated
          equals_expression: 'true'
  postconditions:
    none_of:
    - slot_conditions:
        term_replaced_by:
          name: term_replaced_by
          required: true
    - slot_conditions:
        consider:
          name: consider
          required: true
  description: if a term is not deprecated it should have neither consider nor replaced
    by
- preconditions:
    slot_conditions:
      deprecated:
        name: deprecated
        equals_expression: 'true'
  postconditions:
    slot_conditions:
      label:
        name: label
        pattern: '^obsolete '
  description: if a term is deprecated its label should start with the string obsolete

```
</details>