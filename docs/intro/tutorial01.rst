Part 1
=======

First we will install the package and then we will try some command line examples querying the fruitfly anatomy ontology.

Installation
-------------

Create a directory

.. code-block::

    cd ~
    mkdir oak-tutorial
    cd oak-tutorial

First create a virtual environment

.. code-block::

    python3 -m venv venv
    source venv/bin/activate
    export PYTHONPATH=.:$PYTHONPATH

Make sure you have Python 3.9 or higher

Then install:

.. code-block::

    pip install oaklib

.. code-block::

    runoak --help

You should see a list of all commands.

You can get help on a specific command:

.. code-block::

    runoak search --help

See also the :ref:`cli` section of this documentation

Query the OBO Library
---------------------

Next try using the "search" command to search for a term in the Drosophila anatomy ontology (`fbbt <http://obofoundry.org/ontology/fbbt>`_).

The base command takes an :code:`--input` (or just :code:`-i`) option that specifies the input implementation. We will return to the full syntax later,
but one pattern that is useful to know is :code:`obolibrary:<ontology-file>`.

.. code-block::

    runoak -i obolibrary:fbbt.obo search 'wing vein'

The first time you run this there will be a lag as the file is downloaded, but after that it will be cached. (This is using the Pronto
library under the hood)

After the lag you will get results like:

.. code-block::

    FBbt:00004751 ! wing vein
    FBbt:00004754 ! axillary vein
    FBbt:00004759 ! wing vein L1
    FBbt:00004760 ! wing vein L2

Working with local files
------------------------

.. code-block::

    wget http://purl.obolibrary.org/obo/fbbt.obo
    runoak -i fbbt.obo search 'wing vein'

Fetching ancestors
------------------

Next we will try a different command, plugging in an ID we got from the previous search.

We will use the :code:`ancestors` command to find all rdfs:subClassOf and part-of (BFO:0000050) ancestors of 'wing vein'.

.. code-block::

    runoak -i obolibrary:fbbt.obo ancestors FBbt:00004751 -p i,p

*Here we are using built-in shorthands, but you can get the same effect with the full :ref:`CURIE`s, rdfs:subClassOf and BFO:0000050)

You should see body parts such as cuticle, wing, etc, alongside their ID

Later on we will see how we can make images like:

.. image:: wing-vein.png

Using other backends
--------------------

.. code-block::

    runoak -i ubergraph: search 'wing vein'

This searches the :ref:`ubergraph` backend using the blazegraph search interface. Note that in addition to searching over a wider range
of ontologies, this returns a ranked list that might include matches only to "wing" or "vein". Currently each backend implements
search a little differently, but this will be more unified and controllable in the future.

Using BioPortal
--------------------

First you will need to go to `BioPortal <https://bioportal.bioontology.org/>`_ and get an API key, if you don't already have one.

You will then need to set it:

.. code-block::

    runoak set-apikey bioportal YOUR-API-KEY

This stores it in an OS-dependent folder

.. code-block::

    runoak -i bioportal: search 'wing vein'

Again the results are relevance ranked, and there are a lot of them, as this includes multiple ontologies, you may want to ctrl-C to kill before the end

Next steps
----------

You can play around with some of the other commands, or go right into the next section on programmatic usage!
