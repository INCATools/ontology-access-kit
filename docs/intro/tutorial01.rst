Installation
-------------

Create a directory

.. code-block::

    cd ~
    mkdir oak-tutorial
    cd oak-tutorial

First create a virtual environment

.. code-block::

    python3 -m venv venv
    source venv/bin/activate
    export PYTHONPATH=.:$PYTHONPATH

Make sure you have Python 3.9 or higher

Then install:

.. code-block::

    pip install oaklib

.. code-block::

    runoak --help

Download files
---------------

.. code-block::

    wget