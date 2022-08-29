# Class: GlobalStatistics
_summary statistics for the entire resource_





URI: [reporting:GlobalStatistics](https://w3id.org/linkml/reportGlobalStatistics)




```{mermaid}
 classDiagram
      SummaryStatisticCollection <|-- GlobalStatistics
      
      GlobalStatistics : annotation_property_count
      GlobalStatistics : anonymous_class_expression_count
      GlobalStatistics : anonymous_individual_count
      GlobalStatistics : by_category
      GlobalStatistics : by_ontology
      GlobalStatistics : by_subset
      GlobalStatistics : by_taxon
      GlobalStatistics : class_count
      GlobalStatistics : class_count_excluding_deprecated
      GlobalStatistics : class_count_with_definitions
      GlobalStatistics : datatype_property_count
      GlobalStatistics : description_logic_profile
      GlobalStatistics : distinct_synonym_count
      GlobalStatistics : equivalentclasses_axiom_count
      GlobalStatistics : individual_count
      GlobalStatistics : mapping_count
      GlobalStatistics : named_individual_count
      GlobalStatistics : object_property_count
      GlobalStatistics : ontology_count
      GlobalStatistics : owl_axiom_count
      GlobalStatistics : property_count
      GlobalStatistics : rdf_triple_count
      GlobalStatistics : subclass_of_axiom_count
      GlobalStatistics : synonym_statement_count
      GlobalStatistics : unsatisfiable_class_count
      GlobalStatistics : untyped_entity_count
      

```





## Inheritance
* [SummaryStatisticCollection](SummaryStatisticCollection.md)
    * **GlobalStatistics**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [by_category](by_category.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md)  | statistics keyed by category  |
| [by_taxon](by_taxon.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md)  | statistics keyed by organism taxon  |
| [by_ontology](by_ontology.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md)  | statistics keyed by ontology  |
| [by_subset](by_subset.md) | 0..* <br/> [FacetStatistics](FacetStatistics.md)  | statistics keyed by ontology subset  |
| [class_count](class_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [anonymous_class_expression_count](anonymous_class_expression_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [unsatisfiable_class_count](unsatisfiable_class_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [class_count_excluding_deprecated](class_count_excluding_deprecated.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [class_count_with_definitions](class_count_with_definitions.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [property_count](property_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [object_property_count](object_property_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [datatype_property_count](datatype_property_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [annotation_property_count](annotation_property_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [individual_count](individual_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [named_individual_count](named_individual_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [anonymous_individual_count](anonymous_individual_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [untyped_entity_count](untyped_entity_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [description_logic_profile](description_logic_profile.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [owl_axiom_count](owl_axiom_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [rdf_triple_count](rdf_triple_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [subclass_of_axiom_count](subclass_of_axiom_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [equivalentclasses_axiom_count](equivalentclasses_axiom_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [distinct_synonym_count](distinct_synonym_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [synonym_statement_count](synonym_statement_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [mapping_count](mapping_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [ontology_count](ontology_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['reporting:GlobalStatistics'] |
| native | ['reporting:GlobalStatistics'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: SummaryStatisticCollection
attributes:
  by_category:
    name: by_category
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_taxon:
    name: by_taxon
    description: statistics keyed by organism taxon
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_ontology:
    name: by_ontology
    description: statistics keyed by ontology
    comments:
    - if a large ontology collection like OntoBee is indexed then it makes sense to
      break stats into each sub-ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true
  by_subset:
    name: by_subset
    description: statistics keyed by ontology subset
    comments:
    - For example, GO metagenomics_slim
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: FacetStatistics
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: SummaryStatisticCollection
attributes:
  by_category:
    name: by_category
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_category
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_taxon:
    name: by_taxon
    description: statistics keyed by organism taxon
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_taxon
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_ontology:
    name: by_ontology
    description: statistics keyed by ontology
    comments:
    - if a large ontology collection like OntoBee is indexed then it makes sense to
      break stats into each sub-ontology
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_ontology
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  by_subset:
    name: by_subset
    description: statistics keyed by ontology subset
    comments:
    - For example, GO metagenomics_slim
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: by_subset
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: FacetStatistics
    inlined: true
  class_count:
    name: class_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  anonymous_class_expression_count:
    name: anonymous_class_expression_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_class_expression_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  unsatisfiable_class_count:
    name: unsatisfiable_class_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: unsatisfiable_class_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  class_count_excluding_deprecated:
    name: class_count_excluding_deprecated
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_excluding_deprecated
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  class_count_with_definitions:
    name: class_count_with_definitions
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: class_count_with_definitions
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: class_statistic_group
    range: integer
  property_count:
    name: property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: property_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  object_property_count:
    name: object_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: object_property_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  datatype_property_count:
    name: datatype_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: datatype_property_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  annotation_property_count:
    name: annotation_property_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: annotation_property_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: property_statistic_group
    range: integer
  individual_count:
    name: individual_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: individual_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
  named_individual_count:
    name: named_individual_count
    annotations:
      count_of:
        tag: count_of
        value: owl:NamedIndividual
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: named_individual_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
  anonymous_individual_count:
    name: anonymous_individual_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: anonymous_individual_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: individual_statistic_group
    range: integer
    equals_expression: '{named_individual_count} - {individual_count}'
  untyped_entity_count:
    name: untyped_entity_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: untyped_entity_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    range: integer
  description_logic_profile:
    name: description_logic_profile
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    alias: description_logic_profile
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: string
  owl_axiom_count:
    name: owl_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: owl_axiom_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  rdf_triple_count:
    name: rdf_triple_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: rdf_triple_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  subclass_of_axiom_count:
    name: subclass_of_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: subclass_of_axiom_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  equivalentclasses_axiom_count:
    name: equivalentclasses_axiom_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: equivalentclasses_axiom_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: owl_statistic_group
    range: integer
  distinct_synonym_count:
    name: distinct_synonym_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: distinct_synonym_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  synonym_statement_count:
    name: synonym_statement_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: synonym_statement_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  mapping_count:
    name: mapping_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: mapping_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    slot_group: metadata_statistic_group
    range: integer
  ontology_count:
    name: ontology_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    is_a: count_statistic
    alias: ontology_count
    owner: GlobalStatistics
    domain_of:
    - SummaryStatisticCollection
    range: integer

```
</details>