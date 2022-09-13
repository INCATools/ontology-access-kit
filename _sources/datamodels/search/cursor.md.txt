# Slot: cursor
_when the number of search results exceed the limit this can be used to iterate through results_


URI: [https://w3id.org/linkml/search_datamodel/cursor](https://w3id.org/linkml/search_datamodel/cursor)



<!-- no inheritance hierarchy -->




## Properties

* Range: [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel




## LinkML Specification

<details>
```yaml
name: cursor
description: when the number of search results exceed the limit this can be used to
  iterate through results
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
alias: cursor
domain_of:
- SearchBaseConfiguration
- SearchResultSet
range: integer

```
</details>