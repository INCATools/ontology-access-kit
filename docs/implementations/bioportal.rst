.. _bioportal_implementation:

Bioportal Adapter
==================

The Bioportal adapter uses `ontoportal-client <https://github.com/cthoyt/ontoportal-client>`_ to connect to
any OntoPortal endpoint.

.. warning ::

   Highly incomplete!

So far this only implements:

- :ref:`search_interface`
- :ref:`text_annotator_interface`
- :ref:`mapping_provider_interface`

API Keys
--------------------

First you will need to go to `BioPortal <https://bioportal.bioontology.org/>`_ and get an API key, if you don't already have one.

You will then need to set it:

.. code-block::

    runoak set-apikey bioportal YOUR-API-KEY

This stores it in an OS-dependent folder

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
