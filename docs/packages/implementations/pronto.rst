.. _pronto_implementation:

Pronto / OBO Files Adapter
==========================

About
-----


Initialization
--------------

Pronto will automatically be used for obo format files and obo json files. Currently it will also be
used for RDF/XML files but this is not guaranteed in future.

To ensure use of pronto when specifying a :ref:`selector`, use the :code:`pronto` schema:

.. code ::

    runoak -i pronto:path/to/file.obo COMMAND [COMMAND-OPTIONS]

Code
----

.. currentmodule:: oaklib.implementations.pronto.pronto_implementation
                   
.. autoclass:: ProntoImplementation
