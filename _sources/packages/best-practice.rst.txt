.. _best_practice:

Best Practice
=============

External Services
-----------------

Consider making your code robust regardless of whether the ontology implementation is local or a remote service.

Iterators
^^^^^^^^^

Most interface methods that provide more that one result will return :term:`Iterator`s which yield individual elements.
You can iterate over these in exactly the same way you iterate over lists, for example:

.. code:: python

    >>> for curie in oi.basic_search("cell"):
    >>>     ## do something with results
    >>>     print(f'MATCH: {curie}')

If you like you can directly convert an iterator to a list:

.. code:: python

    >>> curies = list(oi.basic_search("cell"))

However, this may be an anti-pattern if the implementation is a remote service and the results include possible thousands of results,
as this will block on waiting for all results.

For more on iterators, see `How to Use Generators and yield in Python <https://realpython.com/introduction-to-python-generators/>`_

Weaving calls together
^^^^^^^^^^^^^^^^^^^^^^

A common pattern is to iterate over a result set and issue a separate call for each result:

.. code:: python

    >>> for curie in oi.basic_search("cell"):
            >>>     print(f'MATCH: {curie} ! {oi.label(curie)}')

        This is fine if the implementation has a low latency for individual calls, but if the implementation is backed by
        a remote service (for example, a SPARQL endpoint like ontobee or ubergraph, or a remote SQL database) then this will
        issue one network call for each result, which may be inefficient.

        One possibility is to use a dedicated method for retrieving batch results, for example
        >>>     print(f'MATCH: {curie} ! {oi.get_label_by_curie(curie)}')

A better approach is to *chunk* over iterators:

Chunking
^^^^^^^^

The :ref:`.chunk` utility function will chunk iterator calls into sizeable amounts:

.. code:: python

    >>> for curie_it in chunk(impl.basic_search(t)):
        >>>     logging.info('** Next chunk:')
        >>>     for curie, label in impl.labels(curie_it):
        >>>         print(f'{curie} ! {label}')

    This is slightly more boilerplate code, and may not be necessary for an in-memory implementation like Pronto. However, this
    pattern could have considerable advantages for result sets that are potentially large. Even if the external server is
    slow to return results, users will see batches or results rather than waiting on the external server to produce
    >>>     logging.info('** Next chunk:')
    >>>     for curie, label in impl.get_labels_for_curies(curie_it):
    >>>         print(f'{curie} ! {label}')

This is slightly more boilerplate code, and may not be necessary for an in-memory implementation like Pronto. However, this
pattern could have considerable advantages for result sets that are potentially large. Even if the external server is
slow to return results, users will see batches or results rather than waiting on the external server to produce *all* results.

Command Line
------------

If you are extending the CLI module or writing a Python application that uses OAK:

- Use click
- Follow CLIG guidelines
- Ensure that there are tests for the command line using test_click