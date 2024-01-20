.. _simple_obo_implementation:

Simple OBO Adapter
==================

About
-----

This is an alternative to :ref:`pronto_implementation` for loading OBO Format files

Initialization
--------------

To ensure use of simpleobo when specifying a :ref:`selector`, use the :code:`simpleobo` scheme:

.. code ::

    runoak -i simpleobo:path/to/file.obo COMMAND [COMMAND-OPTIONS]

Code
----

.. currentmodule:: oaklib.implementations.simpleobo.simple_obo_implementation
                   
.. autoclass:: SimpleOboImplementation
