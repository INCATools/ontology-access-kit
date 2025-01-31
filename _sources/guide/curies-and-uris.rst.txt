.. _curies_and_uris:

Identifying entities: CURIEs and URIs
====================================

Prefix maps
-----------

Every :term:`Entity` in OAK has a unique :term:`Identifier`. OAK is consistent with semantic
web formalisms where everything is identified by an :term:`IRI`, but in OAK these are
typically compressed into a :term:`CURIE`, using a :term:`Prefix Map`.

For example, to reference the concept of "heart" in the `Uberon <http://obofoundry.org/ontology/uberon.html>`_ ontology,
we use the curie ``UBERON:0000948``. This is a compressed form of the URL `<http://purl.obolibrary.org/obo/UBERON_0000948>`_,
using the :term:`OBO Foundry` prefix map.

On the command line, most OAK commands take CURIEs or lists of CURIEs as inputs (although primary labels and
queries can also be supplied). For example:

.. code-block:: bash

    $ runoak -i ubergraph info UBERON:0000948
    UBERON:0000948 ! heart

Under the hood, on the backend (in this case, :ref:`ubergraph_implementation`), the concept is stored
as a full URI.

Similarly, in Python:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> ont = get_adapter('ubergraph:')
    >>> id = "UBERON:0000948"
    >>> print(ont.label(id))
    heart
    >>> print(ont.curie_to_uri(id))
    http://purl.obolibrary.org/obo/UBERON_0000948

OAK uses the `prefixmaps <https://github.com/linkml/prefixmaps>`_ package to manage CURIEs and URIs,
and by default will use a certain set of standard prefixmaps, including the OBO one,
as well as a linked data prefix map, which provides a set of standard prefixes for non-OBO
resources such as schema.org.

Querying prefixmaps
-------------------

You can get a list of all prefixes known to OAK using the ``prefixes`` command:

.. code-block:: bash

    $ runoak prefixes
    ...
    PO	http://purl.obolibrary.org/obo/PO_
    PORO	http://purl.obolibrary.org/obo/PORO_
    ...
    owl	http://www.w3.org/2002/07/owl#
    skos	http://www.w3.org/2004/02/skos/core#
    ...


You can also query the prefixmap for a particular prefix or set of prefixes:

.. code-block:: bash

    $ runoak prefixes UBERON CL oio skos schema

This will return a table:

.. csv-table:: Example prefixes
    :header: prefix, uri

    UBERON,    http://purl.obolibrary.org/obo/UBERON_
    CL,        http://purl.obolibrary.org/obo/CL_
    oio,       http://www.geneontology.org/formats/oboInOwl#
    skos,      http://www.w3.org/2004/02/skos/core#
    schema,    http://schema.org/

See the `prefixes <https://incatools.github.io/ontology-access-kit/cli.html#runoak-prefixes>`_ command for more details.

Non-default prefixmaps
----------------------

For most purposes, the default prefixmap should suffice.

You can also choose to override the default prefixmap with your own, using the ``--prefix`` or ``--named-prefix-map`` options.

In python this can be done by accessing the prefixmap directly:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> soil_oi = get_adapter("tests/input/soil-profile.skos.nt")
    >>> soil_oi.prefix_map()["soilprofile"] = "http://anzsoil.org/def/au/asls/soil-profile/"
    >>>
    >>> # trivial example: show all CURIEs and labels
    >>> for entity, label in soil_oi.labels(soil_oi.entities()):
    ...        print(f"{entity} ! {label}")


Structure of identifiers
------------------------

OAK doesn't impose any expectations on the structure of identifiers.

For OBO ontologies, all identifiers should conform to the OBO identifier pattern,
which is the prefix (typically all uppercase) followed by a local identifier which is
all numeric (typically zero-padded with 7 digits). However, this is not a requirement for OAK.

Many semantic web ontologies such as schema.org use "semantic" URIs that a human
can understand. These can be used in the same way, as can be seen in the following example.

First, download schema.org (as RDF):

.. code-block:: bash

    $ wget https://schema.org/version/latest/schemaorg-all-http.ttl -O tests/output/schema.rdf

Then, query it on the command line:

.. code-block:: bash

    $ runoak --prefix schema=http://schema.org/ -i tests/output/schema.rdf relationships schema:Person

This will give a table:

.. csv-table:: Query results
    :header: subject, subject_label, predicate, predicate_label, object, object_label

    schema:Person, Person, rdfs:subClassOf, None, schema:Thing, Thing

Note that the URI is contracted to a prefixed ID for terms like `Person` and `subClassOf`

Further reading
--------------

* `OBO Foundry Identifiers <https://obofoundry.org/id-policy>`_
