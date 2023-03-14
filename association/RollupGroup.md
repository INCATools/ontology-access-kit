# Class: RollupGroup



URI: [ontoassoc:RollupGroup](https://w3id.org/oak/association/RollupGroup)



```{mermaid}
 classDiagram
    class RollupGroup
      RollupGroup : associations
        
          RollupGroup ..> Association : associations
        
      RollupGroup : group_object
        
      RollupGroup : sub_groups
        
          RollupGroup ..> RollupGroup : sub_groups
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [group_object](group_object.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | An ontology entity that is the ancestor of the objects in the group's  | direct |
| [sub_groups](sub_groups.md) | 0..* <br/> [RollupGroup](RollupGroup.md) | Container for groups within a rollup group | direct |
| [associations](associations.md) | 0..* <br/> [Association](Association.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RollupGroup](RollupGroup.md) | [sub_groups](sub_groups.md) | range | [RollupGroup](RollupGroup.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:RollupGroup |
| native | ontoassoc:RollupGroup |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RollupGroup
from_schema: https://w3id.org/oak/association
rank: 1000
slots:
- group_object
- sub_groups
- associations

```
</details>

### Induced

<details>
```yaml
name: RollupGroup
from_schema: https://w3id.org/oak/association
rank: 1000
attributes:
  group_object:
    name: group_object
    description: "An ontology entity that is the ancestor of the objects in the group's\
      \ \nassociations and sub-group associations."
    from_schema: https://w3id.org/oak/association
    rank: 1000
    slot_uri: rdf:object
    alias: group_object
    owner: RollupGroup
    domain_of:
    - RollupGroup
    range: uriorcurie
  sub_groups:
    name: sub_groups
    description: Container for groups within a rollup group.
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: sub_groups
    owner: RollupGroup
    domain_of:
    - RollupGroup
    range: RollupGroup
    inlined: true
    inlined_as_list: true
  associations:
    name: associations
    from_schema: https://w3id.org/oak/association
    rank: 1000
    multivalued: true
    alias: associations
    owner: RollupGroup
    domain_of:
    - RollupGroup
    range: Association
    inlined: true
    inlined_as_list: true

```
</details>