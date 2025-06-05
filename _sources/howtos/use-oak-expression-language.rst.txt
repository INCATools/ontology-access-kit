.. _use_oak_expression_language:

Using the OAK Expression Language
=================================

The OAK Expression Language is a concise and powerful way to query and navigate ontologies from the command line.
It provides a set of operators and syntax that allow you to perform advanced searches,
filter results, and combine queries using boolean logic.

It is designed for easy use on the command line, and intentionally uses characters that compose well with
the shell.

Some experience in using the CLI is recommended.

For the full list of OAK command line commands, see:

- :ref:`_command_line_interface`
- `Commands notebook <https://github.com/INCATools/ontology-access-kit/tree/main/docs/examples/Commands>`_

Basics
------

The basic building blocks of the OAK Expression Language are:

- IDs (CURIEs)
- Lists of IDs
- Search queries
- Graph queries
- Boolean combinations

IDs (CURIEs)
^^^^^^^^^^^^

You can specify a single term by providing its ID (:term:`CURIE`). For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info FBbt:00004751

This will retrieve information about the term with ID ``FBbt:00004751`` (*wing vein*).

Note you can use any of the examples in this guide with any OAK command that accepts term lists; for example:

* Fetching definitions: ``runoak -i sqlite:obo:fbbt definitions FBbt:00004751``
* Fetching aliases: ``runoak -i sqlite:obo:fbbt aliases FBbt:00004751``
* Fetching is-a ancestors: ``runoak -i sqlite:obo:fbbt ancestors -p i FBbt:00004751``


Lists of IDs
^^^^^^^^^^^^

You can provide a list of terms, these are implicitly combined with an OR operation. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info FBbt:00004751, FBbt:00004754

This will retrieve information about the terms with IDs "FBbt:00004751" or "FBbt:00004754".

Label Queries
^^^^^^^^^^^^^

You can also search for terms based on their :term:`Label`. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info 'wing vein'

Remember to quote strings. If you instead type:

.. code-block::

   runoak -i sqlite:obo:fbbt info wing vein

This will be interpreted as an OR, and you will get back two terms, one for wing, one for vein

Using label queries assumes a certain amount of familiarity with the names used in the ontology you are
querying. If you are not sure of the exact name, you can use the search functionality:

Search Queries
--------------

OAK supports various search queries to find terms based on their labels, definitions, or other properties.

Exact Match
^^^^^^^^^^^

To search for an exact match of a term, use the ``t=`` prefix followed by the search term. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info 't=wing vein'

This will find terms that exactly match "wing vein".

Starts With
^^^^^^^^^^^

To search for terms that start with a specific string, use the ``t^`` prefix. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info 't^wing vein'

This will find terms that start with "wing vein".

Contains
^^^^^^^^

To search for terms that contain a specific string anywhere in their label or definition, use the ``t~`` prefix. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info 't~wing vein'

This will find terms that contain "wing vein" anywhere in their label or definition.

Regular Expressions
^^^^^^^^^^^^^^^^^^^

To perform a regular expression search, use the ``t/`` prefix followed by a valid regular expression pattern. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info 't/^wing vein L\d+$'

This will find terms that match the regular expression pattern "^wing vein L\d+$".

Graph Queries
-------------

OAK allows you to traverse and query the ontology :term:`Graph` using relationships between terms.

Ancestors
^^^^^^^^^

To find all :term:`ancestors<Ancestor>` of a term, use the ``.anc`` operator, optionally
parameterized by the relationship type(s) (aka :term:`Predicate`).
For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info .anc//p=i "wing vein"

This will find all is-a ancestors of "wing vein" using the "is-a" (``i``) relationship.

The ``//`` syntax can be used with many prefix operators to provide arguments. The general syntax is

``.<operator>//k1=<arg1>,<arg2>,...//k2=<arg1>,<arg2>,...//...``

.. note::

    OAK also includes a separate command ``ancestors``, but being able to use the ``.anc`` operator
    in the term list allows you to combine graph querying with other commands.

.. code-block::

Definitions for all is-a ancestors of "wing vein":

   runoak -i sqlite:obo:fbbt definitions .anc//p=i "wing vein"

Descendants
^^^^^^^^^^^

To find all descendants of a term, use the ``.desc`` operator followed by the relationship type(s). For example:

.. code-block::

   runoak -i sqlite:obo:fbbt search .desc//p=i,p nucleus

This will find all descendants of "nucleus" using the :term:`is-a`  (``i``) and
:term:`part-of`  (``p``) relationships.

MRCAs
^^^^^

To find the most recent common ancestors (:term:`MRCA`) of a set of terms, use the ``.mrca`` operator.

For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info .mrca//p=i,p wing vein, wing

Subproperties
^^^^^^^^^^^^^




Boolean Combinations
--------------------

OAK allows you to combine queries using boolean operators such as AND, OR, NOT.

AND
^^^

