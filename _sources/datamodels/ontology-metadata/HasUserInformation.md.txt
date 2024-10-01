

# Class: HasUserInformation



URI: [omoschema:HasUserInformation](https://w3id.org/oak/ontology-metadata/HasUserInformation)






```{mermaid}
 classDiagram
    class HasUserInformation
    click HasUserInformation href "../HasUserInformation"
      AnnotationPropertyMixin <|-- HasUserInformation
        click AnnotationPropertyMixin href "../AnnotationPropertyMixin"
      

      HasUserInformation <|-- Term
        click Term href "../Term"
      
      
      HasUserInformation : comment
        
      HasUserInformation : curator_note
        
      HasUserInformation : depicted_by
        
          
    
    
    HasUserInformation --> "*" Image : depicted_by
    click Image href "../Image"

        
      HasUserInformation : example_of_usage
        
      HasUserInformation : has_curation_status
        
      HasUserInformation : image
        
          
    
    
    HasUserInformation --> "0..1" Thing : image
    click Thing href "../Thing"

        
      HasUserInformation : page
        
      HasUserInformation : seeAlso
        
          
    
    
    HasUserInformation --> "*" Thing : seeAlso
    click Thing href "../Thing"

        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasUserInformation**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [comment](comment.md) | * <br/> [String](String.md) |  | direct |
| [seeAlso](seeAlso.md) | * <br/> [Thing](Thing.md) |  | direct |
| [image](image.md) | 0..1 <br/> [Thing](Thing.md) |  | direct |
| [example_of_usage](example_of_usage.md) | * <br/> [String](String.md) |  | direct |
| [curator_note](curator_note.md) | * <br/> [String](String.md) |  | direct |
| [has_curation_status](has_curation_status.md) | 0..1 <br/> [String](String.md) |  | direct |
| [depicted_by](depicted_by.md) | * <br/> [Image](Image.md) |  | direct |
| [page](page.md) | * <br/> [String](String.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    alias: comment
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
    multivalued: true
  seeAlso:
    name: seeAlso
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: rdfs:seeAlso
    alias: seeAlso
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    - Axiom
    range: Thing
    multivalued: true
  image:
    name: image
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - skos:example
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000112
    alias: example_of_usage
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true
  curator_note:
    name: curator_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000232
    alias: curator_note
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true
  has_curation_status:
    name: has_curation_status
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:depicted_by
    alias: depicted_by
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: Image
    multivalued: true
  page:
    name: page
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: foaf:page
    alias: page
    owner: HasUserInformation
    domain_of:
    - HasUserInformation
    range: string
    multivalued: true

```
</details>