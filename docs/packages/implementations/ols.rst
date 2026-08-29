.. _ols_implementation:

Ontology Lookup Service (OLS) Adapter
=====================================

Provides access to ontologies provided via the EMBL-EBI `Ontology Lookup Service <https://www.ebi.ac.uk/ols/>`_ (OLS)

Also provides interface to `OxO <https://www.ebi.ac.uk/spot/oxo/>`_ mapping endpoint

This adapter uses `ols-client <https://github.com/cthoyt/ols-client>`_ to connect to
any OLS endpoint.

See the :ref:`OLS tutorial notebook <adapters_examples>` for a worked walkthrough.

Supported operations
--------------------

* labels, definitions (with provenance) and synonyms (with scope, type and xrefs)
* entity metadata maps, subsets, cross-references and SSSOM mappings
* obsoletion status and replacement terms
* OWL types (class / property / individual)
* OBO Graph node projection
* ancestors, descendants and direct relationships, fully paged
* search, within one ontology or across every ontology OLS indexes
* multilingual labels and definitions, where OLS holds translations

Every lookup is an HTTP request, so the adapter caches the whole term payload the
first time any property of a term is requested; all other properties of that term
are then served without further requests.

.. note ::

   Operations that require enumerating an entire ontology (``entities()``,
   ``obsoletes()``) issue one request per 500 terms and are impractical for large
   ontologies. Prefer a local adapter (e.g. ``sqlite:obo:go``) for bulk work.

Code
----

.. currentmodule:: oaklib.implementations.ols.ols_implementation
                   
.. autoclass:: OlsImplementation
