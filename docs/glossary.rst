Glossary
========

This section contains a glossary of the terms used in the OAK documentation
and API, as well as terms used more broadly by different ontology communities.

For a deeper dive into some of these concepts, see the :ref:`guide`.

.. glossary::

   Ontology
    A flexible concept loosely encompassing any collection of :term:`Ontology Elements<Ontology Element>` and statements or relationships connecting them.

    - See also :ref:`basics` in the Guide.

   Ontology Element
    A discrete part of an :term:`Ontology`, with a unique persistent identifier. The most important elements are :term:`Terms<Term>`, but
    other elements can include various metadata artefacts like :term:`Annotation Properties<AnnotationProperty>`
    or :term:`Subsets<Subset>`

   Term
    A core element in an ontology, typically a :term:`Class`, but sometimes used to include :term:`Instances<Instance>`
    or :term:`Relationship Types<Relationship Type>`, depending on context. Note that in some contexts,
    the term "term" means something like a :term:`Label` or :term:`Synonym`, but here we follow standard usage
    and use "term" to refer to the main elements in an ontology.

   Entity
    See :term:`Term`

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

    - See also :ref:`curies_and_uris` in the Guide.

   CURIE
    A :term:`CURIE` is a compact :term:`URI`. For example, ``CL:0000001`` is the CURIE for
    the root :term:`Class` in the Cell Ontology (which has the :term:`Prefix` ``CL``).

    - See also :ref:`curies_and_uris` in the Guide.

   URI
    A Uniform Resource Indicator, a generalization of URL. Most people think of URLs as being solely for addresses for web pages (or APIs) but in semantic web technologies, URLs can serve as actual identifiers for entities like ontology terms.
    Data models like :term:`OWL` and :term:`RDF` use URIs as :term:`identifiers<identifier>`. In OAK, URIs are mapped to :term:`CURIEs<CURIE>`.

    - See also :ref:`curies_and_uris` in the Guide.

   Label
    Usually refers to a human-readable label corresponding to the ``rdfs:label`` :term:`predicate`. Labels are typically unique
    per ontology. In :term:`OBO Format` and in the bio-ontology literature, labels are sometimes called :term:`Names<Name>`.
    Sometimes in the machine learning literature, and in databases such as Neo4J, "label" actually refers to a :term:`Category`.
    In the context of OAK, :term:`Label` is used to refer to the ``rdfs:label`` :term:`Predicate`, or
    sometimes ``skos:prefLabel``.

    - See also :ref:`primary_labels` in the Guide.

   Name
    Usually synonymous with :term:`Label`, but in the formal logic and OWL community, "Name" sometimes denotes an :term:`Identifier`

    - See also :ref:`primary_labels` in the Guide.
    - See also :ref:`curies_and_uris` in the Guide.

   Alias
    An alternative label, name, or synonym for a :term:`Term`. The alias may be identical or close in meaning.
    Different ontologies use different properties
    for representing aliases, with or without metadata. Some ontologies might use a single property like
    ``skos:altLabel``, others may adopt the richer OMO :term:`Synonym` model which allows different synonym
    predicates, as well as metadata about the synonym (who proposed it, what publications support it, etc).

    - See also :ref:`aliases` in the Guide.

   Synonym
    This is an alias for :term:`Alias`. Note that some people use the term "synonym" to mean an alternative
    string that is strictly substitutable, but other ontologies, including many OBO ontologies use the term
    more loosely, and discriminate between exact, related, broad, and narrow synonyms.

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
    Despite the differences, we still use the same terminology for associations as for :term:`Edges<Edge>`.
    The :term:`Subject` of an association is the named entity, which the association is about; it could be
    a gene, a person, a sample, a document, a disease, or any number of things. It could potentially be represented
    by a node in an ontology, but it is more typically a databased entity.
    The :term:`Object` is the ontology term that is used as a descriptor for the subject.
    (Confusingly, in some formats, the "database object" actually refers to the *subject* of the association).

    - See also :ref:`associations` in the Guide.

   Text Annotation
    The process of annotating spans of texts within a text document with references to ontology terms, or the result of this
    process. This is frequently done automatically. The :term:`Bioportal` implementation provides text annotation services.
    More advanced annotation services will be available through AI plugins in OAK in the future.

   Mapping
    The term :term:`Mapping` is often used differently by different communities. In the context of OAK
    it means a pairwise association between two :term:`Ontology Elements<Ontology Element>`, where those
    elements are conceptually similar or close in meaning. OAK adheres closely to the :term:`SSSOM` data model.
    Note that OAK treats mappings as distinct from ontology :term:`Associations<Association>` or
    :term:`Edges<Edge>`, due to different use cases for each of these structures. However, there are
    commonalities, and we use the terms :term:`Subject`, :term:`Object`, and :term:`Predicate` in the same way
    for each of these structures.

    - See also :ref:`mappings` in the OAK Guide.

   SSSOM
    Simple Standard for Sharing Ontological Mappings. SSSOM is the primary :term:`Datamodel` in OAK for passing around :term:`Mappings<Mapping>`.

    - See also :ref:`mappings` in the Guide.

   Graph
    Formally a graph is a data structure consisting of :term:`Nodes<Node>` and :term:`Edges<Edge>`. There are different forms of graphs, but for the purposes of OAK,
    an ontology graph has all :term:`Terms<Term>` as nodes, and relationships connecting terms (is-a, part-of) as edges.
    Note the concept of an ontology graph and an :term:`RDF` graph do not necessarily fully align - RDF graphs of OWL ontologies
    employ numerous blank nodes that obscure the ontology structure. See :term:`Ontology Graph Projection`.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Edge
    See :term:`Relationship`

   Relationship
    A :term:`Relationship` is a type connection between two ontology elements. The first element is called the :term:`Subject`,
    and the second one the :term:`Object`, with the type of connection being the :term:`Predicate`.
    Sometimes Relationships are equated with :term:`Triples<Triple>` in :term:`RDF` but this can be confusing, because some relationships
    map to *multiple* triples when following the OWL RDF serialization. An example is the relationship "finger part-of hand",
    which in OWL is represented using a :term:`Existential Restriction` that maps to 4 triples.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Triple
    The term "triple" is generally only used in the context of the :term:`RDF` data model. A triple is a
    simple statement consisting of a :term:`Subject`, :term:`Predicate`, and :term:`Object`.
    The concept of triple is closely related to, but not identical to, the concept of :term:`Relationship`.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Node
    A :term:`Node` (aka Vertex) is one of the two main elements that make up a :term:`Graph`.
    The other element is an :term:`Edge`. The nodes in a graph typically represent :term:`Classes<Class>`
    but this depends on the :term:`Ontology Graph Projection`. The nodes of a graph might also
    be :term:`Instances<Named Individual>` or :term:`Relationship Types<Predicate>`, or metadata
    elements such as :term:`Subset` definitions.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Subject
    The subject of a :term:`Relationship` or :term:`Association` is the first element.
    The subject is always a :term:`Node`.
    Note that the same node can be the Subject of one edge, and the :term:`Object` of another edge.
    For example, the node for "Scoliosis" in the Human Phenotype Ontology is the subject of the SubClassOf
    edge whose object is "Abnormality of the vertebral column"; it may also be the object of
    a gene-phenotype association edge.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Object
    The term "Object" is highly overloaded. In a general programming context,
    it refers to an instance of a (programmatic) class. But typically in the OAK
    context, it refers to the second element in a :term:`Relationship` or :term:`Association`.
    It is the counterpart to :term:`Subject`.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Relationship Type
    See :term:`Predicate`

   Predicate
    An :term:`Ontology element` that represents the type of a :term:`Relationship`.
    Typically corresponds to an :term:`ObjectProperty` in :term:`OWL`, but this is not always true;
    in particular, the :term:`is-a` relationship type is a builtin construct ``SubClassOf`` in OWL
    Examples:
     * :term:`IS_A` (rdfs:subClassOf)
     * :term:`Part Of` (BFO:0000050)

    - See also :ref:`relationships_and_graphs` in the Guide.

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
    parameterized by a set of :term:`Predicates<Predicate>`. The concept of :term:`Ancestor` and
    graph traversal is closely related to the concept of :term:`Entailment<Entailed Axiom>` in :term:`OWL`.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Descendant
    The converse of :term:`Ancestor`.

   Closure
    In the context of ontologies and OAK "closure" refers to the closure of a predicate, i.e. the
    :term:`Ancestor` of all entities that are reachable by following the predicate or predicates.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Subject Closure
    The :term:`Subject Closure` of an edge is the set of all entities that are reachable by following
    the :term:`Subject` of the edge or association, over a specified set of predicates
    (called the :term:`Subject Closure Predicates`).
    For example, in a disease
    phenotype association, if the disease is "Mucopolysaccharidosis type I", then the subject closure would
    include "Mucopolysaccharidosis", "Lysosomal Storage Disease", "Disease". In cases where the subject
    is a database entity rather than an ontology term, the subject closure may trivially be a singleton
    containing only the subject.

    - See also :ref:`relationships_and_graphs` in the Guide.
    - See also :ref:`associations` in the Guide.

   Object Closure
    The :term:`Object Closure` of an edge is the set of all entities that are reachable by following
    the :term:`Object` of the edge or association, over a specified set of predicates
    (called the :term:`Object Closure Predicates`).
    For example, in a disease
    to phenotype association, if the phenotype is "Abnormality of the vertebral column", then the object closure would
    include "Abnormality of the vertebral column", "Abnormality of the musculoskeletal system", etc.

    - See also :ref:`relationships_and_graphs` in the Guide.
    - See also :ref:`associations` in the Guide.

   MRCA
    The :term:`Most Recent Common Ancestor<MRCA>` of a set of entities is the most specific entity that
    is an ancestor of all entities in the set. See :ref:`relationships_and_graphs`

   Ontology Graph Projection
    The mapping between an ontology as represented in some formalism such as :term:`OWL` ontology onto a :term:`Graph`.
    This is a non-trivial process, because OWL ontologies are not natively represented as graphs, instead they are
    represented as collections of :term:`Axioms<Axiom>`.
    The most common projection is the :term:`RDF` mapping, but this results in a structure that is
    not well suited to graph operations due to the use of :term:`Blank Nodes` to represent OWL
    expressions.
    OAK makes use of a simple projection where common constructs such as OWL existential axioms are mapped
    to :term:`Edges<Edge>`, similar to :term:`Relation Graph`. OAK also projects some axiom types that are
    not yet projected in relation graph, such as those between individuals.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Relation Graph
    Relation Graph is both a tool and a :term:`Ontology Graph Projection`.
    Relation Graph is used behind the scenes in both :term:`Ubergraph` and in :term:`Semantic SQL`.
    For the tool, see `INCATools/relation-graph <https://github.com/INCATools/relation-graph>`_.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Ontology Format
    A syntax for serializing an :term:`Ontology` as text. Examples include :term:`OWL Functional Syntax`,
    various :term:`RDF` formats such as :term:`Turtle`, or :term:`OBO Format`.
    In OAK we take a broad view of the term "Ontology", and also include things
    such as RDF serializations of :term:`SKOS`.

    - See also :ref:`basics` in the Guide.
    - See also `OWL Formats <https://oboacademy.github.io/obook/explanation/owl-format-variants/>`_ in the OBook.

   OWL
    An ontology language that uses constructs from :term:`Description Logic`. OWL is not itself an ontology format, it can be serialized
    through different :term:`Ontology Formats<Ontology Format>` such as :term:`Functional Syntax`, and it can be mapped to :term:`RDF` and serialized via an RDF format.

    - See also `OWL Formats <https://oboacademy.github.io/obook/explanation/owl-format-variants/>`_ in the OBook.

   RDF
    A :term:`Datamodel` consisting of simple :term:`Subject` :term:`Predicate` :term:`Object` :term:`Triples` organized into an RDF :term:`Graph`

    - See also `OWL Formats <https://oboacademy.github.io/obook/explanation/owl-format-variants/>`_ in the OBook.

   FunOWL
    FunOWL is a Python :term:`Ontology Library` that provides a simple API for working with OWL ontologies
    conceptualized using the native OWL :term:`OWL Functional Syntax` representation.

    - See `<https://github.com/Harold-Solbrig/FunOWL>`_

   Functional Syntax
    A syntax / :term:`Ontology Format` that directly expresses the :term:`OWL` data model.

    - See also `OWL Formats <https://oboacademy.github.io/obook/explanation/owl-format-variants/>`_ in the OBook.

   OBO Format
    An :term:`Ontology Format` designed for easy viewing, direct editing, and readable diffs. It is popular in bioinformatics,
    but not widely used or known outside the genomics sphere. OBO is mapped to OWL, but only expresses a subset, and provides some OWL
    abstractions in a more easy to understand fashion.

    - See: `<https://owlcollab.github.io/oboformat/doc/obo-syntax.html>`_
    - See also `OWL Formats <https://oboacademy.github.io/obook/explanation/owl-format-variants/>`_ in the OBook.

   Pronto
    An :term:`Ontology Library` for parsing :term:`OBO Format` with some support for :term:`OWL` files.
    OAK provides a wrapper around Pronto via the :ref:`pronto_implementation`.

    - See: `<https://github.com/althonos/pronto>`_

   OBO Graphs
    A JSON-based serialization :term:`Ontology Format` and also a :term:`Datamodel` for representing :term:`Ontology Graphs<Ontology Graph>`.
    OBO Graphs are designed to be an abstraction that is more suited to data science tasks than
    :term:`OWL` or :term:`RDF`, and utilizes a different :term:`Ontology Graph Projection` than RDF.

   Input Selector
    A syntax that provides a shorthand for selecting an :term:`Adapter` to communicate with an ontology. These may
    be command line based or for a remote endpoint. The syntax is typically ``<selector>:<path>``
    but if a path is specified, a default adapter will be used.

    - See :ref:`selectors`.

   OWL Annotation
    In the context of :term:`OWL`, the term :term:`Annotation` means a piece of metadata that does not have a strict logical
    interpretation. Annotations can be on entities, for example, :term:`Label` annotations, or annotations can be on :term:`Axioms<Axiom>`.

    - See `Section 8.1 in the OWL primer <https://www.w3.org/TR/owl2-primer/#Annotating_Axioms_and_Entities>`_

   Named Individual
    An :term:`Ontology Element` that represents an instance of a class. For example, the instance "John" or "John's heart".
    Note that instances are not commonly directly represented in bio-ontologies, but may be more common
    in other domains.

    - See `Section 4.1 in the OWL primer <https://www.w3.org/TR/owl2-primer/#Classes_and_Instances>`_

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

    - See `Section 4.4 in the OWL primer <https://www.w3.org/TR/owl2-primer/#Object_Properties>`_

   AnnotationProperty
    In OWL, an :term:`AnnotationProperty` is a :term:`Property` that connects an :term:`Ontology Element` to
    another element for the purposes of assigning metadata. Annotation Properties are "logically
    silent". In OAK interfaces, we typically use the term :term:`Metadata` property when
    referring to annotation properties.

   DatatypeProperty
    In OWL, a :term:`DatatypeProperty` is a :term:`Property` that connects an :term:`Ontology Element` to
    a :term:`Literal`. Datatype properties are not widely used in most bio-ontologies,
    and currently OAK has limited support for working with them.

   Definition
    The term "definition" usually means a textual definition that provides clear, operational, necessary and sufficient
    conditions for a :term:`Term`. A :term:`Logical Definition` refers to a definition that is written in some
    formal computable language such as FOL or :term:`OWL`.

   Logical Definition
    A :term:`Logical Definition` is a particular kind of :term:`Axiom` that is used to provide a
    definition of a term that is *computable*.

    - See :ref:`logical_definitions`.

   Subset
    An :term:`Ontology Element` that represents a named collection of elements, typically grouped for some purpose.
    Subsets are commonly used in ontologies like the :term:`Gene Ontology`.

   Reasoner
    An ontology tool that will perform inference over an ontology to yield new *axioms* (e.g. new :term:`Edges<Edge>`) or
    to determine if an ontology is logically :term:`Coherent`.

    - See `Reasoning <https://oboacademy.github.io/obook/reference/reasoning/>`_ in the OBook.
    - See also :ref:`relationships_and_graphs` in the Guide.

   Reasoning
    See :term:`Reasoner` and :term:`Entailed`

   Bioportal
    An :term:`Ontology Repository` that is a comprehensive collection of multiple biologically relevant ontologies.
    Bioportal exposes an :term:`API` endpoint, that is utilized by the OAK :ref:`bioportal_implementation`.

    - See `<https://bioportal.bioontology.org/>`_
    - See :ref:`bioportal_implementation`.

   OntoPortal
    A framework for :term:`Ontology Repositories<Ontology Repository>` that is used by :term:`Bioportal`,
    as well as AgroPortal, EcoPortal, etc.
    - See :ref:`bioportal_implementation`.

   Asserted
    An :term:`Axiom` or :term:`Edge` that is directly asserted in an ontology,
    as opposed to being :term:`Entailed`. Note that asserted edges or axioms usually
    correspond to :term:`Direct` (one-hop) edges, but this isn't always the case.

    - See `Reasoning <https://oboacademy.github.io/obook/reference/reasoning/>`_ in the OBook.

   Entailed
    An :term:`Axiom` or :term:`Edge` that is is inferred by a :term:`Reasoner`.
    Note that all asserted edges or axioms are also entailed. Note also that sometimes
    entailed axioms can include trivial :term:`Tautologies<Tautology>`.

    - See `Reasoning <https://oboacademy.github.io/obook/reference/reasoning/>`_ in the OBook.
    - See also :ref:`relationships_and_graphs` in the Guide.

   Graph Traversal
    A strategy for walking :term:`graphs<Graph>`, such as from a start node to all
    ancestors or descendants. In some cases, graph traversal can be used in place of
    :term:`Reasoning`. See the section on :ref:`relationships_and_graphs` in the OAK guide.

    - See also :ref:`relationships_and_graphs` in the Guide.

   Reflexive
    A :term:`Edge` or :term:`Axiom` that connects an :term:`Ontology Element` to itself.
    These are trivially true (:term:`Tautology`), but in general these are included by
    default in operations involving :term:`Reasoning` and :term:`Graph Traversal`.
    See also the `RO guide to reflexivity<https://oborel.github.io/obo-relations/reflexivity/>`_.

   Tautology
    A :term:`Axiom` or :term:`Edge` that is trivially true.

   OLS
    Ontology Lookup Service. An :term:`Ontology Repository` that is a curated collection of multiple biologically relevant ontologies,
    many from :term:`OBO`.
    OLS exposes an :term:`API` endpoint, that is utilized by the OAK OLS :term:`Implementation`

    - See `<https://www.ebi.ac.uk/ols/index>`_
    - See :ref:`ols_implementation`.

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

    - See `<https://github.com/INCATools/ubergraph>`_
    - See :ref:`ubergraph_implementation`.

   Ontobee
    A :term:`Triplestore` and a :term:`Ontology Repository` that allows for :term:`SPARQL` querying of integrated :term:`OBO` ontologies.
    Accessible via :ref:`ontobee_implementation`.

    - See `<http://www.ontobee.org/>`_
    - See :ref:`ontobee_implementation`.

   Semantic SQL
    Semantic SQL is a proposed standardized schema for representing any RDF/OWL ontology, plus a set of tools for building
    a database conforming to this schema from RDF/OWL files.

    - See `Semantic-SQL <https://github.com/INCATools/semantic-sql>`_

   SKOS
    Simple Knowledge Organization System (SKOS) is a lightweight vocabulary and data model for representing
    terminologies and ontologies. It has some high level similarities to :term:`OWL`, in that it organizes
    knowledge using units such as :term:`Concepts<Concept>`, together with relationships between them, but
    there are a number of differences and the systems are partly complementary.
    In the bio-ontology community and many other communities, OWL is
    predominantly used, but OWL ontologies are frequently augmented with SKOS in order to represent things
    like mappings and term metadata.

   Gene Ontology
    Aka GO. A widely used ontology for bioinformatics and molecular biology. Many of the ontologies in :term:`OBO` have
    adopted many of the conventions of the GO.

   Diff
    A representation of an individual difference between two :term:`Ontologies<Ontology>`.

    - See :ref:`differ_interface`.

   Patch
    A representation of a set of :term:`Diffs<Diff>` that are intended to be applied.

    - See :ref:`patcher_interface`.

   KGCL
    Knowledge Graph Change Language (KGCL) is a :term:`Datamodel` for communicating desired changes (aka :term:`Patch`) to an ontology.
    It can also be used to communicate :term:`Diffs<Diff>` between two ontologies. See `KGCL docs <https://github.com/INCATools/kgcl>`_.

    - See :ref:`patcher_interface`.

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

    - See :ref:`interfaces`.

   Implementation
    Also known as :term:`Adapter`. Typically the details of implementation should not
    be exposed, and developers of applications that use OAK should always :term:`Code to the Interface`.
    For example, the method to query for all :term:`Relationships<Relationship>` from a term should
    have the same meaning regardless of whether the adapter *implementing* the interface is a remote
    triplestore like :term:`Ubergraph`, a :term:`Semantic SQL` adapter, or a local :term:`OBO Graphs` file.
    See the list of :ref:`all implementations<implementations>`

    - See :ref:`implementations`.

   Datamodel
    Aka schema. OAK follows a pluralistic worldview, and includes many different
    datamodels for different purposes. Examples include:
     - The :term:`KGCL` data model, for representing :term:`Diffs<Diff>`
     - The :term:`OBO Graphs` data model, for representing ontologies through simple :term:`Ontology Graph Projections<Ontology Graph Projection>`
     - A data model for representing :term:`Text Annotation` results
     - The :term:`SSSOM` data model, for representing :term:`Mappings<Mapping>`
     - A data model for representing :term:`Semantic Similarity` results

    - See :ref:`datamodels`.

   OntoGPT
    A framework built on OAK that combines ontologies and Large Language Models.

    - See `<https://github.com/monarch-initiative/ontogpt/>`_
