.. _relationships_and_graphs:

Relationships and Graphs
========================

One of the main uses of an ontology is to precisely state the *relationships* between different entities or concepts.

In OAK, classes in ontologies can be related to one another via different *relationship types*. These
may come from a relationship type ontology such as RO, or they may be part of the RDF/OWL framework, such
as :ref:`SubClassOf`.

Exploring relationships
------------------------

Let's explore Uberon, looking at the relationships for *hand* ("manus") and *foot* ("pes")

We will use the ``relationships`` method from :ref:`basic_ontology_interface`.

.. code-block:: python

    >>> from oaklib.selector import get_implementation_from_shorthand
    >>> adapter = get_implementation_from_shorthand("sqlite:obo:uberon")
    >>> for rel in adapter.relationships(["UBERON:0002398", "UBERON:0002387"]):
    ...    print(rel)
    ('UBERON:0002387', 'BFO:0000050', 'UBERON:0002103')
    ('UBERON:0002387', 'RO:0002202', 'UBERON:0006871')
    ('UBERON:0002387', 'RO:0002551', 'UBERON:0001445')
    ('UBERON:0002387', 'rdfs:subClassOf', 'UBERON:0002470')
    ('UBERON:0002387', 'rdfs:subClassOf', 'UBERON:0008784')
    ('UBERON:0002398', 'BFO:0000050', 'UBERON:0002102')
    ('UBERON:0002398', 'RO:0002202', 'UBERON:0006875')
    ('UBERON:0002398', 'RO:0002551', 'UBERON:0001442')
    ('UBERON:0002398', 'rdfs:subClassOf', 'UBERON:0002470')
    ('UBERON:0002398', 'rdfs:subClassOf', 'UBERON:0008785')

We can make this more human readable:

.. code-block:: python

    >>> from oaklib.selector import get_implementation_from_shorthand
    >>> adapter = get_implementation_from_shorthand("sqlite:obo:uberon")
    >>> for s, p, o in adapter.relationships(["UBERON:0002398", "UBERON:0002387"]):
    ...    print((adapter.label(s), adapter.label(p), adapter.label(o)))
    ('pes', 'part of', 'hindlimb')
    ('pes', 'develops from', 'embryonic footplate')
    ('pes', 'has skeleton', 'skeleton of pes')
    ('pes', None, 'autopod region')
    ('pes', None, 'lower limb segment')
    ('manus', 'part of', 'forelimb')
    ('manus', 'develops from', 'embryonic handplate')
    ('manus', 'has skeleton', 'skeleton of manus')
    ('manus', None, 'autopod region')
    ('manus', None, 'upper limb segment')

(note subClassOf labels are outside the ontology so they have no labels)

.. note ::

    if you are used to working with OWL and the underlying RDF/OWL representation
    the presentation as simple triads above can be confusing, as these are not actually
    modeled as triples in the ontology, but rather as more complex axioms involving
    constructs like existential restriction. We will return to this later.

Graph Traversal and Relation Graph Reasoning
--------------------------------------------

The above examples show *direct* relationships between concepts. A common
use case for ontologies is exploring *indirect* or *entailed* relationships.

We will use the ``ancestors`` method from :ref:`basic_ontology_interface`.

.. code-block:: python

    >>> from oaklib.selector import get_implementation_from_shorthand
    >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
    >>> adapter = get_implementation_from_shorthand("sqlite:obo:uberon")
    >>> for anc in adapter.ancestors("UBERON:0002398", predicates=[IS_A, PART_OF]):
    ...    print(f"{anc} '{adapter.label(anc)}'")
    BFO:0000001 'entity'
    BFO:0000002 'continuant'
    BFO:0000004 'independent continuant'
    BFO:0000040 'material entity'
    CARO:0000000 'anatomical entity'
    CARO:0000003 'None'
    CARO:0030000 'biological entity'
    RO:0002577 'system'
    UBERON:0000026 'appendage'
    UBERON:0000061 'anatomical structure'
    UBERON:0000153 'anterior region of body'
    UBERON:0000465 'material anatomical entity'
    UBERON:0000468 'multicellular organism'
    UBERON:0000475 'organism subdivision'
    UBERON:0001062 'anatomical entity'
    UBERON:0002101 'limb'
    UBERON:0002102 'forelimb'
    UBERON:0004708 'paired limb/fin'
    UBERON:0004710 'pectoral appendage'
    UBERON:0010000 'multicellular anatomical structure'
    UBERON:0010707 'appendage girdle complex'
    UBERON:0010708 'pectoral complex'
    UBERON:0015212 'lateral structure'
    UBERON:0002398 'manus'
    UBERON:0002470 'autopod region'
    UBERON:0002529 'limb segment'
    UBERON:0008785 'upper limb segment'
    UBERON:0010538 'paired limb/fin segment'
    UBERON:0010758 'subdivision of organism along appendicular axis'

Graph Traversal Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~

There are actually *two* strategies for getting indirect relationships in OAK:

- HOP, aka *graph walking*
- ENTAILMENT, aka *reasoning*

You can specify which you would like, but if you leave this open the adapter will choose a
default. Not all adapters can implement both strategies.

What are the differences? In many cases the results are the same, but formally the differences are:

- HOP yields all nodes that can be traversed via zero or more hops from the specified starting point(s),
  over the specified relationships
- ENTAILMENT uses deductive reasoning to compute inferred relationships, and yields any relationships
  whose entailed predicate matches the input list

Currently the only OAK adapters to implement ENTAILMENT are:

- :ref:`ubergraph_implementation`
- :ref:`sql_implementation`

In both cases the entailment is done ahead of time using :ref:`relation_graph`.

An example of a case where results between these approaches differ is in computing
the ancestors of ``GO:1901494`` *regulation of cysteine metabolic process*.

Following a path of two hops, we can traverse over a *regulates* relationship to get to *cysteine metabolic process*,
and then over a *has primary input ot output* relationship to the CHEBI concept for *cysteine*

the Relation Ontology doesn't include a property chain naming the relationship between
GO:1901494 and cysteine, so this wouldn't show up in an ancestor lookup for the GO term.

entailment can also yield *new* relationship types. For example, RO contains
an axiom that if A has-part B and B part-of C, then it necessarily follows that A overlaps C.

