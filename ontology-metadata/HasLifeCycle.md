# Class: HasLifeCycle



URI: [omoschema:HasLifeCycle](http://purl.obolibrary.org/obo/omo/schema/HasLifeCycle)




```{mermaid}
 classDiagram
    class HasLifeCycle
      AnnotationPropertyMixin <|-- HasLifeCycle
      

      HasLifeCycle <|-- Term
      
      
      HasLifeCycle : consider
        
          HasLifeCycle --> Any : consider
        
      HasLifeCycle : deprecated
        
      HasLifeCycle : excluded_from_QC_check
        
          HasLifeCycle --> Thing : excluded_from_QC_check
        
      HasLifeCycle : excluded_subClassOf
        
          HasLifeCycle --> Class : excluded_subClassOf
        
      HasLifeCycle : excluded_synonym
        
      HasLifeCycle : has_alternative_id
        
      HasLifeCycle : has_obsolescence_reason
        
      HasLifeCycle : should_conform_to
        
          HasLifeCycle --> Thing : should_conform_to
        
      HasLifeCycle : term_replaced_by
        
          HasLifeCycle --> Any : term_replaced_by
        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasLifeCycle**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [deprecated](deprecated.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [has_obsolescence_reason](has_obsolescence_reason.md) | 0..1 <br/> [String](String.md) |  | direct |
| [term_replaced_by](term_replaced_by.md) | 0..1 <br/> [Any](Any.md) |  | direct |
| [consider](consider.md) | 0..* <br/> [Any](Any.md) |  | direct |
| [has_alternative_id](has_alternative_id.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) | Relates a live term to a deprecated ID that was merged in | direct |
| [excluded_from_QC_check](excluded_from_QC_check.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |
| [excluded_subClassOf](excluded_subClassOf.md) | 0..* <br/> [Class](Class.md) |  | direct |
| [excluded_synonym](excluded_synonym.md) | 0..* <br/> [String](String.md) |  | direct |
| [should_conform_to](should_conform_to.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |








## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:HasLifeCycle |
| native | omoschema:HasLifeCycle |





## LinkML Source

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
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: owl:deprecated
    alias: deprecated
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: boolean
  has_obsolescence_reason:
    name: has_obsolescence_reason
    todos:
    - restrict range
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0000231
    alias: has_obsolescence_reason
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
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
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: IAO:0100001
    alias: term_replaced_by
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: Any
  consider:
    name: consider
    comments:
    - '{''RULE'': ''subject must be deprecated''}'
    in_subset:
    - go permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: obsoletion_related_property
    domain: ObsoleteAspect
    slot_uri: oio:consider
    multivalued: true
    alias: consider
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
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
    rank: 1000
    is_a: obsoletion_related_property
    domain: NotObsoleteAspect
    slot_uri: oio:hasAlternativeId
    multivalued: true
    alias: has_alternative_id
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: uriorcurie
  excluded_from_QC_check:
    name: excluded_from_QC_check
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: excluded_from_QC_check
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: Thing
  excluded_subClassOf:
    name: excluded_subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_subClassOf
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: Class
  excluded_synonym:
    name: excluded_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:hiddenSynonym
    rank: 1000
    is_a: excluded_axiom
    multivalued: true
    alias: excluded_synonym
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
    range: string
  should_conform_to:
    name: should_conform_to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: excluded_axiom
    alias: should_conform_to
    owner: HasLifeCycle
    domain_of:
    - HasLifeCycle
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