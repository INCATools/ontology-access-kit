.. _implementations:

Implementations
===============

Implementations implement one or more :ref:`interfaces`

The most mature implementations are:

- Ubergraph: wraps the public ubergraph endpoint
- Pronto: uses the pronto lib (which itself uses fastobo) to load local obo, rdf/xml owl, or obojson files
- Sql: see [semantic-sql](https://github.com/cmungall/semantic-sql/)

.. warning ::

    Currently numerous methods are not implemented!

Core
----

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   obofiles
   sqldb
   robot
   skos
   ols
   bioportal

Remote Sparql
-------
             
.. toctree::
   :maxdepth: 3
   :caption: Contents:

   sparql
   ubergraph
   ontobee


Portals
-------
             
.. toctree::
   :maxdepth: 3
   :caption: Contents:

   ols
   bioportal
   
