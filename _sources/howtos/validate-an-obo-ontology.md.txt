# How to Validate an OBO ontology using Obo Metadata Ontology schema

## Steps

### Step 1: Obtain the sqlite version of the ontology

Currently the sqlite version of ontologies are not distributed alongside them in OBO

You can either

 - (a) make the sqlite file yourself, see [INCATools/semantic-sql](https://github.com/INCATools/semantic-sql)
 - (b) get a ready-made download from the [s3 bucket](https://s3.amazonaws.com/bbop-sqlite/)

The second option is likely easiest.

For example:

```bash
wget https://s3.amazonaws.com/bbop-sqlite/uberon.db
```

### Step 2: Install oaklib

```bash
pip install oaklib
```

Check your install works:

```bash
runoak --help
```

### Step 3: Validate an individual ontology


```bash
runoak -i sqlite:uberon.db validate
```

This will stream yaml output. The output is linkml objects using the SHACL Validation vocabulary

```
type: https://w3id.org/shacl/MinCountConstraintComponent
severity: ERROR
subject: CARO:0000003
predicate: rdfs:label
info: Missing slot (label) for CARO:0000003

type: https://w3id.org/shacl/MinCountConstraintComponent
severity: ERROR
subject: CARO:0000006
predicate: rdfs:label
info: Missing slot (label) for CARO:0000006
```

### Step 3 (alternative): Validate multiple ontologies

```bash
runoak validate-multiple db/*.db -o obo-validation.tsv
```


## Caveats

Currently only the following are implemented:

* MinCountConstraintComponent checks (required or recommended)
* MaxCountConstraintComponent checks
* DeprecatedPropertyComponent
* DatatypeConstraintComponent: basic type checks (literal vs object) DOES NOT YET CHECK SPECIFIC LITERAL TYPE
* ClosedConstraintComponent


## Using your own schema

TODO: add an option to pass in your own yaml file

## How this works

The Python API is described here:

 - [ValidatorInterface](https://incatools.github.io/ontology-access-kit/packages/interfaces/validator.html)

Currently there is only one implementation, the SqlDatabase implementation

The validation is driven entirely by a [LinkML](https://linkml.io) schema

Currently this schema lives within this repo, but the goal is to have it live outside and be imported

- [linkml generated docs](https://incatools.github.io/ontology-access-kit/datamodels/ontology-metadata/index.html)
- source: [src/oaklib/datamodels/ontology_metadata.yaml](https://github.com/INCATools/ontology-access-kit/blob/main/src/oaklib/datamodels/ontology_metadata.yaml)

Different implementations are free to use this in different ways

The SqlDatabase implementation attempts to do this in a performant way doing whole-database predicate-based queries

Validation results use the [Validator Datamodel](https://incatools.github.io/ontology-access-kit/datamodels/validation), which reuses many URIs from SHACL

## Analysis

See notebooks folder in [https://github.com/cmungall/obo-metadata](https://github.com/cmungall/obo-metadata)
