# Obographs Datamodel

Schema for benchmarking based on obographs

URI: https://github.com/geneontology/obographs
Name: obographs_datamodel



## Classes

| Class | Description |
| --- | --- |
| [Axiom](Axiom.md) | A generic grouping for any OWL axiom that is not captured by existing constru... |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |
| [DomainRangeAxiom](DomainRangeAxiom.md) | An axiom that represents some combination of domain and range assertions |
| [Edge](Edge.md) | An edge is a typed relationship between two nodes |
| [EquivalentNodesSet](EquivalentNodesSet.md) | A clique of nodes that are all mutually equivalent |
| [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | An existential restriction (OWL some values from) expression |
| [Graph](Graph.md) | A graph is a collection of nodes and edges that represents a single ontology |
| [GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes th... |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and... |
| [Meta](Meta.md) | A collection of annotations on an entity or ontology or axiom |
| [Node](Node.md) | A node is a class, property, or other entity in an ontology |
| [PrefixDeclaration](PrefixDeclaration.md) | maps individual prefix to namespace |
| [PropertyChainAxiom](PropertyChainAxiom.md) | An axiom that represents an OWL property chain, e |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |
| [XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |


## Slots

| Slot | Description |
| --- | --- |
| [allValuesFromEdges](allValuesFromEdges.md) | A list of edges that represent subclasses of universal restrictions |
| [basicPropertyValues](basicPropertyValues.md) | A list of open-ended property values that does not correspond to those predef... |
| [chainPredicateIds](chainPredicateIds.md) | A list of identifiers of predicates that form the precedent clause of a prope... |
| [comments](comments.md) | A list of comments about the entity |
| [definedClassId](definedClassId.md) | The class that is defined by this axiom |
| [definition](definition.md) | A definition of an entity |
| [deprecated](deprecated.md) |  |
| [domainClassIds](domainClassIds.md) |  |
| [domainRangeAxioms](domainRangeAxioms.md) | A list of axioms that define the domain and range of a property |
| [edges](edges.md) | All edges present in a graph |
| [equivalentNodesSets](equivalentNodesSets.md) | A list of sets of nodes that form equivalence cliques |
| [fillerId](fillerId.md) | in an OWL restriction expression, the filler is the object of the restriction |
| [genusIds](genusIds.md) | The set of classes that are the genus of the defined class |
| [graphs](graphs.md) | A list of all graphs (ontologies) in an ontology document |
| [id](id.md) | The identifier of the entity |
| [isExact](isExact.md) |  |
| [lbl](lbl.md) | the human-readable label of a node |
| [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | A list of logical definition axioms that define the meaning of a class in ter... |
| [meta](meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... |
| [namespace](namespace.md) | The namespace associated with a prefix in a prefix declaration |
| [nodeIds](nodeIds.md) |  |
| [nodes](nodes.md) | All nodes present in a graph |
| [obj](obj.md) | the object of an edge |
| [pred](pred.md) | the predicate of an edge |
| [predicateId](predicateId.md) |  |
| [prefix](prefix.md) | The prefix of a prefix declaration |
| [prefixes](prefixes.md) | maps prefixes to namespaces |
| [propertyChainAxioms](propertyChainAxioms.md) | A list of axioms that define an OWL property chain |
| [propertyId](propertyId.md) | in an OWL restriction expression, this is the predicate |
| [rangeClassIds](rangeClassIds.md) |  |
| [representativeNodeId](representativeNodeId.md) | The identifier of a node that represents the class in an OWL equivalence cliq... |
| [restrictions](restrictions.md) | The set of restrictions that are the differentia of the defined class |
| [sub](sub.md) | the subject of an edge |
| [subsets](subsets.md) | A list of subsets to which this entity belongs |
| [synonyms](synonyms.md) | A list of synonym property value assertions for an entity |
| [synonymType](synonymType.md) | This standard follows oboInOwl in allowing an open ended list of synonym type... |
| [type](type.md) |  |
| [val](val.md) | the value of a property |
| [version](version.md) |  |
| [xrefs](xrefs.md) | A list of cross references to other entities represented in other ontologies,... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ScopeEnum](ScopeEnum.md) | A vocabulary of terms that can be used to "scope" a synonym |


## Types

| Type | Description |
| --- | --- |
| [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | A binary (true or false) value |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | a compact URI |
| [xsd:date](http://www.w3.org/2001/XMLSchema#date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | The combination of a date and time |
| [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](http://www.w3.org/2001/XMLSchema#double) | A real number that conforms to the xsd:double specification |
| [xsd:float](http://www.w3.org/2001/XMLSchema#float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | An integer |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [OboIdentifierString](OboIdentifierString.md) | A string that represents an OBO identifier |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [SynonymTypeIdentifierString](SynonymTypeIdentifierString.md) | A string that represents a synonym type |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |
| [XrefString](XrefString.md) | A string that is a cross reference to another entity represented in another o... |


## Subsets

| Subset | Description |
| --- | --- |
