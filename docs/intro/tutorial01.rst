Part 1: Getting Started
=======================

First we will install the package and then we will try some command line examples
querying the Drosophila anatomy ontology (`fbbt <http://obofoundry.org/ontology/fbbt>`_).

Installation
-------------

First, create a directory:

.. code-block::

    cd ~
    mkdir oak-tutorial
    cd oak-tutorial

Then create a virtual environment:

.. code-block::

    python3 -m venv venv
    source venv/bin/activate
    export PYTHONPATH=.:$PYTHONPATH

.. note:: Make sure you have Python 3.9 or higher

Then install:

.. code-block::

    pip install oaklib

After successful installation, try invoking OAK via ``runoak``:

.. code-block::

    runoak --help


You should see a list of all commands that are supported by OAK.

You can get help on a specific command:

.. code-block::

    runoak search --help

See also the :ref:`cli` section of this documentation


Query the OBO Library
---------------------

Next try using the "search" command to search for a term in the Drosophila anatomy ontology (`fbbt <http://obofoundry.org/ontology/fbbt>`_).

The base command takes an ``--input`` (or just ``-i``) option that specifies the input
implementation. We will return to the full syntax later, but one pattern that is
useful to know is ``obolibrary:<ontology-file>``.


To do a basic lookup, using either a name or IR

.. code-block::

    runoak -i obolibrary:fbbt.obo info 'wing vein'

The first time you run this there will be a lag as the file is downloaded, but after that it will be cached. (This is using the Pronto
library under the hood). The results should include:

.. code-block::

    FBbt:00004751 ! wing vein

You get the same results wth:

.. code-block::

    runoak -i obolibrary:fbbt.obo info FBbt:00004751

Search
------

You can use the `search` command to search for terms. You can also use a special search syntax like this:

.. code-block::

    runoak -i obolibrary:fbbt.obo search 't^wing vein'

Here ``t`` means "term" (search in all term fields) and ``^`` means "starts with"

This will give results like:

.. code-block::

    FBbt:00004751 ! wing vein
    FBbt:00004754 ! axillary vein
    FBbt:00004759 ! wing vein L1
    FBbt:00004760 ! wing vein L2


Working with local files
------------------------

To work with a local ontology file, you can provide the filename as input:

.. code-block::

    wget http://purl.obolibrary.org/obo/fbbt.obo
    runoak --input fbbt.obo search 'wing vein'


Fetching ancestors
------------------

Next we will try a different command, plugging in an ID we got from the previous search.

We will use the :ref:`ancestors` command to find all subclass-of (``rdfs:subClassOf``) and part-of (``BFO:0000050``) ancestors of 'wing vein'.

.. code-block::

    runoak --input obolibrary:fbbt.obo ancestors FBbt:00004751 --predicates i,p

You should see body parts such as cuticle, wing, etc, alongside their ID.

.. note:: Here we are providing the predicates to traverse via the ``-p/--predicates`` argument.
   The values ``i`` and ``p`` for the predicates argument are short-hand names for
   ``rdfs:subClassOf`` and ``BFO:0000050``, respectively.

   You can get the same effect with the full predicate CURIEs, ``rdfs:subClassOf` and ``BFO:0000050``.

   .. code-block::

      runoak --input obolibrary:fbbt.obo ancestors FBbt:00004751 --predicates rdfs:subClassOf,BFO:0000050


   Possible short-hand names are:
    - ``i`` for the ``rdfs:subClassOf`` predicate
    - ``p`` for the ``BFO:0000050`` predicate
    - ``e`` for the ``owl:equivalentClass`` predicate


Later on we will see how we can make images like:

.. image:: wing-vein.png


Using other backends
--------------------

You can use OAK to query other backends that provides one (or more ontologies) as a graph.


Using Ubergraph
~~~~~~~~~~~~~~~

Ubergraph is an integrated ontology store that contains a merged set of mutually referential OBO ontologies.

.. code-block::

    runoak -i ubergraph: search 'wing vein'

This searches the :ref:`ubergraph` backend using the blazegraph search interface. Note that in addition to searching over a wider range
of ontologies, this returns a ranked list that might include matches only to "wing" or "vein". Currently each backend implements
search a little differently, but this will be more unified and controllable in the future.


Using BioPortal
~~~~~~~~~~~~~~~

BioPortal is a comprehensive repository of biomedical ontologies.

To query BioPortal, first you will need to go to `BioPortal <https://bioportal.bioontology.org/>`_ and get an API key (if you don't already have one).


.. note:: The API Key is assigned to each user upon creating an account on BioPortal.


You will then need to set it:

.. code-block::

    runoak set-apikey --endpoint bioportal YOUR-API-KEY

This stores it in an OS-dependent folder, which is then accessed by OAK for performing API queries.

.. code-block::

    runoak -i bioportal: search 'wing vein'

Again the results are relevance ranked, and there are a lot of them, as this includes multiple ontologies, you may want to ctrl-C to kill before the end.

Next steps
----------

You can play around with some of the other commands, or go right into the next section on programmatic usage!
