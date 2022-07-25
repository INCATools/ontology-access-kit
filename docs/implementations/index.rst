.. _implementations:

Implementations
===============

Implementations implement one or more :ref:`interfaces`

The most mature implementations are:

- Ubergraph: wraps the public ubergraph endpoint
- Pronto: uses the pronto lib (which itself uses fastobo) to load local obo, rdf/xml owl, or obojson files
- Sql: see `semantic-sql <https://github.com/incatools/semantic-sql/>`_

.. warning ::

    Currently numerous methods are not implemented!

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   pronto
   sqldb
   robot
   funowl
   skos
   ols
   bioportal
   sparql
   ubergraph
   ontobee
   ols
   gilda
   aggregator
