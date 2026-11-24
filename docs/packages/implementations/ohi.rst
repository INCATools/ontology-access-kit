.. _ohi_implementation:

ohi.dev Adapter
===============

About
-----

`ohi.dev <https://ohi.dev>`_ is a public catalog of ontology releases. Each release is
published once and never changes, and its files come with sha256 hashes. The catalog also
keeps older releases, so you can load the exact version of an ontology that a project used.

This adapter downloads a release's Turtle file into the OAK cache directory, checks it
against the published hash, and loads it in memory with rdflib, the same way as a local
``.ttl`` file. Each release is downloaded only once.

Installation
------------

The adapter needs the ``ohi-sdk`` package:

.. code:: shell

    $ pip install 'oaklib[ohi]'

Command Line Examples
---------------------

Use the :code:`ohi` selector with a catalog reference. Without a version you get the
latest release:

.. code:: shell

    $ runoak -i ohi:obo/pato info PATO:0000586

Add ``@VERSION`` to load a specific release:

.. code:: shell

    $ runoak -i ohi:obo/pato@2020-02-06 search "increased size"

You can search the catalog for references and versions at `ohi.dev <https://ohi.dev>`_.

Code
----

.. currentmodule:: oaklib.implementations.ohi.ohi_implementation

.. autoclass:: OhiImplementation
