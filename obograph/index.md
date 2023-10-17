# Obographs Datamodel

A data model for graph-oriented representations of ontologies. Each ontology is represented as a Graph, and multiple ontologies can be connected together in a GraphDocument.
The principle elements of a Graph are Node objects and Edge objects. A Node represents an arbitrary ontology element, including but not limited to the core terms in the ontology. Edges represent simple relationships between Nodes. Nodes and Edges can both have Meta objects attached, providing additional metedata.
Not everything in an ontology can be represented as nodes and edges. More complex axioms have specialized structures such as DomainRangeAxiom objects and LogicalDefinitionAxiom.

URI: https://github.com/geneontology/obographs

Name: obographs_datamodel



## Classes

| Class | Description |
| --- | --- |
| [Axiom](Axiom.md) | A generic grouping for any OWL axiom or group of axioms that is not captured by existing constructs in this standard.
 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | An axiom that defines a set of classes or class expressions as being mutually disjoint. Formally, there exists no instance that instantiates more that one of the union of classIds and classExpressions. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DomainRangeAxiom](DomainRangeAxiom.md) | This groups potentially multiple axioms that constrain the usage of a property depending on some combination of domain and range. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[EquivalentNodesSet](EquivalentNodesSet.md) | A clique of nodes that are all mutually equivalent |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and a set of differentia |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PropertyChainAxiom](PropertyChainAxiom.md) | An axiom that represents an OWL property chain, e.g. R <- R1 o ... o Rn |
| [Edge](Edge.md) | An edge is a simple typed relationship between two nodes. When mapping to OWL, an edge represents either (a) s SubClassOf o (b) s SubClassOf p some o (c) s p o (where s and o are individuals) (d) s SubPropertyOf o (e) s EquivalentTo o (f) s type o |
| [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) | An existential restriction (OWL some values from) expression |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a single ontology. |
| [GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes that apply across all of them |
| [Meta](Meta.md) | A collection of annotations on an entity or ontology or edge or axiom. Metadata typically does not affect the logical interpretation of the container but provides useful information to humans or machines. |
| [Node](Node.md) | A node is a class, property, or other entity in an ontology |
| [PrefixDeclaration](PrefixDeclaration.md) | A mapping between an individual prefix (e.g. GO) and a namespace (e.g. http://purl.obolibrary.org/obo/GO_) |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on object. Minimally, a property value has a predicate and a value. It can also have a list of xrefs indicating provenance, as well as a metadata object. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a definition, synonym, or xref |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of an entity |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to an entity |
| [SubsetDefinition](SubsetDefinition.md) | None |
| [SynonymTypeDefinition](SynonymTypeDefinition.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [allValuesFromEdges](allValuesFromEdges.md) | A list of edges that represent subclasses of universal restrictions |
| [basicPropertyValues](basicPropertyValues.md) | A list of open-ended property values that does not correspond to those predef... |
| [chainPredicateIds](chainPredicateIds.md) | A list of identifiers of predicates that form the precedent clause of a prope... |
| [classExpressions](classExpressions.md) | The set of class expressions that are mutually disjoint |
| [classIds](classIds.md) | The set of named classes that are mutually disjoint |
| [comments](comments.md) | A list of comments about the entity |
| [definedClassId](definedClassId.md) | The class that is defined by this axiom |
| [definition](definition.md) | A definition of an entity |
| [deprecated](deprecated.md) |  |
| [disjointClassExpressionsAxioms](disjointClassExpressionsAxioms.md) | A list of logical disjointness axioms that specify that a class or class expr... |
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
| [propertyType](propertyType.md) |  |
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
| [unionEquivalentTo](unionEquivalentTo.md) | If present, this equates to an OWL DisjointUnion expression |
| [unionEquivalentToExpression](unionEquivalentToExpression.md) | if present, this class expression is equivalent ot the (disjoint) union of th... |
| [val](val.md) | the value of a property |
| [valType](valType.md) | the datatype of a property value |
| [version](version.md) |  |
| [xrefs](xrefs.md) | A list of cross references to other entities represented in other ontologies,... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [NodeTypeEnum](NodeTypeEnum.md) | The main type of a node |
| [PropertyTypeEnum](PropertyTypeEnum.md) | The node subtype for property nodes |
| [ScopeEnum](ScopeEnum.md) | A vocabulary of terms that can be used to "scope" a synonym |


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
| [OboIdentifierString](OboIdentifierString.md) | A string that represents an OBO identifier |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [SynonymTypeIdentifierString](SynonymTypeIdentifierString.md) | A string that represents a synonym type |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |
| [XrefString](XrefString.md) | A string that is a cross reference to another entity represented in another o... |


## Subsets

| Subset | Description |
| --- | --- |
