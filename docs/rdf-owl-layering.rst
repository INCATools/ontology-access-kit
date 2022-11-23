.. _rdf_owl_layering:

Layering on RDF/OWL
===================

RDF and OWL are semantic web languages for representing information and ontologies.

You don't need to know much about RDF or OWL to use OAK, but it can help to understand
how OAK is layered on top of these languages.

- RDF is fundamentally about :term:`Triples<Triple>`
- OWL is fundamentally about :term:`Axioms<Axiom>`
- OAK provides a number of other higher level constructs for thinking about ontologies

    - :term:`Entity`
    - :term:`Alias`
    - :term:`Relationship`
    - :term:`Mapping`
    - :term:`Definition`
    - :term:`Metadata`
    - "other" logical constructs


CURIEs, URIs, and prefixmaps
---------------

Relationships between entities
------------------------------

Metadata about entities
-----------------------

Challenges
~~~~~~~~~~

All ontologies within OBO use rdfs:label to provide a human readable label for an entity.
However, this doesn't necessarily hold for non-OBO ontologies or vocabularies.

- Some will use skos:prefLabel (and may include multiple rdfs:labels for synonyms)
- Some will use foaf:name

Even when rdfs:label, is used, the practice may be different.

For some vocabularies, including a human readable label annotation is optional, and the URI is
intended as both the identifier and the label.

Some ontologies may use multiple rdfs:labels, combined with language tags, with the
intention of providing a maximum of a label for a set of languages. But there is
still no guarantee for ontologies "in the wild" that there will be a maximum of one
label per language.

Even when an ontology is not intended to be multilingual, there is no standard way
to type a label literal; some are typed as xsd:string, and some using a ``en`` language tag.
This is important because queries for one may not work for another.

Once we get beyond primary human readable labels (which you might have thought
would be a solved problem!) things get even less standardized.

- SKOS
- SSSOM aims to standardize mappings
- OBO Format via OboInOwl
- OMO

OMO
~~~

Ontology portals
~~~~~~~~~~~~~~~~

OAK Approach
~~~~~~~~~~~~

OAK aims to be as pluralistic as possible, whilst retaining a point of view.

OAK will try and present ontologies through as uniform an interface as possible:

- a single optional but recommended label for each entity (for any given language localization)
- a single optional textual definition for each entity (for any given language localization)
- any number of aliases/synonyms, optionally parameterized by predicate, with optional additional metadata
- ...

For anything that doesn't fit into the above, OAK provides generic mechanisms for access.
But the goal is to make the commonly used constructs easy and intuitive to access.

Labels
~~~~~~

Obsoletion and obsoletion metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In OAK, the terms "obsoletion" and "deprecation" are used interchangeably.

The way in which is to specify an entity is obsolete is fairly standard, using an ``owl:deprecated`` annotation. For example:

In turtle:

.. code-block:: turtle

    MYO:123456 owl:deprecated true .

In OBO Format:

.. code-block:: yaml

    id: MYO:123456
    is_obsolete: true

You can query for all obsolete entities in an ontology using the `obsoletes<https://incatools.github.io/ontology-access-kit/cli.html#runoak-obsoletes>`_ command:

.. code-block:: bash

    $ runoak -i myontology.db obsoletes

In python, this is provided in the :ref:`BasicOntologyInterface`:

.. code-block:: python

    ont = get_implentation_from_shorthand("myontology.db")
    for entity in ont.obsoletes():
        print(entity)

For ontologies that are part of OBO, additional conventions apply. These conventions
are not yet fully standardized within OMO:

- obsolete entities should not be in the signature of any logical axiom

    - note that some older ontologies include obsolete classes as a subclass of an ObsoleteClass node
    - this is not treated in any special way in OAK

- obsolete entities should be accompanied by metadata that provides additional context for humans and machines

    - a `term replaced by<http://purl.obolibrary.org/obo/IAO_0100001>`_ annotation indicates where an automatic replacement can be made
    - a `consider<http://www.geneontology.org/formats/oboInOwl#>`_ annotation indicates potential replacements that should be manually evaluated

In OAK, this can be retrieved like any other metadata using the entity_metadata methods from :ref:`BasicOntologyInterface`.

On the command line:

.. code-block:: bash

    runoak -i sqlite:obo:go entity_metadata GO:0000005

Or for all obsolete entities:

.. code-block:: bash

    runoak -i sqlite:obo:go entity_metadata .is_obsolete

