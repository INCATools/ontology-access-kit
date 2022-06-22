.. _tutorial07:

Part 7: SQLite files
=============

The most efficient way to work with OAK is through SQLite files. OAK accepts SQLite files that follow the `Semantic SQL <https://github.com/INCATools/semantic-sql>`_ schema.

The :ref:`SqlImplementation` wraps SQLite or any relational database.


Download a SQLite file
----------------

You can download ready made SQLite files for any :term:`OBO` Librray ontology

For example: https://s3.amazonaws.com/bbop-sqlite/hp.db

You can also use the ``obosqlite`` ontology selector:

.. code-block::

    runoak -i sqlite:obo:pato search t~shape

This will download the pato.db sqlite file once, and cache it

.. warning::

    The ready-made SQLite files are not made at regular intervals

Building your own SQLite files
-------------------

You can use the ``semsql`` command that should be pre-installed with OAK

There are two paths

- using ODK docker
- without docker, with dependencies pre-installed

With docker
^^^^^^^^^^

If you have an OWL file in ``path/to/obi.owl``

Then you can do this:

.. code-block::

   semsql make --docker path/to/obi.db

This will do a one-time build of obi.db, using the ODK docker. You will need Docker installed (but you don't need to do anythiong else)

You can then query the file as normal:

.. code-block::

   runoak -i path/to/obi.db info assay

.. warning::

   for this to work, the OWL file **must** be in RDF/XML. Also, imports merging will NOT be done by default,
   please merge in advance using ROBOT if this is your desired behavior.

Without docker
^^^^^^^^^

.. code-block::

   semsql make path/to/obi.db

However, for this to work you will need two dependencies loaded and on your path

- rdftab
- relation-graph

Consult the `SemSQL <https://github.com/INCATools/semantic-sql>` docs for more details.

In future we hope to wrap these more seamlessly in Python

Other RDBMSs
------------

We avoid SQLite specific features so in theory OAK should work with any RDBMS that follows the semantic-sql schema,
but currently SQLite is the focus of development and testing

Python ORM
----------

OAK abstracts away the details of the underlying database and ways of accessing it, but for some purposes you
may wish to write direct SQL or use the ORM layer. Consult SemSQL docs for details.