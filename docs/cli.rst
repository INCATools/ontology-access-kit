.. _command_line_interface:

Command Line
============


.. note ::

   we follow the `CLIG <https://clig.dev/>`_ guidelines as far as possible

General Guidelines
------------------

.. note ::

   if you are running this as an internal OAK developer you need to precede the command with :code:`poetry shell`

The general structure is:

.. code:: bash

    runoak --input HANDLE COMMAND [COMMAND ARGS AND OPTIONS]

The value for :code:`--input` (which can be shorted to :code:`-i`) is specified in the :ref:`selectors` documentation.

Examples:

.. code:: bash

    runoak --input ubergraph: COMMAND [COMMAND ARGS AND OPTIONS]
    runoak --input fbbt.obo COMMAND [COMMAND ARGS AND OPTIONS]
    runoak --input cl.db COMMAND [COMMAND ARGS AND OPTIONS]
    runoak --input sqlite:obo:cl COMMAND [COMMAND ARGS AND OPTIONS]

It can be useful to create aliases for individual ontologies. For example, to create an alias for the Uberon ontology:

.. code:: bash

    alias uberon='runoak -i sqlite:obo:uberon'
    alias cl='runoak -i sqlite:obo:cl'
    alias obi='runoak -i sqlite:obo:obi'

You can specify further implementations with :code:`-a` which will create an :ref:`aggregator` implementation that wraps
multiple implementations. For example, you can multiplex queries over different endpoints.

Common Patterns
---------------

Term Lists
^^^^^^^^^^^

Many commands take a *term* or a *list of terms* as their primary argument. These are typically one of:

- a :ref:`CURIE` such as :code:`UBERON:0000955`
- a :ref:`search_syntax` term, which is either:

    - an exact match to a label; for example "limb" or "plasma membrane"
    - a compound search term such as :code:`t~limb` which finds terms with partial matches to limb

Search terms are *expanded* to matching CURIEs, and then fed into the command.

For example, (assuming the alias above) the following command will look up two terms using their labels:

.. code-block:: bash

    uberon info hand foot

This is equivalent to:

.. code-block:: bash

    uberon info UBERON:0002398 UBERON:0002397

Predicates
^^^^^^^^^^

Many commands take a :code:`--predicates` option (shortened to :code:`-p`). This specifies a list of predicates
(aka *relationship types*, see :ref:`Predicates`) to be used in filtering. The list is specified as a comma-delimited
list (no spaces) of CURIEs.

For many biological ontologies, it can be useful to filter on is_a (rdfs:subClassOf) and part_of (BFO:0000050) so
the command line interface understands shortcuts for these:

- :code:`i`: is-a (i.e rdfs:subClassOf between two named classes)
- :code:`p`: part-of

For example, to draw the subgraph of terms starting from "hand" and "foot"
and tracing upwards through is_a and part_of relationships:

.. code-block:: bash

    uberon viz -p i,p hand foot

Cache Control
-------------

OAK may download data from remote sources as part of its normal operations. For
example, using the :code:`sqlite:obo:...` input selector will cause OAK to
fetch the requested Semantic-SQL database from a centralised repository.
Whenever that happens, the downloaded data will be cached in a local directory
so that subsequent commands using the same input selector do not have to
download the file again.

By default, OAK will refresh (download again) a previously downloaded file if
it was last downloaded more than 7 days ago.

The behavior of the cache can be controlled in two ways: with an option on the
command line and with a configuration file.

Controlling the cache on the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The global option :code:`--caching` gives the user some control on how the
cache works.

To change the default cache expiry lifetime of 7 days, the :code:`--caching`
option accepts a value of the form :code:`ND`, where *N* is a positive integer
and *D* can be either :code:`s`, :code:`d`, :code:`w`, :code:`m`, or :code:`y`
to indicate that *N* is a number of seconds, days, weeks, months, or years,
respectively. If the *D* part is omitted, it defaults to :code:`d`.

For example, :code:`--caching=3w` instructs OAK to refresh a cached file if it
was last refreshed 21 days ago.

The :code:`--caching` option also accepts the following special values:

- :code:`refresh` to force OAK to always refresh a file regardless of its age;
- :code:`no-refresh` to do the opposite, that is, preventing OAK from
  refreshing a file regardless of its age;
- :code:`clear` to forcefully clear the cache (which will trigger a refresh as
  a consequence);
- :code:`reset` is a synonym of :code:`clear`.

Note the difference between :code:`refresh` and :code:`clear`. The former will
only cause the requested file to be refreshed, leaving any other file that may
exist in the cache untouched. The latter will delete all cached files, so that
not only the requested file will be downloaded again, but any other
previously cached file will also have to be downloaded again the next time they
are requested.

In both case, refreshing and clearing will only happen if the OAK command in
which the :code:`--caching` option is used attempts to look up a cached file.
Otherwise the option will have no effect.

To forcefully clear the cache independently of any command, the
:ref:`cache-clear` command may be used. The contents of the cache may be
explored at any time with the :ref:`cache-ls` command.

Controlling the cache with a configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finer control of how the cache works is possible through a configuration file
that OAK will look up for at the following locations:

- under GNU/Linux: in ``$XDG_CONFIG_HOME/ontology-access-kit/cache.conf``;
- under macOS: in ``$HOME/Library/Application Support/ontology-access-kit/cache.conf``;
- under Windows: in ``%LOCALAPPDATA%\ontology-access-kit\ontology-access-kit\cache.conf``.

The file should contain lines of the form :code:`pattern = policy`, where:

- *pattern* is a shell-type globbing pattern indicating the files that will be
  concerned by the policy set forth on the line;
- *policy* is the same type of value as expected by the :code:`--caching`
  option as explained in the previous section.

Blank lines and lines starting with :code:`#` are ignored.

If the *pattern* is :code:`default` (or :code:`*`), the corresponding policy
will be used for any cached file that does not have a matching policy.

Here is a sample configuration file:

.. code-block::

    # Uberon will be refreshed if older than 1 month
    uberon.db = 1m
    # FBbt will be refreshed if older than 2 weeks
    fbbt.db = 2w
    # Other FlyBase ontologies will be refreshed if older than 2 months
    fb*.db = 2m
    # All other files will be refreshed if older than 3 weeks
    default = 3w

Note that when looking up the policy to apply to a given file, patterns are
tried in the order they appear in the file. This is why the :code:`fbbt.db`
pattern in the example above must be listed *before* the less specific
:code:`fb*.db` pattern, otherwise it would be ignored. (This does not apply to
the default pattern -- whether it is specified as :code:`default` or as
:code:`*` -- which is always tried after all the other patterns.)

The :code:`--caching` option described in the previous section always takes
precedence over the configuration file. That is, all rules set forth in the
configuration will be ignored if the :code:`--caching` option is specified on
the command line.

Commands
-----------

The following section is autogenerated from the inline docs.
You should get the same results by running:

.. code-block:: bash

    runoak COMMAND --help

For example, to get help on the ``viz`` command:

.. code-block:: bash

    runoak viz --help

.. currentmodule:: oaklib.cli

.. click:: oaklib.cli:main
    :prog: runoak
    :show-nested:
