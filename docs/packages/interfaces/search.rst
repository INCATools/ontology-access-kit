.. _search_interface:

Search Interface
================

The search interface provides a largely implementation-neutral way to query an ontology. It allows for

- exact or partial matches
- matching the beginning of a term
- regular expression search

It also allows you to control which metadata elements are searched over (typically labels and aliases)

Implementations may differ in their behavior. Some implementations may not be able to honor specific requests.
For example, the :ref:`SqlDatabaseImplementation` implementation may not be able to fulfil regular expression queries.

Some endpoints may return results that are ranked by relevance, others may be arbitrary

Command Line
------------

A good way to explore this interface is via the search subcommand:

Ubergraph uses relevancy ranking:

.. code::

    runoak -i ubergraph:uberon search limb

Exact match for a label using sqlite:

.. code::

    poetry run runoak -i db/cl.db search l=neuron

Inexact match for a label or synonym using sqlite:

.. code::

    poetry run runoak -i db/cl.db search .~neuron

Datamodels
----------

Search uses the :ref:`SearchDatamodel` to specify both an input query and search results, see :ref:`datamodels`

Code
----


.. currentmodule:: oaklib.interfaces.search_interface
                   
.. autoclass:: SearchInterface
    :members:

.. autoclass:: SearchConfiguration
    :members:

.. currentmodule:: oaklib.datamodels.search_datamodel
    :members:

.. autosummary::
   :toctree: src

   search


