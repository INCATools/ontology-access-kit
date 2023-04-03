Glossary
========

This section contains a glossary of the terms used in the OAK documentation
and API, as well as terms used more broadly by different ontology communities.

For a deeper dive into some of these concepts, see the :ref:`guide`.

.. glossary::

   Ontology
    A flexible concept loosely encompassing any collection of :term:`Ontology Elements<Ontology Element>` and statements or relationships connecting them

   Ontology Element
    A discrete part of an :term:`Ontology`, with a unique persistent identifier. The most important elements are :term:`Terms<Term>`, but
    other elements can include various metadata artefacts like :term:`Annotation Properties<AnnotationProperty>`
    or :term:`Subsets<Subset>`

   Term
    A core element in an ontology, typically a :term:`Class`, but sometimes used to include :term:`Instances<Instance>`
    or :term:`Relationship Types<Relationship Type>`, depending on context. Note that in some contexts,
    the term "term" means something like a :term:`Label` or :term:`Synonym`, but here we follow standard usage
    and use "term" to refer to the main elements in an ontology.

   Concept
    See :term:`Term`

   Class
    An :term:`Ontology Element` that formally represents something that can be instantiated.
    For example, the class "heart" represented in the :term:`Uberon` ontology by the :term:`CURIE`
    ``UBERON:0000948``. In most bio-ontologies, term "Class" is often synonymous with :term:`Terms<Term>`.

   Identifier
    An identifier is a string that serves to uniquely identify some kind of entity such as an :term:`Ontology Element`.
    In :term:`Semantic Web` and :term:`Linked Data` technologies, identifiers are always :term:`IRIs<IRI>`, although
    they may be shortened to :term:`CURIEs<CURIE>` within individual documents.

   CURIE
    A :term:`CURIE` is a compact :term:`URI`. For example, ``CL:0000001`` is the CURIE for
    the root :term:`Class` in the Cell Ontology (which has the :term:`Prefix` ``CL``).

   URI
    A Uniform Resource Indicator, a generalization of URL. Most people think of URLs as being solely for addresses for web pages (or APIs) but in semantic web technologies, URLs can serve as actual identifiers for entities like ontology terms.
    Data models like :term:`OWL` and :term:`RDF` use URIs as :term:`identifiers<identifier>`. In OAK, URIs are mapped to :term:`CURIEs<CURIE>`.

   Label
    Usually refers to a human-readable label corresponding to the ``rdfs:label`` :term:`predicate`. Labels are typically unique
    per ontology. In :term:`OBO Format` and in the bio-ontology literature, labels are sometimes called :term:`Names<Name>`.
    Sometimes in the machine learning literature, and in databases such as Neo4J, "label" actually refers to a :term:`Category`.
    In the context of OAK, :term:`Label` is used to refer to the ``rdfs:label`` :term:`Predicate`, or
    sometimes ``skos:prefLabel``.

   Name
    Usually synonymous with :term:`Label`, but in the formal logic and OWL community, "Name" sometimes denotes an :term:`Identifier`

   Category
    The term :term:`Category` is frequently ambiguous. In the context of OAK it refers to a high-level grouping
    :term:`Class` that may come from an upper ontology like :term:`COB` or a schema language like
    :term:`Biolink` or schema.org.

   Annotation
    The term :term:`Annotation` is frequently ambiguous. It can refer to:
     - :term:`Text Annotation`
     - :term:`OWL Annotation`
     - :term:`Association`

   Association
    In the context of OAK, an :term:`Association` is a statement that connects some kind of named entity (such as
    a gene, a person, a sample, or a disease) to an :term:`Ontology Element`. In the context of many bio-ontologies like
    the :term:`Gene Ontology` or :term:`Human Phenotype Ontology`, Associations are usually called
    "annotations". Associations can be seen as special cases of :term:`Edges<Edge>`, but it is often convenient to
    treat them differently (for example, associations frequently have additional metadata and evidence,
    and often have nuanced semantics that different from standard ontology edges).

   Text Annotation
    The process of annotating spans of texts within a text document with references to ontology terms, or the result of this
    process. This is frequently done automatically. The :term:`Bioportal` implementation provides text annotation services.
    More advanced annotation services will be available through AI plugins in OAK in the future.

   Mapping
    The term :term:`Mapping` is often used differently by different communities. In the context of OAK
    it means a pairwise association between two :term:`Ontology Elements<Ontology Element>`, where those
    elements are conceptually similar or close in meaning. OAK adheres closely to the :term:`SSSOM` data model.

   SSSOM
    Simple Standard for Sharing Ontological Mappings. SSSOM is the primary :term:`Datamodel` in OAK for passing around :term:`Mappings<Mapping>`.

   Graph
    Formally a graph is a data structure consisting of :term:`Nodes<Node>` and :term:`Edges<Edge>`. There are different forms of graphs, but for the purposes of OAK,
    an ontology graph has all :term:`Terms<Term>` as nodes, and relationships connecting terms (is-a, part-of) as edges.
    Note the concept of an ontology graph and an :term:`RDF` graph do not necessarily fully align - RDF graphs of OWL ontologies
    employ numerous blank nodes that obscure the ontology structure. See :term:`Ontology Graph Projection`.

   Edge
    See :term:`Relationship`

   Node
    A :term:`Node` (aka Vertex) is one of the two main elements that make up a :term:`Graph`.
    The other element is an :term:`Edge`. The nodes in a graph typically represent :term:`Classes<Class>`
    but this depends on the :term:`Ontology Graph Projection`. The nodes of a graph might also
    be :term:`Instances<Named Individual>` or :term:`Relationship Types<Predicate>`, or metadata
    elements such as :term:`Subset` definitions.

   Relationship Type
    See :term:`Predicate`

   Predicate
    An :term:`Ontology element` that represents the type of a :term:`Relationship`.
    Typically corresponds to an :term:`ObjectProperty` in :term:`OWL`, but this is not always true;
    in particular, the :term:`is-a` relationship type is a builtin construct ``SubClassOf`` in OWL
    Examples:
     * :term:`IS_A` (rdfs:subClassOf)
     * :term:`Part Of` (BFO:0000050)

   IS_A:
    The :term:`is-a` relationship type. This is a builtin construct in :term:`OWL` and is not
    represented as an :term:`Ontology Element`. In OAK, the :term:`IS_A` relationship type is
    represented as a :term:`Predicate` with the :term:`IRI` ``owl:subClassOf``.

   Part Of
    The :term:`Part Of` relationship type. This is one of the most important relationship types
    in many ontologies such as :term:`GO`, :term:`Uberon`, and others.
    In OAK, the :term:`Part Of` relationship type is
    represented as a :term:`Predicate` with the :term:`CURIE` ``BFO:0000050``.

   Ancestor
    The :term:`Ancestor` of an entity is the set of all entities that are reachable by following
    all :term:`Relationship`s, from :term:`subject` or :term:`object`. Ancestor traversal is frequently
    paramaterized by a set of :term:`Predicates<Predicate>`. The concept of :term:`Ancestor` and
    graph traversal is closely related to the concept of :term:`Entailment<Entailed Axiom>` in :term:`OWL`.

   Descendant
    The converse of :term:`Ancestor`.

   Ontology Graph Projection
    The mapping between an ontology as represented in some formalism such as :term:`OWL` ontology onto a :term:`Graph`.
    This is a non-trivial process, because OWL ontologies are not natively represented as graphs, instead they are
    represented as collections of :term:`Axioms<Axiom>`.
    The most common projection is the :term:`RDF` mapping, but this results in a structure that is
    not well suited to graph operations due to the use of :term:`Blank Nodes` to represent OWL
    expressions.
    OAK makes use of a simple projection where OWL existential axioms are mapped to :term:`Edges<Edge>`,
    similar to :term:`Relation Graph`.

   Relation Graph
    Relation Graph is both a tool and a :term:`Ontology Graph Projection`.
    Relation Graph is used behind the scenes in both :term:`Ubergraph` and in :term:`Semantic SQL`.

   Ontology Format
    A syntax for serializing an :term:`Ontology` as text. Examples include :term:`OWL Functional Syntax`,
    various :term:`RDF` formats such as :term:`Turtle`, or :term:`OBO Format`.
    In OAK we take a broad view of the term "Ontology", and also include things
    such as RDF serializations of :term:`SKOS`.
    See also:
     - :term:`guide_ontology_languages`

   OWL
    An ontology language that uses constructs from :term:`Description Logic`. OWL is not itself an ontology format, it can be serialized
    through different :term:`Ontology Formats<Ontology Format>` such as :term:`Functional Syntax`, and it can be mapped to :term:`RDF` and serialized via an RDF format.

   RDF
    A :term:`Datamodel` consisting of simple :term:`Subject` :term:`Predicate` :term:`Object` :term:`Triples` organized into an RDF :term:`Graph`

   FunOWL
    FunOWL is a Python :term:`Ontology Library` that provides a simple API for working with OWL ontologies
    conceptualized using the native OWL :term:`OWL Functional Syntax` representation.

   OBO Format
    An :term:`Ontology Format` designed for easy viewing, direct editing, and readable diffs. It is popular in bioinformatics,
    but not widely used or known outside the genomics sphere. OBO is mapped to OWL, but only expresses a subset, and provides some OWL
    abstractions in a more easy to understand fashion. See: `<https://owlcollab.github.io/oboformat/doc/obo-syntax.html>`_

   Pronto
    An :term:`Ontology Library` for parsing :term:`OBO Format` with some support for :term:`OWL` files.
    OAK provides a wrapper around Pronto via the :ref:`pronto_implementation`.

   OBO Graphs
    A JSON-based serialization :term:`Ontology Format` and also a :term:`Datamodel` for representing :term:`Ontology Graphs<Ontology Graph>`.
    OBO Graphs are designed to be an abstraction that is more suited to data science tasks than
    :term:`OWL` or :term:`RDF`, and utilizes a different :term:`Ontology Graph Projection` than RDF.

   OWL Annotation
    In the context of :term:`OWL`, the term :term:`Annotation` means a piece of metadata that does not have a strict logical
    interpretation. Annotations can be on entities, for example, :term:`Label` annotations, or annotations can be on :term:`Axioms<Axiom>`.

   Named Individual
    An :term:`Ontology Element` that represents an instance of a class. For example, the instance "John" or "John's heart".
    Note that instances are not commonly directly represented in bio-ontologies, but may be more common
    in other domains.

   Property
    An :term:`Ontology Element` that represents an attribute or a characteristic of an element.
    In :term:`OWL`, properties are divided into disjoint categories:
      * :term:`ObjectProperty`
      * :term:`AnnotationProperty`
      * :term:`DatatypeProperty`

   ObjectProperty
    In OWL, an :term:`ObjectProperty` is a :term:`Property` that connects two :term:`Named Individuals<Named Individual>`.
    Object Properties are also used in :term:`Class` :term:`Axioms<Axiom>`, to express generalizations about
    how instances of those classes are necessarily related.

   AnnotationProperty
    In OWL, an :term:`AnnotationProperty` is a :term:`Property` that connects an :term:`Ontology Element` to
    another element for the purposes of assigning metadata. Annotation Properties are "logically
    silent". In OAK interfaces, we typically use the term :term:`Metadata` property when
    referring to annotation properties.

   DatatypeProperty
    In OWL, a :term:`DatatypeProperty` is a :term:`Property` that connects an :term:`Ontology Element` to
    a :term:`Literal`. Datatype properties are not widely used in most bio-ontologies,
    and currently OAK has limited support for working with them.

   Triple
    A simple :term:`Relationship` that is a tuple of :term:`Subject`, :term:`Predicate`, and :term:`Object`.

   Relationship
    A :term:`Relationship` is a type connection between two ontology elements. The first element is called the :term:`Subject`,
    and the second one the :term:`Object`, with the type of connection being the :term:`Predicate`.
    Sometimes Relationships are equated with :term:`Triples<Triple>` in :term:`RDF` but this can be confusing, because some relationships
    map to *multiple* triples when following the OWL RDF serialization. An example is the relationship "finger part-of hand",
    which in OWL is represented using a :term:`Existential Restriction` that maps to 4 triples.

   Subset
    An :term:`Ontology Element` that represents a named collection of elements, typically grouped for some purpose.
    Subsets are commonly used in ontologies like the :term:`Gene Ontology`.

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

   Triplestore
    A :term:`Graph` database that stores :term:`Triples<Triple>` in a :term:`RDF` :term:`Graph`. Triplestores are used to
    store :term:`Ontology` data, and to provide :term:`SPARQL` querying over the data.

   SPARQL
    A :term:`Query Language` for querying :term:`RDF` :term:`Graphs<Graph>`. SPARQL is the standard query language for
    :term:`Triplestores<Triplestore>`. SPARQL queries are typically executed against a remote :term:`SPARQL Endpoint`
    but they can also be executed against a local RDF file.
    OAK typically abstracts away from languages like SPARQL, but it is possible to pass-through
    SPARQL.

   SQL
    A :term:`Query Language` for querying relational databases. While the use of :term:`SPARQL` is more common in
    for ontologies, one of the most performant OAK :term:`Implementations<Implementation>` is a :term:`Semantic SQL` database.

   Ubergraph
    A:term:`Triplestore` and a :term:`Ontology Repository` that allows for :term:`SPARQL` querying of integrated :term:`OBO` ontologies.
    Accessible via :ref:`ubergraph_implementation`.
    Ubergraph includes inferred :term:`Relation Graph` edges as triples.

   Ontobee
    A :term:`Triplestore` and a :term:`Ontology Repository` that allows for :term:`SPARQL` querying of integrated :term:`OBO` ontologies.
    Accessible via :ref:`ontobee_implementation`.

   Semantic SQL
    Semantic SQL is a proposed standardized schema for representing any RDF/OWL ontology, plus a set of tools for building
    a database conforming to this schema from RDF/OWL files. See `Semantic-SQL <https://github.com/INCATools/semantic-sql>`_

   Diff
    A representation of an individual difference between two :term:`Ontologies<Ontology>`.

   Patch
    A representation of a set of :term:`Diffs<Diff>` that are intended to be applied.

   KGCL
    Knowledge Graph Change Language (KGCL) is a :term:`Datamodel` for communicating desired changes (aka :term:`Patch`) to an ontology.
    It can also be used to communicate :term:`Diffs<Diff>` between two ontologies. See `KGCL docs <https://github.com/INCATools/kgcl>`_.

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

   Iterator
    A programming language construct used frequently in OAK - it allows for passing of results from API calls without fetching
    everything in advance. See `<https://realpython.com/python-iterators-iterables/>`_.

   Interface
    A programmatic abstraction that allows us to focus on *what* something should do rather than *how* it is done.
    Contrast with :ref:`Interface`. The *how* is managed by an :term:`Implementation`.

   Implementation
    Also known as :term:`Adapter`. Typically the details of implementation should not
    be exposed, and developers of applications that use OAK should always :term:`Code to the Interface`.
    For example, the method to query for all :term:`Relationships<Relationship>` from a term should
    have the same meaning regardless of whether the adapter *implementing* the interface is a remote
    triplestore like :term:`Ubergraph`, a :term:`Semantic SQL` adapter, or a local :term:`OBO Graphs` file.
    See the list of :ref:`all implementations<implementations>`

   Datamodel
    Aka schema. OAK follows a pluralistic worldview, and includes many different
    datamodels for different purposes. Examples include:
     - The :term:`KGCL` data model, for representing :term:`Diffs<Diff>`
     - The :term:`OBO Graphs` data model, for representing ontologies through simple :term:`Ontology Graph Projections<Ontology Graph Projection>`
     - A data model for representing :term:`Text Annotation` results
     - The :term:`SSSOM` data model, for representing :term:`Mappings<Mapping>`
     - A data model for representing :term:`Semantic Similarity` results
    See the list of all :ref:`datamodels`.
