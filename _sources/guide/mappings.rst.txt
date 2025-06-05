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

The `Simple Standard for Sharing Ontological Mappings <https://w3id.org/sssom>`_ (SSSOM) is a standard
for ontology mappings. It provides both a standard TSV/CSV format, and a standard way of encoding mappings in ontologies.

OAK uses SSSOM as its primary data model for mappings, except in the :ref:`basic_ontology_interface` where
mappings are represented as simple lists of mapped CURIEs, without any metadata.

The :ref:`mapping_provider_interface` provides a way to access mappings using the richer SSSOM model.

Mappings in OAK
---------------

To see all mappings for a concept or concept, you can use the mappings command.

See the `Notebook example on mappings <https://github.com/INCATools/ontology-access-kit/blob/main/docs/examples/Commands/Mappings.ipynb>`_.

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon mappings UBERON:0000955
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

    $ runoak -i sqlite:obo:uberon mappings UBERON:0000955 --output-type sssom

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

Directionality of mappings
--------------------------

While mappings are often thought of as bidirectional, this is not quite true in practice:

- Some mapping predicates such as ``skos:broadMatch`` and ``skos:narrowMatch`` are inherently directed, with the meaining inverted in the opposite direction
- Many mappings are only be asserted in one ontology, and may be "invisible" when queried from the mapped ontology

At the time of writing, most ontologies bundle mappings that are uncommitted `oio:hasDbXref`.

Additionally, most mappings are only asserted in one direction. This can be very confusing for
users of ontologies, as they often need special "insider knowledge" about which ontologies
provide which mappings.

We saw above that if we query the Uberon ontology for mappings for the Uberon concept "brain" (UBERON:0000955),
we get mappings to ZFA, because these mappings are bundled with Uberon.

OAK is smart enough to allow querying from either direction; e.g. if we query Uberon for a ZFA ID:

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon mappings ZFA:0000008
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

This is the exact same mapping -- it doesn't matter if we query for ZFA:0000008 or UBERON:0000955.

But note if we query *in the ZFA ontology* for the Uberon term we don't get it. This returns no results:

.. code-block:: bash

    $ runoak -i sqlite:obo:zfa mappings UBERON:0000955

If we query for the ZFA ID we see the complete set of ZFA mappings for that term:

.. code-block:: bash

    $ runoak -i sqlite:obo:zfa mappings ZFA:0000008
    ...
    subject_id: ZFA:0000008
    predicate_id: oio:hasDbXref
    object_id: TAO:0000008
    mapping_justification: semapv:UnspecifiedMatching
    subject_label: brain
    subject_source: ZFA
    object_source: TAO
    ...

So ZFA bundles mappings to TAO, but not UBERON.

At the time of writing, ZFA *does* bundle mappings to CL:

.. code-block:: bash

    $ runoak -i sqlite:obo:zfa mappings CL:0000540
    ...
    predicate_id: oio:hasDbXref
    mapping_justification: semapv:UnspecifiedMatching
    subject_id: ZFA:0009248
    subject_label: neuron
    object_id: CL:0000540
    subject_source: ZFA
    object_source: CL
    ...

In the future, OAK may have easier ways to query a union of ontologies, and OBO ontologies may
redistribute reciprocal mappings, but for now it helps to know how each ontology handles mappings to
use these effectively.

Support for SSSOM
-------------------

Currently SSSOM is supported as an *export* format, and as an internal datamodel, but not as an *import* format. Currently the only
way to access mappings is if they are bundled with the ontology. Note that bundled mappings typically lack
a lot the rich metadata that is distributed with SSSOM.

For working directly with SSSOM files you can use the
`SSSOM Python library <https://github.com/mapping-commons/sssom-py>`_.

Generating Mappings
-------------------

OAK also includes a functionality for *generating* mappings, via the `lexmatch` command.

See the `Lexmatch tutorial <https://oboacademy.github.io/obook/tutorial/lexmatch-tutorial/>`_ on OBO Academy.

Further reading
---------------

- `Mappings in SSSOM <https://oboacademy.github.io/obook/tutorial/sssom-manual/>`_
- `Lexmatch tutorial <https://oboacademy.github.io/obook/tutorial/lexmatch-tutorial/>`_
- :ref:`mapping_provider_interface`
