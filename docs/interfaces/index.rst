.. _interfaces:

Interfaces
===============

oaklib provides a variety of *interfaces* that abstract away from
implementation details and provide a coherent set of operations to
perform on an ontology. Developers can code to the interface largely without
worrying about whether the implementation is a relational database, a local
file, etc.

The most common operations are found in the :ref:`BasicOntologyInterface`

See also :ref:`BasicOntologyInterface`

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   basic
   search
   subsetting
   relation-graph
   mapping-provider
   obograph
   owl
   summary-statistics
   rdf
   skos
   validator
   semsim
   differ
   patcher
   
.. note::

    Some interfaces may not be "pure" interfaces is that they may provide
    a default implementation, which may or may not be overridden by an
    implementation