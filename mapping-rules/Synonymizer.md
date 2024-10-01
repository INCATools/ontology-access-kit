

# Class: Synonymizer


_Specification of a rule for generating a synonym or alternate lexical element._





URI: [mappingrules:Synonymizer](https://w3id.org/oak/mapping-rules-datamodel/Synonymizer)






```{mermaid}
 classDiagram
    class Synonymizer
    click Synonymizer href "../Synonymizer"
      Synonymizer : description
        
      Synonymizer : in_place
        
      Synonymizer : match
        
      Synonymizer : match_scope
        
      Synonymizer : prefix
        
      Synonymizer : qualifier
        
      Synonymizer : replacement
        
      Synonymizer : tests
        
          
    
    
    Synonymizer --> "*" Test : tests
    click Test href "../Test"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [description](description.md) | 0..1 <br/> [String](String.md) | Description of the rule | direct |
| [match](match.md) | 0..1 <br/> [RegularExpressionString](RegularExpressionString.md) | Reg-ex rule to match substrings in labels | direct |
| [match_scope](match_scope.md) | 0..1 <br/> [String](String.md) | Synonym scope of the reg-ex rule, e | direct |
| [replacement](replacement.md) | 0..1 <br/> [RegularExpressionString](RegularExpressionString.md) | Reg-ex rule to replace substrings in labels | direct |
| [qualifier](qualifier.md) | 0..1 <br/> [String](String.md) | Type of match for the new synonym generated | direct |
| [prefix](prefix.md) | 0..1 <br/> [String](String.md) | The rule applies to nodes of a specific prefix | direct |
| [in_place](in_place.md) | 0..1 <br/> [Boolean](Boolean.md) | Whether the rule is applied in place or not | direct |
| [tests](tests.md) | * <br/> [Test](Test.md) | Unit tests for each rules | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [synonymizer](synonymizer.md) | range | [Synonymizer](Synonymizer.md) |
| [RuleSet](RuleSet.md) | [rules](rules.md) | range | [Synonymizer](Synonymizer.md) |






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
description: Specification of a rule for generating a synonym or alternate lexical
  element.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  description:
    name: description
    description: Description of the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    domain_of:
    - MappingRule
    - Synonymizer
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: RegularExpressionString
  match_scope:
    name: match_scope
    description: Synonym scope of the reg-ex rule, e.g. exact, narrow
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: RegularExpressionString
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: string
  prefix:
    name: prefix
    description: The rule applies to nodes of a specific prefix.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    domain_of:
    - RuleSet
    - Synonymizer
    - Test
    range: string
  in_place:
    name: in_place
    description: Whether the rule is applied in place or not.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: boolean
  tests:
    name: tests
    description: Unit tests for each rules.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Synonymizer
    range: Test
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: Synonymizer
description: Specification of a rule for generating a synonym or alternate lexical
  element.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  description:
    name: description
    description: Description of the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    alias: description
    owner: Synonymizer
    domain_of:
    - MappingRule
    - Synonymizer
    range: string
  match:
    name: match
    description: Reg-ex rule to match substrings in labels.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: match
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: RegularExpressionString
  match_scope:
    name: match_scope
    description: Synonym scope of the reg-ex rule, e.g. exact, narrow
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: match_scope
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  replacement:
    name: replacement
    description: Reg-ex rule to replace substrings in labels
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: replacement
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: RegularExpressionString
  qualifier:
    name: qualifier
    description: Type of match for the new synonym generated.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: qualifier
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: string
  prefix:
    name: prefix
    description: The rule applies to nodes of a specific prefix.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    alias: prefix
    owner: Synonymizer
    domain_of:
    - RuleSet
    - Synonymizer
    - Test
    range: string
  in_place:
    name: in_place
    description: Whether the rule is applied in place or not.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: in_place
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: boolean
  tests:
    name: tests
    description: Unit tests for each rules.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: tests
    owner: Synonymizer
    domain_of:
    - Synonymizer
    range: Test
    multivalued: true

```
</details>