.. _associations:

Associations and Curated Annotations
====================================

Background
----------

The main purpose of OAK is to provide uniform access onto an :term:`Ontology`.
Ontologies are frequently used in combination with some form of tagging data entities.
In the bio-ontologies and other realms, this kind of tagging is usually called :term:`Annotation`
(but this term can be ambiguous).

There are many different formats and data models for associations. The :term:`Gene Ontology` uses
the :term:`GAF` format, which associates genes or gene products with terms in the ontology,
alongside additional contextual information and provenance. There is a similar format for
:term:`Human Phenotype Ontology` associations, which associate disease identifiers with phenotypic feature
terms, alongside information about severity, age of onset, as well as provenance. Outside
the bio-ontology world, the :term:`Open Annotation` standard provides a way of associating
a wide range of entities of different types.

The difference in use cases make supporting a single data model challenging. However, there
are a number of core elements that are typically shared.

The association:

- is typically about something, i.e the :term:`Subject` of the association
- relates the subject to another thing (the :term:`Object`), typically a class from an ontology
- may have an (explicit or implicit) :term:`Predicate` indicating the nature of the relationship between subject and object
- should have provenance, typically indicated via CURIEs to publications like DOIs or PMIDs
- may have some kind of semantic modifier, including a negation flag
- may have any number of pieces of additional evidence, providence, or administrative metadata
- may include additional *denormalized* fields for convenience.

The first three of these constitute the OAK :term:`Edge` data model. You may well ask,
why treat associations differently from other kinds of edges in the ontology?

There are a variety of answers to this question. Some are pragmatically oriented:

- associations have historically been separated from ontology relationships in many domains
- the operations we may want to do on one may differ from those on the other
- associations typically emphasize the importance of provenance and additional metadata whereas ontology relationships are taken "as given"
- associations are typically curated by different groups than those that curate ontologies

Others answers are more formally oriented:

- ontology relationships have strict OWL logical semantics (usually some combination of :term:`SubClassOf` and :term:`SomeValuesFrom`), whereas associations don't have defined semantics (or are weak Some-Some axioms)
- ontology relationships represent *term* invariant relationships, whereas associations are *contingent*

For a more detailed treatment of these formal aspects, see `On beyond Gruber: "Ontologies" in today's biomedical information systems and the limits of OWL <https://pubmed.ncbi.nlm.nih.gov/34384571/>`_.

Association support in OAK
---------------------------

.. warning::

    The current way associations are loaded and modeled in OAK is subject to change

Data Model
~~~~~~~~~~

See the `Association data model <https://w3id.org/oak/association/>`_ for details of the data model.

The data model is intentionally minimalist, and intends to capture the core features of multiple
association data models. A generic ``PropertyValue`` object captures domain-specific extensions.

Selecting association sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of ways to select an association source.

On the command line you can supplement the main ontology input (passed with ``--input`` or ``-i``) with
an ``--associations`` option (shorthand ``-g``). You will also need to specify the association
format (``--associations-type`` or ``-G``).

The following will query HPO associations for any diseases associated with "Abnormal lacrimal gland morphology"
or any is-a :term:`Descendant`:

.. code-block:: bash

    wget http://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa
    runoak -i sqlite:obo:hp -G hpoa -g phenotype.hpoa associations -p i HP:0011482


Further reading
---------------

- `Ontogenesis article on associations <https://ontogenesis.knowledgeblog.org/50/>`_
- `Gene Ontology: tool for the unification of biology <https://www.nature.com/articles/ng0500_25>`_
- `On beyond Gruber: "Ontologies" in today's biomedical information systems and the limits of OWL <https://pubmed.ncbi.nlm.nih.gov/34384571/>`_.
