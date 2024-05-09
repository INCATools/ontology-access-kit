.. _pantherdb_implementation:

PantherDB Adapter
=============

Command Line Examples
----------------------

Use the :code:`pantherdb` selector, with an optional NCBI Taxon local ID.

Annotation
^^^^^^^^^^

.. code:: shell

    runoak -i pantherdb:9606 associations -Q subject UniProtKB:P04217 --no-autolabel

Enrichment
^^^^^^^^^^

.. code:: shell

   runoak -i pantherdb:9606 enrichment -U my-gene-ids.txt

Mapping
^^^^^^^^^^

.. code:: shell

   runoak -i pantherdb:9606 mappings UniProtKB:P04217

Code
----
.. currentmodule:: oaklib.implementations.pantherdb.pantherdb_implementation

.. autoclass:: PantherDBImplementation
