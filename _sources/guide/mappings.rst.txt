.. _mappings:

Mappings and Cross-References
=============================

Mappings are a way of connecting the same or similar concepts in different ontologies.
Historically, mappings have been handled very differently depending on the ontology or community:

- for OBO Format ontologies, the ``xref`` tag is used, which corresponds to ``oboInOwl:hasDbXref``
- for many linked data resources, ``owl:sameAs`` is used
- for some ontologies, ``owl:equivalentClass`` is used
- in other cases, SKOS triples may be used
- sometimes mappings are distributed as simple CSVs, outside the ontology

In addition to the basic vocabulary used, the data models for mappings differs a lot.

SSSOM
-----

The `Simple Standard for Sharing Ontological Mappings <https://w3id.org/sssom>` is a standard
for ontology mappings. It provides both a standard TSV/CSV format, and a standard way of encoding mappings in ontologies.

Mappings in OAK
---------------

To see all mappings for a concept or concept, you can use the mappings command:

.. code-block:: bash

    runoak -i sqlite:obo:uberon mappings brain

This will return YAML conforming to SSSOM by default. Like all OAK
commands, this also allows for other output formats.

To get this as SSSOM TSV:

.. code-block:: bash

    runoak -i sqlite:obo:uberon mappings brain --output-type sssom

Under the hood, OAK will query using standard mapping predicates, including
those from SKOS and OboInOwl.

Using the Python interface, there are two levels in which to access mappings.

- The :ref:`basic_ontology_interface` provides a simple interface that exposes mappings as simple tuples
- The :ref:`mapping_provider_interface` provides access to the full SSSOM model


Further reading
---------------

-
- `Mappings in SSSOM <https://oboacademy.github.io/obook/tutorial/sssom-manual/>`_