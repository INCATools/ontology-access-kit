.. _selectors:

Ontology Implementation Selectors
=================

In the command line interface and in Python code, *descriptors* can be used as a shorthand way to refer to either a local or remote ontology, plus
a method for parsing/querying it. The OntologyResource that is returned can be used
to instantiate an implementation. The descriptors can also be used in the :ref:`cli`

Syntax
-----

A descriptor is EITHER:

 - prefixed with a *scheme* OR
 - is a *path (in which case the scheme is inferred)

Examples
-----

Examples of scheme-less descriptors, implicit implementation:

- :code:`tests/input/go-nucleus.obo` - local obo format file loaded with pronto
- :code:`tests/input/go-nucleus.json` - local obojson format file loaded with pronto
- :code:`tests/input/go-nucleus.owl` - local OWL rdf/xml format file (loaded with pronto at the moment may change)
- :code:`tests/input/go-nucleus.db` - local sqlite3 db loaded with SqlImplementation
- :code:`http://purl.obolibrary.org/obo/pato.obo` - NOT IMPLEMENTED; download locally for now
- :code:`http://purl.obolibrary.org/obo/pato.owl` - NOT IMPLEMENTED; download locally for now

Examples of explicit schemes:

- :code:`pronto:tests/input/go-nucleus.obo` - local obo format file loaded with pronto
- :code:`pronto:tests/input/go-nucleus.json` - local obojson format file loaded with pronto
- :code:`pronto:tests/input/go-nucleus.owl` - local OWL rdf/xml format file (loaded with pronto at the moment may change)
- :code:`pronto:tests/input/go-nucleus.db` - local sqlite3 db loaded with SqlImplementation
- :code:`prontolib:pato.obo` - remote obo format file loaded from OBO Library with pronto
- :code:`prontolib:pato.owl` - remote owl format file loaded from OBO Library with pronto
- :code:`bioportal:` all of bioportal
- :code:`bioportal:pato` pato in bioportal (NOT IMPLEMENTED)
- :code:`ontobee:` all of ontobee
- :code:`ontobee:pato` pato in ontobee (NOT IMPLEMENTED)
- :code:`ols:` all of OLS
- :code:`ols:pato` pato in OLS (NOT IMPLEMENTED)
- :code:`ubergraph:` all of OLS
- :code:`ubergraph:pato` pato in ubergraph (NOT IMPLEMENTED)

See :ref:`cli` for more examples

Schemes
-------

pronto
^^^^

Implementation: :ref:`ProntoImplementation`

The slug is a path to a file on disk. Must be in obo or owl or json

prontolib
^^^^

Implementation: :ref:`ProntoImplementation`

The slug is the name of the resource on obo, e.g. pato.obo, cl.owl

sqlite
^^^^

Implementation: :ref:`SqlImplementation`

The slug is the path to the sqlite .db file on local disk

obosqlite
^^^^

Implementation: :ref:`SqlImplementation`

The slug is the name of the ontology, e.g 'hp', 'uberon'

TODO: download from s3

ontobee
^^^^

Implementation: :ref:`OntobeeImplementation`

Currently the slug is ignored

ols
^^^^

Implementation: :ref:`OlsImplementation`

Currently the slug is ignored

bioportal
^^^^

Implementation: :ref:`BioportalImplementation`

Currently the slug is ignored

funowl
^^^^

Implementation: :ref:`OwlImplementation`

NOT IMPLEMENTED YET

owlery
^^^^

Implementation: :ref:`OwleryImplementation`

NOT IMPLEMENTED YET

Functions
----

.. automodule:: oaklib.selector
    :members:
