# Enum: DefinitionConstraintComponent




_An extension of SHACL constraint component for constraining definitions_



URI: [DefinitionConstraintComponent](DefinitionConstraintComponent.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| DefinitionConstraint | omoschema:DCC.Any | A general problem with a definition |
| DefinitionPresence | omoschema:DCC.S0 | An entity must have a definition |
| Conventions | omoschema:DCC.S1 | Definitions should conform to conventions |
| Harmonized | omoschema:DCC.S1.1 | Definitions should be harmonized |
| GenusDifferentiaForm | omoschema:DCC.S3 | A definition should follow the genus-differentia form |
| SingleGenus | omoschema:DCC.S3.1 | An entity must have a single genus |
| Circularity | omoschema:DCC.S7 | A definition must not be circular |
| MatchTextAndLogical | omoschema:DCC.S11 | Text definitions and logical forms should match |









## See Also

* [https://github.com/INCATools/ontology-access-kit/issues/305](https://github.com/INCATools/ontology-access-kit/issues/305)

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: DefinitionConstraintComponent
description: An extension of SHACL constraint component for constraining definitions
from_schema: http://purl.obolibrary.org/obo/omo/schema
source: https://philpapers.org/archive/SEPGFW.pdf
see_also:
- https://github.com/INCATools/ontology-access-kit/issues/305
rank: 1000
permissible_values:
  DefinitionConstraint:
    text: DefinitionConstraint
    description: A general problem with a definition
    meaning: omoschema:DCC.Any
  DefinitionPresence:
    text: DefinitionPresence
    description: An entity must have a definition
    meaning: omoschema:DCC.S0
    is_a: DefinitionConstraint
  Conventions:
    text: Conventions
    description: Definitions should conform to conventions
    meaning: omoschema:DCC.S1
    is_a: DefinitionConstraint
  Harmonized:
    text: Harmonized
    description: Definitions should be harmonized
    meaning: omoschema:DCC.S1.1
    is_a: DefinitionConstraint
  GenusDifferentiaForm:
    text: GenusDifferentiaForm
    description: A definition should follow the genus-differentia form
    meaning: omoschema:DCC.S3
    is_a: DefinitionConstraint
  SingleGenus:
    text: SingleGenus
    description: An entity must have a single genus
    meaning: omoschema:DCC.S3.1
    is_a: GenusDifferentiaForm
  Circularity:
    text: Circularity
    description: A definition must not be circular
    meaning: omoschema:DCC.S7
    is_a: DefinitionConstraint
  MatchTextAndLogical:
    text: MatchTextAndLogical
    description: Text definitions and logical forms should match
    meaning: omoschema:DCC.S11
    is_a: DefinitionConstraint

```
</details>
