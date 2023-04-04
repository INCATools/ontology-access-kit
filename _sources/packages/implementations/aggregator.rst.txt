.. _aggregator_implementation:

Aggregator Adapter
==================

.. warning ::

   Highly incomplete!

This wraps any number of other implementations, multiplexing queries and aggregating results, treating
as if it were a single unified endpoints

Command Line Usage
------------------

Use the :code:`--add` (:code:`-a`) option before the main command to add additional implementations.

E.g

.. code::

    runoak -i db/mp.db -a db/hp.db COMMAND [COMMAND OPTIONS]

Code
----

.. currentmodule:: oaklib.implementations.aggregator.aggregator_implementation
                   
.. autoclass:: AggregatorImplementation
