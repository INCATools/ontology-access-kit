.. _obsoletion:

Obsoletion
=========

Looking up obsoleted entities
----------------------------

In OAK, the terms :term:`Obsolete` and "deprecated" are used interchangeably.

Obsoletion is an important part of any ontology's lifecycle. Sometimes it is necessary to
obsolete an :term:`Identifier` because it is no longer a good representation of a concept,
or because it becomes out of scope, or it is discovered to be equivalent to an existing concept.

A good ontology will never *delete* an identifier, but will instead mark it as obsolete.

The way in which is to specify an entity is obsolete is fairly standard, using an ``owl:deprecated`` :term:`Annotation Assertion`.

In :term:`Turtle`:

.. code-block:: turtle

    MYO:123456 owl:deprecated true ;
               rdfs:label "obsolete foo" .

In :term:`OBO Format`:

.. code-block:: yaml

    id: MYO:123456
    name: obsolete foo
    is_obsolete: true

Note the use of the :term:`Label` prefixed with "obsolete" is purely a convention, the
standard way to mark an entity as obsolete is to use the ``owl:deprecated`` annotation assertion.

You can query for all obsolete entities in an ontology using the `obsoletes <https://incatools.github.io/ontology-access-kit/cli.html#runoak-obsoletes>`_ command:

.. code-block:: bash

    $ runoak -i sqlite:obo:hp obsoletes
    ...
    HP:0040180	obsolete Hyperkeratosis pilaris
    HP:0040193	obsolete Pinealoblastoma
    HP:0040199	obsolete Flat midface
    ...

You can also use ``.is_obsolete`` as a query term as input to other commands, e.g

.. code-block:: bash

    $ runoak -i sqlite:obo:hp term-metadata .is_obsolete

In python, querying obsoleted entities is provided by the :ref:`basic_ontology_interface`:

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:hp")
    >>> for entity in sorted(adapter.obsoletes()):
    ...    print(entity)
    <BLANKLINE>
    ...
    HP:0040180
    ...
    HP:0040199
    ...

Conventions and standards
-------------------------

For ontologies that are part of OBO, additional conventions apply. These conventions
are not yet fully standardized within OMO:

obsolete entities should not be in the signature of any logical axiom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- note that some older ontologies include obsolete classes as a subclass of an ObsoleteClass node
- this is not treated in any special way in OAK

obsolete entities should be accompanied by metadata that provides additional context for humans and machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- a `term replaced by <http://purl.obolibrary.org/obo/IAO_0100001>`_ annotation indicates where an automatic replacement can be made
- a `consider <http://www.geneontology.org/formats/oboInOwl#>`_ annotation indicates potential replacements that should be manually evaluated

In OAK, this can be retrieved like any other metadata using the entity_metadata methods from :ref:`BasicOntologyInterface`.

On the command line:

.. code-block:: bash

    $ runoak -i sqlite:obo:go term-metadata GO:0000005

returns:

.. code-block:: yaml

    IAO:0000115:
    - OBSOLETE. Assists in the correct assembly of ribosomes or ribosomal subunits in
      vivo, but is not a component of the assembled ribosome when performing its normal
      biological function.
    id:
    - GO:0000005
    oio:consider:
    - GO:0042254
    - GO:0044183
    - GO:0051082
    oio:hasExactSynonym:
    - ribosomal chaperone activity
    oio:hasOBONamespace:
    - molecular_function
    oio:id:
    - GO:0000005
    owl:deprecated:
    - 'true'
    rdfs:comment:
    - This term was made obsolete because it refers to a class of gene products and a
      biological process rather than a molecular function.
    rdfs:label:
    - obsolete ribosomal chaperone activity

To get information about all obsolete entities in an ontology, use the ``.is_obsolete`` query term:

.. code-block:: bash

    $ runoak -i sqlite:obo:go term-metadata .is_obsolete

Merged entities
---------------

In some OBO ontologies such as GO, Mondo, CHEBI, and HPO it is common practice to *merge* entities.
This is similar to standard obsoletion with a replaced-by term, but this is more extreme as metadata
about the merged entity is lost.

In OBO format, this is handled with the ``alt_id`` tag. For example:

.. code-block:: yaml

    id: X:1
    name: x1
    alt_id: X:2

Here, there was previously an entity ``X:2``, this was merged into ``X:1``, and all metadata
about ``X:2`` is lost (although some of it may have been copied into metadata for ``X:1``).

Note that there is no separate entry for X:2 in the OBO file.

In the OBO Format to OWL Translation, this is treated just like obsoletion with replacement,
except there is no metadata about the original class (other than its deprecated axiom), and
there is an additional IAO "obsoletion reason" annotation, with type "term merged".

The above example would be translated to:

.. code-block:: turtle

    X:1 rdfs:label "x1" .
    X:1 oboInOwl:hasAlternativeId X:2 .

    X:2 owl:deprecated true .
    X:2 IAO:0100001 X:1 .
    X:2 IAO:0000231 IAO:0000227 .

OAK uses the underlying OWL model as the standard, so from OAK's perspective, the structure of merged terms and terms that have been obsoleted with
replacement is this is largely similar.

If you run:

.. code-block:: bash

    $ runoak -i sqlite:obo:hp obsoletes

It will show all deprecated IDs, regardless of whether they were merged or not (i.e
alt_ids from OBO format are included). Note that merged entities will show "None" for the
label.

If you wish to exclude merged IDs (i.e. the equivalent of OBO Format stanzas that have
an ``is_obsolete: true``) then pass ``--no-include-merged`` to the command:

.. code-block:: bash

    $ runoak -i sqlite:obo:hp obsoletes --no-include-merged

Further Reading
---------------

* `kgcl:NodeObsoletion <http://w3id.org/kgcl/NodeObsoletion>`_


