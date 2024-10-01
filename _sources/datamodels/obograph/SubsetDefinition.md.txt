

# Class: SubsetDefinition



URI: [oio:SubsetProperty](http://www.geneontology.org/formats/oboInOwl#SubsetProperty)






```{mermaid}
 classDiagram
    class SubsetDefinition
    click SubsetDefinition href "../SubsetDefinition"
      SubsetDefinition : id
        
      SubsetDefinition : lbl
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [OboIdentifierString](OboIdentifierString.md) | The unique identifier of the entity | direct |
| [lbl](lbl.md) | 0..1 <br/> [String](String.md) | the human-readable label of a node | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [subsetDefinitions](subsetDefinitions.md) | range | [SubsetDefinition](SubsetDefinition.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:SubsetProperty |
| native | obographs:SubsetDefinition |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SubsetDefinition
from_schema: https://github.com/geneontology/obographs
slots:
- id
- lbl
class_uri: oio:SubsetProperty

```
</details>

### Induced

<details>
```yaml
name: SubsetDefinition
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
    owner: SubsetDefinition
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
    owner: SubsetDefinition
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: string
class_uri: oio:SubsetProperty

```
</details>