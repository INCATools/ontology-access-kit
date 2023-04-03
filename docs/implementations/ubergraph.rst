.. _ubergraph_implementation:

Ubergraph Adapter
=================

About
-----

`Ubergraph <https://github.com/INCATools/ubergraph>`_ is a SPARQL
endpoint serving multiple OBO ontologies, pre-processed with

- relation-graph
- information content scores
- biolink categories

This implementation is a specialization of the :ref:`sparql` interface, tuned for Ubergraph

.. note::

    This is a remote endpoint implementation - as such, throttling is implemented
    to limit overuse

Interfaces Implemented
----------------------

This implements most interfaces. It also attempts to implement each in the most performant way, avoiding
iterative queries, attempting instead to batch queries into larger SPARQL query

Connecting
^^^^^^

Use ``ubergraph:`` as a selector.

To restrict queries to a particular ontology, use the ontology ID as a suffix, e.g. ``ubergraph:uberon``

Search
^^^^^^

.. code::

   runoak -i ubergraph: search hippocampus

Code
----

.. currentmodule:: oaklib.implementations.ubergraph.ubergraph_implementation
                   
.. autoclass:: UbergraphImplementation

.. autoclass:: RelationGraphEnum

              
