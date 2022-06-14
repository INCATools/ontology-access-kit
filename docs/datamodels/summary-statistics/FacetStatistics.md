# Class: FacetStatistics
_summary statistics for a data facet_





URI: [reporting:FacetStatistics](https://w3id.org/linkml/reportFacetStatistics)




```{mermaid}
 classDiagram
      SummaryStatisticCollection <|-- FacetStatistics
      
      FacetStatistics : annotation_property_count
      FacetStatistics : anonymous_class_expression_count
      FacetStatistics : anonymous_individual_count
      FacetStatistics : class_count
      FacetStatistics : class_count_excluding_deprecated
      FacetStatistics : class_count_with_definitions
      FacetStatistics : datatype_property_count
      FacetStatistics : description_logic_profile
      FacetStatistics : distinct_synonym_count
      FacetStatistics : equivalentclasses_axiom_count
      FacetStatistics : facet
      FacetStatistics : individual_count
      FacetStatistics : mapping_count
      FacetStatistics : named_individual_count
      FacetStatistics : object_property_count
      FacetStatistics : ontology_count
      FacetStatistics : owl_axiom_count
      FacetStatistics : property_count
      FacetStatistics : rdf_triple_count
      FacetStatistics : subclass_of_axiom_count
      FacetStatistics : synonym_statement_count
      FacetStatistics : unsatisfiable_class_count
      FacetStatistics : untyped_entity_count
      

```





## Inheritance
* [SummaryStatisticCollection](SummaryStatisticCollection.md)
    * **FacetStatistics**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [facet](facet.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [class_count](class_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [class_count_excluding_deprecated](class_count_excluding_deprecated.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [class_count_with_definitions](class_count_with_definitions.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [property_count](property_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [object_property_count](object_property_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [datatype_property_count](datatype_property_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [annotation_property_count](annotation_property_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [individual_count](individual_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [named_individual_count](named_individual_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [anonymous_individual_count](anonymous_individual_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [untyped_entity_count](untyped_entity_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [description_logic_profile](description_logic_profile.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [owl_axiom_count](owl_axiom_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [rdf_triple_count](rdf_triple_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [equivalentclasses_axiom_count](equivalentclasses_axiom_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [distinct_synonym_count](distinct_synonym_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [synonym_statement_count](synonym_statement_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [mapping_count](mapping_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [ontology_count](ontology_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GlobalStatistics](GlobalStatistics.md) | [by_category](by_category.md) | range | FacetStatistics |
| [GlobalStatistics](GlobalStatistics.md) | [by_taxon](by_taxon.md) | range | FacetStatistics |
| [GlobalStatistics](GlobalStatistics.md) | [by_ontology](by_ontology.md) | range | FacetStatistics |
| [GlobalStatistics](GlobalStatistics.md) | [by_subset](by_subset.md) | range | FacetStatistics |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['reporting:FacetStatistics'] |
| native | ['reporting:FacetStatistics'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: FacetStatistics
description: summary statistics for a data facet
from_schema: https://w3id.org/linkml/summary_statistics
is_a: SummaryStatisticCollection
attributes:
  facet:
    name: facet
    from_schema: https://w3id.org/linkml/summary_statistics
    key: true

```
</details>

### Induced

<details>
```yaml
name: FacetStatistics
description: summary statistics for a data facet
from_schema: https://w3id.org/linkml/summary_statistics
is_a: SummaryStatisticCollection
attributes:
  facet:
    name: facet
    from_schema: https://w3id.org/linkml/summary_statistics
    key: true
    alias: facet
    owner: FacetStatistics
    range: string
  class_count:
    name: class_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: class_count
    owner: FacetStatistics
    slot_group: class_statistic_group
    range: integer
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: anonymous_class_expression_count
    owner: FacetStatistics
    slot_group: class_statistic_group
    range: integer
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: unsatisfiable_class_count
    owner: FacetStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_excluding_deprecated:
    name: class_count_excluding_deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: class_count_excluding_deprecated
    owner: FacetStatistics
    slot_group: class_statistic_group
    range: integer
  class_count_with_definitions:
    name: class_count_with_definitions
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: class_count_with_definitions
    owner: FacetStatistics
    slot_group: class_statistic_group
    range: integer
  property_count:
    name: property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: property_count
    owner: FacetStatistics
    slot_group: property_statistic_group
    range: integer
  object_property_count:
    name: object_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: object_property_count
    owner: FacetStatistics
    slot_group: property_statistic_group
    range: integer
  datatype_property_count:
    name: datatype_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: datatype_property_count
    owner: FacetStatistics
    slot_group: property_statistic_group
    range: integer
  annotation_property_count:
    name: annotation_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: annotation_property_count
    owner: FacetStatistics
    slot_group: property_statistic_group
    range: integer
  individual_count:
    name: individual_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: individual_count
    owner: FacetStatistics
    slot_group: individual_statistic_group
    range: integer
  named_individual_count:
    name: named_individual_count
    annotations:
      count_of:
        tag: count_of
        value: owl:NamedIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: named_individual_count
    owner: FacetStatistics
    slot_group: individual_statistic_group
    range: integer
  anonymous_individual_count:
    name: anonymous_individual_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: anonymous_individual_count
    owner: FacetStatistics
    slot_group: individual_statistic_group
    range: integer
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: untyped_entity_count
    owner: FacetStatistics
    range: integer
  description_logic_profile:
    name: description_logic_profile
    from_schema: https://w3id.org/linkml/summary_statistics
    alias: description_logic_profile
    owner: FacetStatistics
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: owl_axiom_count
    owner: FacetStatistics
    slot_group: owl_statistic_group
    range: integer
  rdf_triple_count:
    name: rdf_triple_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: rdf_triple_count
    owner: FacetStatistics
    slot_group: owl_statistic_group
    range: integer
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: subclass_of_axiom_count
    owner: FacetStatistics
    slot_group: owl_statistic_group
    range: integer
  equivalentclasses_axiom_count:
    name: equivalentclasses_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: equivalentclasses_axiom_count
    owner: FacetStatistics
    slot_group: owl_statistic_group
    range: integer
  distinct_synonym_count:
    name: distinct_synonym_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: distinct_synonym_count
    owner: FacetStatistics
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count:
    name: synonym_statement_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: synonym_statement_count
    owner: FacetStatistics
    slot_group: metadata_statistic_group
    range: integer
  mapping_count:
    name: mapping_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: mapping_count
    owner: FacetStatistics
    slot_group: metadata_statistic_group
    range: integer
  ontology_count:
    name: ontology_count
    from_schema: https://w3id.org/linkml/summary_statistics
    is_a: count_statistic
    alias: ontology_count
    owner: FacetStatistics
    range: integer

```
</details>