.. Backoff-Utils documentation master file, created by
   sphinx-quickstart on Wed Apr 11 11:51:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################################
Backoff-Utils
####################################################################

.. rubric:: Python Library for Backoff/Retry Strategies

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. sidebar:: Version Compatability

  **Backff-Utils** have only been tested with Python 3.6 and higher.

  They *might* work on earlier versions of Python 3.x, but will definitely
  **not** work on Python 2.x.


.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Contents:

  Home <self>
  Getting Started <getting_started>
  Using the Library <using>
  Strategies Explained <strategies>
  API Reference <api>
  Contributing <contributing>
  Testing Reference <testing>
  Glossary <glossary>

**Backoff-Utils** is a Python library that provides Python functions and decorators
that apply various backoff / retry strategies to your Python function and method
calls.

.. contents::
  :depth: 3
  :backlinks: entry

***************
Installation
***************

To install **Backoff-Utils**, just execute:

.. code:: bash

  $ pip install backoff-utils

***********************
Hello, World Example
***********************

.. code:: python

  from backoff_utils import strategies

  # Using a Function Call
  from backoff_utils import backoff

  def some_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 3600,
                   strategy = strategies.Exponential)

  # Using a Decorator
  from backoff_utils import backoff

  @apply_backoff(strategy = strategies.Exponential, max_tries = 3, max_delay = 3600)
  def some_decorated_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = some_decorated_function('value1', 'value2', kwarg1 = 'value3')

*********************
Why Backoff-Utils?
*********************

.. epigraph::

  *Because now and again, stuff breaks.*

Often, when making external API calls to third-party systems, something goes
wrong. The internet might glitch. The API we're calling might timeout. Gremlins
might eat your packets. Any number of things can go wrong, and Murphy's law tells
us that they will.

Which is why we need :term:`backoff strategies`. Basically, these are techniques
that we can use to retry function calls after a given delay - and keep retrying
them until either the function call works, or until we've tried so many times that
we just give up and handle the error.

This library is meant to be an incredibly simple utility that provides a number
of easy-to-use backoff strategies. Its core API is to expose:

  * the :ref:`backoff() <_backoff.backoff>` function, which lets you apply
    a given backoff strategy to any Python function call, and;
  * the :ref:`@apply_backoff() <_decorator.apply_backoff>` decorator, which lets
    you decorate any function or method call so that a given backoff strategy is
    *always* applied when the decorated function/method is called.

.. seealso::

  For more information about how to use the library, please see |strong|
  :doc:`Using the Library <using>` |/strong|

*******************
Library Features
*******************

Supported Strategies
=======================

The library supports five of the most-common backoff strategies that we've come
across:

* :ref:`Exponential <exponential-backoff>`
* :ref:`Fibonacci <fibonaccial-backoff>`
* :ref:`Fixed <fixed-backoff>`
* :ref:`Linear <linear-backoff>`
* :ref:`Polynomial <polynomial-backoff>`

In addtion, you can also :ref:`create your own custom strategies <custom-strategies>`
as well.

.. seealso::

  For more information about the backoff strategies supported, please see:
  |strong| :doc:`Strategies Explained <strategies>` |/strong|


Additional Features
=====================

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


**************************************
Feedback, Support, and Contributing
**************************************

We're happy to maintain this library going forward, and would always love to
hear users' feedback - especially if you're running into issues.

Please report issues or questions on the
`project's Github page <https://github.com/insightindustry/backoff-utils/issues>`_

We also welcome community contributions - for more information, please see:
:doc:`Contributing <contributing>`.

*********************
Indices and tables
*********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
