.. Backoff-Utils documentation master file, created by
   sphinx-quickstart on Wed Apr 11 11:51:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

******************
Backoff-Utils
******************

**Python Library for Backoff/Retry Strategies**

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. sidebar:: Version Compatability

  The **Backff-Utils** are designed to be compatible with Python 2.7 and
  Python 3.4 or higher.

.. include:: _unit_tests_code_coverage.rst

.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Contents:

  Home <self>
  Getting Started <getting_started>
  Using the Library <using>
  Strategies Explained <strategies>
  API Reference <api>
  Contributor Guide <contributing>
  Testing Reference <testing>
  Release History <history>

  Glossary <glossary>

**Backoff-Utils** is a Python library that provides Python functions and decorators
that apply various backoff / retry strategies to your Python function and method
calls.

The library has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.4, 3.5, 3.6, 3.7, and 3.8.

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

---------------

Installation
===============

.. include:: _installation.rst

------------------

Hello, World Example
=======================

.. include:: _hello-world.rst

------------------

Why Backoff-Utils?
=====================

.. epigraph::

  *Because now and again, stuff breaks.*

Often, when making external API calls to third-party systems, something goes
wrong. The internet might glitch. The API we're calling might timeout. Gremlins
might eat our packets. Any number of things can go wrong, and Murphy's law tells
us that they will.

Which is why we need :term:`backoff strategies <backoff strategy>`. Basically,
these are techniques that we can use to retry function calls after a given delay
- and keep retrying them until either the function call works, or until we've
tried so many times that we just give up and handle the error.

This library is meant to be an incredibly simple utility that provides a number
of easy-to-use backoff strategies. Its core API is to expose:

  * the :func:`backoff() <backoff_utils._backoff.backoff>` function, which lets you apply
    a given backoff strategy to any Python function call, and;
  * the :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator, which lets
    you decorate any function or method call so that a given backoff strategy is
    *always* applied when the decorated function/method is called.

.. seealso::

  For more information about how to use the library, please see |strong|
  :doc:`Using the Library <using>` |/strong|

Library Features
===================

Supported Strategies
-----------------------

The library supports five of the most-common backoff strategies that we've come
across:

* :ref:`Exponential <exponential>`
* :ref:`Fibonacci <fibonacci>`
* :ref:`Fixed <fixed>`
* :ref:`Linear <linear>`
* :ref:`Polynomial <polynomial>`

In addtion, you can also :ref:`create your own custom strategies <custom-strategies>`
as well.

.. seealso::

  For more information about the backoff strategies supported, please see:
  |strong| :doc:`Strategies Explained <strategies>` |/strong|


Additional Features
--------------------

In addition to the basic strategies, the library also supports:

* :ref:`random jitter <jitter>`
* :ref:`argument-adjustment on retry <argument-adjustment>`
* :ref:`selective exception capture <exception-handling>`
* :ref:`chained backoff strategies <chaining-strategies>`
* :ref:`failure handlers <failure-handling>`
* :ref:`success handlers <success-handling>`
* :ref:`cut-off after a max delay <max-delay>`
* :ref:`cut-off after max tries <max-tries>`
* :ref:`scaling <scale-factor>`
* :ref:`minimum delay <minimum-delay>`


Feedback, Support, and Contributing
=====================================

We're happy to maintain this library going forward, and would always love to
hear users' feedback - especially if you're running into issues.

Please report issues or questions on the
`project's Github page <https://github.com/insightindustry/backoff-utils/issues>`_

We also welcome community contributions - for more information, please see the
|strong| :doc:`Contributor Guide <contributing>` |/strong|.

Indices and tables
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
