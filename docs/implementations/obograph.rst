.. obograph_implementation:

OBO Graph Adapter
=================

About
-----

This is an alternative to :ref:`pronto_implementation` for loading OBO Graph JSON files.

Initialization
--------------

To ensure use of this implementation when specifying a :ref:`selector`, use the :code:`obograph` scheme:

.. code ::

    runoak -i obograph:path/to/file.json COMMAND [COMMAND-OPTIONS]

Code
----

.. currentmodule:: oaklib.implementations.obograph.obograph_implementation
                   
.. autoclass:: OboGraphImplementation
