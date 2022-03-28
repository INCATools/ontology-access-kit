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
# alternate implementations commented out
resource = OntologyResource(slug='tests/input/go-nucleus.obo', local=True)
ont = SqlDatabaseBasicImpl.create(resource)
for curie in ont.basic_search("cell"):
    print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    for rel, fillers in ont.get_outgoing_relationships().items():
        print(f'  RELATION:: {rel} ! {impl.get_label_by_curie(rel)}')
        for filler in fillers:
            print(f'     * {filler} ! {impl.get_label_by_curie(filler)}')
```

See also

- [demo notebook](https://github.com/cmungall/obolib/blob/main/notebooks/basic-demo.ipynb)

## Command Line

```bash
obolib -i sqlite:go-nucleus.db search nucl
```

## Documentation

See sphinx [todo]

## Potential Refactoring

Currently all implementations exist in this repo/module, this results in a lot of dependencies

One possibility is to split out each implementation into its own repo and use a plugin architecture
