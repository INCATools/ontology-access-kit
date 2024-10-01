

# Class: TermInfo



URI: [sim:TermInfo](https://w3id.org/linkml/similarity/TermInfo)






```{mermaid}
 classDiagram
    class TermInfo
    click TermInfo href "../TermInfo"
      TermInfo : id
        
      TermInfo : label
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [String](String.md) |  | direct |
| [label](label.md) | 0..1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | [subject_termset](subject_termset.md) | range | [TermInfo](TermInfo.md) |
| [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | [object_termset](object_termset.md) | range | [TermInfo](TermInfo.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:TermInfo |
| native | sim:TermInfo |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TermInfo
from_schema: https://w3id.org/oak/similarity
attributes:
  id:
    name: id
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    identifier: true
    domain_of:
    - TermInfo
    required: true
  label:
    name: label
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: rdfs:label
    domain_of:
    - TermInfo

```
</details>

### Induced

<details>
```yaml
name: TermInfo
from_schema: https://w3id.org/oak/similarity
attributes:
  id:
    name: id
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    identifier: true
    alias: id
    owner: TermInfo
    domain_of:
    - TermInfo
    range: string
    required: true
  label:
    name: label
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: rdfs:label
    alias: label
    owner: TermInfo
    domain_of:
    - TermInfo
    range: string

```
</details>