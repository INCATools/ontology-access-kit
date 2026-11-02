# Value Set Configuration

A datamodel for configuring value sets and value set expansions

URI: https://w3id.org/linkml/value-set-configuration

Name: value-set-configuration



## Classes

| Class | Description |
| --- | --- |
| [Resolver](Resolver.md) | A mechanism for resolving using an ontology |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[NamedResolver](NamedResolver.md) | A resolver that is associated with a named resource or prefix |
| [ValueSetConfiguration](ValueSetConfiguration.md) | configuration for value set expansion |



## Slots

| Slot | Description |
| --- | --- |
| [default_resolver](default_resolver.md) | The default resolver to use for value set expansion |
| [method](method.md) | The method used to resolve the value set |
| [name](name.md) | The name of the resource or prefix |
| [prefix_resolvers](prefix_resolvers.md) | Mapping of prefixes to resolvers |
| [resource_resolvers](resource_resolvers.md) |  |
| [shorthand](shorthand.md) | A shorthand for the resolver, using the OAK shorthand syntax, for example, 'o... |
| [shorthand_prefix](shorthand_prefix.md) |  |
| [url](url.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ResolverMethod](ResolverMethod.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
