.. association_provider_interface:


Association Provider
==============

Synopsis
--------

.. code:: python

TODO

About
-----

This interface provides a collection of methods for querying associations.

Associations (also known as annotations) connect data elements or entities to
an ontology class. Examples of associations include:

- Gene associations to terms in ontologies like GO, Mondo, Uberon, HPO, MPO, CL
- Associations between spans of text and ontology entities

Data models and file formats include:

- The GO GAF and GPAD formats.
- The HPOA association file format.
- KGX (Knowledge Graph Exchange).
- The W3 `Open Annotation <https://www.w3.org/TR/annotation-model/>`_ (OA) data model

The OA datamodel considers an annotation to be between a *body* and a *target*:

.. image:: https://www.w3.org/TR/annotation-vocab/images/examples/annotation.png

Implementations
---------------

Command Line Use
----------------

.. code::

   runoak -i foo.db associations UBERON:0002101


Code
----

Example
^^^^^^^

Autodoc
^^^^^^^


.. currentmodule:: oaklib.interfaces.association_provider_interface
                   
.. autoclass:: AssociationProviderInterface
    :members:
