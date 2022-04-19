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

Then open wing-vein.png

If you omit the --output option then the png will be written to a temp file and immediately opened:

.. code-block::

    runoak -i obolibrary:fbbt.obo viz FBbt:00004751 -p i,p

How this works
---------------

 - First,

Programmatic usage
---------------

TODO: use test_obograph_utils for example


