# Class: Ontology




URI: [owl:Ontology](http://www.w3.org/2002/07/owl#Ontology)




## Inheritance

* [Thing](Thing.md)
    * [NamedObject](NamedObject.md)
        * **Ontology**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [has_ontology_root_term](has_ontology_root_term.md) | [Class](Class.md) | 0..* | None  | . |
| [license](license.md) | [Thing](Thing.md) | 1..1 | None  | . |
| [source](source.md) | [string](string.md) | 0..* | None  | . |
| [versionIRI](versionIRI.md) | [uriorcurie](uriorcurie.md) | 1..1 | None  | . |
| [versionInfo](versionInfo.md) | [string](string.md) | 1..1 | None  | . |
| [comment](comment.md) | [string](string.md) | 0..* | None  | . |
| [creator](creator.md) | [string](string.md) | 0..* | None  | . |
| [imports](imports.md) | [string](string.md) | 0..1 | None  | . |
| [id](id.md) | [uriorcurie](uriorcurie.md) | 1..1 | this maps to the URI in RDF  | . |


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









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Ontology
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: NamedObject
slots:
- has_ontology_root_term
- license
- source
- versionIRI
- versionInfo
- comment
- creator
- imports
slot_usage:
  title:
    name: title
    required: true
  license:
    name: license
    required: true
  versionIRI:
    name: versionIRI
    required: true
  versionInfo:
    name: versionInfo
    required: true
class_uri: owl:Ontology

```
</details>

### Induced

<details>
```yaml
name: Ontology
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: NamedObject
slot_usage:
  title:
    name: title
    required: true
  license:
    name: license
    required: true
  versionIRI:
    name: versionIRI
    required: true
  versionInfo:
    name: versionInfo
    required: true
attributes:
  has_ontology_root_term:
    name: has_ontology_root_term
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: IAO:0000700
    multivalued: true
    alias: has_ontology_root_term
    owner: Ontology
    range: Class
  license:
    name: license
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: dcterms:license
    alias: license
    owner: Ontology
    range: Thing
    required: true
  source:
    name: source
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:source
    multivalued: true
    alias: source
    owner: Ontology
    range: string
  versionIRI:
    name: versionIRI
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: version_property
    slot_uri: owl:versionIRI
    alias: versionIRI
    owner: Ontology
    range: uriorcurie
    required: true
  versionInfo:
    name: versionInfo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: version_property
    slot_uri: owl:versionInfo
    alias: versionInfo
    owner: Ontology
    range: string
    required: true
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: rdfs:comment
    multivalued: true
    alias: comment
    owner: Ontology
    range: string
  creator:
    name: creator
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: provenance_property
    slot_uri: dcterms:creator
    multivalued: true
    alias: creator
    owner: Ontology
    range: string
  imports:
    name: imports
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: owl:imports
    alias: imports
    owner: Ontology
    range: string
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: Ontology
    range: uriorcurie
    required: true
class_uri: owl:Ontology

```
</details>