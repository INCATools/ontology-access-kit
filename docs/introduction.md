
## Introduction

Ontology Access Toolkit (OAK) is a Python library for common ontology operations over a variety of backends.

This library provides a collection of different interfaces for different kinds of ontology operations, including:

 - basic features of an ontology element, such as its label, definition, relationships, or aliases.
 - search an ontology for a term.
 - update, delete, or modify terms.
 - provide specialized object models for more advanced operations, such as graph traversal, or OWL axiom processing, or text annotation.

These interfaces are *separated* from any particular backend. This means the same API can be used regardless of whether the ontology:

 - is served by a remote API such as OLS or BioPortal.
 - is present locally on the filesystem in owl, obo, obojson, or sqlite formats.
 - is to be downloaded from a remote repository such as the OBO library.
 - is queried from a remote database, including SPARQL endpoints, A SQL database, a Solr/ES endpoint.

### Basic Python Example

The following code will load an ontology from a SQLite3 database, lookup
basic information on terms matching a search

```python
from src.oaklib.resource import OntologyResource
from src.oaklib.implementations.sqldb.sql_implementation import SqlImplementation

resource = OntologyResource(slug='tests/input/go-nucleus.db', local=True)
si = SqlImplementation(resource)
for curie in si.basic_search("nucleus"):
    print(f'{curie} ! {si.label(curie)}')
    print(f'Definition: {si.definition(curie)}')
    for rel, fillers in si.outgoing_relationship_map(curie).items():
        print(f'  RELATION: {rel} ! {si.label(rel)}')
        for filler in fillers:
            print(f'     * {filler} ! {si.label(filler)}')
```

### Basic Command Line Example

```bash
runoak -i obi.db info "assay"
```