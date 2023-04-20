Introduction
------------

Ontology Access Toolkit (OAK) is a Python library for common
:term:`Ontology` operations over a variety of :term:`Adapters<Adapter>`.

This library provides a collection of different :term:`Interfaces<Interface>` for different
kinds of ontology operations, including:

-  basic features of an :term:`Ontology Element`, such as its :term:`Label`, :term:`Definition`,
   :term:`Relationships<Relationship>`, or :term:`Synonyms<Synonym>`.
-  :term:`Search` an ontology for a term.
-  :term:`Apply` modifications to terms, including adding, deleting, or updating
-  numerous specialized operations, such as :term:`Graph Traversal`, or :term:`Axiom` processing,
   :term:`Ontology Alignment`, or :term`Text Annotation`.

These interfaces are *separated* from any particular backend. This means
the same API can be used regardless of whether the ontology:

-  is served by a remote API such as :term:`OLS` or :term:`BioPortal`.
-  is present locally on the filesystem in :term:`OWL`, :term:`OBO Format`,
   :term:`OBO Graphs`, or :term:`SQLite` formats.
-  is to be downloaded from a remote :term:`Ontology Repository` such as the :term:`OBO Library`.
-  is queried from a remote database, including :term:`SPARQL` endpoints, A SQL
   database, a Solr/ES endpoint.

Basic Python Example
~~~~~~~~~~~~~~~~~~~~

The following code will load an ontology from a :term:`SQLite` database, lookup
basic information on terms matching a search

.. code:: python

   >>> from oaklib import get_adapter
   >>> adapter = get_adapter("sqlite:obo:cl")
   >>> for curie in adapter.basic_search("T cell"):
   ...     print(f'{curie} ! {adapter.label(curie)}')
   ...     print(f'Definition: {adapter.definition(curie)}')
   ...     for rel, fillers in adapter.outgoing_relationship_map(curie).items():
   ...         print(f'  RELATION: {rel} ! {adapter.label(rel)}')
   ...         for filler in fillers:
   ...             print(f'     * {filler} ! {adapter.label(filler)}')
   CL:0000084 ! T cell
   Definition: A type of lymphocyte whose defining characteristic is the expression of a T cell receptor complex.
      RELATION: RO:0002202 ! develops from
         * CL:0000827 ! pro-T cell
      RELATION: RO:0002215 ! capable of
         * GO:0002456 ! T cell mediated immunity
      RELATION: rdfs:subClassOf ! None
         * CL:0000542 ! lymphocyte


Basic Command Line Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   $ runoak -i sqlite:obo:obi info "assay"

This does a basic lookup of the term "assay" in :term:`OBI`
