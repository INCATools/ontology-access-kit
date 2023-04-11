# Class: HasSynonyms
_a mixin for a class whose members can have synonyms_




URI: [omoschema:HasSynonyms](http://purl.obolibrary.org/obo/omo/schema/HasSynonyms)



```{mermaid}
 classDiagram
    class HasSynonyms
      AnnotationPropertyMixin <|-- HasSynonyms
      

      HasSynonyms <|-- Term
      
      
      HasSynonyms : alternative_term
        
      HasSynonyms : editor_preferred_term
        
      HasSynonyms : has_broad_synonym
        
      HasSynonyms : has_exact_synonym
        
      HasSynonyms : has_narrow_synonym
        
      HasSynonyms : has_related_synonym
        
      HasSynonyms : IEDB_alternative_term
        
      HasSynonyms : ISA_alternative_term
        
      HasSynonyms : OBO_foundry_unique_label
        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasSynonyms**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_exact_synonym](has_exact_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | direct |
| [has_narrow_synonym](has_narrow_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | direct |
| [has_broad_synonym](has_broad_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | direct |
| [has_related_synonym](has_related_synonym.md) | 0..* <br/> [LabelType](LabelType.md) |  | direct |
| [alternative_term](alternative_term.md) | 0..* <br/> [String](String.md) |  | direct |
| [ISA_alternative_term](ISA_alternative_term.md) | 0..* <br/> [String](String.md) |  | direct |
| [IEDB_alternative_term](IEDB_alternative_term.md) | 0..* <br/> [String](String.md) |  | direct |
| [editor_preferred_term](editor_preferred_term.md) | 0..* <br/> [String](String.md) |  | direct |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | 0..* <br/> [String](String.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |








## Comments

* the GO-style synonym model has four distinct scopes, with additional types as annotation axioms
* the OBI synonym model is to use alternative_term, or potentially a subproperty

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:HasSynonyms |
| native | omoschema:HasSynonyms |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasSynonyms
description: a mixin for a class whose members can have synonyms
comments:
- the GO-style synonym model has four distinct scopes, with additional types as annotation
  axioms
- the OBI synonym model is to use alternative_term, or potentially a subproperty
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
slots:
- has_exact_synonym
- has_narrow_synonym
- has_broad_synonym
- has_related_synonym
- alternative_term
- ISA_alternative_term
- IEDB_alternative_term
- editor_preferred_term
- OBO_foundry_unique_label

```
</details>

### Induced

<details>
```yaml
name: HasSynonyms
description: a mixin for a class whose members can have synonyms
comments:
- the GO-style synonym model has four distinct scopes, with additional types as annotation
  axioms
- the OBI synonym model is to use alternative_term, or potentially a subproperty
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    multivalued: true
    alias: has_exact_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    multivalued: true
    alias: has_narrow_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    multivalued: true
    alias: has_broad_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
  has_related_synonym:
    name: has_related_synonym
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:hasRelatedSynonym
    multivalued: true
    alias: has_related_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:altLabel
    rank: 1000
    slot_uri: IAO:0000118
    multivalued: true
    alias: alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:0001847
    multivalued: true
    alias: ISA_alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:9991118
    multivalued: true
    alias: IEDB_alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000111
    multivalued: true
    alias: editor_preferred_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000589
    multivalued: true
    alias: OBO_foundry_unique_label
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string

```
</details>