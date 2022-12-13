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

- Implementations: How to create a connector object that can talk to a backend or work with a particular file format
- Interfaces: How to perform operations on a basic ontology interface, regardless of the backend

Code the first example
----------

We are going to use an example from the :ref:`basic_ontology_interface`, using a :ref:`pronto` implementation.

As preparation, we expect ``fbbt.obo`` to exist in the top level directory.

:code:`fbbt.obo` can be downloaded here: http://purl.obolibrary.org/obo/fbbt.obo

Then create a python program: ``my_oak_demo/demo.py`` and add the following:

.. code-block:: python

    oi = get_implementation_from_shorthand("fbbt.obo")

Next, let's perform some basic lookup operations on the ontology:

.. code-block:: python

    rels = oi.outgoing_relationship_map('FBbt:00004751')

    for rel, parents in rels.items():
        print(f'  {rel} ! {oi.label(rel)}')
        for parent in parents:
            print(f'    {parent} ! {oi.label(parent)}')

We first obtain all of the outgoing relationships from the 
FBbt class for "wing vein", which has the id of ``FBbt:00004751``.

Next, we iterate through all the relationships, and print the labels for 
both the relationship and the connected entities (here named ``parents``) using
the ``label()`` method of :ref:`basic_ontology_interface` object.

.. note::

   behind the scenes, the :ref:`pronto` implementation is being used, but as an application
   programmer you shouldn't care about the specific implementation - code to the interface.
   The beauty of OAK is that the *same code* will work with other backends!

You should see something similar to:

.. code-block:: python

    rdfs:subClassOf ! subClassOf
      FBbt:00007245 ! cuticular specialization
    RO:0002202 ! develops_from
      FBbt:00046035 ! presumptive wing vein
    BFO:0000050 ! part_of
      FBbt:00006015 ! wing blade

Extending the example
---------

Next we will write a function that takes as input

- an ontology handle
- a term ID (CURIE)

And writes out information about that term

.. code-block:: python

    def show_info(oi: BasicOntologyInterface, term_id: str):
        print("ID: {term_id}")
        print("Name: {oi.label(term_id)}")
        print("Definition: {oi.definition(term_id)}")
        for rel, parent in oi.outgoing_relationships(term_id):
            print(f'  {rel} {oi.label(rel)} {parent} {oi.label(parent)}')
