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

   Class
    An :term:`Ontology element` that formally represents something that can be instantiated. For example, the class "heart"

   Mapping
    See :ref:`SSSOM`

   SSSOM
    Simple Standard for Sharing Ontological Mappings. SSSOM is the primary :term:`Datamodel` in OAK for passing around :term:`Mapping`s.

   Graph
    Formally a graph is a data structure consisting of :term:`Nodes` and :term:`Edges`. There are different forms of graphs, but for the purposes of OAK,
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

   Pronto
    An :term:`Ontology Library` for parsing obo and owl files

   Iterator
    A programming language construct used frequently in OAK - it allows for passing of results from API calls without fetching
    everything in advance

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
    Bioportal exposes an :term:`API` endpoint, that is utilized by the OAK Bioportal :term:`Implementation`

   OLS
    Ontology Lookup Service. An :term:`Ontology Repository` that is a curated collection of multiple biologically relevant ontologies,
    many from :term:`OBO`.
    OLS exposes an :term:`API` endpoint, that is utilized by the OAK OLS :term:`Implementation`

   Ubergraph
    A:term:`Triplestore` and a :term:`Ontology Repository` that allows for :term:`SPARQL` querying of integrated :term:`OBO` ontologies.
    Accessible via AK Ubergraph :term:`Implementation`
