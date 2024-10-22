.. _use_llms

How to use Large Language Models (LLMs) with OAK
===============================================

Large Language Models (LLMs) such as ChatGPT have powerful text pattern matching and processing abilities,
and general question answering capabilities. LLMs can be used in conjunction with ontologies for a number
of tasks, including:

- Summarizing lists of ontology terms and other OAK outputs
- Annotating text using ontology terms
- Reviewing ontology branches or different kinds of ontology axioms

For more on LLMs, see:

- `Google LLM guide <https://ai.google.dev/docs/concepts>`_

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

`Talisman <https://github.com/monarch-initiative/talisman>`_ allows for an LLM analog of the
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

See also the `LLM Notebook <https://incatools.github.io/ontology-access-kit/examples/Adapters/LLM/LLM-Tutorial.html>`_.

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

Validating Definitions
~~~~~~~~~~~~~~~~~~~~~~

The LLM adapter currently interprets ``validate-definitions`` as comparing the specified definition
against the abstracts of papers cited in the definition provenance, or by comparing the definition
against the database objects that are cited as definition provenance.

Here is an example of validating definitions for GO terms:

.. code-block:: bash

    runoak --stacktrace -i llm:sqlite:obo:go validate-definitions \
      i^GO: -o out.jsonl -O jsonl

The semsql version of GO has other ontologies merged in, so the ``i^GO:`` query only validates
against actual GO terms.

You can also pass in a configuration object.
This should conform to the `Validation Data Model <https://w3id.org/oak/validation-datamodel>`_

For example, this configuration yaml provides a specific prompt and also a URL for
documentation aimed at ontology developers.

.. code-block:: yaml

    prompt_info: Please also use the following GO guidelines
    documentation_objects:
      - https://wiki.geneontology.org/Guidelines_for_GO_textual_definitions

All specified URLs are downloaded and converted to text and included in the prompt.

The configuration yaml is passed in as follows:

.. code-block:: bash


    runoak --stacktrace  -i llm:{claude-3-opus}:sqlite:obo:go validate-definitions \
         -C src/oaklib/conf/go-definition-validation-llm-config.yaml i^GO: -O yaml

Validating Mappings
~~~~~~~~~~~~~~~~~~~

The LLM adapter validates mappings by looking up info on the mapped entity and
comparing it with the main entity.

.. code-block:: bash

    runoak --stacktrace -i llm:{gpt-4}:sqlite:obo:go validate-mappings \
       .desc//p=i molecular_function -o out.jsonl -O jsonl

Selecting alternative models
----------------------------

If you are using the :ref:`llm_implementation` then by default it will use a model such
as `gpt-4` or `gpt-4-turbo` (this may change in the future).

You can specify different models by using the `{}` syntax:

.. code-block:: bash

    runoak -i llm:{gpt-3.5-turbo}:sqlite:obo:cl generate-definitions .descendant//p=i "T cell"

We are using `Datasette LLM package <https://llm.datasette.io/en/stable/>`_ which provides a *plugin*
mechanism for adding new models. See `Plugin index <https://llm.datasette.io/en/stable/plugins/index.html>`_.

However, LLM can sometimes be slow to add new models, so here it can be useful to the awesome
`LiteLLM <https://github.com/BerriAI/litellm/>`_ package, which provides a proxy to a wide range of models.

Installing LLM plugins
~~~~~~~~~~~~~~~~~~~~~~

The ``llm`` command line tool makes it easy to access other models via its
`extensible plugin system <https://llm.datasette.io/en/stable/plugins/index.html>`_.

Normally, you would do something like this:

.. code-block:: bash

    pipx install llm
    llm install llm-gemini
    llm -m gemini-pro "what is the best ontology?"

However, this will install the plugin in a different environment from OAK. If you are running OAK
as a developer, then you can do this:

.. code-block:: bash

    cd ontology-access-kit
    poetry run llm install llm-gemini

This will install the plugin in the same environment as OAK.

If you need to update this:

.. code-block:: bash

    cd ontology-access-kit
    poetry run llm install -U llm-gemini

TODO: instructions for non-developers.

Mixtral via Ollama and LiteLLM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ollama run mixtral

.. code-block:: bash

    pipx install litellm
    litellm -m ollama/mixtral

Next edit your extra-openai-models.yaml as detailed in the llm
[other model docs](https://llm.datasette.io/en/stable/other-models.html):

.. code-block:: yaml

    - model_name: ollama/mixtral
      model_id: litellm-mixtral
      api_base: "http://0.0.0.0:8000"

Then you can use the model in OAK:

.. code-block:: bash

    runoak -i llm:{litellm-mixtral}:sqlite:obo:cl generate-definitions .descendant//p=i "T cell"

Mixtral via groq and LiteLLM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`groq <https://groq.com/>`_ provides an API over souped-up hardware running Llama2 and Mixtral.
You can configure in a similar way to ollama above, but here we are proxying to a remote server:

. code-block:: bash

    pipx install litellm
    litellm -m groq/mixtral-8x7b-32768

Next edit your extra-openai-models.yaml as detailed in the llm
[other model docs](https://llm.datasette.io/en/stable/other-models.html):

.. code-block:: yaml

    - model_name: litellm-groq-mixtral
      model_id: litellm-groq-mixtral
      api_base: "http://0.0.0.0:8000"

Then you can use the model in OAK:

.. code-block:: bash

    runoak -i llm:{litellm-groq-mixtral}:sqlite:obo:cl validate-mappings .descendant//p=i "T cell"
