.. _validator_interface:

Validator Interface
--------------------

.. warning ::

   Currently the main validator methods are only implemented for :ref:`SqlDatabaseImplementation`

The validate method is configured using a *metadata schema*. The default one used is:

- `Ontology Metadata <https://incatools.github.io/ontology-access-kit/datamodels/ontology-metadata/index.html>`_

This is specified using LinkML which provides an expressive way to state constraints on metadata elements,
such as :ref:`AnnotationProperty` assertions in ontologies. For example, this schema states that definition
is *recommended* (not required), and that it is single-valued.

Different projects may wish to configure this - it is possible to pass in a different or modified schema

For more details see `this howto guide <https://incatools.github.io/ontology-access-kit/howtos/validate-an-obo-ontology>`_


.. currentmodule:: oaklib.interfaces.validator_interface
                   
.. autoclass:: ValidatorInterface
    :members:
