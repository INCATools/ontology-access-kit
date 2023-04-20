.. _concepts:

**NOTE** this is largely replaced by the :ref:`guide`

Ontology Concepts
=================

Here we describe some of the over-arching concepts in this library. Note that distinct :ref:`datamodels` may impose
their own specific views of the world, but the concepts here are intended as a kind of lingua-franca.

Ontology
--------

This library has a very broad concept of what an Ontology is, in keeping with the broad range of use cases addressed.

For many users the concept of an ontology is quite straightforward - it's something like what is described in the GO
paper from 2000, a collection of thousands of inter-related terms. However, the concept of "ontology" turns out to be
very flexible and malleable, and might include things like:

* things that are more "schema-like", such as schema.org or PROV
* formal logical artifacts like BFO
* an "instance graph" for example of countries and their connections
* a knowledge base encoded in RDF
* the entirety of wikidata
* in OWL, an ontology is just a collection of axioms

We try to be as pluralistic as possible and provide a way to access all of the above using
the appropriate abstractions. However, the main community served is "classic" ontologies such
as those found in the OBO library or those encoded in OWL.

Ontology Element
----------------

Ontologies can be conceived of as collection of different kinds of *elements*, which can loosely be thought of as something
with a persistent identifier, and optionally having various kinds of metadata associated with it.

The different kinds of elements are:

* Classes or Concepts -- the predominant kind, for most ontologies
* Properties or Relationship Types
* Individuals or Instances
* Subsets
* Ontologies (an ontology is itself an ontology element)
* Various other elements used for particular purposes

These are not necessarily disjoint categories!

.. note ::

   We sometimes use the term "term" but this can be ambiguous. Sometimes it is equated with the OWL concept of a Class, sometimes it it used
   more broadly to encompass other elements that may have names/labels (for example, Scotland, which is an instance, not a class). And sometimes
   it is used to refer to the string by which the element is denoted!

When working with a specific datamodel these may be partitioned more strictly. For example, in OWL, there are three disjoint kinds of properties:

- ObjectProperties
- AnnotationProperties
- DatatypeProperties

The BasicOntologyInterface does not discriminate between different kinds of elements. This can be confusing,
if you ask for all elements thinking you might get back only the "terms" but you would also get elements for
relationship types, subsets, etc.

Imports and Ontologies within Ontologies
----------------------------------------

Many users are accustomed to ontologies being simple stand-alone monolithic entities, and a lot of tooling makes that assumption.

In fact, many ontologies are organized as modular components that are *imported* by other ontologies, much the same way that
software has evolved from monolithic programs to modular systems. Sometimes for ontologies releases, the imports are *merged* such that
what appears to be one ontology has pieces of other ontologies incorporated in.

This library is designed to handle all of these scenarios. In the BasicOntologyInterface, you don't have to worry about imports,
you just get a view where everything appears as if it were in a single ontologies (even this ontologies actually a combination of
ontologies). Other interfaces let you explore the compositional structure in more detail.

URIs and CURIEs and identifiers
-------------------------------

Some communities prefer to use prefixed identifiers like GO:0008152, others prefer to use URIs as identifiers. This is driven
largely by the tools and infrastructure used, with "semantic web" stacks using URIs and data science/bioinformatics tools
using identifiers.

We bridge these worlds by using CURIEs, essentially prefixed identifiers where there is a well-defined prefix expansion.

Most methods in the interfaces in this library accept CURIEs, but these can always be expanded and contracted.

Prefix Maps
-----------

A prefix map maps between prefixes and their URI base expansions.

Relationships / Edges
---------------------

.. note ::

   It may seem surprising but the OWL standard has no construct that directly corresponds to what we call
   a relationship here.

Mappings
--------

Ontology Format
---------------

Statements and Axioms
---------------------

.. note ::

   You only need to understand this if you are working with the OwlInterface or the RdfInterface.

Subsets
-------

Labels/Names
-------------

It is common for biological ontologies to use an opaque identifier for each element, and include exactly one "name" or "label"
which serves as a unique string for humans to identify the element. In OWL representations, the name is typically represented
using rdfs:label.

This is by no means universal:

- some ontologies use non-opaque identifiers, and omit a separate label field
- some ontologies may use a different property, such as skos:prefLabel
- some ontologies may have some elements that are "dangling" and do not have label populated
- sometimes the same label may be shared by different identifiers, even within an ontology
- some ontologies may have multiple labels for an element

     * this may be intentional, as in the case of different languages (wikidata)
     * or it may be unintentional, for example, resulting from ontology merges of different versions of the same ontology

The OWL datamodel allows for complete flexibility here, giving ontology providers the freedom to model things however they like.
The OBO Format datamodel (and the corresponding obojson) is a little more restrictive here, for example, disallowing multiple labels.

The OBO community have defined a suite of QC checks implemented in the OBO dashboard to try and get ontologies align to a datamodel
where elements have exactly one label.

This library aims to be pluralistic and allow for all scenarios. However, it makes the common case the most "convenient".
And it may also be the case that some interfaces impose a certain restriction - for example, the obograph interface uses
the obograph datamodel which has a maximum cardinality of 1 for labels.

Some implementations may also impose their own restrictions - e.g. pronto, OLS, and bioportal all roughly adhere to the OBO model
of making label be single-valued.
