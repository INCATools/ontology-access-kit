.. cli:

Command Line
============

Preamble
---

.. warning ::

   currently things are set up such that there is a single main command :code:`runoak`, which has
   a growing number of subcommands. In the future we may decide to split the subcommands
   into other commands.

.. note ::

   we follow the `CLIG <https://clig.dev/>`_ guidelines as far as possible

General Guidelines
------------------

.. note ::

   if you are running this as an internal OAK developer you need to precede the command with :code:`poetry shell`

The general structure is:

.. code:

    runoak --input IMPLEMENTATION COMMAND [COMMAND ARGS AND OPTIONS]

The value for :code:`--input` (which can be shorted to :code:`-i`) is specified in the :ref:`selectors` documentation

You can specify further implementations with :code:`-a` which will create an :ref:`aggregator` implementation that wraps
multiple implementations. For example, you can multiplex queries over different endpoints.

Common Patterns
---------------

Term Lists
^^^^^^^^^^^

Many commands take a *term* or a *list of terms* as their primary argument. These are typically one of:

- a :ref:`CURIE` such as :code:`UBERON:0000955`
- a :ref:`search-syntax` term, which is either:

    - an exact match to a label; for example "limb" or "plasma membrane"
    - a compound search term such as :code:`t~limb` which finds terms with partial matches to limb

Search terms are *expanded* to matching CURIEs, and then fed into the command

Be warned that use of search terms can make some commands "explode"

Predicates
^^^^^^^^^^

Many commands take a :code:`--predicates` option (shortened to :code:`-p`). This specifies a list of predicates
(aka *relationship types*, see :ref:`Predicates`) to be used in filtering. The list is specified as a comma-delimited
list (no spaces) of CURIEs.

For many biological ontologies, it can be useful to filter on is_a (rdfs:subClassOf) and part_of (BFO:0000050) so
the command line interface understands shortcuts for these:

- :code:`i`: is-a (i.e rdfs:subClassOf between two named classes)
- :code:`p`: part-of

However, this library is not restricted to biological ontologies, and in future we may allow customizable shortcuts.

Command Line Docs
-----------------

.. currentmodule:: oaklib.cli

.. click:: oaklib.cli:main
    :prog: runoak
    :show-nested:

