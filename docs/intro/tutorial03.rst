Part 3: Triplestore Backends
=======

Previously we have been working with *local* ontology files in sqlite format, following the :term:`Semantic SQL` schema.
We will now show how OAK can be used to access information in a remote :term:`Triplestore`. The same approach can be used to
query local files in any :term:`RDF` format such as :term:`Turtle`.

Triplestore Concepts
-------------------

There are a number of triplestores that include ontology content queryable using :term:`SPARQL`.

OAK includes built in support for a number of triplestores, including:

- :term:`Ubergraph`, an enriched triplestore containing a core set of biological ontologies
- :term:`Ontobee`, a triplestore including all :term:`OBO Foundry` ontologies
- :term:`Wikidata`, a triplestore containing a broad set of knowledge encodes as triples
- :term:`LOV`, (Linked Open Vocabularies), a triplestore containing generic semantic web ontologies and ontology-like schemas

Additionally, **OAK is capable of treating any local RDF file on disk as if it were a triplestore**

All triplestores are fairly standardized in that they all conform to the SPARQL standard. However, triplestores differ in
how they store ontologies, and different ontologies conform to different metadata standards. This means it can be challenging
writing code with uniform behavior across different triplestores. OAK attempts to bridge these differences as far as possible.
OAK interfaces specify the logical operation, and behind the scenes, OAK will emit the most appropriate SPARQL query.

Ubergraph
--------

For full documentation, see :ref:`ubergraph_implementation`

Connecting
^^^^^^^^^^

In this example we will use the ``ontologies()`` method for :ref:`basic_ontology_interface` to list
all ontologies the adapter knows about.

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("ubergraph:")
    >>> for ont in adapter.ontologies():
    ...     print(ont)
    <BLANKLINE>
    ...
    bspo.owl
    chebi.owl
    ...

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> term_id = "UBERON:0002544"
    >>> print(adapter.label(term_id))
    digit
    >>> print(adapter.definition(term_id))
    A subdivision of the autopod that has as part a...

Relationships
^^^^^^^^^^^^^

We can query for :term:`Asserted Relationships`:

.. code-block:: python

    >>> for rel in adapter.relationships([term_id]):
    ...    print(rel)
    <BLANKLINE>
    ...
    ('UBERON:0002544', 'RO:0002160', 'NCBITaxon:32523')
    ...
    ('UBERON:0002544', 'rdfs:subClassOf', 'UBERON:0005881')

And also for :term:`Entailed Relationships` -- this time specifying
the predicate :term:`IS_A`.

.. code-block:: python

    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> for rel in adapter.relationships([term_id], predicates=[IS_A], include_entailed=True):
    ...    print(rel)
    <BLANKLINE>
    ...
    ('UBERON:0002544', 'rdfs:subClassOf', 'UBERON:0001062')
    ...
