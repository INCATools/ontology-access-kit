.. _mappings:

Mappings and Cross-References
=============================

:term:`Mappings<Mapping>` are a way of connecting the same or similar concepts in different ontologies.
Historically, mappings have been handled very differently depending on the ontology or community:

- for :term:`OBO Format` ontologies, the ``xref`` tag is used, which corresponds to ``oboInOwl:hasDbXref``
- for many :term:`Linked Data` resources, ``owl:sameAs`` is used
- for some ontologies, ``owl:equivalentClass`` :term:`Axioms<Axiom>` are used
- in other cases, :term:`SKOS` triples may be used
- sometimes mappings are distributed as simple :term:`CSV` files, outside the ontology

In addition to the basic vocabulary used, the :term:`Data Models<Datamodel>` for mappings differs a lot.

SSSOM
-----

The `Simple Standard for Sharing Ontological Mappings <https://w3id.org/sssom>` (SSSOM) is a standard
for ontology mappings. It provides both a standard TSV/CSV format, and a standard way of encoding mappings in ontologies.

OAK uses SSSOM as its primary data model for mappings, except in the :ref:`basic_ontology_interface` where
mappings are represented as simple lists of mapped CURIEs, without any metadata.

Mappings in OAK
---------------

To see all mappings for a concept or concept, you can use the mappings command:

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon mappings brain
    ...
    ---
    subject_id: UBERON:0000955
    predicate_id: oio:hasDbXref
    object_id: ZFA:0000008
    mapping_justification: semapv:UnspecifiedMatching
    subject_label: brain
    subject_source: UBERON
    object_source: ZFA
    ---
    ...


This will return YAML conforming to SSSOM by default. Like all OAK
commands, this also allows for other output formats.

To get this as SSSOM TSV:

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon mappings brain --output-type sssom

.. csv-table:: uberon sssom mappings
    :header: subject_id,subject_label,predicate_id,object_id,mapping_justification,subject_source,object_source

    UBERON:0000955,brain,oio:hasDbXref,HBA:4005,semapv:UnspecifiedMatching,UBERON,HBA
    UBERON:0000955,brain,oio:hasDbXref,MA:0000168,semapv:UnspecifiedMatching,UBERON,MA
    UBERON:0000955,brain,oio:hasDbXref,MAT:0000098,semapv:UnspecifiedMatching,UBERON,MAT

Under the hood, OAK will query using standard mapping predicates, including
those from :term:`SKOS` and :term:`OboInOwl`.

Using the Python interface, there are two levels in which to access mappings.

- The :ref:`basic_ontology_interface` provides a simple interface that exposes mappings as simple tuples
- The :ref:`mapping_provider_interface` provides access to the full SSSOM model

In Python
^^^^^^^^^

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:uberon")
    >>> for m in adapter.sssom_mappings("UBERON:0000955"):
    ...    print(m.subject_id, m.object_id, m.predicate_id)
    <BLANKLINE>
    ...
    UBERON:0000955 CALOHA:TS-0095 oio:hasDbXref
    UBERON:0000955 DHBA:10155 oio:hasDbXref
    UBERON:0000955 EFO:0000302 oio:hasDbXref
    ...

Generating Mappings
-------------------

OAK also includes a functionality for *generating* mappings, via the `lexmatch` command.

Further reading
---------------

- `Mappings in SSSOM <https://oboacademy.github.io/obook/tutorial/sssom-manual/>`_