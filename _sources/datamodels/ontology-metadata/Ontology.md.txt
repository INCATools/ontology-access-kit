

# Class: Ontology


_An OWL ontology_





URI: [owl:Ontology](http://www.w3.org/2002/07/owl#Ontology)






```{mermaid}
 classDiagram
    class Ontology
    click Ontology href "../Ontology"
      NamedObject <|-- Ontology
        click NamedObject href "../NamedObject"
      
      Ontology : comment
        
      Ontology : created
        
      Ontology : creator
        
          
    
    
    Ontology --> "*" Agent : creator
    click Agent href "../Agent"

        
      Ontology : has_ontology_root_term
        
          
    
    
    Ontology --> "*" Class : has_ontology_root_term
    click Class href "../Class"

        
      Ontology : id
        
      Ontology : imports
        
      Ontology : license
        
          
    
    
    Ontology --> "1" Thing : license
    click Thing href "../Thing"

        
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

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [title](title.md) | 1 <br/> [NarrativeText](NarrativeText.md) |  | direct |
| [has_ontology_root_term](has_ontology_root_term.md) | * <br/> [Class](Class.md) |  | direct |
| [license](license.md) | 1 <br/> [Thing](Thing.md) |  | direct |
| [source](source.md) | * <br/> [String](String.md) |  | direct |
| [versionIRI](versionIRI.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [versionInfo](versionInfo.md) | 1 <br/> [String](String.md) |  | direct |
| [comment](comment.md) | * <br/> [String](String.md) |  | direct |
| [creator](creator.md) | * <br/> [Agent](Agent.md) |  | direct |
| [created](created.md) | 0..1 <br/> [String](String.md) | when the term came into being | direct |
| [imports](imports.md) | 0..1 <br/> [String](String.md) |  | direct |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | this maps to the URI in RDF | [NamedObject](NamedObject.md) |
| [type](type.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasProvenance](HasProvenance.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Term](Term.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Class](Class.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Property](Property.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [AnnotationProperty](AnnotationProperty.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [ObjectProperty](ObjectProperty.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [TransitiveProperty](TransitiveProperty.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [NamedIndividual](NamedIndividual.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [HomoSapiens](HomoSapiens.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Agent](Agent.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Image](Image.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |
| [Subset](Subset.md) | [isDefinedBy](isDefinedBy.md) | range | [Ontology](Ontology.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Ontology |
| native | omoschema:Ontology |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Ontology
description: An OWL ontology
from_schema: https://w3id.org/oak/ontology-metadata
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
description: An OWL ontology
from_schema: https://w3id.org/oak/ontology-metadata
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
  title:
    name: title
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    slot_uri: dcterms:title
    alias: title
    owner: Ontology
    domain_of:
    - Ontology
    range: narrative text
    required: true
  has_ontology_root_term:
    name: has_ontology_root_term
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: IAO:0000700
    alias: has_ontology_root_term
    owner: Ontology
    domain_of:
    - Ontology
    range: Class
    multivalued: true
  license:
    name: license
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:license
    alias: license
    owner: Ontology
    domain_of:
    - Ontology
    range: Thing
    required: true
  source:
    name: source
    from_schema: https://w3id.org/oak/ontology-metadata
    exact_mappings:
    - http://purl.org/dc/terms/source
    - oio:source
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:source
    alias: source
    owner: Ontology
    domain_of:
    - Ontology
    - Axiom
    range: string
    multivalued: true
  versionIRI:
    name: versionIRI
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: version_property
    slot_uri: owl:versionIRI
    alias: versionIRI
    owner: Ontology
    domain_of:
    - Ontology
    range: uriorcurie
    required: true
  versionInfo:
    name: versionInfo
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:version
    rank: 1000
    is_a: version_property
    slot_uri: owl:versionInfo
    alias: versionInfo
    owner: Ontology
    domain_of:
    - Ontology
    range: string
    required: true
  comment:
    name: comment
    comments:
    - in obo format, a term cannot have more than one comment
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: informative_property
    slot_uri: rdfs:comment
    alias: comment
    owner: Ontology
    domain_of:
    - HasUserInformation
    - Ontology
    - Axiom
    range: string
    multivalued: true
  creator:
    name: creator
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:creator
    alias: creator
    owner: Ontology
    domain_of:
    - HasProvenance
    - Ontology
    range: Agent
    multivalued: true
    structured_pattern:
      syntax: '{orcid_regex}'
      interpolated: true
      partial_match: false
  created:
    name: created
    description: when the term came into being
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:createdOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:created
    alias: created
    owner: Ontology
    domain_of:
    - HasProvenance
    - Ontology
    range: string
    multivalued: false
  imports:
    name: imports
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdf:type
    designates_type: true
    alias: type
    owner: Ontology
    domain_of:
    - Thing
    range: uriorcurie
    multivalued: true
class_uri: owl:Ontology

```
</details>