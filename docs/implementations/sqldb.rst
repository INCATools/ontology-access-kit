.. _sql_implementation:

SQL Database Adapter
====================

This wraps either a local or remote SQL Database

The schema is assumed to follow:

- `Semantic-SQL <https://github.com/incatools/semantic-sql>`_

This uses the rdftab library to build an RDF-level `statements` table, on which numerous SQL Views
are layered, providing higher level access

Initialization
-------------

If you omit a scheme and specify a filesystem path ending with :code:`.db` then the SqlDatabase implementation is selected, with
sqlite as a sub-scheme.

You can explicitly specify a sqlite database via a selector :code:`sqlite:path/to/sqlitefile.db`

Code
----

.. currentmodule:: oaklib.implementations.sqldb.sql_implementation
                   
.. autoclass:: SqlImplementation
    :members: create

SQL Alchemy ORM Model
---------------------

We use the SQLA Models from the `semantic-sql <https://github.com/incatools/semantic-sql>`_ project.

This is under-the-hood and users of oaklib don't need to know the details. However, if you ever need to
craft a custom complex query this can provide a useful way to do this.

.. currentmodule:: semsql.sqla.semsql
                   
.. autoclass:: Statements
.. autoclass:: Edge
.. autoclass:: EntailedEdge
