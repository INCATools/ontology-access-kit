

# Class: HasSynonyms


_a mixin for a class whose members can have synonyms_





URI: [omoschema:HasSynonyms](https://w3id.org/oak/ontology-metadata/HasSynonyms)






```{mermaid}
 classDiagram
    class HasSynonyms
    click HasSynonyms href "../HasSynonyms"
      AnnotationPropertyMixin <|-- HasSynonyms
        click AnnotationPropertyMixin href "../AnnotationPropertyMixin"
      

      HasSynonyms <|-- Term
        click Term href "../Term"
      
      
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
| [has_exact_synonym](has_exact_synonym.md) | * <br/> [LabelType](LabelType.md) |  | direct |
| [has_narrow_synonym](has_narrow_synonym.md) | * <br/> [LabelType](LabelType.md) |  | direct |
| [has_broad_synonym](has_broad_synonym.md) | * <br/> [LabelType](LabelType.md) |  | direct |
| [has_related_synonym](has_related_synonym.md) | * <br/> [LabelType](LabelType.md) |  | direct |
| [alternative_term](alternative_term.md) | * <br/> [String](String.md) |  | direct |
| [ISA_alternative_term](ISA_alternative_term.md) | * <br/> [String](String.md) |  | direct |
| [IEDB_alternative_term](IEDB_alternative_term.md) | * <br/> [String](String.md) |  | direct |
| [editor_preferred_term](editor_preferred_term.md) | * <br/> [String](String.md) |  | direct |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | * <br/> [String](String.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |








## Comments

* the GO-style synonym model has four distinct scopes, with additional types as annotation axioms
* the OBI synonym model is to use alternative_term, or potentially a subproperty

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  has_exact_synonym:
    name: has_exact_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasExactSynonym
    alias: has_exact_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    - Axiom
    disjoint_with:
    - label
    range: label type
    multivalued: true
  has_narrow_synonym:
    name: has_narrow_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasNarrowSynonym
    alias: has_narrow_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  has_broad_synonym:
    name: has_broad_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: synonym
    slot_uri: oio:hasBroadSynonym
    alias: has_broad_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  has_related_synonym:
    name: has_related_synonym
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasRelatedSynonym
    alias: has_related_synonym
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: label type
    multivalued: true
  alternative_term:
    name: alternative_term
    in_subset:
    - allotrope permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:altLabel
    rank: 1000
    slot_uri: IAO:0000118
    alias: alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  ISA_alternative_term:
    name: ISA_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:0001847
    alias: ISA_alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  IEDB_alternative_term:
    name: IEDB_alternative_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: OBI:9991118
    alias: IEDB_alternative_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  editor_preferred_term:
    name: editor_preferred_term
    in_subset:
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000111
    alias: editor_preferred_term
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true
  OBO_foundry_unique_label:
    name: OBO_foundry_unique_label
    todos:
    - add uniquekey
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: alternative_term
    slot_uri: IAO:0000589
    alias: OBO_foundry_unique_label
    owner: HasSynonyms
    domain_of:
    - HasSynonyms
    range: string
    multivalued: true

```
</details>