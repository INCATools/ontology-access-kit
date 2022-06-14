
## Introduction

Ontology Access Toolkit (OAK) is a Python library for common ontology operations over a variety of backends.

This library provides a collection of different interfaces for different kinds of ontology operations, including:

 - lookup basic features of an ontology element, such as its label, definition, relationships, or aliases.
 - search an ontology for a term.
 - update, delete, or modify terms.
 - provide specialized object models for more advanced operations, such as graph traversal, or OWL axiom processing, or text annotation.

These interfaces are *separated* from any particular backend. This means the same API can be used regardless of whether the ontology:

 - is served by a remote API such as OLS or BioPortal.
 - is present locally on the filesystem in owl, obo, obojson, or sqlite formats.
 - is to be downloaded from a remote repository such as the OBO library.
 - is queried from a remote database, including SPARQL endpoints, A SQL database, a Solr/ES endpoint.

### Basic Python Example

```python
from src.oaklib.resource import OntologyResource
from src.oaklib.implementations.sqldb.sql_implementation import SqlImplementation

resource = OntologyResource(slug='tests/input/go-nucleus.db', local=True)
si = SqlImplementation(resource)
for curie in si.basic_search("cell"):
    print(f'{curie} ! {si.get_label_by_curie(curie)}')
    print(f'Definition: {si.get_definition_by_curie(curie)}')
    for rel, fillers in si.get_outgoing_relationship_map_by_curie(curie).items():
        print(f'  RELATION: {rel} ! {si.get_label_by_curie(rel)}')
        for filler in fillers:
            print(f'     * {filler} ! {si.get_label_by_curie(filler)}')
```

### Basic Command Line Example

```bash
runoak -i obi.db info "assay"
```