.. _robot_template_implementation:

ROBOT Template Adapter
=============

.. warning::

    This is experimental and incomplete.

This is an extension of the abstract :ref:`TabularInterface` adapter that provides
access to a collection of `ROBOT templates <http://robot.obolibrary.org/template>`_.

Note that it does *NOT* use the ROBOT tool itself to access these, it uses custom
code that only implements a portion of the spec.

One of the main driving use cases here is to enable KGCL commands with ontologies that use ROBOT
templates.

For example, the `OBI templates folder on GitHub <https://github.com/obi-ontology/obi/tree/016ca67c7e6f31a048780cee56afde24d4af7125/src/ontology/templates>`_
contains a collection of ROBOT templates.

- assays.tsv
- biobank-specimens.tsv
- ...

Assuming these are in a local path ``my/path/templates``, you can use a selector:

.. code-block:: bash

    runoak -i robottemplate:my/path/templates COMMAND ...

Or in python:

.. code-block:: python

    from oaklib import get_adapter
    adapter = get_adapter('robottemplate:my/path/templatestemplates')

Note that this does NOT trigger compilation of the templates into OWL - this implementation works
on the templates as a collection of TSVs, facilitating update operations.

Command Line Examples
----------------------

From here we assume your templates are in a local folder ``./templates``.

Basic operations
~~~~~~~~~~~~~~~~

Currently very few operations are supported, but you can do basic things like:

.. code-block:: bash

    runoak -i robottemplate:templates info OBI:0002516

Returns:

- OBI:0002516 ! brain specimen

Or limited search:

    runoak -i robottemplate:templates info l~brain

Returns:

- OBI:0002516 ! brain specimen
- OBI:0003357 ! brain region atlas image data set
- ...

Applying KGCL commands
~~~~~~~~~~~~~~~~~~~~~~~

You can also apply KGCL commands:

.. code-block:: bash

    runoak -i robottemplate:templates apply \
      "rename OBI:0002516 from 'brain specimen' to 'brain sample'" -o new_templates

This will create a new copy of all templates in ``new_templates``, with the label
column modified in biobank-specimens.tsv

.. warning::

    only a small subset of KGCL is implemented so far.