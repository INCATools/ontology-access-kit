
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class SubjectPrefix(Base):
    """
    This may move to another module as it is generally useful
    """
    __tablename__ = 'subject_prefix'
    
    subject = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subject_prefix(subject={self.subject},value={self.value},)"
        
    
        
    


class TextualTransformation(Base):
    """
    Represents a transformation of a subject text value, e.g. lemmatization
    """
    __tablename__ = 'textual_transformation'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"textual_transformation(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    


class ProcessedStatement(Base):
    """
    A statement that is enhanced with a processed/transformed text value
    """
    __tablename__ = 'processed_statement'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    transformation_predicate = Column(Text(), primary_key=True)
    transformed_value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"processed_statement(subject={self.subject},predicate={self.predicate},value={self.value},transformation_predicate={self.transformation_predicate},transformed_value={self.transformed_value},)"
        
    
        
    


class Match(Base):
    """
    TODO: Reuse SSSOM here
    """
    __tablename__ = 'match'
    
    subject_id = Column(Text(), primary_key=True)
    subject_label = Column(Text(), primary_key=True)
    subject_source = Column(Text(), primary_key=True)
    subject_match_field = Column(Text(), primary_key=True)
    subject_preprocessing = Column(Text(), primary_key=True)
    object_id = Column(Text(), primary_key=True)
    object_label = Column(Text(), primary_key=True)
    object_source = Column(Text(), primary_key=True)
    object_match_field = Column(Text(), primary_key=True)
    object_preprocessing = Column(Text(), primary_key=True)
    match_string = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"match(subject_id={self.subject_id},subject_label={self.subject_label},subject_source={self.subject_source},subject_match_field={self.subject_match_field},subject_preprocessing={self.subject_preprocessing},object_id={self.object_id},object_label={self.object_label},object_source={self.object_source},object_match_field={self.object_match_field},object_preprocessing={self.object_preprocessing},match_string={self.match_string},)"
        
    
        
    


class Prefix(Base):
    """
    Maps CURIEs to URIs
    """
    __tablename__ = 'prefix'
    
    prefix = Column(Text(), primary_key=True)
    base = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"prefix(prefix={self.prefix},base={self.base},)"
        
    
        
    


class Statements(Base):
    """
    Represents an RDF triple
    """
    __tablename__ = 'statements'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"statements(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    


class Node(Base):
    """
    The basic unit of representation in an RDF or OWL graph
    """
    __tablename__ = 'node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"node(id={self.id},)"
        
    
        
    


