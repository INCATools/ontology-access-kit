.. _funowl_implementation:

FunOwl Adapter
===============

.. currentmodule:: oaklib.implementations.funowl.funowl_implementation

The ``owl:`` selector loads local OWL files with the py-horned-owl-backed OWL
object model. The older ``funowl:`` selector and class name are retained for
backward compatibility, but the implementation is now built on
`py-horned-owl <https://github.com/ontology-tools/py-horned-owl>`_ rather than
the old ``funowl`` package. Plain local ``.owl``, ``.ofn``, ``.omn``, and
``.owx`` paths resolve here by default unless you choose an explicit scheme such
as ``sqlite:`` or ``sparql:``.

See the :ref:`OWL tutorial notebook <adapters_examples>` for a worked walkthrough.

Because the OWL axioms are held in memory rather than a normalized projection of
them, this adapter is the one to reach for when you need axiom-level access:
``axioms()`` and ``filter_axioms()`` return py-horned-owl objects, and
disjointness, transitive properties and property chains are all queryable. It also
implements the graph, search, patch, dump, summary-statistics and text-annotation
interfaces, so it is a drop-in replacement for the SQL adapter in most workflows.
Language-tagged literals are respected, so multilingual ontologies can be queried
by language.

.. note ::

   Annotation assertions are indexed by subject the first time entity metadata is
   requested. Bulk operations (``entities()``, ``labels()``, ``nodes()``) are
   therefore linear in the size of the ontology.

.. autoclass:: FunOwlImplementation
