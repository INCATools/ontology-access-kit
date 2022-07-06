Glossary
========

.. glossary::

   Ontology
    A flexible concept loosely encompassing any collection of :term:`Ontology elements` and statements or relationships connecting them

   Ontology element
    A discrete part of an :term:`Ontology`, with a unique persistent identifier. The most important elements are :ref:`Term`s, but
    other elements can include various metadata artefacts like :ref:`Annotation Property`s or :ref:`Subset`s

   Term
    A core element in an ontology, typically a :term:`Class`, but sometimes used to include instances or relationship types,
    depending on context.

   Concept
    See :term:`Term`

   CURIE
    A :term:`CURIE` is a compact :term:`URI`. For example, ``CL:0000001``.

   URI
    A Uniform Resource Indicator, a generalization of URL. Most people think of URLs as being solely for addresses for web pages (or APIs) but in semantic web technologies, URLs can serve as actual identifiers for entities like ontology terms.
    Data models like :term:`OWL` and :term:`RDF` use URIs as identifiers. In OAK, URIs are mapped to :term:`CURIE`s

   Label
    Usually refers to a human-readable label corresponding to the ``rdfs:label`` :term:`predicate`. Labels are typically unique
    per ontology. In OBO Format and in the bio-ontology literature, labels are sometimes called :term:`Names<Name>`.
    Sometimes in the machine learning literature, and in databases such as Neo4J, "label" actually refers to a :term:`Category`.

   Name
    Usually synonymous with :term:`Label`, but in the formal logic and OWL community, "Name" sometimes denotes an :term:`Identifier`

   Class
    An :term:`Ontology element` that formally represents something that can be instantiated. For example, the class "heart"

   Annotation
    This term is frequently ambiguous. It can refer to :term:`Text Annotation`, :term:`OWL Annotation`, or :term:`Association`.

   Text Annotation
    The process of annotating spans of texts within a text document with references to ontology terms, or the result of this
    process. This is frequently done automatically. The :term:`Bioportal` implementation provides text annotation services.
    More advanced annotation services will be available through AI plugins in OAK in the future.

   Mapping
    See :ref:`SSSOM`

   SSSOM
    Simple Standard for Sharing Ontological Mappings. SSSOM is the primary :term:`Datamodel` in OAK for passing around :term:`Mapping`s.

   Graph
    Formally a graph is a data structure consisting of :term:`Nodes<Node>` and :term:`Edges<Edge>`. There are different forms of graphs, but for the purposes of OAK,
    an ontology graph has all :term:`Term`s as nodes, and relationships connecting terms (is-a, part-of) as edges.
    Note the concept of an ontology graph and an :term:`RDF` graph do not necessarily fully align - RDF graphs of OWL ontologies
    employ numerous blank nodes that obscure the ontology structure.

   OWL
    An ontology language that uses constructs from :term:`Description Logic`. OWL is not itself an ontology format, it can be serialized
    through different formats such as :term:`Functional Syntax`, and it can be mapped to :term:`RDF` and serialized via an RDF format.

   RDF
    A datamodel consisting of simple :term:`Subject` :term:`Predicate` :term:`Object` :term:`Triples` organized into an RDF :term:`Graph`

   OBO Format
    A serialization format for ontologies designed for easy viewing, direct editing, and readable diffs. It is popular in bioinformatics,
    but not widely used or known outside the genomics sphere. OBO is mapped to OWL, but only expresses a subset, and provides some OWL
    abstractions in a more easy to understand fashion.

   KGCL
    Knowledge Graph Change Language (KGCL) is a :term:`Datamodel` for communicating desired changes to an ontology.
    It can also be used to communicate differences between two ontologies. See `KGCL docs <https://github.com/INCATools/kgcl>`_.

   OWL Annotation
    In the context of :term:`OWL`, the term :term:`Annotation` means a piece of metadata that does not have a strict logical
    interpretation. Annotations can be on entities, for example, :term:`Label` annotations, or annotations can be on :term:`Axioms<Axiom>`.

   Pronto
    An :term:`Ontology Library` for parsing obo and owl files

   Iterator
    A programming language construct used frequently in OAK - it allows for passing of results from API calls without fetching
    everything in advance.

   Interface
    A programmatic abstraction that allows us to focus on *what* something should do rather than *how* it is done.
    See :ref:`interfaces`. The *how* is managed by an :term:`Implementation`

   Implementation
    See :ref:`implementations`

   Datamodel
    See :ref:`datamodels`

   Named Individual
    An :term:`Ontology element` that represents an instance of a class. . For example, the instance "John" or "John's heart".
    Note that instances are not commonly represented in ontologies, and are not currently well supported in OAK.

   Property
    An :term:`Ontology element` that represents an attribute or a characteristic of an element.
    In :term:`OWL`, properties are divided into disjoint categories:
      * :term:`ObjectProperty`
      * :term:`AnnotationProperty`
      * :term:`DatatypeProperty`

   Edge
    See :term:`Relationship`

   Triple
    See :term:`Relationship`

   Relationship
    A :term:`Relationship` is a type connection between two ontology elements. The first element is called the :term:`subject`,
    and the second one the :term:`object`, with the type of connection being the :term:`Relationship Type`.
    Sometimes Relationships are equated with :term:`Triples<Triple>` in :term:`RDF` but this can be confusing, because some relationships
    map to *multiple* triples when following the OWL RDF serialization. An example is the relationship "finger part-of hand",
    which in OWL is represented using a :term:`Existential Restriction` that maps to 4 triples.

   Relationship Type
    See :term:`Predicate`

   Predicate
    An :term:`Ontology element` that represents the type of a :term:`Relationship`.
    Typically corresponds to an :term:`ObjectProperty` in :term:`OWL`, but this is not always true;
    in particular, the :term:`is-a` relationship type is a builtin construct ``SubClassOf`` in OWL
    Examples:
     * is-a
     * part-of (BFO:0000050)

   Subset
    An :term:`Ontology element` that represents a named collection of elements, typically grouped for some purpose

   Reasoner
    An ontology tool that will perform inference over an ontology to yield new *axioms* (e.g. new :term:`Edges<Edge>`) or
    to determine if an ontology is logically :term:`Coherent`.

   Bioportal
    An :term:`Ontology Repository` that is a comprehensive collection of multiple biologically relevant ontologies.
    Bioportal exposes an :term:`API` endpoint, that is utilized by the OAK :ref:`bioportal_implementation`. 

   OLS
    Ontology Lookup Service. An :term:`Ontology Repository` that is a curated collection of multiple biologically relevant ontologies,
    many from :term:`OBO`.
    OLS exposes an :term:`API` endpoint, that is utilized by the OAK OLS :term:`Implementation`

   Ubergraph
    A:term:`Triplestore` and a :term:`Ontology Repository` that allows for :term:`SPARQL` querying of integrated :term:`OBO` ontologies.
    Accessible via AK Ubergraph :term:`Implementation`

   Semantic SQL
    Semantic SQL is a proposed standardized schema for representing any RDF/OWL ontology, plus a set of tools for building
    a database conforming to this schema from RDF/OWL files. See `Semantic-SQL <https://github.com/INCATools/semantic-sql>`_

   Semantic Similarity
    A means of measuring similarity between either pairs of ontology concepts, or between entities annotated using ontology
    concepts. There is a wide variety of different methods for calculating semantic similarity, for example :term:`Jaccard Similarity`
    and :term:`Information Content` based measures.

   Information Content
    A measure of how informative an ontology concept is; broader concepts are less informative as they encompass many things,
    whereas more specific concepts are more unique. This is usually measured as ``-log2(Pr(term))``. The method of calculating
    the probability varies, depending on which predicates are taken into account (for many ontologies, it makes sense to
    use part-of as well as is-a), and whether the probability is the probability of observing a descendant term, or of an
    entity annotated using that term.
