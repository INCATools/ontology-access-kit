.. _funowl_implementation:

FunOwl Adapter
===============

.. currentmodule:: oaklib.implementations.funowl.funowl_implementation

The ``funowl`` adapter keeps its historical selector and class name for backward
compatibility, but it is now implemented on top of
`py-horned-owl <https://github.com/ontology-tools/py-horned-owl>`_ rather than
the old ``funowl`` package. Plain local ``.owl``, ``.ofn``, ``.omn``, and
``.owx`` paths resolve here by default unless you choose an explicit scheme such
as ``sqlite:`` or ``sparql:``.

.. autoclass:: FunOwlImplementation
