

# Class: PropertyValue


_A generic tag-value that can be associated with an association._





URI: [ontoassoc:PropertyValue](https://w3id.org/oak/association/PropertyValue)






```{mermaid}
 classDiagram
    class PropertyValue
    click PropertyValue href "../PropertyValue"
      PropertyValue : predicate
        
      PropertyValue : value_or_object
        
          
    
    
    PropertyValue --> "0..1" Any : value_or_object
    click Any href "../Any"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The type of relationship between the subject and object | direct |
| [value_or_object](value_or_object.md) | 0..1 <br/> [Any](Any.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) | [property_values](property_values.md) | range | [PropertyValue](PropertyValue.md) |
| [Association](Association.md) | [property_values](property_values.md) | range | [PropertyValue](PropertyValue.md) |
| [NegatedAssociation](NegatedAssociation.md) | [property_values](property_values.md) | range | [PropertyValue](PropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:PropertyValue |
| native | ontoassoc:PropertyValue |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyValue
description: A generic tag-value that can be associated with an association.
from_schema: https://w3id.org/oak/association
slots:
- predicate
- value_or_object

```
</details>

### Induced

<details>
```yaml
name: PropertyValue
description: A generic tag-value that can be associated with an association.
from_schema: https://w3id.org/oak/association
attributes:
  predicate:
    name: predicate
    description: The type of relationship between the subject and object.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdf:predicate
    alias: predicate
    owner: PropertyValue
    domain_of:
    - PositiveOrNegativeAssociation
    - PropertyValue
    slot_group: core_triple
    range: uriorcurie
  value_or_object:
    name: value_or_object
    from_schema: https://w3id.org/oak/association
    rank: 1000
    alias: value_or_object
    owner: PropertyValue
    domain_of:
    - PropertyValue
    range: Any

```
</details>