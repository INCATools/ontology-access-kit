

# Class: NamedObject


_Anything with an IRI_





URI: [omoschema:NamedObject](https://w3id.org/oak/ontology-metadata/NamedObject)






```{mermaid}
 classDiagram
    class NamedObject
    click NamedObject href "../NamedObject"
      Thing <|-- NamedObject
        click Thing href "../Thing"
      

      NamedObject <|-- Ontology
        click Ontology href "../Ontology"
      NamedObject <|-- Term
        click Term href "../Term"
      
      
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
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | this maps to the URI in RDF | direct |
| [type](type.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | [Thing](Thing.md) |





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


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
aliases:
- named entity
- identified object
- IRI
is_a: Thing
attributes:
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    designates_type: true
    alias: type
    owner: NamedObject
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true

```
</details>