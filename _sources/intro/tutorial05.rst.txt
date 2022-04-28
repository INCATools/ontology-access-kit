Part 5: Graph Visualization
=====================

Install OBOGraphViz
--------------

.. code-block::

    npm install obographviz

Command Line Usage
-----------------

.. code-block::

    runoak -i obolibrary:fbbt.obo viz FBbt:00004751 -p i,p -o wing-vein.png

Then open the file wing-vein.png using a tool such as Preview, or in a web browser.

If you omit the --output option then the png will be written to a temp file and immediately opened:

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


