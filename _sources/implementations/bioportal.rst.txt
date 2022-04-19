Bioportal Endpoint
==================

.. warning ::

   Highly incomplete!

So far this only implements:

- :ref:`SearchInterface`
- :ref:`TextAnnotatorInterface`
- :ref:`MappingProviderInterface`

Command Line Examples
----------------------

Use the :code:`bioportal` selector:

.. code::

    runoak -i bioportal: COMMAND [COMMAND-ARGUMENTS-AND-OPTIONS]

Currently ontology sub-selectors are not supported

Search
^^^^^^

.. code::

   runoak -i bioportal: search tentacle

Note that bioportal implements relevance-ranked search, so if you search with a multiword term like "octopus brain",
after first returning any exact matches it will return matches to "octopus" and "brain".

Mappings
^^^^^^^^

.. code::

   runoak -i bioportal: term-mappings UBERON:0002101  -O sssom -o my-mappings.sssom.tsv

Currently mappings may be missing some crucial metadata

Code
----

.. currentmodule:: oaklib.implementations.bioportal.bioportal_implementation
                   
.. autoclass:: BioportalImplementation
