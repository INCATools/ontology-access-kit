# Enum: ValidationResultType



URI: [ValidationResultType](ValidationResultType.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| DatatypeConstraintComponent | sh:DatatypeConstraintComponent | constraint in which the range is a type, and the slot value must conform to t... |
| MinCountConstraintComponent | sh:MinCountConstraintComponent | cardinality constraint where the slot value must be greater or equal to a spe... |
| MaxCountConstraintComponent | sh:MaxCountConstraintComponent | cardinality constraint where the slot value must be less than or equal to a s... |
| DeprecatedPropertyComponent | vm:DeprecatedPropertyComponent | constraint where the instance slot should not be deprecated |
| MaxLengthConstraintComponent | sh:MaxLengthConstraintComponent | constraint where the slot value must have a length equal to or less than a sp... |
| MinLengthConstraintComponent | sh:MinLengthConstraintComponent | constraint where the slot value must have a length equal to or less than a sp... |
| PatternConstraintComponent | sh:PatternConstraintComponent | constraint where the slot value must match a given regular expression pattern |
| ClosedConstraintComponent | sh:ClosedConstraintComponent | constraint where the slot value must be allowable for the type of an instance |
| RuleConstraintComponent | None | constraint where the structure of an object must conform to a specified rule |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results






## LinkML Source

<details>
```yaml
name: ValidationResultType
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
permissible_values:
  DatatypeConstraintComponent:
    text: DatatypeConstraintComponent
    description: constraint in which the range is a type, and the slot value must
      conform to the type
    meaning: sh:DatatypeConstraintComponent
    annotations:
      element:
        tag: element
        value: linkml:range
  MinCountConstraintComponent:
    text: MinCountConstraintComponent
    description: cardinality constraint where the slot value must be greater or equal
      to a specified minimum
    meaning: sh:MinCountConstraintComponent
    annotations:
      element:
        tag: element
        value: linkml:minimum_value
  MaxCountConstraintComponent:
    text: MaxCountConstraintComponent
    description: cardinality constraint where the slot value must be less than or
      equal to a specified maximum
    meaning: sh:MaxCountConstraintComponent
    annotations:
      element:
        tag: element
        value: linkml:maximum_value
  DeprecatedPropertyComponent:
    text: DeprecatedPropertyComponent
    description: constraint where the instance slot should not be deprecated
    meaning: vm:DeprecatedPropertyComponent
    annotations:
      element:
        tag: element
        value: linkml:deprecated
  MaxLengthConstraintComponent:
    text: MaxLengthConstraintComponent
    description: constraint where the slot value must have a length equal to or less
      than a specified maximum
    meaning: sh:MaxLengthConstraintComponent
  MinLengthConstraintComponent:
    text: MinLengthConstraintComponent
    description: constraint where the slot value must have a length equal to or less
      than a specified maximum
    meaning: sh:MinLengthConstraintComponent
  PatternConstraintComponent:
    text: PatternConstraintComponent
    description: constraint where the slot value must match a given regular expression
      pattern
    meaning: sh:PatternConstraintComponent
    annotations:
      element:
        tag: element
        value: linkml:pattern
  ClosedConstraintComponent:
    text: ClosedConstraintComponent
    description: constraint where the slot value must be allowable for the type of
      an instance
    meaning: sh:ClosedConstraintComponent
    annotations:
      element:
        tag: element
        value: linkml:attributes
  RuleConstraintComponent:
    text: RuleConstraintComponent
    description: constraint where the structure of an object must conform to a specified
      rule

```
</details>
