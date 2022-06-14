# Class: NamedObject
_Anything with an IRI_





URI: [omoschema:NamedObject](http://purl.obolibrary.org/obo/schema/NamedObject)




```{mermaid}
 classDiagram
      Thing <|-- NamedObject
      
      NamedObject : id
      NamedObject : type
      

```





## Inheritance
* [Thing](Thing.md)
    * **NamedObject**
        * [Ontology](Ontology.md)
        * [Term](Term.md) [ HasSynonyms HasLifeCycle HasProvenance HasMappings HasCategory HasUserInformation HasMinimalMetadata]



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | this maps to the URI in RDF  | . |
| [type](type.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Axiom](Axiom.md) | [annotatedSource](annotatedSource.md) | range | NamedObject |



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:NamedObject'] |
| native | ['omoschema:NamedObject'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedObject
description: Anything with an IRI
from_schema: http://purl.obolibrary.org/obo/omo/schema
aliases:
- named entity
- identified object
- IRI
is_a: Thing
slots:
- id

```
</details>

### Induced

<details>
```yaml
name: NamedObject
description: Anything with an IRI
from_schema: http://purl.obolibrary.org/obo/omo/schema
aliases:
- named entity
- identified object
- IRI
is_a: Thing
attributes:
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: NamedObject
    range: uriorcurie
    required: true
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    designates_type: true
    alias: type
    owner: NamedObject
    range: uriorcurie

```
</details>