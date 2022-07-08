.. _gilda_implementation:

Gilda Endpoint
==============
Command Line Examples
----------------------
Use the :code:`gilda` selector:

.. code:: shell

    $ runoak -i gilda: COMMAND [COMMAND-ARGUMENTS-AND-OPTIONS]

Currently ontology sub-selectors are not supported

Search
^^^^^^
.. code:: shell

   $ runoak -i gilda: search tentacle

Code
----
.. currentmodule:: oaklib.implementations.gilda

.. autoclass:: GildaImplementation
