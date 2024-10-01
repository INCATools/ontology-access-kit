

# Slot: weight


_Weighting of the rule. A weight of zero corresponds to 0.5 confidence in the mapping. Setting to +1 or -1 indicates moderate confidence or lack of confidence. A logit scale is used. All weights are summed together to determine the final confidence._





URI: [mappingrules:weight](https://w3id.org/oak/mapping-rules-datamodel/weight)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Postcondition](Postcondition.md) |  |  no  |







## Properties

* Range: [Float](Float.md)





## See Also

* [https://en.wikipedia.org/wiki/Logit](https://en.wikipedia.org/wiki/Logit)
* [https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png](https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png)

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:weight |
| native | mappingrules:weight |




## LinkML Source

<details>
```yaml
name: weight
description: Weighting of the rule. A weight of zero corresponds to 0.5 confidence
  in the mapping. Setting to +1 or -1 indicates moderate confidence or lack of confidence.
  A logit scale is used. All weights are summed together to determine the final confidence.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
see_also:
- https://en.wikipedia.org/wiki/Logit
- https://upload.wikimedia.org/wikipedia/commons/5/57/Logit.png
rank: 1000
alias: weight
owner: Postcondition
domain_of:
- Postcondition
range: float

```
</details>