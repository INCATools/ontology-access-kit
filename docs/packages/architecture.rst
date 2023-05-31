.. architecture:

Architecture
============

Ontology Interfaces
-------------------

.. currentmodule:: oaklib.interfaces

This library provides a collection of ontology :ref:`interfaces` that describe a set of operations
that can be performed on an ontology

The core interface is :ref:`BasicOntologyInterface` which provides some of the most common operations
you can do on an ontology, mostly simple lookup operations. Here is a simplified picture:

.. mermaid::

   classDiagram
      class OntologyInterface {
          +interfaces_implemented()
      }
      class BasicOntologyInterface {
          +label(curie)
          +definition(curie)
          +all_entity_curies(curie)
          +basic_search(search_term)
          +get_outgoing_relationships_by_curie(curie)
          +...()
      }
      OntologyInterface <|-- BasicOntologyInterface

Implementations
-------------------

Interfaces don't do much by themselves. Client code never instantiates these directly. Instead, :ref:`implementations` do all the work.

Here is an example of code that uses an Ubergraph implementation to do a simple lookup:

.. code:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("ubergraph:uberon")
    >>> print(adapter.label("UBERON:0001825"))
    paranasal sinus

Behind the scenes, this is implemented using a SPARQL query over the Ubergraph endpoint.

You can do the same thing using a different implementation. This one uses the
:ref:`sql_implementation`:

.. code:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:uberon")
    >>> print(adapter.label("UBERON:0001825"))
    paranasal sinus

There are other implementations - for relational databases, for ontology portal APIs, for OWL ontologies...

Why so many implementations? The answer is that different use cases require different implementations.

Ontology portal APIs work great, so long as the ontology you care about is loaded, and you don't have to repeated calls with high
network latency. Local files work great, but they require downloads, and have a high memory burden for large ontologies (most
ontologies are small, but there is a long tail of very large ontologies like PRO, CHEBI, NCBITaxon, DRON, ...).

Other Interfaces
----------------

The basic interface is only intended for, well, basic operations. These typically serve 80% of use cases. But
there are many many uses for ontologies. Some of these demand particular *abstractions* over an ontology; e.g
as a graph-like artefact, as an OWL bundle of axioms, or as a terminological-lexical artefact.

We provide a number of different interfaces, designed for these different purposes. Here are a few:

.. mermaid::

  classDiagram
      class OntologyInterface {
          +interfaces_implemented()
      }
      class BasicOntologyInterface {
          +label(curie)
          +definition(curie)
          +all_entity_curies(curie)
          +basic_search(search_term)
          +get_outgoing_relationships_by_curie(curie)
          +...()
      }
      OntologyInterface <|-- BasicOntologyInterface
      class OwlInterface {
          +all_axioms()
          +get_axioms_about(curie)
          +...()
      }
      BasicOntologyInterface <|-- OwlInterface
      class RelationGraphInterface {
          +entailed_relationships(curies)
          +ancestors(curie)
          +...()
      }
      BasicOntologyInterface <|-- RelationGraphInterface
      class PatcherInterface {
          +apply_patch(patch)
          +...()
      }
      BasicOntologyInterface <|-- PatcherInterface
      class QCInterface {
          +terms_without_definitions()
          +get_obo_conformance_report()
          +...()
      }
      BasicOntologyInterface <|-- QCInterface
      class SubsetterInterface {
          +extract_subset(seed_curies)
          +fill_gaps(seed_curies)
          +...()
      }
      BasicOntologyInterface <|-- SubsetterInterface

It's highly unlikely you will care about all of these - in fact most applications will only need one!

Example: OWL Ontology Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some interfaces may require
a particular *object model* (note that the BasicOntologyInterface avoids an object model, with operations
accepting and returning simple scalars, dicts, and lists). See :ref:`datamodels` for a description of data models used.

An example would be an OWL interface that uses an OWL object model (here funowl)

.. mermaid::

  classDiagram
      class OntologyInterface {
          +interfaces_implemented()
      }
      class BasicOntologyInterface {
          +label(curie)
          +definition(curie)
          +entities(curie)
          +basic_search(search_term)
          +relationships(curie)
          +...()
      }
      OntologyInterface <|-- BasicOntologyInterface
      class OwlInterface {
          +all_axioms()
          +get_axioms_about(curie)
          +...()
      }
      BasicOntologyInterface <|-- OwlInterface
      OwlInterface --> OwlOntology
      class OwlOntology {
          +axioms()
          +...
      }
      class Axiom {
          +Annotation annotations[]
      }
      OwlOntology --> Axiom
      class SubClassOf {
          +ClassExpression subClass
          +ClassExpression superClass
      }
      Axiom <|-- SubClassOf
      class EquivalentClasses {
          +ClassExpression ops[]
      }
      Axiom <|-- EquivalentClasses

.. note:: If this seems a little involved, don't worry! You don't need to use the OWL interface
          or the OWL datamodel. It is intended for use cases where there is a *particular need*
          for this level of abstraction!

Partial and Complete Implementation
-----------------------------------

Not all implementations work with all interfaces. Even if an implementation implements an
interface, it may not implement all operations.

See :ref:`implementations` for full documentation on each implementation (more coming soon), but
to give you a sense:

- the Pronto based implementation will not support all of OWL (which is fine for most purposes)
- Same for the Ontology Portal APIs, which focus on the most common operations a developer may need
- Search/autocomplete are the specialization of ontology portal APIs, as these are backed by powerful lexical indexes
- In theory any SPARQL endpoint can support all of OWL in the future, but this will take some work to implement
- we plan to have full OWL support for the SQL Database endpoint

.. warning ::

    At this stage in development of this library, most implementations are partial and things are subject to change!
