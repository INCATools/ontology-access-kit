.. _mapping_provider_interface:

Mapping Provider
==============

Synopsis
--------

.. code:: python

   >>> DIGIT = 'UBERON:0002544'
   >>> oi = OlsImplementation()
   >>> for m in oi.get_sssom_mappings_by_curie(DIGIT):
   >>>     print(f'{m.subject_id} <-> {m.object_id}')

About
-----

This interface provides a "mappings" abstraction.

.. note ::

    This interface is for serving pre-calculated mappings.
    See :ref:`sssom_utils` for on-the-fly mapping creation

.. warning ::

    Some aspects may change, in particular how symmetrical mappings are handled

Data Model
-----------

The central datamodel used here is `SSSOM <http://w3id.org/sssom>`_


Implementations
---------------

- :ref:`BioportalImplementation`

    - uses the BioPortal API endpoint, which has pregenerated mappings using LOOM
    - requires an :ref:`APIkey`
    - implements a small subset of SSSOM fields
    - match types are unspecified

- :ref:.OlsImplementation` currently implements a subset of SSSOM fields

    - uses the OLS OxO API endpoint, which serves mappings that are provided by source ontologies
    - implements a subset of SSSOM fields
    - the original source is provided

- Others

     - Most other implementations provide this but only serve up limited SSSOM metadata, as only the base triple is stored
     - :ref:`.ProntoImplementation`
     - :ref:`.SqlImplementation`
     - :ref:`.UbergraphImplementation`
     - :ref:`.OntobeeImplementation`

Command Line Use
----------------

.. code::

   runoak -i bioportal: term-mappings UBERON:0002101  -O sssom -o limb-mappings.sssom.tsv


Code
----

Example
^^^^^^^

Autodoc
^^^^^^^


.. currentmodule:: oaklib.interfaces.mapping_provider_interface
                   
.. autoclass:: MappingProviderInterface
    :members:
