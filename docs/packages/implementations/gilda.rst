.. _gilda_implementation:

Gilda Adapter
=============

Command Line Examples
----------------------

Use the :code:`gilda` selector:

.. code:: shell

    $ runoak -i gilda: COMMAND [COMMAND-ARGUMENTS-AND-OPTIONS]

Currently ontology sub-selectors are not supported

Annotation
^^^^^^^^^^
.. code:: shell

   $ runoak -i gilda: annotate -W "cell cortex"

Code
----
.. currentmodule:: oaklib.implementations.gilda

.. autoclass:: GildaImplementation
