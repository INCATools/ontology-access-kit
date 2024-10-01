

# Class: Thing


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [owl:Thing](http://www.w3.org/2002/07/owl#Thing)






```{mermaid}
 classDiagram
    class Thing
    click Thing href "../Thing"
      Thing <|-- NamedObject
        click NamedObject href "../NamedObject"
      
      Thing : type
        
      
```





## Inheritance
* **Thing**
    * [NamedObject](NamedObject.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasMappings](HasMappings.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [HasMappings](HasMappings.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [HasMappings](HasMappings.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [HasMappings](HasMappings.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [HasLifeCycle](HasLifeCycle.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [HasLifeCycle](HasLifeCycle.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [HasCategory](HasCategory.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [HasUserInformation](HasUserInformation.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [HasUserInformation](HasUserInformation.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Ontology](Ontology.md) | [license](license.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Term](Term.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [has_rank](has_rank.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Class](Class.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Property](Property.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Property](Property.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Property](Property.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Property](Property.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Property](Property.md) | [image](image.md) | range | [Thing](Thing.md) |
| [AnnotationProperty](AnnotationProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [AnnotationProperty](AnnotationProperty.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [AnnotationProperty](AnnotationProperty.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [AnnotationProperty](AnnotationProperty.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [AnnotationProperty](AnnotationProperty.md) | [image](image.md) | range | [Thing](Thing.md) |
| [ObjectProperty](ObjectProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [ObjectProperty](ObjectProperty.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [ObjectProperty](ObjectProperty.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [ObjectProperty](ObjectProperty.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [ObjectProperty](ObjectProperty.md) | [image](image.md) | range | [Thing](Thing.md) |
| [TransitiveProperty](TransitiveProperty.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [TransitiveProperty](TransitiveProperty.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [TransitiveProperty](TransitiveProperty.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [TransitiveProperty](TransitiveProperty.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [TransitiveProperty](TransitiveProperty.md) | [image](image.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [NamedIndividual](NamedIndividual.md) | [image](image.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [HomoSapiens](HomoSapiens.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Agent](Agent.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [broadMatch](broadMatch.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [closeMatch](closeMatch.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [exactMatch](exactMatch.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [narrowMatch](narrowMatch.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Image](Image.md) | [image](image.md) | range | [Thing](Thing.md) |
| [Axiom](Axiom.md) | [has_axiom_label](has_axiom_label.md) | range | [Thing](Thing.md) |
| [Axiom](Axiom.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Subset](Subset.md) | [excluded_from_QC_check](excluded_from_QC_check.md) | range | [Thing](Thing.md) |
| [Subset](Subset.md) | [should_conform_to](should_conform_to.md) | range | [Thing](Thing.md) |
| [Subset](Subset.md) | [conformsTo](conformsTo.md) | range | [Thing](Thing.md) |
| [Subset](Subset.md) | [seeAlso](seeAlso.md) | range | [Thing](Thing.md) |
| [Subset](Subset.md) | [image](image.md) | range | [Thing](Thing.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
abstract: true
attributes:
  type:
    name: type
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    designates_type: true
    alias: type
    owner: Thing
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true
class_uri: owl:Thing

```
</details>