# Enum: InformationContentScaleEnum



URI: [InformationContentScaleEnum](InformationContentScaleEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| log2_bits | None | IC(t) = -log2(Pr(t)), i |
| normalized | None | IC(t) = -log(Pr(t)) / log(N) * 100, i |




## Slots

| Name | Description |
| ---  | --- |
| [scale](scale.md) | The scale or units of the IC scores |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity






## LinkML Source

<details>
```yaml
name: InformationContentScaleEnum
from_schema: https://w3id.org/oak/similarity
rank: 1000
permissible_values:
  log2_bits:
    text: log2_bits
    description: IC(t) = -log2(Pr(t)), i.e. information measured in bits. This is
      the default.
  normalized:
    text: normalized
    description: IC(t) = -log(Pr(t)) / log(N) * 100, i.e. IC scaled to 0-100 relative
      to the maximum possible IC for a background set of size N. Used by Ubergraph.

```
</details>
