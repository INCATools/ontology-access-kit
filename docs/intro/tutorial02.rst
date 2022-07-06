Part 2: Basic Python
=====================

For this tutorial some basic Python knowledge is assumed.

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

We are going to use an example from the :ref:`BasicOntologyInterface`, using a :ref:`pronto` implementation.


As preparation, we expect ``fbbt.obo`` to exist in the top level directory.

:code:`fbbt.obo` can be downloaded here: http://purl.obolibrary.org/obo/fbbt.obo

Then create a python program: ``my_oak_demo/demo.py`` and add the following:

.. code-block:: python

    from oaklib.resource import OntologyResource
    from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
    resource = OntologyResource(slug='fbbt.obo', local=True)
    oi = ProntoImplementation(resource)

- We first import the general ``OntologyResource`` implementation which allows us to declare where to get the ontology from.
- We then load this resource using the ``ProntoImplementation``, which allows us to perform all operations on the resource that we could do with `pronto <https://github.com/althonos/pronto>`_.

.. warning::

    The way in which a connection is made to a backend may change in the near future!

Next, let us use :term:`Pronto` to actually query the ontology:

.. code-block:: python

    rels = oi.get_outgoing_relationships_by_curie('FBbt:00004751')

    for rel, parents in rels.items():
        print(f'  {rel} ! {oi.get_label_by_curie(rel)}')
        for parent in parents:
            print(f'    {parent} ! {oi.get_label_by_curie(parent)}')

We first obtain all of the outgoing relationships from the 
FBbt class for "wing vein", which has the id of ``FBbt:00004751``.

Next, we iterate through all the relationships, and print the labels for 
both the relationship and the connected entities (here named ``parents``) using
the ``get_label_by_curie()`` method of the ``ProntoImplementation`` object.


You should see something similar to:

.. code-block:: python

    rdfs:subClassOf ! subClassOf
      FBbt:00007245 ! cuticular specialization
    RO:0002202 ! develops_from
      FBbt:00046035 ! presumptive wing vein
    BFO:0000050 ! part_of
      FBbt:00006015 ! wing blade

