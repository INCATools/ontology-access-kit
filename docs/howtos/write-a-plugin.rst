.. _plugin_howto

How to write a plugin
=====================

What is a plugin?
-----------------

A plugin is a software component that adds a specific feature to an existing computer program.
When a program supports plug-ins, it enables customization (`Wikipedia <https://en.wikipedia.org/wiki/Plug-in_(computing)>`_).

In the context of OAK, plugins allow you to add optional functionality to OAK.

An example of a plugin would be a code that uses a machine learning library such as Spacy or NLTK to provide an :ref:`implementation`
of a :ref:`text_annotator`. We wouldn't want to include this in the main library due to the additional dependencies required.
But we might want to allow people to drop in this functionality, e.g.

.. code-block::

    runoak -i my_awesome_plugin: annotate "my text here"

An example plugin
-----------------

`oakx-robot <https://github.com/INCATools/oakx-robot>`_ is a plugin that implements the :ref:`validator` interface, providing
access to OWL reasoners through robot.

You can use this programmatically by first installing it:

.. code-block::

    pip install oakx-robot

And then using the plugin's :ref:`selector`, which is ``robot``:

.. code-block::

    runoak -i robot:tests/input/go-nucleus-unsat.owl validate

This can also be used programmatically

.. code-block:: python

    from oaklib.selector import get_resource_from_shorthand, discovered_plugins, get_adapter
    from oakx_robot.robot_implementation import RobotImplementation, OWL_NOTHING

    path = 'tests/input/go-nucleus-unsat.owl'
    oi = get_adapter(f'robot:{path}')
    if oi.is_coherent():
        print('Congratulations! The ontology is coherent')
    else:
        print('Reasoner detected usatisfiable classes')
        for c in oi.unsatisfiable_classes():
            print(f'Unsatisfiable: {c}')

Creating a plugin
-----------------

Discuss on the issue tracker
^^^^^^^^^^^^^^^^^^^^

First make an issue on the OAK issue tracker - someone may be developing a plugin similar to yours!
You will also want to propose the namespace/scheme you will use.

Create a new project
^^^^^^^^^^^^^^^^^^^^

First create a new python project in the way you would normally do this.

We recommend using poetry, but you can adapt these to whichever system you like:

.. code-block::

    poetry new --src oakx-my-awesome-plugin

The project name should always start with ``oakx-``. Remember, poetry will make a python project that
uses underscores in the name

Then make sure OAK is added as a dependency:

.. code-block::

   poetry add oaklib

Implement one or more interfaces
^^^^^^^^^^^^^^^^^^^

1. Create an Implementation Class
2. Have this implement at least one interface
3. Implement ``__post_init__()``, which initializes the implementation using a Resource object.

Example:

`oakx-robot implementation <https://github.com/INCATools/oakx-robot/blob/main/src/oakx_robot/robot_implementation.py>`_

Implement a selector
^^^^^^^^^^^^^^^^^^^

OAK recognizes plugins by looking for `entry points <https://packaging.python.org/en/latest/specifications/entry-points/>`_ 
in the ``oaklib.plugins`` group. The name of each entry point should be the selector scheme you implement, and the object 
reference of the entry point should be the corresponding implementation. The scheme should match the name used for your 
project, and should be unique, concise, and descriptive. Don't pollute the top level namespace!

The way you specify entry points will depend on the packaging tool your project uses. When using Poetry, your project
would include something like the following in ``pyproject.toml``:

.. code-block:: toml

    [tool.poetry.plugins."oaklib.plugins"]
    robot = "oakx_robot.robot_implementation:RobotImplementation"

If your project does not use Poetry, consult your build tool's documentation for information on how to implement an entry
point (e.g. using `setuptools <https://setuptools.pypa.io/en/latest/userguide/entry_point.html#entry-points-for-plugins>`_).

Write tests
^^^^^^^^^^^^

Write tests as you would for any other project

See for example `oakx-robot tests <https://github.com/INCATools/oakx-robot/tree/main/tests>`_

Release to PyPI
---------------

Release to PyPI as you would any other module. E.g. with poetry:

.. code-block::

    poetry publish