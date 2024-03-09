# Class: Synonymizer



URI: [mappingrules:Synonymizer](https://w3id.org/oak/mapping-rules-datamodel/Synonymizer)




```{mermaid}
 classDiagram
    class Synonymizer
      Synonymizer : match
        
      Synonymizer : match_scope
        
      Synonymizer : prefix
        
      Synonymizer : qualifier
        
      Synonymizer : replacement
        
      Synonymizer : tests
        
          Synonymizer --> Test : tests
        
      Synonymizer : the_rule
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [the_rule](the_rule.md) | 0..1 <br/> [String](String.md) | Description of the rule | direct |
| [match](match.md) | 0..1 <br/> [String](String.md) | Reg-ex rule to match substrings in labels | direct |
| [match_scope](match_scope.md) | 0..1 <br/> [String](String.md) | Scope of the reg-ex rule | direct |
| [replacement](replacement.md) | 0..1 <br/> [String](String.md) | Reg-ex rule to replace substrings in labels | direct |
| [qualifier](qualifier.md) | 0..1 <br/> [String](String.md) | Type of match for the new synonym generated | direct |
| [prefix](prefix.md) | 0..1 <br/> [String](String.md) | The rule applies to nodes of a specific prefix | direct |
| [tests](tests.md) | 0..1 <br/> [Test](Test.md) | Unit tests for each rules | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [synonymizer](synonymizer.md) | range | [Synonymizer](Synonymizer.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:Synonymizer |
| native | mappingrules:Synonymizer |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Synonymizer
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  the_rule:
    name: the_rule
    description: Description of the rule.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  match_scope:
    name: match_scope
    description: Scope of the reg-ex rule
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  prefix:
    name: prefix
    description: The rule applies to nodes of a specific prefix.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    - Test
    range: string
  tests:
    name: tests
    description: Unit tests for each rules.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: Test

```
</details>

### Induced

<details>
```yaml
name: Synonymizer
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  the_rule:
    name: the_rule
    description: Description of the rule.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: the_rule
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: match
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  match_scope:
    name: match_scope
    description: Scope of the reg-ex rule
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: match_scope
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: replacement
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: qualifier
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  prefix:
    name: prefix
    description: The rule applies to nodes of a specific prefix.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: prefix
    owner: Synonymizer
    domain_of:
    - Synonymizer
    - Test
    range: string
  tests:
    name: tests
    description: Unit tests for each rules.
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    alias: tests
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: Test

```
</details>