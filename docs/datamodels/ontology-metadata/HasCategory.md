

# Class: HasCategory



URI: [omoschema:HasCategory](https://w3id.org/oak/ontology-metadata/HasCategory)






```{mermaid}
 classDiagram
    class HasCategory
    click HasCategory href "../HasCategory"
      AnnotationPropertyMixin <|-- HasCategory
        click AnnotationPropertyMixin href "../AnnotationPropertyMixin"
      

      HasCategory <|-- Term
        click Term href "../Term"
      
      
      HasCategory : category
        
      HasCategory : conformsTo
        
          
    
    
    HasCategory --> "*" Thing : conformsTo
    click Thing href "../Thing"

        
      HasCategory : has_obo_namespace
        
      HasCategory : in_subset
        
          
    
    
    HasCategory --> "*" Subset : in_subset
    click Subset href "../Subset"

        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasCategory**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_obo_namespace](has_obo_namespace.md) | * <br/> [String](String.md) |  | direct |
| [category](category.md) | 0..1 <br/> [String](String.md) |  | direct |
| [in_subset](in_subset.md) | * <br/> [Subset](Subset.md) | Maps an ontology element to a subset it belongs to | direct |
| [conformsTo](conformsTo.md) | * <br/> [Thing](Thing.md) |  | direct |



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
| self | omoschema:HasCategory |
| native | omoschema:HasCategory |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasCategory
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
slots:
- has_obo_namespace
- category
- in_subset
- conformsTo

```
</details>

### Induced

<details>
```yaml
name: HasCategory
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:hasOBONamespace
    alias: has_obo_namespace
    owner: HasCategory
    domain_of:
    - HasCategory
    range: string
    multivalued: true
  category:
    name: category
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: HasCategory
    domain_of:
    - HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: oio:inSubset
    alias: in_subset
    owner: HasCategory
    domain_of:
    - HasCategory
    range: Subset
    multivalued: true
  conformsTo:
    name: conformsTo
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    alias: conformsTo
    owner: HasCategory
    domain_of:
    - HasCategory
    range: Thing
    multivalued: true

```
</details>