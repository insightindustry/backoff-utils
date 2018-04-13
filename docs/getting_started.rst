*************************************
Getting Started
*************************************

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. contents::
  :depth: 3
  :backlinks: entry

Installation
====================================

To install **Backoff-Utils**, just execute:

.. code-block:: bash

  $ pip install backoff-utils

Once installed, to import **Backoff-Utils** into your project you can use:

.. code-block:: python

  #: Import the backoff() function.
  from backoff_utils import backoff

  #: Import the @apply_backoff() decorator.
  from backoff_utils import apply_backoff

  #: Import backoff strategies.
  from backoff_utils import strategies

Hello, World
===============

As a quick reference, here are some examples. Each of the examples below performs
up to three attempts, applying an :term:`exponential backoff` strategy with
default configuration:

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
  from backoff_utils import apply_backoff

  @apply_backoff(max_tries = 3, strategy = strategies.Exponential)
  def some_decorated_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = some_decorated_function('value1', 'value2', kwarg1 = 'value3')

Library Capabilities
=========================================

There are two ways in which you can apply a backoff/retry strategy using the
**Backoff-Utils**. Which approach you want to use will probably depend on your
code and your code conventions:

  * :ref:`using a function call <function-approach>`
  * :ref:`using a decorator <decorator-approach>`

Both of these approaches support the following backoff strategies:

  * :ref:`Exponential <exponential-backoff>`
  * :ref:`Fibonaccial <fibonaccial-backoff>`
  * :ref:`Fixed <fixed-backoff>`
  * :ref:`Linear <linear-backoff>`
  * :ref:`Polynomial <polynomial-backoff>`
  * :ref:`custom strategies <custom-strategies>`

While the library's defaults are usable out-of-the-box, your backoff strategy
can be further tailored to your needs. The library also supports:
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

.. seealso::

  While the **Backoff-Utils** are very straightforward to use, we recommend
  you review |strong| :doc:`Using the Library <using>` |/strong| to learn
  more about what it can do, and for a deep dive please see the
  |strong| :doc:`API Reference <api>` |/strong|.
