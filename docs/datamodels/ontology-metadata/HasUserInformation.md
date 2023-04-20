# Class: HasUserInformation



URI: [omoschema:HasUserInformation](http://purl.obolibrary.org/obo/omo/schema/HasUserInformation)



```{mermaid}
 classDiagram
    class HasUserInformation
      AnnotationPropertyMixin <|-- HasUserInformation
      

      HasUserInformation <|-- Term
      
      
      HasUserInformation : comment
        
      HasUserInformation : curator_note
        
      HasUserInformation : depicted_by
        
          HasUserInformation ..> Image : depicted_by
        
      HasUserInformation : example_of_usage
        
      HasUserInformation : has_curation_status
        
      HasUserInformation : image
        
          HasUserInformation ..> Thing : image
        
      HasUserInformation : page
        
      HasUserInformation : seeAlso
        
          HasUserInformation ..> Thing : seeAlso
        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasUserInformation**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [comment](comment.md) | 0..* <br/> [String](String.md) |  | direct |
| [seeAlso](seeAlso.md) | 0..* <br/> [Thing](Thing.md) |  | direct |
| [image](image.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |
| [example_of_usage](example_of_usage.md) | 0..* <br/> [String](String.md) |  | direct |
| [curator_note](curator_note.md) | 0..* <br/> [String](String.md) |  | direct |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> [String](String.md) |  | direct |
| [depicted_by](depicted_by.md) | 0..* <br/> [Image](Image.md) |  | direct |
| [page](page.md) | 0..* <br/> [String](String.md) |  | direct |



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
| self | omoschema:HasUserInformation |
| native | omoschema:HasUserInformation |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasUserInformation
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
slots:
- comment
- seeAlso
- image
- example_of_usage
- curator_note
- has_curation_status
- depicted_by
- page

```
</details>

### Induced

<details>
```yaml
name: HasUserInformation
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: rdfs:seeAlso
    multivalued: true
    alias: seeAlso
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
  image:
    name: image
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: sdo:image
    alias: image
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: Thing
  example_of_usage:
    name: example_of_usage
    in_subset:
    - allotrope permitted profile
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - skos:example
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000112
    multivalued: true
    alias: example_of_usage
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
  curator_note:
    name: curator_note
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000232
    multivalued: true
    alias: curator_note
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
  has_curation_status:
    name: has_curation_status
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000114
    alias: has_curation_status
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
  depicted_by:
    name: depicted_by
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:depicted_by
    multivalued: true
    alias: depicted_by
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: Image
  page:
    name: page
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    multivalued: true
    alias: page
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string

```
</details>