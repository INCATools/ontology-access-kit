

# Class: HasProvenance



URI: [omoschema:HasProvenance](https://w3id.org/oak/ontology-metadata/HasProvenance)






```{mermaid}
 classDiagram
    class HasProvenance
    click HasProvenance href "../HasProvenance"
      AnnotationPropertyMixin <|-- HasProvenance
        click AnnotationPropertyMixin href "../AnnotationPropertyMixin"
      

      HasProvenance <|-- Term
        click Term href "../Term"
      
      
      HasProvenance : contributor
        
          
    
    
    HasProvenance --> "*" Agent : contributor
    click Agent href "../Agent"

        
      HasProvenance : created
        
      HasProvenance : created_by
        
      HasProvenance : creation_date
        
      HasProvenance : creator
        
          
    
    
    HasProvenance --> "*" Agent : creator
    click Agent href "../Agent"

        
      HasProvenance : date
        
      HasProvenance : definition_source
        
      HasProvenance : editor_note
        
      HasProvenance : imported_from
        
          
    
    
    HasProvenance --> "*" NamedIndividual : imported_from
    click NamedIndividual href "../NamedIndividual"

        
      HasProvenance : isDefinedBy
        
          
    
    
    HasProvenance --> "0..1" Ontology : isDefinedBy
    click Ontology href "../Ontology"

        
      HasProvenance : ontology_term_requester
        
      HasProvenance : term_editor
        
      HasProvenance : term_tracker_item
        
      
```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasProvenance**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [created_by](created_by.md) | 0..1 <br/> [String](String.md) |  | direct |
| [creation_date](creation_date.md) | * <br/> [String](String.md) |  | direct |
| [contributor](contributor.md) | * <br/> [Agent](Agent.md) |  | direct |
| [creator](creator.md) | * <br/> [Agent](Agent.md) |  | direct |
| [created](created.md) | 0..1 <br/> [String](String.md) | when the term came into being | direct |
| [date](date.md) | * <br/> [String](String.md) | when the term was updated | direct |
| [isDefinedBy](isDefinedBy.md) | 0..1 <br/> [Ontology](Ontology.md) |  | direct |
| [editor_note](editor_note.md) | * <br/> [NarrativeText](NarrativeText.md) |  | direct |
| [term_editor](term_editor.md) | * <br/> [String](String.md) |  | direct |
| [definition_source](definition_source.md) | * <br/> [String](String.md) |  | direct |
| [ontology_term_requester](ontology_term_requester.md) | 0..1 <br/> [String](String.md) |  | direct |
| [imported_from](imported_from.md) | * <br/> [NamedIndividual](NamedIndividual.md) |  | direct |
| [term_tracker_item](term_tracker_item.md) | * <br/> [String](String.md) |  | direct |



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
| self | omoschema:HasProvenance |
| native | omoschema:HasProvenance |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasProvenance
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
slots:
- created_by
- creation_date
- contributor
- creator
- created
- date
- isDefinedBy
- editor_note
- term_editor
- definition_source
- ontology_term_requester
- imported_from
- term_tracker_item

```
</details>

### Induced

<details>
```yaml
name: HasProvenance
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  created_by:
    name: created_by
    deprecated: proposed obsoleted by OMO group 2022-04-12
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: creator
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:created_by
    alias: created_by
    owner: HasProvenance
    domain_of:
    - HasProvenance
    - Axiom
    range: string
  creation_date:
    name: creation_date
    deprecated: proposed obsoleted by OMO group 2022-04-12
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    deprecated_element_has_exact_replacement: created
    rank: 1000
    is_a: provenance_property
    slot_uri: oio:creation_date
    alias: creation_date
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  contributor:
    name: contributor
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:contributor
    alias: contributor
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: Agent
    multivalued: true
    structured_pattern:
      syntax: '{orcid_regex}'
      interpolated: true
      partial_match: false
  creator:
    name: creator
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - prov:wasAttributedTo
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:creator
    alias: creator
    owner: HasProvenance
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
    owner: HasProvenance
    domain_of:
    - HasProvenance
    - Ontology
    range: string
    multivalued: false
  date:
    name: date
    description: when the term was updated
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:authoredOn
    rank: 1000
    is_a: provenance_property
    slot_uri: dcterms:date
    alias: date
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  isDefinedBy:
    name: isDefinedBy
    from_schema: https://w3id.org/oak/ontology-metadata
    close_mappings:
    - pav:importedFrom
    - dcterms:publisher
    rank: 1000
    slot_uri: rdfs:isDefinedBy
    alias: isDefinedBy
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: Ontology
  editor_note:
    name: editor_note
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000116
    alias: editor_note
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: narrative text
    multivalued: true
  term_editor:
    name: term_editor
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000117
    alias: term_editor
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  definition_source:
    name: definition_source
    todos:
    - restrict range
    in_subset:
    - obi permitted profile
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000119
    alias: definition_source
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
    multivalued: true
  ontology_term_requester:
    name: ontology_term_requester
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000234
    alias: ontology_term_requester
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
  imported_from:
    name: imported_from
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000412
    alias: imported_from
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: NamedIndividual
    multivalued: true
  term_tracker_item:
    name: term_tracker_item
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: provenance_property
    slot_uri: IAO:0000233
    alias: term_tracker_item
    owner: HasProvenance
    domain_of:
    - HasProvenance
    range: string
    multivalued: true

```
</details>