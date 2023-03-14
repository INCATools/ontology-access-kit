# Obographs Datamodel

A data model for graph-oriented representations of ontologies. Each ontology is represented as a Graph, and multiple ontologies can be connected together in a GraphDocument.
The principle elements of a Graph are Node objects and Edge objects. A Node represents an arbitrary ontology element, including but not limited to the core terms in the ontology. Edges represent simple relationships between Nodes. Nodes and Edges can both have Meta objects attached, providing additional metedata.
Not everything in an ontology can be represented as nodes and edges. More complex axioms have specialized structures such as DomainRangeAxiom objects and LogicalDefinitionAxiom.

URI: https://github.com/geneontology/obographs
Name: obographs_datamodel



## Classes

| Class | Description |
| --- | --- |
| [Axiom](Axiom.md) | A generic grouping for any OWL axiom or group of axioms that is not captured ... |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |
| [DomainRangeAxiom](DomainRangeAxiom.md) | This groups potentially multiple axioms that constrain the usage of a propert... |
| [Edge](Edge.md) | An edge is a simple typed relationship between two nodes |
| [EquivalentNodesSet](EquivalentNodesSet.md) | A clique of nodes that are all mutually equivalent |
| [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | An existential restriction (OWL some values from) expression |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |
| [GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes th... |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and... |
| [Meta](Meta.md) | A collection of annotations on an entity or ontology or edge or axiom |
| [Node](Node.md) | A node is a class, property, or other entity in an ontology |
| [PrefixDeclaration](PrefixDeclaration.md) | A mapping between an individual prefix (e |
| [PropertyChainAxiom](PropertyChainAxiom.md) | An axiom that represents an OWL property chain, e |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |
| [SubsetDefinition](SubsetDefinition.md) |  |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |
| [SynonymTypeDefinition](SynonymTypeDefinition.md) |  |
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
| [id](id.md) | The unique identifier of the entity |
| [isExact](isExact.md) |  |
| [lang](lang.md) | the language of a property value |
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
| [prefixes](prefixes.md) | A collection of mappings between prefixes and namespaces, used to map CURIEs ... |
| [propertyChainAxioms](propertyChainAxioms.md) | A list of axioms that define an OWL property chain |
| [propertyId](propertyId.md) | in an OWL restriction expression, this is the predicate |
| [rangeClassIds](rangeClassIds.md) |  |
| [representativeNodeId](representativeNodeId.md) | The identifier of a node that represents the class in an OWL equivalence cliq... |
| [restrictions](restrictions.md) | The set of restrictions that are the differentiating features of the defined ... |
| [sub](sub.md) | the subject of an edge |
| [subsetDefinitions](subsetDefinitions.md) |  |
| [subsets](subsets.md) | A list of subsets to which this entity belongs |
| [synonyms](synonyms.md) | A list of synonym property value assertions for an entity |
| [synonymType](synonymType.md) | This standard follows oboInOwl in allowing an open ended list of synonym type... |
| [synonymTypeDefinitions](synonymTypeDefinitions.md) |  |
| [type](type.md) |  |
| [val](val.md) | the value of a property |
| [valType](valType.md) | the datatype of a property value |
| [version](version.md) |  |
| [xrefs](xrefs.md) | A list of cross references to other entities represented in other ontologies,... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ScopeEnum](ScopeEnum.md) | A vocabulary of terms that can be used to "scope" a synonym |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [OboIdentifierString](OboIdentifierString.md) | A string that represents an OBO identifier |
| [String](String.md) | A character string |
| [SynonymTypeIdentifierString](SynonymTypeIdentifierString.md) | A string that represents a synonym type |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |
| [XrefString](XrefString.md) | A string that is a cross reference to another entity represented in another o... |


## Subsets

| Subset | Description |
| --- | --- |
