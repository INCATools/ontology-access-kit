# obographs_datamodel

A data model for graph-oriented representations of ontologies. Each ontology is represented as a Graph, and multiple ontologies can be connected together in a GraphDocument.
The principle elements of a Graph are Node objects and Edge objects. A Node represents an arbitrary ontology element, including but not limited to the core terms in the ontology. Edges represent simple relationships between Nodes. Nodes and Edges can both have Meta objects attached, providing additional metedata.
Not everything in an ontology can be represented as nodes and edges. More complex axioms have specialized structures such as DomainRangeAxiom objects and LogicalDefinitionAxiom.

URI: https://github.com/geneontology/obographs

