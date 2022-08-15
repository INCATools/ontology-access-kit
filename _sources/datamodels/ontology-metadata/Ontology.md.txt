# Class: Ontology
_An OWL ontology_





URI: [owl:Ontology](http://www.w3.org/2002/07/owl#Ontology)




```{mermaid}
 classDiagram
      NamedObject <|-- Ontology
      
      Ontology : comment
      Ontology : created
      Ontology : creator
      Ontology : has_ontology_root_term
      Ontology : id
      Ontology : imports
      Ontology : license
      Ontology : source
      Ontology : title
      Ontology : type
      Ontology : versionInfo
      Ontology : versionIRI
      

```





## Inheritance
* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * **Ontology**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [title](title.md) | 1..1 <br/> [NarrativeText](NarrativeText.md)  |   |
| [has_ontology_root_term](has_ontology_root_term.md) | 0..* <br/> [Class](Class.md)  |   |
| [license](license.md) | 1..1 <br/> [Thing](Thing.md)  |   |
| [source](source.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [versionIRI](versionIRI.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  |   |
| [versionInfo](versionInfo.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [comment](comment.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [creator](creator.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [created](created.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | when the term came into being  |
| [imports](imports.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [id](id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  | this maps to the URI in RDF  |
| [type](type.md) | 0..* <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasProvenance](HasProvenance.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [Term](Term.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [Class](Class.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [Property](Property.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [AnnotationProperty](AnnotationProperty.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [ObjectProperty](ObjectProperty.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [TransitiveProperty](TransitiveProperty.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [NamedIndividual](NamedIndividual.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |
| [Subset](Subset.md) | [isDefinedBy](isDefinedBy.md) | range | Ontology |



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['owl:Ontology'] |
| native | ['omoschema:Ontology'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Ontology
description: An OWL ontology
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: NamedObject
slots:
- title
- has_ontology_root_term
- license
- source
- versionIRI
- versionInfo
- comment
- creator
- created
- imports
slot_usage:
  title:
    name: title
    domain_of:
    - Ontology
    - Ontology
    required: true
  license:
    name: license
    domain_of:
    - Ontology
    - Ontology
    required: true
  versionIRI:
    name: versionIRI
    domain_of:
    - Ontology
    - Ontology
    required: true
  versionInfo:
    name: versionInfo
    domain_of:
    - Ontology
    - Ontology
    required: true
class_uri: owl:Ontology

```
</details>

### Induced

<details>
```yaml
name: Ontology
description: An OWL ontology
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: NamedObject
slot_usage:
  title:
    name: title
    domain_of:
    - Ontology
    - Ontology
    required: true
  license:
    name: license
    domain_of:
    - Ontology
    - Ontology
    required: true
  versionIRI:
    name: versionIRI
    domain_of:
    - Ontology
    - Ontology
    required: true
  versionInfo:
    name: versionInfo
    domain_of:
    - Ontology
    - Ontology
    required: true
attributes:
  title:
    name: title
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: dcterms:title
    alias: title
    owner: Ontology
    domain_of:
    - Ontology
    - Ontology
    range: narrative text
    required: true
  has_ontology_root_term:
    name: has_ontology_root_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000700
    multivalued: true
    alias: has_ontology_root_term
    owner: Ontology
    domain_of:
    - Ontology
    range: Class
  license:
    name: license
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:license
    alias: license
    owner: Ontology
    domain_of:
    - Ontology
    - Ontology
    range: Thing
    required: true
  source:
    name: source
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:source
    multivalued: true
    alias: source
    owner: Ontology
    domain_of:
    - Ontology
    - Axiom
    range: string
  versionIRI:
    name: versionIRI
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: version_property
    slot_uri: owl:versionIRI
    alias: versionIRI
    owner: Ontology
    domain_of:
    - Ontology
    - Ontology
    range: uriorcurie
    required: true
  versionInfo:
    name: versionInfo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: version_property
    slot_uri: owl:versionInfo
    alias: versionInfo
    owner: Ontology
    domain_of:
    - Ontology
    - Ontology
    range: string
    required: true
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
    owner: Ontology
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: Ontology
    domain_of:
    - HasProvenance
    - Ontology
    range: string
  created:
    name: created
    description: when the term came into being
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    close_mappings:
    - pav:createdOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:created
    multivalued: false
    alias: created
    owner: Ontology
    domain_of:
    - HasProvenance
    - Ontology
    range: string
  imports:
    name: imports
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: owl:imports
    alias: imports
    owner: Ontology
    domain_of:
    - Ontology
    range: string
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: core_property
    identifier: true
    alias: id
    owner: Ontology
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
    owner: Ontology
    domain_of:
    - Thing
    range: uriorcurie
class_uri: owl:Ontology

```
</details>