SQL Database Implementation
===========================

This wraps either a local or remote SQL Database

The schema is assumed to follow:

- [semantic-sql](https://github.com/cmungall/semantic-sql/)

This uses the rdftab library to build an RDF-level `statements` table, on which numerous SQL Views
are layered, providing higher level access

Code
----

.. currentmodule:: obolib.implementations.sqldb.sql_implementation
                   
.. autoclass:: SqlImplementation
    :members: create

SQL Alchemy ORM Model
---------------------

We use the SQLA Models from the [semantic-sql](https://github.com/cmungall/semantic-sql/) project.

This is under-the-hood and users of obolib don't need to know the details. However, if you ever need to
craft a custom complex query this can provide a useful way to do this.

.. currentmodule:: obolib.implementations.sqldb.model
                   
.. autoclass:: Statements
.. autoclass:: Edge
