.. _faq_commandline:

FAQ: Command Line
=================

How do I see a list of commands?
-------------------------------

Type:

.. code-block:: bash

    runoak --help

This will list all OAK commands, as well as listing all *global* options.

How do I get help on a command?
-------------------------------

Type:

.. code-block:: bash

    runoak COMMAND --help

Each command typically comes with some examples of use

How do I get more examples of command line usage?
-------------------------------------------------

See the ``Commands <https://github.com/INCATools/ontology-access-kit/tree/main/docs/examples/Commands>`_ folder
of the Jupyter notebooks directory in GitHub. Our aim is to eventually have one notebook per command.

I want to query an ontology, what do I pass for the ``--input`` option?
-----------------------------------------------------------------------

There are a number of different ways to access an ontology. If your ontology is in the
:term:`Semantic SQL` repository (which includes everything in :term:`OBO`) then the easiest
thing is to provide a value of the form ``sqlite:obo:<MyOntID>``.

For example:

.. code-block:: bash

    runoak -i sqlite:obo:chebi info cysteine

See the :ref:`selectors` documentation.

Why do I get a "no such option" error when I pass the "--input" option?
------------------------------------------------------------------

If you see this error it means you have likely specified the ``--input`` (or ``-i``)
option *after* the main subcommand.

This is correct:

.. code-block:: bash

    runoak --input SOURCE COMMAND COMMAND-OPTION... ARGUMENT...

This is **not** correct:

.. code-block:: bash

    runoak COMMAND --input SOURCE ARGUMENT...

What do the codes "i" and "p" mean?
-----------------------------------

Many commands take a :code:`--predicates` option, the value is a comma separated list of :term:`CURIEs<CURIE>`.
You can use "i" as a shortcut for is_a (rdfs:subClassOf) and "p" as a shortcut for part_of (BFO:0000050)

See the section :ref:`relationships_and_graphs` in the :ref:`guide`.

Can I pass a list of IDs (CURIEs) as input to a command?
--------------------------------------------------------

Yes, almost all commands accept lists of CURIEs. These are treated formally as a disjunctive query,
i.e. the command operates on the union of all identifiers.

Can I pass entity labels as command inputs?
-------------------------------------------

Yes. This can be very handy if you don't have IDs memorized or don't want to issue another command.

.. code-block:: bash

    runoak -i sqlite:obo:ro info 'part of' 'develops from'

Can I pass lexical queries as command inputs?
---------------------------------------------

Yes. See :ref:`search-syntax`

For example, all terms with a label matching "device".

.. code-block:: bash

    runoak -i sqlite:obo:obi l~device

Can I pass the results of graph queries as command inputs?
---------------------------------------------

Yes. See :ref:`search-syntax`.

You can use ``.descendants`` (or just ``.desc``) to query for descendants, and ``.ancestors`` (or just ``.anc``) to
query for ancestors. Both of these can be pameterized by predicate arguments (after the optional ``//``).

For example, to get all logical definitions of is-a descendants (i.e entailed subclasses)
of "bone element" in UBERON:

.. code-block:: bash

    runoak -i sqlite:obo:uberon logical-definitions .desc//p=i "bone element"

Can I make boolean combinations of query terms?
-----------------------------------------------

Yes. See :ref:`search-syntax`

For example, all bone elements that are part of a forelimb:

.. code-block:: bash

    runoak -i sqlite:obo:uberon logical-definitions .desc//p=i "bone element" .and .desc//p=i,p "forelimb"

Can I chain commands together, unix-style?
------------------------------------------

Yes! Most commands take a term list as input, and allow for ``-`` to specify input from standard input

For example, to pipe the output from the ``descendants`` command into the ``definitions`` command:

.. code-block:: bash

    alias cl='runoak -i sqlite:obo:cl'
    cl descendants interneuron | cl definitions -

The first column of the output from the descendants command will be used as input for the next command.

What does the symbol ``@`` mean in a query term list
----------------------------------------------------

Most OAK commands accept as input a simple list of terms. Some commands operate on *pairs* of terms.
The ``@`` symbol separates two term lists.

For example:

.. code-block:: bash

    runoak -i sqlite:obo:cl similarity CL:0002405 CL:0002039 CL:0000893 @ CL:0001042 CL:0000935

Can I use the command line to visualize a subgraph?
---------------------------------------------------

Is there an over-arching philosophy or set of design principles to the OAK command line?
----------------------------------------------------------------------------------------

Yes! We follow the `CLIG <https://glib.dev>`_ guidelines as far as possible, in order
to provide both internal consistency and consistency with other commands.

OAK is also designed to be *chainable* as far as possible. Most OAK commands take
*term lists* as input

The command isn't working the way I expected - how do I get help?
----------------------------------------

You are welcome to post questions on our issue tracker or slack channel. It can help if you pass the
``--stacktrace`` global option and copy the full stacktrace.