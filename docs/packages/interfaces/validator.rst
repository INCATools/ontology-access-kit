.. _validator_interface:

Validator Interface
--------------------

The Validator Interface provides access to a number of different validation operations over ontologies.

The notion of validation in OAK is intentionally very flexible, and may encompass:

 * *Schema* validation, for example, checking definitions are strings and have 0..1 cardinality.
 * *Logical* validation, using a reasoner.
 * *Lexical* validation, for example, ensuring there are no spelling errors
 * *Stylistic* validation, against a style guide
 * *Content* validation, checking the content of the ontology against domain knowledge or other ontologies.

Different adapters may implement different portions of this.

Schema Validation
~~~~~~~~~~~~~~~~~

The core validate method is configured using a *metadata schema*. The default one used is:

- `Ontology Metadata <https://w3id.org/oak/ontology-metadata>`_

This is specified using LinkML which provides an expressive way to state constraints on metadata elements,
such as :ref:`AnnotationProperty` assertions in ontologies. For example, this schema states that definition
is *recommended* (not required), and that it is single-valued.

Different projects may wish to configure this - it is possible to pass in a different or modified schema

For more details see `this howto guide <https://incatools.github.io/ontology-access-kit/howtos/validate-an-obo-ontology>`_

.. warning::

    Currently only implemented for :ref`sql_implementation`

LLM-based validation
~~~~~~~~~~~~~~~~~~~~

See :ref:`use_llms`


.. currentmodule:: oaklib.interfaces.validator_interface
                   
.. autoclass:: ValidatorInterface
    :members:
