

# Class: Test


_A unit test for a rule, specifies an intended output for an input_





URI: [mappingrules:Test](https://w3id.org/oak/mapping-rules-datamodel/Test)






```{mermaid}
 classDiagram
    class Test
    click Test href "../Test"
      Test : input
        
      Test : output
        
      Test : prefix
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [input](input.md) | 0..1 <br/> [String](String.md) | Input string for the rule | direct |
| [output](output.md) | 0..1 <br/> [String](String.md) | Output based on the rule | direct |
| [prefix](prefix.md) | 0..1 <br/> [String](String.md) | The prefix that qualifies for the rule | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Synonymizer](Synonymizer.md) | [tests](tests.md) | range | [Test](Test.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:Test |
| native | mappingrules:Test |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Test
description: A unit test for a rule, specifies an intended output for an input
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  input:
    name: input
    description: Input string for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Test
  output:
    name: output
    description: Output based on the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    domain_of:
    - Test
  prefix:
    name: prefix
    description: The prefix that qualifies for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    domain_of:
    - RuleSet
    - Synonymizer
    - Test

```
</details>

### Induced

<details>
```yaml
name: Test
description: A unit test for a rule, specifies an intended output for an input
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  input:
    name: input
    description: Input string for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: input
    owner: Test
    domain_of:
    - Test
    range: string
  output:
    name: output
    description: Output based on the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    rank: 1000
    alias: output
    owner: Test
    domain_of:
    - Test
    range: string
  prefix:
    name: prefix
    description: The prefix that qualifies for the rule.
    from_schema: https://w3id.org/oak/synonymizer-datamodel
    alias: prefix
    owner: Test
    domain_of:
    - RuleSet
    - Synonymizer
    - Test
    range: string

```
</details>