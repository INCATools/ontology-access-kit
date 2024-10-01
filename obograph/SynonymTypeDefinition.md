

# Class: SynonymTypeDefinition



URI: [oio:SynonymType](http://www.geneontology.org/formats/oboInOwl#SynonymType)






```{mermaid}
 classDiagram
    class SynonymTypeDefinition
    click SynonymTypeDefinition href "../SynonymTypeDefinition"
      SynonymTypeDefinition : id
        
      SynonymTypeDefinition : lbl
        
      SynonymTypeDefinition : pred
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [OboIdentifierString](OboIdentifierString.md) | The unique identifier of the entity | direct |
| [lbl](lbl.md) | 0..1 <br/> [String](String.md) | the human-readable label of a node | direct |
| [pred](pred.md) | 0..1 <br/> [String](String.md) | the predicate of an edge | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [synonymTypeDefinitions](synonymTypeDefinitions.md) | range | [SynonymTypeDefinition](SynonymTypeDefinition.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:SynonymType |
| native | obographs:SynonymTypeDefinition |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SynonymTypeDefinition
from_schema: https://github.com/geneontology/obographs
slots:
- id
- lbl
- pred
class_uri: oio:SynonymType

```
</details>

### Induced

<details>
```yaml
name: SynonymTypeDefinition
from_schema: https://github.com/geneontology/obographs
attributes:
  id:
    name: id
    description: The unique identifier of the entity
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://owlcollab.github.io/oboformat/doc/obo-syntax.html#2.5
    rank: 1000
    identifier: true
    alias: id
    owner: SynonymTypeDefinition
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: OboIdentifierString
    required: true
  lbl:
    name: lbl
    description: the human-readable label of a node
    comments:
    - the name "lbl" exists for legacy purposes, this should be considered identical
      to label in rdfs
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - label
    - name
    rank: 1000
    slot_uri: rdfs:label
    alias: lbl
    owner: SynonymTypeDefinition
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: string
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: SynonymTypeDefinition
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - SynonymTypeDefinition
    range: string
class_uri: oio:SynonymType

```
</details>