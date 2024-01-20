# Class: NamedObject
_Anything with an IRI_




URI: [omoschema:NamedObject](http://purl.obolibrary.org/obo/omo/schema/NamedObject)



```{mermaid}
 classDiagram
    class NamedObject
      Thing <|-- NamedObject
      

      NamedObject <|-- Ontology
      NamedObject <|-- Term
      
      
      NamedObject : id
        
      NamedObject : type
        
      
```





## Inheritance
* [Thing](Thing.md)
    * **NamedObject**
        * [Ontology](Ontology.md)
        * [Term](Term.md) [ [HasSynonyms](HasSynonyms.md) [HasLifeCycle](HasLifeCycle.md) [HasProvenance](HasProvenance.md) [HasMappings](HasMappings.md) [HasCategory](HasCategory.md) [HasUserInformation](HasUserInformation.md) [HasMinimalMetadata](HasMinimalMetadata.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | this maps to the URI in RDF | direct |
| [type](type.md) | 0..* <br/> [Uriorcurie](Uriorcurie.md) |  | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Axiom](Axiom.md) | [annotatedSource](annotatedSource.md) | range | [NamedObject](NamedObject.md) |




## Aliases


* named entity
* identified object
* IRI



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:NamedObject |
| native | omoschema:NamedObject |





## LinkML Source

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
rank: 1000
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
rank: 1000
is_a: Thing
attributes:
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: NamedObject
    domain_of:
    - NamedObject
    range: uriorcurie
    required: true
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    designates_type: true
    alias: type
    owner: NamedObject
    domain_of:
    - Thing
    range: uriorcurie

```
</details>