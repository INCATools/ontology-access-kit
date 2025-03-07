.. _datamodels:

Datamodels
==========

This library provides different datamodels designed for different
purposes. They are intentionally overlapping in content, and may be
lossy with respect to one another.

.. note:: You don't need to use *any* of these to use the
          BasicOntologyInterface, which uses simple python datatypes.

Each datamodel represents the perspective of one or more :ref:`interfaces`. For example,
the funowl datamodel is used by OwlInterface, and represents the perspective of an ontology
as being a collection of Owl *axioms*. Other interfaces present different views and do
not need this.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   ontology-metadata/index
   search/index
   obograph/index
   sssom/index
   funowl/index
   kgcl/index
   similarity/index
   summary-statistics/index
   taxon-constraints/index
   validation/index
   lexical-index/index
   mapping-rules/index
   text-annotator/index
   cross-ontology-diff/index
   association/index
   fhir/index
   item-lists/index
   value_set_configuration/index



