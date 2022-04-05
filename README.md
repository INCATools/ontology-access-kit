# Ontology Access Kit: Python lib for common ontology operations over a variety of backends

![](https://github.com/incatools/ontology-access-kit/workflows/Build/badge.svg)
[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg)](https://mybinder.org/v2/gh/incatools/ontology-access-kit/main?filepath=notebooks)

This library provides a collection of different interfaces for different kinds of ontology operations, including:

 - lookup of basic features of an ontology element, such as it's label, definition, relationships, or aliases
 - search an ontology for a term
 - validating an ontology
 - updating, deleting, or modifying terms
 - ontology term matching
 - generating and visualizing subgraphs
 - provide specialized object models for more advanced operations, such as graph traversal, or OWL axiom processing, or text annotation

These interfaces are *separated* from any particular backend. This means the same API can be used regardless of whether the ontology:

 - is served by a remote API such as OLS or BioPortal
 - is present locally on the filesystem in owl, obo, obojson, or sqlite formats
 - is to be downloaded from a remote repository such as the OBO library
 - is queried from a remote database, including SPARQL endpoints (Ontobee/Ubergraph), A SQL database, a Solr/ES endpoint

## Documentation:

- [incatools.github.io/ontology-access-kit](https://incatools.github.io/ontology-access-kit)

## Current status

 - only a handful of interface-implementaton combos are implemented

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

- [demo notebook](https://github.com/incatools/ontology-access-kit/blob/main/notebooks/basic-demo.ipynb)

## Command Line

There is currently a very limited CLI. See [CLI docs](https://incatools.github.io/ontology-access-kit/cli.html)

### Search

Use the pronto backend to fetch and parse an ontology from the OBO library, then use the `search` command

```bash
oaklib -i obolibrary:pato.obo search osmol 
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

### QC and Validation

Perform validation on PR using sqlite/rdftab instance:

```bash
oaklib validate -i sqlite:../semantic-sql/db/pr.db
```

### List all terms

List all terms obolibrary has for mondo

```bash
oaklib validate -i obolibrary:mondo.obo terms
```

### Lexical index

Make a lexical index of all terms in Mondo:

```bash
oaklib lexmatch -i obolibrary:mondo.obo -L mondo.index.yaml
```

### Mapping

Create a SSSOM mapping file for a set of ontologies:

```bash
robot merge -I http://purl.obolibrary.org/obo/hp.owl -I http://purl.obolibrary.org/obo/mp.owl convert --check false -o hp-mp.obo
oaklib lexmatch -i hp-mp.obo -o hp-mp.sssom.tsv
```




### Visualization of ancestor graphs

Use the sqlite backend to find all terms matching the string "nucl" walk up the graph and visualize it

```bash
oaklib -i sqlite:tests/input/go-nucleus.db  viz nucl
```

TODO: add figure to docs

## Documentation

- [incatools.github.io/ontology-access-kit](https://incatools.github.io/ontology-access-kit)

## Potential Refactoring

Currently all implementations exist in this repo/module, this results in a lot of dependencies

One possibility is to split out each implementation into its own repo and use a plugin architecture

## PyPI release

TODO
