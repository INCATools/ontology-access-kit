.. _selectors:

Ontology Adapter Selectors
=================

In the command line interface and in Python code, *descriptors* can be used as a shorthand way to refer to either a local or remote ontology, plus
a method for parsing/querying it. The OntologyResource that is returned can be used
to instantiate an implementation. The descriptors can also be used in the :ref:`cli`

.. note::

    Ontologies are available in a sometimes bewildering range of formats. One thing that constantly
    trips people up is the distinction between ontology *language* and *serialization*. OWL is an ontology
    language, *not* a syntax. OWL has its own syntaxes such as :term:`Manchester Syntax`, OWL-XML and :term:`Functional Syntax' -- additionally
    it can be *mapped* to RDF, which is its *own* datamodel/language, with its *own* serializations (:term:`Turtle`,
    RDF/XML (NOT the same as OWL-XML), JSON-LD, ...). Confusing, huh? We are doing our best in this library
    to simplify things for you the user, please be patient!

Syntax
-----

A descriptor is EITHER:

 - prefixed with a *scheme* OR
 - is a *path (in which case the scheme is inferred)

Examples
-----

Examples of scheme-less descriptors, implicit implementation:

- :code:`tests/input/go-nucleus.obo` - local :term:`OBO Format` file loaded with pronto
- :code:`tests/input/go-nucleus.json` - local :term:`OBO Graphs` json format file loaded with pronto
- :code:`tests/input/go-nucleus.owl` - local OWL rdf/xml format file (loaded with rdflib at the moment, may change)
- :code:`tests/input/go-nucleus.owl.ttl` - local OWL :term:`Turtle` file (loaded with rdflib at the moment, may change)
- :code:`tests/input/go-nucleus.db` - local sqlite3 db loaded with SqlImplementation
- :code:`http://purl.obolibrary.org/obo/pato.obo` - NOT IMPLEMENTED; download locally for now
- :code:`http://purl.obolibrary.org/obo/pato.owl` - NOT IMPLEMENTED; download locally for now

Examples of explicit schemes:

- :code:`sparql:tests/input/go-nucleus.owl.ttl` - local OWL file in turtle serialization
- :code:`sparql:tests/input/go-nucleus.owl` - local OWL file (RDF/XML assumed unless explicit format option passed)
- :code:`pronto:tests/input/go-nucleus.obo` - local :term:`OBO Format` file loaded with pronto
- :code:`pronto:tests/input/go-nucleus.json` - local :term:`OBO Graphs` json format file loaded with pronto
- :code:`pronto:tests/input/go-nucleus.owl` - local OWL rdf/xml format file (loaded with pronto at the moment may change)
- :code:`pronto:tests/input/go-nucleus.db` - local sqlite3 db loaded with SqlImplementation
- :code:`prontolib:pato.obo` - remote :term:`OBO Format` file loaded from OBO Library with pronto
- :code:`prontolib:pato.owl` - remote owl format file loaded from OBO Library with pronto
- :code:`sqlite:tests/input/go-nucleus.db` - local SQLite file
- :code:`sqlite:tests/input/go-nucleus.owl` - convert OWL to SQLite and query using sql_implementation
- :code:`sqlite:obo:go` - pre-made SQLite from :term:`Semantic SQL` registry
- :code:`bioportal:` all of bioportal
- :code:`bioportal:pato` pato in bioportal
- :code:`ontobee:` all of ontobee
- :code:`ontobee:pato` pato in ontobee
- :code:`ols:` all of OLS
- :code:`ols:pato` pato in OLS (NOT IMPLEMENTED)
- :code:`ubergraph:` all of OLS
- :code:`ubergraph:pato` pato in ubergraph

See :ref:`cli` for more examples

Schemes
-------

pronto
^^^^

Implementation: :ref:`pronto_implementation`

The slug is a path to a file on disk. Must be in obo or owl or json

prontolib
^^^^

Implementation: :ref:`pronto_implementation`

The slug is the name of the resource on obo, e.g. pato.obo, cl.owl

sqlite
^^^^

Implementation: :ref:`sql_implementation`

The slug is the path to the sqlite .db file on local disk

obosqlite
^^^^

Implementation: :ref:`sql_implementation`

The slug is the name of the ontology, e.g 'hp', 'uberon'

TODO: download from s3

ontobee
^^^^

Implementation: :ref:`ontobee_implementation`

Currently the slug is ignored

ols
^^^^

Implementation: :ref:`ols_implementation`

Currently the slug is ignored

bioportal
^^^^

Implementation: :ref:`bioportal_implementation`

Currently the slug is ignored

funowl
^^^^

Implementation: :ref:`funowl_implementation`

NOT IMPLEMENTED YET

Functions
----

.. automodule:: oaklib.selector
    :members:
