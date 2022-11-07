# Class: Thing


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [owl:Thing](http://www.w3.org/2002/07/owl#Thing)


```{mermaid}
 classDiagram
    class Thing
      Thing <|-- NamedObject
      
      Thing : type
      
```




## Inheritance
* **Thing**
    * [NamedObject](NamedObject.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 0..* <br/> uriorcurie | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasMappings](HasMappings.md) | [broadMatch](broadMatch.md) | range | Thing |
| [HasMappings](HasMappings.md) | [closeMatch](closeMatch.md) | range | Thing |
| [HasMappings](HasMappings.md) | [exactMatch](exactMatch.md) | range | Thing |
| [HasMappings](HasMappings.md) | [narrowMatch](narrowMatch.md) | range | Thing |
| [HasProvenance](HasProvenance.md) | [contributor](contributor.md) | range | Thing |
| [HasLifeCycle](HasLifeCycle.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [HasLifeCycle](HasLifeCycle.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [HasCategory](HasCategory.md) | [conformsTo](conformsTo.md) | range | Thing |
| [HasUserInformation](HasUserInformation.md) | [seeAlso](seeAlso.md) | range | Thing |
| [HasUserInformation](HasUserInformation.md) | [image](image.md) | range | Thing |
| [Ontology](Ontology.md) | [license](license.md) | range | Thing |
| [Term](Term.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [Term](Term.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [Term](Term.md) | [contributor](contributor.md) | range | Thing |
| [Term](Term.md) | [broadMatch](broadMatch.md) | range | Thing |
| [Term](Term.md) | [closeMatch](closeMatch.md) | range | Thing |
| [Term](Term.md) | [exactMatch](exactMatch.md) | range | Thing |
| [Term](Term.md) | [narrowMatch](narrowMatch.md) | range | Thing |
| [Term](Term.md) | [conformsTo](conformsTo.md) | range | Thing |
| [Term](Term.md) | [seeAlso](seeAlso.md) | range | Thing |
| [Term](Term.md) | [image](image.md) | range | Thing |
| [Class](Class.md) | [has_rank](has_rank.md) | range | Thing |
| [Class](Class.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [Class](Class.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [Class](Class.md) | [contributor](contributor.md) | range | Thing |
| [Class](Class.md) | [conformsTo](conformsTo.md) | range | Thing |
| [Class](Class.md) | [seeAlso](seeAlso.md) | range | Thing |
| [Class](Class.md) | [image](image.md) | range | Thing |
| [Property](Property.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [Property](Property.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [Property](Property.md) | [contributor](contributor.md) | range | Thing |
| [Property](Property.md) | [conformsTo](conformsTo.md) | range | Thing |
| [Property](Property.md) | [seeAlso](seeAlso.md) | range | Thing |
| [Property](Property.md) | [image](image.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [contributor](contributor.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [conformsTo](conformsTo.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [seeAlso](seeAlso.md) | range | Thing |
| [AnnotationProperty](AnnotationProperty.md) | [image](image.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [contributor](contributor.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [conformsTo](conformsTo.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [seeAlso](seeAlso.md) | range | Thing |
| [ObjectProperty](ObjectProperty.md) | [image](image.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [contributor](contributor.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [conformsTo](conformsTo.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [seeAlso](seeAlso.md) | range | Thing |
| [TransitiveProperty](TransitiveProperty.md) | [image](image.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [contributor](contributor.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [broadMatch](broadMatch.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [closeMatch](closeMatch.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [exactMatch](exactMatch.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [narrowMatch](narrowMatch.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [conformsTo](conformsTo.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [seeAlso](seeAlso.md) | range | Thing |
| [NamedIndividual](NamedIndividual.md) | [image](image.md) | range | Thing |
| [Axiom](Axiom.md) | [has_axiom_label](has_axiom_label.md) | range | Thing |
| [Axiom](Axiom.md) | [seeAlso](seeAlso.md) | range | Thing |
| [Subset](Subset.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | Thing |
| [Subset](Subset.md) | [should_conform_to](should_conform_to.md) | range | Thing |
| [Subset](Subset.md) | [contributor](contributor.md) | range | Thing |
| [Subset](Subset.md) | [conformsTo](conformsTo.md) | range | Thing |
| [Subset](Subset.md) | [seeAlso](seeAlso.md) | range | Thing |
| [Subset](Subset.md) | [image](image.md) | range | Thing |







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Thing |
| native | omoschema:Thing |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Thing
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
abstract: true
slots:
- type
class_uri: owl:Thing

```
</details>

### Induced

<details>
```yaml
name: Thing
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
abstract: true
attributes:
  type:
    name: type
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    multivalued: true
    designates_type: true
    alias: type
    owner: Thing
    domain_of:
    - Thing
    range: uriorcurie
class_uri: owl:Thing

```
</details>