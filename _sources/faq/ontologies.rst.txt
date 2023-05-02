.. _faq_ontologies:

FAQ: Ontologies
===============

What is an ontology?
--------------------

See the section :ref:`basics` in the :ref:`guide`.

Do we need ontologies now we have ChatGPT?
------------------------------------------

Large Language Models (LLMs) fine-tuned on instruction tasks display impressive abilities to work
with knowledge using a purely natural language interface. However, at this time, LLMs lack any
grounding for the answers they provide, something ontologies are very good at.

The OAK developers are very interested in the fusion of LLM research and knowledge-based ontology
research. See our :term:`OntoGPT` project for examples.

What is OWL?
------------

OWL (Web Ontology Language) is a data model for expressing ontologies, oriented around
set-theoretic logical :term:`Axioms<Axiom>`.

See :term:`OWL`.

What is OBO Format?
-------------------

OBO Format is a simple format for expressing a subset of OWL in a way that is easily
read and produced.

See :term:`OBO Format`.

What is OBO
------------

OBO (Open Bio Ontologies) is a repository of ontologies intending to conform to common
standards.

.. note::

    OBO does not require OBO Format.

What's a synonym and how do I access them?
------------------------------------------

See the section :ref:`aliases` in the OAK guide.

You can query for synonyms on the command line:

.. code-block:: bash

    runoak -i sqlite:obo:cl aliases "T cell"

.. csv-table:: Ancestor statistics
    :header: curie,pred,alias

    CL:0000084,rdfs:label,T cell
    CL:0000084,oio:hasExactSynonym,T lymphocyte
    CL:0000084,oio:hasExactSynonym,T-cell
    CL:0000084,oio:hasExactSynonym,T-lymphocyte
    CL:0000084,oio:hasRelatedSynonym,immature T cell
    CL:0000084,oio:hasRelatedSynonym,mature T cell