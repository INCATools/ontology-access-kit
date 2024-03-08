How to use Large Language Models (LLMs) with OAK
===============================================

Large Language Models (LLMs) such as ChatGPT have powerful text pattern matching and processing abilities,
and general question answering capabilities. LLMs can be used in conjunction with ontologies for a number
of tasks, including:

- Summarizing lists of ontology terms and other OAK outputs
- Annotating text using ontology terms
- Reviewing ontology branches or different kinds of ontology axioms

This guide is in 3 sections:

- Summary of ontology-LLM tools that directly leverage OAK, but are not part of the OAK framework
- How to use OAK in conjunction with existing generic LLM tools
- The OAK LLM implementation

LLM frameworks that use OAK
---------------------------

OntoGPT
~~~~~~~

`OntoGPT <https://github.com/monarch-initiative/ontogpt>`_ extracts knowledge from text according
to a LinkML schema and LinkML dynamic value set specifications. OAK is used for grounding ontology terms.

CurateGPT
~~~~~~~~~

`CurateGPT <https://github.com/monarch-initiative/curate-gpt>`_ is a general purpose knowledge management
and editing tool that uses LLMs for enhanced search and autosuggestions.

Talisman
~~~~~~~~

`Talisman <https://github.com/monarch-initiative/talisma>`_ allows for an LLM analog of the
OAK `enrichment` command. It summarizes collections of terms or descriptions of genes.

Using OAK in conjunction with existing LLM tools
------------------------------------------------

LLMs such as ChatGPT can take any kind of textual output, including outputs of OAK.

For example, you could query all T-cell types:

.. code-block:: bash

    runoak -i sqlite:obo:cl labels .descendant//p=i "T cell"

And then copy the results into the ChatGPT window and ask "give me detailed descriptions of these T-cell types".

This kind of workflow is not very automatable. OAK is designed in part for the Command Line, so
LLM CLI tools such as the datasette ``llm`` tool pair naturally

.. code-block:: bash

    pipx install llm
    runoak -i sqlite:obo:cl labels .descendant//p=i "T cell" | llm --system "summarize the following terms"

OAK LLM Adapter
---------------

OAK provides a number of different adapters (implementations) for each of its interfaces.
Some adapters provide direct access to an ontology or collection of ontologies; others act as *wrappers*
onto another adapter, and inject additional functionality.

The OAK LLM adapter is one such adapter. It provides a number of implementations of a subset of OAK
commands and interfaces.

See :ref:`llm_implementation` for details on the OAK LLM adapter.

The basic idea is that you can prefix any existing adapter with ``llm:``; for example:

.. code-block:: bash

    runoak -i llm:my-ont.json ...

If can specify the model which you wish to use within `{}`s, for example:

.. code-block:: bash

    runoak -i llm:{litellm-groq-mixtral}:sqlite:obo:cl ...

We recommend the LiteLLM package to allow for access of a broad range of models through a proxy.

Examples are provided here on the command line, but this can also be done programmatically.

.. code-block:: python

    from oaklib import get_adapter
    adapter = get_adapter("llm:sqlite:obo:cl")

Note that the output of LLMs is non-deterministic and unpredictable, so the LLM adapter should
not be used for tasks where precision is required.

Annotation
~~~~~~~~~~

.. code-block:: bash

    runoak -i llm:sqlite:obo:hp annotate "abnormalities were found in the eye and the liver"

Suggesting Definitions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    runoak -i llm:sqlite:obo:uberon generate-definitions \
         finger toe \
         --style-hints "write definitions in formal genus-differentia form"

Validating Mappings
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    runoak --stacktrace -i llm:{gpt-4}:sqlite:obo:go validate-mappings \
       .desc//p=i molecular_function -o out.jsonl -O jsonl