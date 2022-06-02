Part 5: Graph Visualization
=====================

This section of the tutorial requires two dependencies that are outside OAK.

- Graphviz
- OBOGraphViz

Install Graphviz
----------------

Graphviz is an open-source graph visualization software that provides a way to
represent information about graphs and networks.

For installation refer to `Graphviz.org/download/ <https://graphviz.org/download/>`_.


Install OBOGraphViz
-------------------

OBOGraphViz is a Javascript package that allows you to visualize OBOGraphs using Graphviz.

You can use ``npm`` or ``yarn`` to install the OBOGraphViz package.

.. code-block::

    npm install obographviz


Command Line Usage
-----------------

Using OAK, you can generate graph visualizations directly from the command line as follows:

.. code-block::

    runoak -i obolibrary:fbbt.obo viz FBbt:00004751 -p i,p -o wing-vein.png

Then open the file ``wing-vein.png`` using a tool such as Preview, or in a web browser.

If you omit the ``-o/--output`` option then the png will be written to a temp file and immediately opened:

.. code-block::

    runoak -i obolibrary:fbbt.obo viz FBbt:00004751 -p i,p


How this works
---------------

 - First, the :ref:`OboGraphInterface` is invoked to query all ancestors of the term
 - in this case the implementation is :ref:`pronto` plus graph walking code
 - after an obograph is generated this is passed to the obographviz library


Programmatic usage
---------------

TODO: use test_obograph_utils for example


