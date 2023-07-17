.. _logical_definitions:

Logical Definitions
===================

:term:`Logical Definitions<LogicalDefinition>` are special kinds of :term:`Axioms<Axiom>` that
define a term in terms of other terms, in a way that is *computable*. OAK provides ways of
operating structurally on logical definitions. Logical definitions may also be used by
:term:`Reasoners<Reasoner>` to infer :term:`Entailed` axioms.

Typically, logical definitions are not directly used by consumers of ontologies, so
this section can be skipped by many OAK users. However, if you are interested in
generating, analyzing, summarizing, or other kinds of operations on logical definitions,
this section is intended to provide an overview of the basic concepts.

Logical Definitions in OWL
--------------------------

In OWL, logical definitions are represented using the
`EquivalentClasses axiom <https://www.w3.org/TR/owl2-syntax/#EquivalentClasses>`_.
But note that not every equivalence axioms is a logical definition, according to how
we use the term in OAK. For example, an equivalence axiom connects two *named classes*
doesn't really function to define either class, as this would be circular.

For purposes here, we consider any equivalence axiom between a *named class* on the left
hand side and an *anonymous class expression* on the right hand side to be a logical definition.

These equivalence axioms can be viewed in ontology browsers such as OLS. For example,
the Uberon [fingernail](http://purl.obolibrary.org/obo/UBERON_0009565) class, has an
equivalence axiom to the expression:

.. code-block::

    Equivalent to
        (nail and part of (RO) some manual digit)


Genus-differentia form logical definitions
------------------------------------------

OAK includes dedicated functionality for logical definitions that follow *genus-differentia*
form. These are sometimes known as *Aristotelian definitions*. A genus-differentia definition
takes the form:

``a C is a G that D``

where ``C`` is the defined class, ``G`` is the genus, and ``D`` is the differentia or *differentiating
characteristics*. The differentiating characteristics are typically a list of :term:`Predicate` and "Filler"
class pairs.

For example:

``a fingernail is a nail that is part of a finger``

Here we are defining a fingernail (defined class) in terms of a specialization of a parent class (nail, the genus)
based on a differentiating characteristics (differentia) based on parthood (the predicate) and
a specific "filler" (finger).

This seems trivial but in fact these kinds of definitions -- when provided in computable
form -- can be used to automate a large amount of ontology development. And they can
be useful for queries over an ontology too.

It is generally considered good practice for textual definitions to be consistent with
the computable genus-differentia form.

The Obo Graphs Model
--------------------

The :term:`OBO Graphs` data model includes a data structure / class for representing
logical definitions in genus-differentia form. It limits the differentiae to be a set
of existential restrictions, with no nesting.

Currently most operations in OAK that deal with logical definitions expect them to be
in this form. This can sometimes be limiting if you wish to operate over more complicated
OWL axioms. We may provide support for this in the future, but for now the simple form
provided in the OBO Graphs data model works for a large number of ontologies. The simple
form is often recommended because mistakes are far more common when more complicated
structures are used.

Querying for logical definitions in OAK
----------------------------------------

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon logical-definitions .desc//p=i nail

By default, results are returned in YAML:

.. code-block:: yaml

      definedClassId: UBERON:0009565
      genusIds:
      - UBERON:0001705
      restrictions:
      - fillerId: UBERON:0002389
        propertyId: BFO:0000050
      ...

You can specify `-O csv` to get it in tabular form:

.. csv-table:: uberon nail logical definitions
    :header: definedClassId,definedClassId_label,genusIds,genusIds_label,restrictions,restrictionsPropertyIds,restrictionsPropertyIds_label,restrictionsFillerIds,restrictionsFillerIds_label

    UBERON:0009565,nail of manual digit,UBERON:0001705,nail,BFO:0000050=UBERON:0002389,BFO:0000050,part of,UBERON:0002389,manual digit
    UBERON:0009567,nail of pedal digit,UBERON:0001705,nail,BFO:0000050=UBERON:0001466,BFO:0000050,part of,UBERON:0001466,pedal digit
    UBERON:0011273,nail of manual digit 1,UBERON:0001705,nail,BFO:0000050=UBERON:0001463,BFO:0000050,part of,UBERON:0001463,manual digit 1
    UBERON:0011274,nail of manual digit 2,UBERON:0001705,nail,BFO:0000050=UBERON:0003622,BFO:0000050,part of,UBERON:0003622,manual digit 2
    UBERON:0011275,nail of manual digit 3,UBERON:0001705,nail,BFO:0000050=UBERON:0003623,BFO:0000050,part of,UBERON:0003623,manual digit 3
    UBERON:0011276,nail of manual digit 4,UBERON:0001705,nail,BFO:0000050=UBERON:0003624,BFO:0000050,part of,UBERON:0003624,manual digit 4
    UBERON:0011277,nail of manual digit 5,UBERON:0001705,nail,BFO:0000050=UBERON:0003625,BFO:0000050,part of,UBERON:0003625,manual digit 5
    UBERON:0011278,nail of pedal digit 1,UBERON:0001705,nail,BFO:0000050=UBERON:0003631,BFO:0000050,part of,UBERON:0003631,pedal digit 1
    UBERON:0011279,nail of pedal digit 2,UBERON:0001705,nail,BFO:0000050=UBERON:0003632,BFO:0000050,part of,UBERON:0003632,pedal digit 2
    UBERON:0011280,nail of pedal digit 3,UBERON:0001705,nail,BFO:0000050=UBERON:0003633,BFO:0000050,part of,UBERON:0003633,pedal digit 3
    UBERON:0011281,nail of pedal digit 4,UBERON:0001705,nail,BFO:0000050=UBERON:0003634,BFO:0000050,part of,UBERON:0003634,pedal digit 4
    UBERON:0011282,nail of pedal digit 5,UBERON:0001705,nail,BFO:0000050=UBERON:0003635,BFO:0000050,part of,UBERON:0003635,pedal digit 5

The command has a number of options for transforming this to a matrix, customizing
where rows, columns, and values with be defined classes, genus terms, predicates, or fillers.

:term:`OBO Format` also provides a compact way of showing logical definitions, these can be
seen in OAK using the ``-O obo`` option:

.. code-block:: bash

    $ runoak -i sqlite:obo:uberon logical-definitions .desc//p=i nail -O obo

.. code-block::

    [Term]
    id: UBERON:0009565 ! nail of manual digit
    intersection_of: UBERON:0001705 ! nail
    intersection_of: BFO:0000050 UBERON:0002389 ! manual digit

    [Term]
    id: UBERON:0009567 ! nail of pedal digit
    intersection_of: UBERON:0001705 ! nail
    intersection_of: BFO:0000050 UBERON:0001466 ! pedal digit


Reasoning using logical definitions
-----------------------------------

Currently OAK does not support classification-style reasoning. If you need this,
we recommend doing this ahead of time using a tool like ROBOT.

Logical definitions and design patterns
---------------------------------------

Creating logical definitions by hand can be time consuming and error prone. Many groups
choose to do this via a templating system such as:

- ROBOT templates
- DOSDPs
- OTTR templates
- LinkML-OWL

Currently OAK does not support generating logical definition axioms or any other OWL
axioms from templates, but it might in the future

Generating logical definitions
------------------------------

Sometimes it can be useful to generate logical definitions using heuristic methods such
as lexical pattern matching. In general these generated definitions should be reviewed
by experienced ontology developers before being added, but they can be useful to both
get a sense of missing definitions or as an aid to manual definition creation.

Some OAK commands have a ``generate`` counterpart; above we saw the ``logical-definitions``
command which is for looking up existing logical definitions. The ``generate-logical-definitions``
counterpart can be used for generating logical definitions based on specified lexical patterns.

At this time, this command is experimental, and the flags may change.

Analyzing logical definitions
------------------------------

OAK will soon provide commands for analyzing logical definitions, in particular to determine
consistency of lattice population.

Validating logical definitions
------------------------------

The ``validate-definitions`` command is used for validating text definitions - one aspect
of this is checking for consistency between text and logical definitions.

Further reading
---------------

* `Use of OWL within the Gene Ontology <https://www.biorxiv.org/content/10.1101/010090v1>`_
* `Cross-Product Extensions of the Gene Ontology <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2910209/>`_