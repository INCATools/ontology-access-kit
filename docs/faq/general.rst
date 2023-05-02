.. _faq_general:

FAQ: General
==========

What is OAK?
------------

OAK is for both technical and non-technical users of ontologies. Non-technical users can use the :ref:`cli` to
query ontologies in a variety of ways. Technical users can write Python code that uses the OAK library to
perform ontology-related tasks, ranging from basic lookup, search, graph traversals, validation, data annotation,
mapping, and OWL processing.

Are there any tutorials for OAK?
--------------------------------

Yes! There are a few sources:

- The main :ref:`tutorial` on this site
- The OBO Academy OAK command line tutorial (`<https://doi.org/10.5281/zenodo.7708963>`_)
- The Monarch OAK tutorial for Python developers (`Video <https://www.youtube.com/watch?v=nVTWazO_Gu0>`_)

Are there runnable examples of how to use OAK?
----------------------------------------------

There are three main sources of examples:

- :ref:`notebooks`
- Python "docstrings" that are present throughout the :ref:`packages` documentation
- Unit tests, in the tests folder of the GitHub repo.

I am familiar with both Python and Ontologies. Where should I start?
--------------------------------------------------------------------

See the list of all methods in all interfaces, in the package documentation:

- :ref:`interfaces`



I find ontologies confusing. Is there a general guide to help me?
-----------------------------------------------------------------

Yes! See the :ref:`guide`.

Why is it called OAK?
---------------------

OAK stands for the Ontology Access Kit. The name was chosen to mirror a companion
package, the Ontology Development Kit (ODK), and also as a homage to Oakland, where
some of the OAK developers are based.

How do I install OAK?
---------------------

See :ref:`tutorial01` of the tutorial.

Can I use OAK if I don't know Python?
-------------------------------------

OAK provides a fully-featured command line interface. See :ref:`tutorial01` of the tutorial.

Once you have installed OAK (see above), you can use the command ``runoak`` to run any of
a large number of subcommands.

To get a full list, see:

.. code-block:: bash

    runoak --help

Typically you use OAK in combination with an ontology from some source, specified with a selector,
for example:

.. code-block:: bash

    runoak -i sqlite:obo:hp COMMAND OPTIONS... ARGUMENTS...

Can I contribute to OAK?
------------------------

Please consult the `CONTRIBUTING.md <https://github.com/INCATools/ontology-access-kit/blob/main/.github/CONTRIBUTING.md>`_ guide


Is OAK just for bio-ontologies?
-------------------------------

No, OAK can be used for any ontology, provided certain minimal conventions are followed:

- the ontology should be available in a standard format like OWL (OR: should be available in a portal such as an :term:`OntoPortal` portal)
- if the ontology uses non-standard properties for :term:`Annotations<Annotation>`, a mapping should be provided

Can OAK access ontologies in ontology portals such as MatPortal or BioPortal?
-----------------------------------------------------------------------------

Yes, OAK has a number of :term:`Adapters<Adapter>` that can "talk to" a remote endpoint provided that
endpoint speaks a standard API such as the :term:`OntoPortal` alliance API or the :term:`OLS` API.

See:

- :ref:`bioportal_implementation`
- :ref:`ols_implementation`

Note that not all OAK operations are supported for all endpoints. Some would be too expensive to do via
API calls.

Endpoints such as the :term:`BioPortal` API or the OLS excel in particular at tasks
such as :term:`Text Annotation`, where it is possible to run a text against a large bank
of ontologies without having to download any locally.

For example, on the command line:

.. code-block:: bash

    runoak -i bioportal: annotate "the quick brown fox"

Can OAK access ontologies in triplestores such as OntoBee or Ubergraph?
-----------------------------------------------------------------------

Yes, see:

- :ref:`ubergraph_implementation`
- :ref:`ontobee_implementation`

Note that different triplestores will have different selections of ontologies loaded,
and the loads may not be synchronized, so results may differ.

Additionally, each triplestore has different capabilities (e.g. full text search), and may store
ontologies differently. For example, :term:`Ubergraph` stores the full :term:`Relation Graph`
closure, which is particularly convenient for OAK graph operations. Some graph operations
involving ancestry over arbitrary sets of :term:`predicates<Predicate>` may not be possible on
other triplestores.

Can OAK access local files?
---------------------------

Yes. The main use case for OAK is accessing an ontology or ontologies serialized in some standard
format and stored locally on disk.

Can OAK access OBO Format files?
--------------------------------

Yes. There are currently two adapters for working with OBO Format:

- :ref:`pronto_implementation`
- :ref:`simpleobo_implementation`

Currently pronto is the default. It is fast and implements the complete OBO Format specification.
However, it can be very rigorous in enforcing syntactic rules, and as a result some
ontologies will not load.


Does OAK support all of OWL?
----------------------------

Currently supporting all of :term:`OWL` is out of scope for OAK. However, this should not
be a major blocker for most intended uses of OAK, as an application library.

The main application of OWL is for constructing and maintaining ontologies - after an
ontology is released, only a small subset of OWL constructs are typically used (e.g
SubClassOf, SomeValuesFrom, Annotations).

There are a variety of ways of consuming OWL in OAK

- The recommended way is to use :ref:`sql_implementation`, which works off of RDF/OWL compiled to sqlite3
- You can also use :ref:`funowl_implementation`, but this requires the ontology is in :term:`Functional Syntax`
- You can use a local or remote OWL ontologies serialized as RDF via the :ref:`sparql_implementation`
- Using a tool like :ref:`ROBOT` to convert an OWL ontology to a serialization like :term:`OBO Format`

Note that in future it is likely that OAK will support a wider range of OWL constructs

Does OAK support reasoning?
---------------------------

Currently OAK does not have access to :term:`Reasoning`. But note that this is often not a limitation.

- OAK has the ability to traverse :term:`ancestors<Ancestor>` and :term:`descendants<Descendant>`
- :ref:`sql_implementation` has transitive reasoning performed in advance, calculating the :term:`Relation Graph` closure

There is an experimental `ROBOT plugin <https://github.com/INCATools/oakx-robot>`_ that can be used
to interface with an OWL reasoner via ROBOT.

We also have plans to interface with Rust reasoners such as `Whelk <https://github.com/INCATools/whelk.rs>`_.



Can I use OAK to do graph queries over ontologies?
--------------------------------------------------

On the command line you can use the commands ``ancestors``, ``tree``, ``viz``, all of which are
variants of fetching and displaying ancestors.

Can I use OAK to do lexical search?
-----------------------------------

Yes. See :ref:`search_syntax`

Can I use OAK as a text annotator?
-----------------------------------

Yes. See the :ref:`text_annotator_interface`.

