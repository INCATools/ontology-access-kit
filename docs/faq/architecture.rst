.. _faq_architecture:

FAQ: Architecture and Design
============================

What is an interface?
---------------------

OAK is designed so that application developers can focus on *coding to an interface* without
worrying about the details of the implementation.

For example, the following code will talk to the SQLite backend for CL to find all :term:`IS_A`
descendants of "neuron", and show them alongside their labels:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> for d in adapter.descendants("CL:0000540", predicates=[IS_A]):
    ...     print(d, adapter.label(d))
    <BLANKLINE>
    ...
    CL:0011103 sympathetic neuron
    ...

In this case, the developer does not need to know anything about the underlying implementation.
It could be SQL or a flat file.

In this case, the ``ancestors`` and ``label`` methods are both part of the :ref:`basic_ontology_imerface`

The actual implementation when ``sqlite:obo:cl`` is used as an input selector is the :ref:`sql_implementation`,
but the application developer doesn't need to know this.

What is a Data Model?
---------------------

A :ref:`Datamodel` is a way of structuring data for a particular domain. OAK takes a pluralistic
approach, and supports many different data models for different tasks. These are often coupled
with interfaces:

- :ref:`basic_ontology_interface` avoids data models and yields simple structures like lists of tuples
- :ref:`text_annotator_interface` uses the `<https://w3id.org/oak/text-annotator>`_ data model
- :ref:`mapping_provider_interface` uses the :term:`SSSOM` data model
- :ref:`class_enrichment_calculation_interface` uses the `<https://w3id.org/oak/class-enrichment>`_ data model
- :ref:`patcher_interface` uses the :term:`KGCL` data model
- :ref:`association_provider_interface` uses the `<https://w3id.org/oak/association>`_ data model
- :ref:`validator_interface` uses the `<https://w3id.org/oak/validation>`_
- ...

When used within Python, an object oriented structure is followed, where the different
attributes of the data model are accessed via ``.`` notation.

For example, :ref:`mapping_provider_interface` provides a method ``sssom_mappings`` which
yields :term:`Mapping` objects conforming to the SSSOM data model. A mapping object has fields like
``subject_id``:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("tests/input/go-nucleus.obo")
    >>> for mapping in adapter.sssom_mappings(["GO:0005886"], source="Wikipedia"):
    ...     print(mapping.subject_id, mapping.object_id)
    GO:0005886 Wikipedia:Cell_membrane

OAK uses a mixture of native an external data models.

Native data models have the OAK w3id namespace - for example, `<https://w3id.org/oak/class-enrichment>`_.

What is an iterator and why does OAK use them so much?
---------------------

OAK uses iterators in place of lists in a lot of places, in order to make the
code more scalable and more amenable to streaming.

See :term:`Iterator`.



