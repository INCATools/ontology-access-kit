.. _tutorial07:

Part 7: SQLite files
=============

The most efficient way to work with OAK is through SQLite files. OAK accepts SQLite files that follow the `Semantic SQL <https://github.com/INCATools/semantic-sql>`_ schema.

The :ref:`sql_implementation` wraps SQLite or any relational database.

.. hint::

    You may also want to try the `Semantic-SQL tutorial <https://github.com/INCATools/semantic-sql/blob/main/notebooks/SemanticSQL-Tutorial.ipynb>`_

Download a SQLite file
----------------

You can download ready made SQLite files for any :term:`OBO` Library ontology

For example: the Cell Ontology (CL) is available from https://s3.amazonaws.com/bbop-sqlite/cl.db.gz

Example
^^^^^

.. code-block::

    wget https://s3.amazonaws.com/bbop-sqlite/cl.db.gz
    gzip -d cl.db.gz
    runoak -i cl.db relationships "enteric neuron"

This will show all relationships centered around the subject of CL:0007011:

.. csv-table:: Ancestor statistics
    :header: id, label, visits, distance

    subject,predicate,object,subject_label,predicate_label,object_label
    CL:0007011,BFO:0000050,UBERON:0002005,enteric neuron,part of,enteric nervous system
    CL:0007011,RO:0002100,UBERON:0002005,enteric neuron,has soma location,enteric nervous system
    CL:0007011,RO:0002202,CL:0002607,enteric neuron,develops from,migratory enteric neural crest cell
    CL:0007011,rdfs:subClassOf,CL:0000029,enteric neuron,None,neural crest derived neuron
    CL:0007011,rdfs:subClassOf,CL:0000107,enteric neuron,None,autonomic neuron

.. hint::

    OAK will automatically treat anything with ``.db`` as a sqlite database

You can be more explicit and force the sqlite adapter to be used, regardless of suffix using a ``sqlite`` :ref:`selector`:

.. code-block::

    wget https://s3.amazonaws.com/bbop-sqlite/cl.db.gz
    gzip -d cl.db.gz
    runoak -i sqlite:cl.db relationships "enteric neuron"

Fetching ready-made SQLite files
^^^^^

You can also specify that the sqlite file should be loaded from the repository:

.. code-block::

    runoak -i sqlite:obo:pato search t~shape

This will download the pato.db sqlite file once, and cache it.

PyStow is used to cache the file, and the default location is ``~/.data/oaklib``.

By default, a cached SQLite file will be automatically refreshed (downloaded
again) if it is older than 7 days. For details on how to alter the behavior of
the cache, see the :ref:`Cache Control` section in the CLI documentation.

Building your own SQLite files
-------------------

You can use the ``semsql`` command that should be pre-installed with OAK

There are two paths

- using ODK docker
- without docker, with dependencies pre-installed

With docker
^^^^^^^^^^

If you have an OWL file in ``./path/to/obi.owl``

Then you can do this:

.. code-block::

   docker run -w /work  -v `pwd`:/work --rm -ti obolibrary/odkfull:dev semsql make path/to/obi.db

This will do a one-time build of obi.db, using the ODK docker. You will need Docker installed (but you don't need to do anything else)

You can then query the file as normal:

.. code-block::

   runoak -i path/to/obi.db info assay

.. warning::

   for this to work, the OWL file **must** be in RDF/XML. Also, imports merging will NOT be done by default,
   please merge in advance using ROBOT if this is your desired behavior.

.. note::

   The recipe above works for any OWL file in a descendant of your current folder.
   If you wish to use a file outside of your current folder, then change the
   option from ``-v `pwd`:/work`` to ``-v /path/to/:/work/``

Without docker
^^^^^^^^^

**Prerequisites**

For this to work you will need to install the following dependencies and ensure they're loaded in your `PATH`.

1. `relation-graph <https://github.com/balhoff/relation-graph#installation>`_

2. `rdftab <https://github.com/ontodev/rdftab.rs#installation>`_  

3. `riot` - On MacOS, can install using `HomeBrew <https://brew.sh/>`_ via: ``brew install jena``

Then, run:

.. code-block::

   semsql make path/to/obi.db

Consult the `SemSQL docs <https://github.com/INCATools/semantic-sql>`_ for more details.

In future we hope to wrap these more seamlessly in Python.

Validating an ontology
-----------------

the SQLite implementation is the most efficient way to validate an ontology

.. code-block::

    runoak -i sqlite:obo:cl validate

Other RDBMSs
------------

We avoid SQLite specific features so in theory OAK should work with any RDBMS that follows the semantic-sql schema,
but currently SQLite is the focus of development and testing

Python ORM
----------

OAK abstracts away the details of the underlying database and ways of accessing it, but for some purposes you
may wish to write direct SQL or use the ORM layer. Consult SemSQL docs for details.
