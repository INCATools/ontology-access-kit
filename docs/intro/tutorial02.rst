Part 2: Basic Python
=====================

.. note::

  This part of the tutorial will walk through how to use basic OAK functionality within a Python program. We will
  be making use of lightweight obo format files - future parts of this tutorial will instruct on how to use other
  formats and remote endpoints.

.. important::

    For this tutorial some basic Python knowledge is assumed. Familiarity with object-oriented concepts
    is also useful.

Install Poetry
--------------

For this section we are going to use `Poetry <https://python-poetry.org/>`_ to set up a project. If you are an experienced
developer feel free to adapt these instructions to your favored package manager, otherwise we advise sticking closely to
the instructions.

Create a new project
--------------

.. code-block::

    poetry new --src -n my-oak-demo
    cd my-oak-demo
    poetry add oaklib

Basic Concepts
-------------

The two basic concepts you will learn here are:

- Adaptors (Implementations): How to create a connector object that can talk to a backend or work with a particular file format
- Interfaces: How to perform operations on a basic ontology interface, regardless of the backend

Code the first example
----------

We are going to use an example from the :ref:`basic_ontology_interface`, using the Cell Ontology (CL).

Then create a python program: ``my_oak_demo/demo.py`` and add the following:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:cl")

Next, let's perform some basic lookup operations on the ontology:

.. code-block:: python

    >>> print(adapter.label('CL:4023017'))
    sst GABAergic cortical interneuron
    >>> print(adapter.definition('CL:4023017'))
    A GABAergic neuron located in the cerebral cortex that expresses somatostatin (sst)

You can look up the methods above in the documentation for the :ref:`basic_ontology_interface`

Now we will query for outgoing relationships from the sst GABAergic cortical interneuron:

.. code-block:: python

    >>> for s, p, o in adapter.relationships(['CL:4023017']):
    ...     print(s, p, o)
    CL:4023017 RO:0002292 PR:000015665
    CL:4023017 rdfs:subClassOf CL:0010011

Extending the example
---------

Next we will write a function that takes as input

- an ontology :term:`adapter`
- a term ID (term:`CURIE`)

And write out information about that term

.. code-block:: python

    >>> from oaklib import BasicOntologyInterface
    >>> def show_info(adapter: BasicOntologyInterface, term_id: str):
    ...     print(f"ID: {term_id}")
    ...     print(f"Name: {adapter.label(term_id)}")
    ...     print(f"Definition: {adapter.definition(term_id)}")
    ...     for rel, parent in adapter.outgoing_relationships(term_id):
    ...         print(f'  {rel} ({adapter.label(rel)}) {parent} ({adapter.label(parent)})')

We can now try this:

.. code-block:: python

    >>> show_info(adapter, 'CL:4023017')
    ID: CL:4023017
    Name: sst GABAergic cortical interneuron
    Definition: A GABAergic neuron located in the cerebral cortex that expresses somatostatin (sst)
      RO:0002292 (expresses) PR:000015665 (somatostatin)
      rdfs:subClassOf (None) CL:0010011 (cerebral cortex GABAergic interneuron)