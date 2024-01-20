.. _faq_troubleshooting:

FAQ: Troubleshooting
====================

Why do I get a "Error: No such option: -i" message
--------------------------------------------------

The :code:`--input` or :code:`-i` option must come *before* the subcommand name. This is because
the input option is one of the few options that are shared across *all* subcommands.
For example, you should write :code:`runoak -i my-ont.owl lexmatch -o results.sssom.tsv`

How do I get a BioPortal API key?
---------------------------------

See the instructions on :ref:`bioportal_implementation`.

My OBO Format file won't parse
------------------------------

The default parser used for obo files is :term:`Pronto`. Pronto strictly enforces obo format syntax rules, and
not all ontologies conform. To get around this, current best practice is to convert the obo to owl, and then
work with either owl or sqlite files. Guidance may change on this in the near future as we make this easier.

My OWL file takes too long to load
----------------------------------

By default, rdflib is used to parse OWL files (via :ref:`sparql_adapter`), and this is known to be slow. If fast loading is important, we
recommend you use sqlite that is converted from the OWL, via :ref:`sql_adapter`.

My cached SQLite ontology is out of date
----------------------------------------

We use pystow to cache pre-made sqlite3 databases. Currently pystow does not have any
cache management capabilities - this means it is up to you to purge old copies.

For example, to purge a stale copy of the cl database:

.. code-block:: bash

    rm ~/.data/oaklib/cl.db*

Note it is necessary to delete both the ``.db`` file and the ``.db.gz`` file

I don't understand the interface/method I want to use
------------------------------------------------------

We are always striving to improve the documentation.

Please `file an issue <https://github.com/INCATools/ontology-access-kit/issues>`_ and we
fill try and improve the documentation based on your feedback.
