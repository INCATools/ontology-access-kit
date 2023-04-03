.. ontobee:

Ontobee Adapter
===============

Specializes the :ref:`sparql` implementation to allow access for ontologies on the `Ontobee <https://www.ontobee.org/>`_ linked data server.

ntobee is the default linked data server for most OBO Foundry library ontologies. Ontobee has also been used for many non-OBO ontologies.

Initialization
--------------

Access to all ontologies on Ontobee is via a selector with syntax :code:`ontobee:` (i.e. specify the ontobee scheme with no slug)

To access a specific ontology on ontobee follow the scheme with the ontology ID (all in lowercase). E.g.

.. code ::

   runoak -i ontobee:mp COMMAND [COMMAND-OPTIONS]


Code
----

.. currentmodule:: oaklib.implementations.ontobee.ontobee_implementation
                   
.. autoclass:: OntobeeImplementation
