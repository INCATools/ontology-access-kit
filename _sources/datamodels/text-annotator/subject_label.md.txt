# Slot: subject_label
_The portion of the subject text that is matched, ranging from subject_start to subject_end_


URI: [https://w3id.org/linkml/text_annotator/subject_label](https://w3id.org/linkml/text_annotator/subject_label)



<!-- no inheritance hierarchy -->




## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/text_annotator




## LinkML Specification

<details>
```yaml
name: subject_label
description: The portion of the subject text that is matched, ranging from subject_start
  to subject_end
from_schema: https://w3id.org/linkml/text_annotator
exact_mappings:
- bpa:text
rank: 1000
alias: subject_label
domain_of:
- HasSpan
range: string

```
</details>