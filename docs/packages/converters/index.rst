.. _converters:

Converters
==========

OAK uses a number of different Data Models (See  :ref:`datamodels`) for representing ontologies and
ontology-related information.

Command Line Usage
-------------------

The general pattern is:

.. code-block:: bash

    $ runoak -i INPUT-SPEC dump -O FORMAT -o OUTPUT-FILE

Converting from Obo Graphs
---------------------------

Currently the only converters implemented are for converting between
the OboGraphs data model and other models.

.. code-block:: python

    >>> from oaklib.utilities.obograph_utils import load_obograph_document
    >>> graph_doc = load_obograph_document("tests/input/go-nucleus.json")

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   data-model-converter
   obo-graph-to-fhir
   obo-graph-to-obo-format
   obo-graph-to-owl
