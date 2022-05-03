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

Many commands take a *term* or a *list of terms* as their primary argument. These are typically one of:

- a :ref:`CURIE` such as :code:`UBERON:0000955`
- a :ref:`search-syntax` term, which is either:

    - an exact match to a label; for example "limb" or "plasma membrane"
    - a compound search term such as :code:`t~limb` which finds terms with partial matches to limb

Search terms are *expanded* to matching CURIEs, and then fed into the command

Be warned that use of search terms can make some commands "explode"

Command Line Docs
-----------------

.. currentmodule:: oaklib.cli

.. click:: oaklib.cli:main
    :prog: runoak
    :show-nested:

.. currentmodule:: oaklib.omk.omk_cli

.. click:: aklib.omk.omk_cli:main
    :prog: omk
    :show-nested:
