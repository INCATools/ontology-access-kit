.. _faq:

OAK FAQ
==========

This is a list of Frequently Asked Questions about OAK.  Feel free to
suggest new entries!

How do I...
-----------

... Install OAK

... get all ancestors of a term?
   You can TODO

... Contribute code

.. _whatis:

What is...
-----------

An iterator
    TODO

.. _usingwith:

Using OAK with...
--------------------

Bioportal
    todo

Troubleshooting
---------------

... Why do I get a "Error: No such option: -i" message
    The :code:`--input` or :code:`-i` option must come *before* the subcommand name. This is because
    the input option is one of the few options that are shared across *all* subcommands.
    For example, you should write :code:`runoak -i my-ont.owl lexmatch -o results.sssom.tsv`