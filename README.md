# obolib: Common ontology operations over a variety of backends

![](https://github.com/cmungall/obolin/workflows/Build/badge.svg)
[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg)](https://mybinder.org/v2/gh/cmungall/obolib/main?filepath=notebooks)

This library provides a collection of different interfaces for different kinds of ontology operations, including:

 - lookup of basic features of an ontology element, such as it's label, definition, relationships, or aliases
 - search an ontology for a term
 - updating, deleting, or modifying terms
 - provide specialized object models for more advanced operations, such as graph traversal, or OWL axiom processing, or text annotation

These interfaces are *separated* from any particular backend. This means the same API can be used regardless of whether the ontology:

 - is served by a remote API such as OLS or BioPortal
 - is present locally on the filesystem in owl, obo, obojson, or sqlite formats
 - is to be downloaded from a remote repository such as the OBO library
 - is queried from a remote database, including SPARQL endpoints, A SQL database, a Solr/ES endpoint

## Documentation:

- [cmungall.github.io/obolib](https://cmungall.github.io/obolib)

## Current status

 - only a handful of interface-implementaton combos are implemented
 - anything could change including the name, "obolib" may be presumptious

## Example

```python
resource = OntologyResource(slug='tests/input/go-nucleus.db', local=True)
oi = SqlImplementation.create(resource)
for curie in oi.basic_search("cell"):
    print(f'{curie} ! {oi.get_label_by_curie(curie)}')
    for rel, fillers in oi.get_outgoing_relationships().items():
        print(f'  RELATION:: {rel} ! {oi.get_label_by_curie(rel)}')
        for filler in fillers:
            print(f'     * {filler} ! {oi.get_label_by_curie(filler)}')
```

For more examples, see

- [demo notebook](https://github.com/cmungall/obolib/blob/main/notebooks/basic-demo.ipynb)

## Command Line

There is currently a very limited CLI

For demo purposes we will switch to the obolibrary/pronto backend, but any implementation can be used:

```bash
obolib -i obolibrary:pato.obo search osmol 
```

Returns:

```
PATO:0001655 ! osmolarity
PATO:0001656 ! decreased osmolarity
PATO:0001657 ! increased osmolarity
PATO:0002027 ! osmolality
PATO:0002028 ! decreased osmolality
PATO:0002029 ! increased osmolality
PATO:0045034 ! normal osmolality
PATO:0045035 ! normal osmolarity
```

## Documentation

See sphinx [todo]

## Potential Refactoring

Currently all implementations exist in this repo/module, this results in a lot of dependencies

One possibility is to split out each implementation into its own repo and use a plugin architecture
