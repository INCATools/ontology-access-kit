.. _interfaces:

Interfaces
===============

oaklib provides a variety of *interfaces* that abstract away from
implementation details and provide a coherent set of operations to
perform on an ontology. Developers can code to the interface largely without
worrying about whether the implementation is a relational database, a local
file, etc.

For example, the :ref:`ubergraph_implementation` implements :ref:`search_interface` which
has the method :meth:`oaklib.interfaces.search_interface.SearchInterface.basic_search`, so you can write code like this:

.. code:: python

    >>> from oaklib.implementations import UbergraphImplementation
    >>> adapter = UbergraphImplementation()
    >>> for r in adapter.basic_search('CA4 hippocampus'):
    ...     print(r)


The most common operations are found in the :ref:`basic_ontology_interface`


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   basic
   search
   subsetting
   validator
   relation-graph
   mapping-provider
   obograph
   text-annotator
   owl
   summary-statistics
   differ
   patcher
   semantic-similarity
   class-enrichment
   
.. note::

    Some interfaces may not be "pure" interfaces is that they may provide
    a default implementation, which may or may not be overridden by an
    implementation
