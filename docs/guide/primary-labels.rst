.. _primary-labels:

Primary Labels
==============

Looking up labels
------------------

The :ref:`basic_ontology_interface` provides a way to look up the primary label for an
entity or set of entities. For example:

.. code-block:: python

    >>> ont = get_implementation_from_selector('ubergraph:')
    >>> id = "UBERON:0000948"
    >>> print(ont.label(id))
    heart

Note the assumption here is that there is at most a single primary label for an entity,
but this assumption turns out to not universally hold.

First, not all entities will have a primary label. It's common practice for
many semantic web ontologies to use semantic identifiers, and omit a label.

In these cases, if no label is found, OAK simply returns ``None``

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

    >>> # use the standard sparql adapter over local files
    >>> soil_oi = get_implementation_from_shorthand("soil-profile.skos.nt"))
    >>> # add a custom prefix
    >>> soil_oi.prefix_map()["soilprofile"] = "http://anzsoil.org/def/au/asls/soil-profile/"
    >>> # create a mapper for mapping OMO to a custom vocab
    >>>  soil_oi.ontology_metamodel_mapper = OntologyMetadataMapper(
    >>>        [], curie_converter=soil_oi.converter
    >>>    )


Multilingual ontologies
------------------------

Many ontologies assume English as a default, and only provide a single
primary label (whether this is via rdfs:label, or via another property).

Others may provide multiple primary labels, with a maximum of one per language.

OAK still makes the maximum one primary label assumption, but you can
set the language as a property of the adapter. For example:

.. code-block:: python

    >> oi.preferred_language = "fr"

Other edge cases
----------------

Even for OBO ontologies, there are some edge cases, such as cases
where we may find multiple labels for a single entity. This can
happen when two or more ontologies are merged, and these ontologies
contain the same entity, but with different labels.

Even when an ontology is not intended to be multilingual, there is no standard way
to type a label literal; some are typed as xsd:string, and some using a ``en`` language tag.
This is important because queries for one may not work for another.

Further reading
----------------

- `OBO Foundry: Naming Conventions <https://obofoundry.org/principles/fp-012-naming-conventions.html>`_