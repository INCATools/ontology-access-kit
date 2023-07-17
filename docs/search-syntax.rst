.. _search_syntax:

Search Syntax
=================

The search syntax is mapped to the :ref:`search` interface

.. warning::

    the current syntax is preliminary and will be fully documented once accepted.
    See the tutorial for current documentation.

Boolean Combinations
--------------------

.. warning::

    this feature is experimental and will be documented after acceptance

Multiple terms can be specified with boolean combinators:

.. code-block::

    SEARCH1 SEARCH2 .not SEARCH3

The implicit combinator is OR. This will take the union of search1 and search2 and subtract search3 results

Search Datamodel
----

.. automodule:: oaklib.datamodels.search
    :members:
