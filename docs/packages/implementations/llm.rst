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

Validation of Mappings
^^^^^^^^^^^^^^^^^^^^^^

.. code:: shell

   runoak -i llm:sqlite:obo:go validate-mappings .desc//p=i "molecular_function"

See:

 - `MapperGPT <https://arxiv.org/abs/2310.03666>`_
 - `GO RHEA Analysis <https://github.com/cmungall/rhea-go-llm-analysis>`_

Code
----
.. currentmodule:: oaklib.implementations.llm.llm_implementation

.. autoclass:: LLMImplementation
