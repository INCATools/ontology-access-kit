# Class: Synonymizer



URI: [mrules:Synonymizer](https://w3id.org/linkml/mapping_rules_datamodel/Synonymizer)



```{mermaid}
 classDiagram
    class Synonymizer
      Synonymizer : match
      Synonymizer : match_scope
      Synonymizer : qualifier
      Synonymizer : replacement
      Synonymizer : the_rule
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [the_rule](the_rule.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Description of the rule | direct |
| [match](match.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Reg-ex rule to match substrings in labels | direct |
| [match_scope](match_scope.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Scope of the reg-ex rule | direct |
| [replacement](replacement.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Reg-ex rule to replace substrings in labels | direct |
| [qualifier](qualifier.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Type of match for the new synonym generated | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [synonymizer](synonymizer.md) | range | [Synonymizer](Synonymizer.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mrules:Synonymizer |
| native | mrules:Synonymizer |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Synonymizer
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
rank: 1000
attributes:
  the_rule:
    name: the_rule
    description: Description of the rule.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: string
  match_scope:
    name: match_scope
    description: Scope of the reg-ex rule
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: string
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    range: string

```
</details>

### Induced

<details>
```yaml
name: Synonymizer
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
rank: 1000
attributes:
  the_rule:
    name: the_rule
    description: Description of the rule.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: the_rule
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: match
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  match_scope:
    name: match_scope
    description: Scope of the reg-ex rule
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: match_scope
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: replacement
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    rank: 1000
    alias: qualifier
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string

```
</details>