To perform an AND operation between two queries, use the ``.and`` operator. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info .mrca//p=i [ FBbt:00052481 FBbt:00100571 ]

This finds the most recent common ancestor of "FBbt:00052481" and "FBbt:00100571" (which is "neuroblast").

Note that like any graph command for most ontologies this is only meaningful if parameterized by a predicate.
With some ontologies, there are edges such as "overlaps" or "adjacent to" that yield trivial but non
informative MRCAs.

OR
^^

To perform an OR operation between two queries, use the ``.or`` operator.

.. code-block::

   runoak -i sqlite:obo:fbbt info .desc//p=i,p antenna .or .desc//p=i,p wing

This will find terms that are parts of of either "antenna" or "wing".

Note that ``.or`` is already assumed for term lists, so you can also write:

.. code-block::

   runoak -i sqlite:obo:fbbt info .desc//p=i,p antenna .desc//p=i,p wing


NOT
^^^

To exclude terms that match a specific query, use the ``.not`` operator. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info .desc//p=i vein .not .desc//p=i,p wing

You should think of this more like a "minus" operator - expressions are currently evaluated in order,
so the ``.not`` (exclusion list) should come after the inclusion list.


Nesting
-------

You can nest queries using square brackets to create more complex expressions, or to explicitly
control the order of precedence.

Always leave spaces around the square brackets.

.. code-block::

   runoak -i sqlite:obo:fbbt info [ .desc//p=i cell .not .desc//p=i neuron ] .and [ .desc//p=i,p head .or .desc//p=i,p thorax ]

This will find all terms that are descendants of "cell" but not descendants of "neuron",
and are either parts of "head" or "thorax".

Note that prefix operators such as ``.desc`` bind more tightly than infix operators such as ``.and``.

Using files and redirects
-------------------------

IDFILE
^^^^^^

Use this is to read a list of term IDs from a file. For example:

.. code-block::

   runoak -i sqlite:obo:fbbt info .idfile my_terms.txt

STDIN
^^^^^

You can also use the special file name ``-`` to read from standard input. For example:

.. code-block::

   cat my_terms.txt | runoak -i sqlite:obo:fbbt info -

Other Operators
---------------

IN
^^

The ``.in`` operator allows you to query by subset

.. code-block::

   runoak -i sqlite:obo:fbbt info .in cellxgene_subset

FILTER
^^^^^^

The ``.filter`` operator allows you to provide arbitrary python filters.

QUERY
^^^^^

The ``.query`` operator allows you to pass through a query to the underlying store (SPARQL, SQL).

For example, the ``sqlite`` backend uses SQL, so you can pass through SQL:

.. code-block::

   runoak -i sqlite:obo:uberon info .query \
    "SELECT subject from has_dbxref_statement where value like 'ZFA:%'"

This is equivalent to:

.. code-block::

   runoak -i sqlite:obo:uberon info x^ZFA:

NR
^^

The ``.nr`` operator takes a set of terms and returns the non-redundant set of terms
from that list (parameterized by a predicate or predicates).

MRCA
^^^^

The ``.mrca`` operator takes a set of terms are returns the most recent common ancestors (:term:`MRCA`).
Parameterized by a predicate or predicates.

Example:

.. code-block::

   runoak -i sqlite:obo:uberon info .mrca//p=i,p .idfile my_terms.txt

RAND
^^^^

Pick a random subset of terms. Parameterized by ``n`` (number of terms).

Definitions for random terms in the Cell Ontology:

.. code-block::

   runoak -i sqlite:obo:cl definitions .rand

For 10 random terms

.. code-block::

   runoak -i sqlite:obo:cl definitions .rand//n=10

.. note::

    The ``.rand`` operator will sample from all terms in the ontology. This
    could include terms imported and merged from other ontologies. For
    finer-grained control, use the ``.sample`` operator, which allows the
    combination of a sample operator with the results of evaluating any
    OAK expression.

SAMPLE
^^^^^^

The ``.sample`` operator takes a random sample of terms. It is parameterized by ``n`` (number of terms
in sample).

Definitions for 3 random terms:

.. code-block::

   runoak -i sqlite:obo:obi definitions .sample//n=3 i^OBI:

To compare 3 random terms with 3 other random terms:

.. code-block::

   runoak -i sqlite:obo:cl similarity .sample//n=3 i^CL: @ .sample//n=3 i^CL:

Others
^^^^^^

* ``.is_obsolete``: all :term:`Obsolete` terms
* ``.non_obsolete``: all non-obsoletes
* ``.dangling``: all :term:`Dangling` terms
* ``.child``: non-transitive version of ``.desc``. Also parameterized by predicate.
* ``.parent``: non-transitive version of ``.anc``. Also parameterized by predicate.
* ``.sib``: all siblings of a term. Also parameterized by predicate.
* ``.all``: all terms
* ``.classes``: all classes
* ``.relations``: all relations

