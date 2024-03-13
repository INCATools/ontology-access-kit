.. _llm_implementation:

LLM Adapter
=============

See also :ref:`use_llms`

Command Line Examples
----------------------

Use the :code:`llm` selector, wrapping an existing source

.. code:: shell

    runoak -i llm:sqlite:obo:cl COMMAND [COMMAND-ARGUMENTS-AND-OPTIONS]

Annotation
^^^^^^^^^^
.. code:: shell

   runoak -i llm:sqlite:obo:hp annotate "abnormalities were found in the eye and the liver"

Code
----
.. currentmodule:: oaklib.implementations.llm.llm_implementation

.. autoclass:: LLMImplementation
