Part 3: Triplestore Backends
=======

Previously we have been working with *local* ontology files in :term:`OBO Format`. We will now show how OAK
can be used to access information in a local or remote :term:`Triplestore`.

Triplestore Concepts
-------------------

There are a number of triplestores that include ontology content queryable using :term:`SPARQL`.

OAK includes built in support for a number of triplestores, including:

- :term:`Ubergraph`, an enriched triplestore containing a core set of biological ontologies
- :term:`Ontobee`, a triplestore including all :term:`OBO Foundry` ontologies
- :term:`Wikidata`, a triplestore containing a broad set of knowledge encodes as triples
- :term:`LOV`, (Linked Open Vocabularies), a triplestore containing generic semantic web ontologies and ontology-like schemas

Additionally, **OAK is capable of treating any local RDF file on disk as if it were a triplestore**

All triplestores are standardized in that they all conform to the SPARQL standard. However, triplestores differ in
how they store ontologies, and different ontologies conform to different metadata standards. This means it can be challenging
writing code with uniform behavior across different triplestores. OAK attempts to bridge these differences as far as possible

Ubergraph
--------

See:

- :ref:`ubergraph_implementation`

Connecting
^^^^^^^^^^

.. code-block:: python

    from oaklib.implementations import UbergraphImplementation

    oi = UbergraphImplementation()



Operations
^^^^^^^^^^

.. code-block:: python

    term_id = "UBERON:0002544"
    print(oi.get_label_by_curie(term_id))

Will write out "digit"

    for rel in oi.entailed_outgoing_relationships_by_curie(term_id):
       print(rel)

