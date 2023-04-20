.. _aliases:

Aliases and Synonyms
=====================

Most ontologies allow for multiple aliases or :term:`Synonyms<Synonym>` for a given entity. These are typically
distinguished from the :term:`primary label <Label>`.

There exists a wide variety of ways in which aliases are represented in ontologies, reflecting
both different historic practice, and different uses cases. Most ontologies represent synonyms/aliases
as strings / :term:`Literal` values, but note that some systems (e.g. SKOS) may occasionally
represent a synonym as a distinct :term:`Node` in the RDF graph.

Use Cases
---------

Search
^^^^^^

One of the most common use cases for aliases is to allow for :term:`Search`.

For example, in the :term:<Gene Ontology>, the entity ``GO:0000050`` has the primary label "urea cycle", but a user
may be searching using the string "ornithine cycle". In this case, the search system should
be able to return the right concept using a synonym in GO.

In :term:`OBO Format`, a partial representation of this class is:

.. code-block:: yaml

        id: GO:0000050
        name: urea cycle
        synonym: "ornithine cycle" EXACT []
        synonym: "urea biosynthesis" RELATED []

To support search, a relatively simple synonym system is required, although advanced searches
may want to boost search, or allow for contextual info in search (see contextual usage, below)

Text mining and NLP
^^^^^^^^^^^^^^^^^^^

Many text mining and NLP tasks rely on being able to :term:`recognize or ground concepts in text<Text Annotation>`.

For example, a phrase:

.. code-block::

    Inherited mutations in the PTEN gene increase the risk of developing breast cancer

Contains many different concepts, many of which are denoted by something other than their primary label.

For example, in NCIT the primary label for the concept "breast cancer" is "malignant breast neoplasm", so
use of synonyms may be required to ground this concept.

Adding more synonyms to ontologies can help with text mining, see `Funk et al 2016 <https://jbiomedsem.biomedcentral.com/articles/10.1186/s13326-016-0096-7>`_

Different aliases for different communities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ontologies aim to provide a largely *terminology-neutral* view of concepts or entities. In practice, this
means that sometimes some communities are prioritized when providing primary labels; e.g

- in :term:`Uberon`, species-neutral terms and terms from comparative anatomy are prioritized, e.g "manus" over "hand"
- Scientific or medical terminology is typically favored over less precise layperson terminology

However, it can be very important to provide strings that are intended for use within a particular community
(e.g. human anatomy users of Uberon, or layperson users of HPO).

Different applications may use metadata about target community differently - e.g. customizing both search and display
(favoring the community label), or even making a community specific version of an ontology,
with community synonyms replacing primary labels.

For more information see:

- `Vasilevsky et al <https://www.nature.com/articles/s41588-018-0096-x>`_, Plain-language medical vocabulary for precision diagnosis
- `OMO issues 70 <https://github.com/information-artifact-ontology/ontology-metadata/issues/70>`_

Different Languages
^^^^^^^^^^^^^^^^^^^

Many ontologies need to support an international community of users.


Different approaches to representing synonym metadata
---------------------------------

**There is no universal standard for representing synonyms in ontologies.**

Ontologies vary in both structure and vocabularies (:term:`Annotation Properties<Annotation Property>`) used.

Some ontologies like :term:`SWEET` create a different concept/class URI for each synonym,
and related these to the "primary" concept using an :term:`Equivalence Axiom`.

It is more common to represent synonyms as :term:`Literals<Literal>`, so that there is a clear separation
between the concept and its string forms -- but this is by no means universal.

There are a lot of different predicates used for connecting entities to these literals:

- :term:`SKOS` provides `skos:altLabel`
- :term:`oboInOwl` (oio) provides 4 different predicates: `oio:hasExactSynonym`, `oio:hasRelatedSynonym`,
  `oio:hasBroadSynonym`, `oio:hasNarrowSynonym`
- :term:`IAO` has `IAO:0000118` (has alternative label)
- Many ontologies mint their own specific properties

Within the context of OBO ontologies, the :term:`OMO` vocabulary attempts to unify these different models,
but there is still wide variation, even within OBO.

One area where there *is* standardization is :term:`Language Tags<Language Tag>` in RDF. However, there is still
a lack of consensus in many ontologies whose primary language is english whether to
tag each element with a ``@en`` or to leave as an untyped or string literal.

Representation of synonyms in OAK
---------------------------------

OAK aims to be as pluralistic as possible, and to support a wide variety of ontologies
and use cases, both for bio-ontologies, and any kind of ontology.

The approach we take is a multi-level representation. The core OAK data model
has a simple representation of synonyms, and then we provide different interfaces
for different ways of representing synonyms.

The primary advanced interface is the :ref:`obograph_interface`.

Simple Core Model
^^^^^^^^^^^^^^^^^
The BasicOntologyInterface in OAK allows for a simple representation of synonyms,
as either lists of strings associated with entities, or predicate-string tuples.

.. note::

    For full documentation , see :ref:`basic_ontology_interface`


The ``entity_aliases`` method returns a list of strings.

Example:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:hp")
    >>> for alias in sorted(adapter.entity_aliases("HP:0001698")):
    ...     print(alias)
    Fluid around heart
    Pericardial effusion
    Pericardial effusions

This is too simplistic for some purposes - often we want to know more about
the predicate, so we can use ``alias_relationships``

.. code-block:: python

    >>> for pred, alias in sorted(adapter.alias_relationships("HP:0001698")):
    ...     print(pred, alias)
    oio:hasExactSynonym Fluid around heart
    oio:hasExactSynonym Pericardial effusions
    rdfs:label Pericardial effusion

(note that label is treated as an alias by default, but you can pass ``exclude_labels=True`` to
override this)

You can get the same information on the command line with the ``aliases`` command:

.. code-block:: bash

    $ alias hp='runoak -i sqlite:obo:hp'
    $ hp aliases HP:0001698

This will give a table:

.. csv-table:: HPO basic aliases
    :header: curie,pred,alias

    HP:0001698,rdfs:label,Pericardial effusion
    HP:0001698,oio:hasExactSynonym,Fluid around heart
    HP:0001698,oio:hasExactSynonym,Pericardial effusions

Obo Graph Data Model
^^^^^^^^^^^^^^^^^^^^

The :ref:`obograph_interface` provides a more advanced representation of synonyms,
conforming to the :ref:`obograph_datamodel`.

.. note::

    For full documentation , see :ref:`obograph_interface`

.. code-block:: python

    >>> adapter = get_adapter("sqlite:obo:hp")
    >>> for entity, spv in adapter.synonym_property_values(["HP:0001698"]):
    ...     xrefs = ", ".join(spv.xrefs)
    ...     print(f"{entity} pred: {spv.pred} ({spv.synonymType}) '{spv.val}' [{xrefs}]")
    HP:0001698 pred: hasExactSynonym (layperson) 'Fluid around heart' [ORCID:0000-0002-6548-5200]
    HP:0001698 pred: hasExactSynonym (None) 'Pericardial effusions' []

You can also get similar behavior by passing ``--obo-model`` to the ``aliases`` command:

.. code-block:: bash

    $ hp aliases HP:0001698 --obo-model

.. csv-table:: HPO full aliases
    :header: curie,pred,value,type,xrefs

    HP:0001698,hasExactSynonym,Fluid around heart,layperson,['ORCID:0000-0002-6548-5200']
    HP:0001698,hasExactSynonym,Pericardial effusions,None,[]


