.. _faq:

Frequently Asked Questions
==========

This is a list of Frequently Asked Questions about OAK.  Feel free to
suggest new entries!

.. warning::

    This FAQ is still quite incomplete!

.. _how:

How do I...
-----------

... Install OAK
   See :ref:`tutorial01` of the tutorial.

... get all ancestors of a term?
   On the command line you can use the commands ``ancestors``, ``tree``, ``viz``, all of which are
   variants of fetching and displaying ancestors.
   In programs you can use :ref:`obograph_interface`

... Contribute code
   Please consult the `CONTRIBUTING.md <https://github.com/INCATools/ontology-access-kit/blob/main/.github/CONTRIBUTING.md>`_ guide

.. _whatis:

What is...
-----------

OAK for
    OAK is for both technical and non-technical users of ontologies. Non-technical users can use the :ref:`cli` to
    query ontologies in a variety of ways. Technical users can write Python code that uses the OAK library to
    perform ontology-related tasks, ranging from basic lookup, search, graph traversals, validation, data annotation,
    mapping, and OWL processing.

An iterator
    See :term:`Iterator` in the glossary

.. _usingwith:

Using OAK with...
--------------------

The Command Line
    OAK provides a fully-featured command line interface. See :ref:`tutorial08` of the tutorial.

Bioportal
    OAK can be used to query any ontology in Bioportal - or many of the Portals in the OntoPortal alliance.
    See :ref:`bioportal_implementation`.

OLS
    OAK can be used to query any ontology in OLS.
    See :ref:`ols_implementation`.

SQLite
    OAK can query any SQL database that conforms to the :term`Semantic SQL` standard. SQLite is a database
    system that works directly with files rather than through a database management system. It is frequently
    the most performant way to work with ontologies in OAK, as there is no parsing involved.
    See :ref:`tutorial08`.

.. _cli_faq:

Command Line
------------

What do the codes "i" and "p" mean?
    Many commands take a :code:`--predicates` option, the value is a comma separated list of CURIEs.
    You can use "i" as a shortcut for is_a (rdfs:subClassOf) and "p" as a shortcut for part_of (BFO:0000050)

Troubleshooting
---------------

... Why do I get a "Error: No such option: -i" message
    The :code:`--input` or :code:`-i` option must come *before* the subcommand name. This is because
    the input option is one of the few options that are shared across *all* subcommands.
    For example, you should write :code:`runoak -i my-ont.owl lexmatch -o results.sssom.tsv`

... How do I get a bioportal API key
    See the instructions on :ref:`bioportal_implementation`.

... My OBO Format file won't parse
    The default parser used for obo files is :term:`Pronto`. Pronto strictly enforces obo format syntax rules, and
    not all ontologies conform. To get around this, current best practice is to convert the obo to owl, and then
    work with either owl or sqlite files. Guidance may change on this in the near future as we make this easier.

... It takes a long time to load my OWL file
    By default, rdflib is used to parse OWL files, and this is known to be slow. If fast loading is important, we
    recommend you use sqlite that is converted from the OWL.
