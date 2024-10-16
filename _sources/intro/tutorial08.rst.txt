.. _tutorial08:

Part 8: Applying Changes to Ontologies
=============

.. warning::

    Apply changes is an experimental feature. This documentation is provided for alpha testers
    to try out existing functionality. Currently only a fraction of the KGCL specification is
    implemented.

OAK allows various kinds of changes to be applied to ontologies, including:

- Changing :term:`Names<Name>` of concepts
- Adding or removing edges
- Obsoleting concepts
- ...

Like most aspects of OAK, all changes in OAK conform to a :term:`Datamodel`. The datamodel used by OAK is :term:`KGCL`.

About KGCL
----------

KGCL is a datamodel for describing changes to ontologies at a high level.

The KGCL datamodel can be expressed in different forms:

- Natively, as YAML or JSON documents
- As RDF
- As Python Objects
- Using a Domain Specific Language (DSL) optimised for easy reading and writing

OAK uses KGCL objects to communicate desired changes to an ontology. This is an example of the `Command Pattern <https://en.wikipedia.org/wiki/Command_pattern>`_.

For example, rather than simply calling a method ``obsolete_class(term: CURIE)``, we instead:

1. Create a :ref:`ClassObsoletion` object
2. Pass that object to an implementation of the :ref:`PatcherInterface`

While this involves an additional step, this pattern offers a number of advantages

- proposed changes can be created in queue and deployed at the appropriate time in the future
- a single extensible interface can be used, and new operations can be created without changing the interface

Command Line
-----------

A subset of commands *mutate* the ontology specified via the ``--input`` option. This includes

- set-obsolete
- migrate-curies
- ...

With a mutation command, there are a number of different options for how changes are persisted:

- write in place, using the general option ``--autosave``
- saving to a new resource using the general option ``--save-to``
- exporting to a different kind of resource or format using a command-specific ``--output``

The behavior of these options may vary depending on the input, and some may be inapplicable.

For example, if the input is an external triplestore such as :term:`Ontobee` or :term:`Ubergraph`, or
an external read-only API like :term:`BioPortal` or :term:`OLS` then saving in place is not allowed.

Example: Sqlite3
^^^^^^^

We assume here that we have a local sqlite3 file called ``go-edit.db`` and we want to obsolete
a concept "nucleus".

To do this in place:

.. code-block::

    runoak --autosave -i sqlite:go-edit.db set-obsolete nucleus

This will apply the obsoletion changes directly and update the input file

To instead save to a different sqlite file:

.. code-block::

    runoak --save-to sqlite:go-edit-out.db -i sqlite:go-edit.db set-obsolete nucleus

Note that *exports* are not currently implemented for sqlite

Example: OBO Files
^^^^^^^

To make edits and export to a new file:

.. code-block::

    runoak  -i go-edit.obo set-obsolete nucleus -o go-edit-out.obo -O obo

This will apply the obsoletion changes in memory and then save results to a separate obo file.
