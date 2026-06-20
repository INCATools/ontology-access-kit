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

.. autoclass:: FunOwlImplementation