class RdfLevelSummaryStatistic(Base):
    """
    Abstract grouping for views/classes that provide some kind of count summary about an individual element
    """
    __tablename__ = 'rdf_level_summary_statistic'
    
    element = Column(Text(), primary_key=True)
    count_value = Column(Integer(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_level_summary_statistic(element={self.element},count_value={self.count_value},)"
        
    
        
    


class RelationGraphConstruct(Base):
    """
    A construct used as part of a Relation Graph
    """
    __tablename__ = 'relation_graph_construct'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"relation_graph_construct(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    


class OwlComplexAxiom(Base):
    """
    An axiom that is composed of two or more statements
    """
    __tablename__ = 'owl_complex_axiom'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_complex_axiom(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    


class RepairAction(Base):
    """
    Represents an action that needs to be taken to repair a problem
    """
    __tablename__ = 'repair_action'
    
    subject = Column(Text(), primary_key=True)
    description = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"repair_action(subject={self.subject},description={self.description},)"
        
    
        
    


class Problem(Base):
    """
    Represents an instance of a problem pertaining to conformance to OBO guidelines
    """
    __tablename__ = 'problem'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"problem(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    


class NodeToNodeStatement(Statements):
    """
    A statement where object is non-null and value is not populated
    """
    __tablename__ = 'node_to_node_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"node_to_node_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class NodeToValueStatement(Statements):
    """
    A statement where value is non-null and object is not populated
    """
    __tablename__ = 'node_to_value_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"node_to_value_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfListStatement(Statements):
    """
    A statement that is used to represent aspects of RDF lists
    """
    __tablename__ = 'rdf_list_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_list_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class BlankNode(Node):
    """
    A node with an ID that is not preserved between databases
    """
    __tablename__ = 'blank_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"blank_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class IriNode(Node):
    """
    
    """
    __tablename__ = 'iri_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"iri_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ClassNode(Node):
    """
    A node that represents an RDFS/OWL class
    """
    __tablename__ = 'class_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class PropertyNode(Node):
    """
    Note this only directly classifies nodes asserted to be rdf:Properties
    """
    __tablename__ = 'property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class NamedIndividualNode(Node):
    """
    A node that represents an OWL Named Individual
    """
    __tablename__ = 'named_individual_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"named_individual_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class CountOfPredicates(RdfLevelSummaryStatistic):
    """
    Number of distinct usages of a predicate. NOTE MAY CHANGE: does not currently count existential usage in OWL
    """
    __tablename__ = 'count_of_predicates'
    
    element = Column(Text(), primary_key=True)
    count_value = Column(Integer(), primary_key=True)
    
    
    def __repr__(self):
        return f"count_of_predicates(element={self.element},count_value={self.count_value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class CountOfInstantiatedClasses(RdfLevelSummaryStatistic):
    """
    Number of distinct instantiations of a class. Note in many OBOs, classes are not directly instantiated
    """
    __tablename__ = 'count_of_instantiated_classes'
    
    element = Column(Text(), primary_key=True)
    count_value = Column(Integer(), primary_key=True)
    
    
    def __repr__(self):
        return f"count_of_instantiated_classes(element={self.element},count_value={self.count_value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class CountOfSubclasses(RdfLevelSummaryStatistic):
    """
    Number of subclasses for a given class
    """
    __tablename__ = 'count_of_subclasses'
    
    element = Column(Text(), primary_key=True)
    count_value = Column(Integer(), primary_key=True)
    
    
    def __repr__(self):
        return f"count_of_subclasses(element={self.element},count_value={self.count_value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Edge(RelationGraphConstruct):
    """
    A relation graph edge that connects two entities by a predicate. Note an edge is distinct from a statement, in that an axiom such as A SubClassOf R some B is represented as multiple statements, but is a single relation graph edge
    """
    __tablename__ = 'edge'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"edge(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphQuery(RelationGraphConstruct):
    """
    A subgraph query encompasses as subgraph edge and a seed/anchor object and seed/anchor predicate
    """
    __tablename__ = 'subgraph_query'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_query(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EntailedEdge(RelationGraphConstruct):
    """
    A relation graph edge that is inferred
    """
    __tablename__ = 'entailed_edge'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"entailed_edge(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EntailedEdgeCycle(RelationGraphConstruct):
    """
    An edge that composes with another edge to make a cycle
    """
    __tablename__ = 'entailed_edge_cycle'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    secondary_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"entailed_edge_cycle(subject={self.subject},predicate={self.predicate},object={self.object},secondary_predicate={self.secondary_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TransitiveEdge(RelationGraphConstruct):
    """
    A relation graph edge that is formed from a chain of one or more edges
    """
    __tablename__ = 'transitive_edge'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"transitive_edge(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OntologyNode(Node):
    """
    A node representing an ontology
    """
    __tablename__ = 'ontology_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"ontology_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class DeprecatedNode(Node):
    """
    
    """
    __tablename__ = 'deprecated_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"deprecated_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlReifiedAxiom(Statements):
    """
    An OWL axiom that has been reified - i.e. it includes an [id](id) field that uniquely identifies that axiom and which can be the subject of additional statements
    """
    __tablename__ = 'owl_reified_axiom'
    
    id = Column(Text(), primary_key=True)
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_reified_axiom(id={self.id},stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlAxiom(Statements):
    """
    
    """
    __tablename__ = 'owl_axiom'
    
    id = Column(Text(), primary_key=True)
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_axiom(id={self.id},stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlAxiomAnnotation(Statements):
    """
    
    """
    __tablename__ = 'owl_axiom_annotation'
    
    axiom_predicate = Column(Text(), primary_key=True)
    axiom_object = Column(Text(), primary_key=True)
    axiom_value = Column(Text(), primary_key=True)
    axiom_language = Column(Text(), primary_key=True)
    axiom_datatype = Column(Text(), primary_key=True)
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_axiom_annotation(axiom_predicate={self.axiom_predicate},axiom_object={self.axiom_object},axiom_value={self.axiom_value},axiom_language={self.axiom_language},axiom_datatype={self.axiom_datatype},stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlSubclassOfSomeValuesFrom(OwlComplexAxiom):
    """
    Composition of subClassOf and SomeValuesFrom
    """
    __tablename__ = 'owl_subclass_of_some_values_from'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_subclass_of_some_values_from(subject={self.subject},predicate={self.predicate},object={self.object},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlEquivalentToIntersectionMember(OwlComplexAxiom):
    """
    Composition of `OwlEquivalentClass`, `OwlIntersectionOf`, and `RdfListMember`; `C = X1 and ... and Xn`
    """
    __tablename__ = 'owl_equivalent_to_intersection_member'
    
    subject = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_equivalent_to_intersection_member(subject={self.subject},object={self.object},predicate={self.predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class LexicalProblem(Problem):
    """
    a problem with the textual value of an annotation property
    """
    __tablename__ = 'lexical_problem'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"lexical_problem(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TrailingWhitespaceProblem(Problem):
    """
    
    """
    __tablename__ = 'trailing_whitespace_problem'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"trailing_whitespace_problem(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class PropertyUsedWithDatatypeValuesAndObjects(Problem):
    """
    A problem in which the same property is used two two different ways, one in which the range is a literal value, the other where it is an object.
    """
    __tablename__ = 'property_used_with_datatype_values_and_objects'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"property_used_with_datatype_values_and_objects(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class NodeWithTwoLabelsProblem(Problem):
    """
    
    """
    __tablename__ = 'node_with_two_labels_problem'
    
    label1 = Column(Text(), primary_key=True)
    label2 = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"node_with_two_labels_problem(label1={self.label1},label2={self.label2},subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AllProblems(Problem):
    """
    
    """
    __tablename__ = 'all_problems'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"all_problems(subject={self.subject},predicate={self.predicate},value={self.value},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfTypeStatement(NodeToNodeStatement):
    """
    A statement that indicates the asserted type of the subject entity
    """
    __tablename__ = 'rdf_type_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_type_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsSubclassOfStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'rdfs_subclass_of_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_subclass_of_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsSubpropertyOfStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'rdfs_subproperty_of_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_subproperty_of_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsLabelStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'rdfs_label_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_label_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsDomainStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'rdfs_domain_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_domain_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsRangeStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'rdfs_range_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_range_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfFirstStatement(RdfListStatement):
    """
    A statement that connects a list to its first element. This is a low-level triple, it is unlikely you need to use this directly. It is used to define rdf_list_member_statement, which is more useful
    """
    __tablename__ = 'rdf_first_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_first_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfRestStatement(RdfListStatement):
    """
    A statement that connects a list to its remaining elements. This is a low-level triple, it is unlikely you need to use this directly. It is used to define rdf_list_member_statement, which is more useful
    """
    __tablename__ = 'rdf_rest_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_rest_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfRestTransitiveStatement(RdfListStatement):
    """
    
    """
    __tablename__ = 'rdf_rest_transitive_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_rest_transitive_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfListMemberStatement(RdfListStatement):
    """
    
    """
    __tablename__ = 'rdf_list_member_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_list_member_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfListNode(BlankNode):
    """
    A node representing an RDF list. Note that you will not likely need to use this directly.
    """
    __tablename__ = 'rdf_list_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdf_list_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeByAncestor(SubgraphQuery):
    """
    An edge within a subgraph anchored around a set of ancestor terms
    """
    __tablename__ = 'subgraph_edge_by_ancestor'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_ancestor(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeByDescendant(SubgraphQuery):
    """
    An edge within a subgraph anchored around a set of descendant terms
    """
    __tablename__ = 'subgraph_edge_by_descendant'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_descendant(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeByAncestorOrDescendant(SubgraphQuery):
    """
    
    """
    __tablename__ = 'subgraph_edge_by_ancestor_or_descendant'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_ancestor_or_descendant(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeByParent(SubgraphQuery):
    """
    An edge within a subgraph anchored around a set of parent terms
    """
    __tablename__ = 'subgraph_edge_by_parent'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_parent(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeByChild(SubgraphQuery):
    """
    An edge within a subgraph anchored around a set of child terms
    """
    __tablename__ = 'subgraph_edge_by_child'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_child(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubgraphEdgeBySelf(SubgraphQuery):
    """
    A special null form of a subgraph query where there is no expansion
    """
    __tablename__ = 'subgraph_edge_by_self'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    anchor_object = Column(Text(), primary_key=True)
    anchor_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subgraph_edge_by_self(subject={self.subject},predicate={self.predicate},object={self.object},anchor_object={self.anchor_object},anchor_predicate={self.anchor_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EntailedEdgeSamePredicateCycle(EntailedEdgeCycle):
    """
    An entailed_edge_cycle over a single predicate
    """
    __tablename__ = 'entailed_edge_same_predicate_cycle'
    
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    secondary_predicate = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"entailed_edge_same_predicate_cycle(subject={self.subject},predicate={self.predicate},object={self.object},secondary_predicate={self.secondary_predicate},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ObjectPropertyNode(PropertyNode):
    """
    A node representing an OWL object property
    """
    __tablename__ = 'object_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"object_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnnotationPropertyNode(PropertyNode):
    """
    A node representing an OWL annotation property
    """
    __tablename__ = 'annotation_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"annotation_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlImportsStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'owl_imports_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_imports_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlInverseOfStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'owl_inverse_of_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_inverse_of_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlComplementOfStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'owl_complement_of_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_complement_of_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlEquivalentClassStatement(NodeToNodeStatement):
    """
    A statement that connects two class_nodes where both classes are equivalent
    """
    __tablename__ = 'owl_equivalent_class_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_equivalent_class_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlSameAsStatement(NodeToNodeStatement):
    """
    A statement that connects two individual nodes where both individual are equivalent
    """
    __tablename__ = 'owl_same_as_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_same_as_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlDisjointClassStatement(NodeToNodeStatement):
    """
    
    """
    __tablename__ = 'owl_disjoint_class_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_disjoint_class_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousExpression(BlankNode):
    """
    An OWL expression, such as a class expression. Expressions are "anonymous" as they are a composition of named elements rather than a named element themselves
    """
    __tablename__ = 'anonymous_expression'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasTextDefinitionStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'has_text_definition_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_text_definition_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasOioSynonymStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'has_oio_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_oio_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasSynonymStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'has_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasMatchStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'has_match_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_match_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasMappingStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'has_mapping_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_mapping_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AxiomDbxrefAnnotation(OwlAxiomAnnotation):
    """
    
    """
    __tablename__ = 'axiom_dbxref_annotation'
    
    axiom_predicate = Column(Text(), primary_key=True)
    axiom_object = Column(Text(), primary_key=True)
    axiom_value = Column(Text(), primary_key=True)
    axiom_language = Column(Text(), primary_key=True)
    axiom_datatype = Column(Text(), primary_key=True)
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"axiom_dbxref_annotation(axiom_predicate={self.axiom_predicate},axiom_object={self.axiom_object},axiom_value={self.axiom_value},axiom_language={self.axiom_language},axiom_datatype={self.axiom_datatype},stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OntologyStatusStatement(NodeToValueStatement):
    """
    
    """
    __tablename__ = 'ontology_status_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"ontology_status_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class RdfsSubclassOfNamedStatement(RdfsSubclassOfStatement):
    """
    
    """
    __tablename__ = 'rdfs_subclass_of_named_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"rdfs_subclass_of_named_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TransitivePropertyNode(ObjectPropertyNode):
    """
    A node representing an OWL transitive object property
    """
    __tablename__ = 'transitive_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"transitive_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SymmetricPropertyNode(ObjectPropertyNode):
    """
    A node representing an OWL symmetric object property
    """
    __tablename__ = 'symmetric_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"symmetric_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ReflexivePropertyNode(ObjectPropertyNode):
    """
    A node representing an OWL reflexive object property
    """
    __tablename__ = 'reflexive_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"reflexive_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class IrreflexivePropertyNode(ObjectPropertyNode):
    """
    A node representing an OWL irreflexive object property
    """
    __tablename__ = 'irreflexive_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"irreflexive_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AsymmetricPropertyNode(ObjectPropertyNode):
    """
    
    """
    __tablename__ = 'asymmetric_property_node'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"asymmetric_property_node(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousClassExpression(AnonymousExpression):
    """
    An OWL anonymous class expression, such as for example `SomeValuesFrom(partOf Hand)`
    """
    __tablename__ = 'anonymous_class_expression'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousPropertyExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_property_expression'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_property_expression(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousIndividualExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_individual_expression'
    
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_individual_expression(id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasExactSynonymStatement(HasOioSynonymStatement):
    """
    
    """
    __tablename__ = 'has_exact_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_exact_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasBroadSynonymStatement(HasOioSynonymStatement):
    """
    
    """
    __tablename__ = 'has_broad_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_broad_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasNarrowSynonymStatement(HasOioSynonymStatement):
    """
    
    """
    __tablename__ = 'has_narrow_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_narrow_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasRelatedSynonymStatement(HasOioSynonymStatement):
    """
    
    """
    __tablename__ = 'has_related_synonym_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_related_synonym_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasExactMatchStatement(HasMatchStatement):
    """
    
    """
    __tablename__ = 'has_exact_match_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_exact_match_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasBroadMatchStatement(HasMatchStatement):
    """
    
    """
    __tablename__ = 'has_broad_match_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_broad_match_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasNarrowMatchStatement(HasMatchStatement):
    """
    
    """
    __tablename__ = 'has_narrow_match_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_narrow_match_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasRelatedMatchStatement(HasMatchStatement):
    """
    
    """
    __tablename__ = 'has_related_match_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_related_match_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class HasDbxrefStatement(HasMappingStatement):
    """
    
    """
    __tablename__ = 'has_dbxref_statement'
    
    stanza = Column(Text(), primary_key=True)
    subject = Column(Text(), primary_key=True)
    predicate = Column(Text(), primary_key=True)
    object = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    datatype = Column(Text(), primary_key=True)
    language = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"has_dbxref_statement(stanza={self.stanza},subject={self.subject},predicate={self.predicate},object={self.object},value={self.value},datatype={self.datatype},language={self.language},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlRestriction(AnonymousClassExpression):
    """
    An OWL restriction, such as `SomeValuesFrom(partOf Hand)`
    """
    __tablename__ = 'owl_restriction'
    
    on_property = Column(Text(), primary_key=True)
    filler = Column(Text(), primary_key=True)
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_restriction(on_property={self.on_property},filler={self.filler},id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlSomeValuesFrom(OwlRestriction):
    """
    An OWL SomeValuesFrom restriction
    """
    __tablename__ = 'owl_some_values_from'
    
    on_property = Column(Text(), primary_key=True)
    filler = Column(Text(), primary_key=True)
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_some_values_from(on_property={self.on_property},filler={self.filler},id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlAllValuesFrom(OwlRestriction):
    """
    
    """
    __tablename__ = 'owl_all_values_from'
    
    on_property = Column(Text(), primary_key=True)
    filler = Column(Text(), primary_key=True)
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_all_values_from(on_property={self.on_property},filler={self.filler},id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlHasValue(OwlRestriction):
    """
    
    """
    __tablename__ = 'owl_has_value'
    
    on_property = Column(Text(), primary_key=True)
    filler = Column(Text(), primary_key=True)
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_has_value(on_property={self.on_property},filler={self.filler},id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class OwlHasSelf(OwlRestriction):
    """
    
    """
    __tablename__ = 'owl_has_self'
    
    on_property = Column(Text(), primary_key=True)
    filler = Column(Text(), primary_key=True)
    id = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"owl_has_self(on_property={self.on_property},filler={self.filler},id={self.id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


