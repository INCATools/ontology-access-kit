.. _primary_labels:

Primary Labels
==============

Looking up labels
------------------

The :ref:`basic_ontology_interface` provides a way to look up the primary :term:`Label` for an
entity or set of entities. For example:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> ont = get_adapter('ubergraph:')
    >>> id = "UBERON:0000948"
    >>> print(ont.label(id))
    heart

Note the assumption here is that there is at most a single primary label for an entity,
but this assumption turns out to not universally hold.

First, not all entities will have a primary label. It's common practice for
many semantic web ontologies to use :term:`Semantic Identifiers`, and omit a label.

In these cases, if no label is found, OAK simply returns ``None``.

Additionally, some ontologies may have multiple primary labels, one per language.

Custom label annotation properties
---------------------------

By default, OAK will use the ``rdfs:label`` property to find the primary label.
While this should work with an OBO ontology, it is not guaranteed to work with
other ontologies. Some ontologies may use a different property like:

- ``skos:prefLabel`` (this is common for skos vocabularies)
- ``foaf:name``

Some adapters will allow you to use custom mappings from rdfs:label to these
other properties. Here you can either specify a specific *profiles*, or
provide a set of mappings in SSSOM form.

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> from oaklib.mappers import OntologyMetadataMapper
    >>> # use the standard sparql adapter over local files
    >>> adapter = get_adapter("tests/input/soil-profile.skos.nt")
    >>> # add a custom prefix
    >>> adapter.prefix_map()["soilprofile"] = "http://anzsoil.org/def/au/asls/soil-profile/"
    >>> # create a mapper for mapping OMO to a custom vocab
    >>> mapper = OntologyMetadataMapper([], curie_converter=adapter.converter)
    >>> mapper.use_skos_profile()
    >>> adapter.ontology_metamodel_mapper = mapper
    >>> for entity in adapter.entities():
    ...     print(entity, adapter.label(entity))
    <BLANKLINE>
    ...
    soilprofile:voids-cracks-1 Fine (voids cracks)
    soilprofile:voids-cracks-2 Medium (voids cracks)
    soilprofile:voids-cracks-3 Coarse (voids cracks)
    soilprofile:voids-cracks-4 Very coarse (voids cracks)
    soilprofile:voids-cracks-5 Extremely coarse (voids cracks)
    ...



Multilingual ontologies
------------------------

Many ontologies assume English as a default, and only provide a single
primary label (whether this is via rdfs:label, or via another :term:`Annotation Property`).

Others may provide multiple primary labels, with a maximum of one per language.

OAK still makes the maximum one primary label assumption, but you can
set the language as a property of the adapter. For example:

.. code-block:: python

    >> adapter.preferred_language = "fr"

Other edge cases
----------------

Even for OBO ontologies, there are some edge cases, such as cases
where we may find multiple labels for a single entity. This can
happen when two or more ontologies are merged, and these ontologies
contain the same entity, but with different labels.

This is not infrequent when we have triplestores that merge together
multiple ontologies as in Ubergraph.

Even when an ontology is not intended to be multilingual, there is no standard way
to type a label literal; some are typed as xsd:string, and some using a ``en`` language tag.
This is important because queries for one may not work for another.

OAK is intended to abstract over some of these implementation differences,
and to provide a *common interface* such that intererable code can be
written that will work with a wide variety of ontologies and vocabularies.

Further reading
----------------

- `OBO Foundry: Naming Conventions <https://obofoundry.org/principles/fp-012-naming-conventions.html>`_