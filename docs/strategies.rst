***********************
Strategies Explained
***********************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

---------------

Why Are Backoff Strategies Useful?
====================================

.. epigraph::

  *Because now and again, stuff breaks.*

Often, when making function calls, something goes wrong. The internet might
glitch. The API we're calling might timeout. Gremlins might eat your packets.
Any number of things can go wrong, and Murphy's law tells us that they will.

Which is why we need :term:`backoff strategies <backoff strategy>`. Basically, a
backoff strategy is a technique that we can use to retry failing function calls
after a given delay - and keep retrying them until either the function call works,
or until we've tried so many times that we just give up and handle the error.

---------------

How Do Strategies Work?
=========================

In the **Backoff-Utils** library, strategies exist to calculate the delay that
should be applied between retries. That's all they do. Everything else is
handled by the :func:`backoff() <backoff_utils._backoff.backoff>` function and
:func:`@apply_backoff <backoff_utils._decorator.apply_backoff>` decorator.

The library supports five different strategies, each of which inherits from
:class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`.

.. caution::

  :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>` is itself
  an abstract base class and cannot be instantiated directly. You can subclass
  it to create your own custom strategies, or you can supply one of our ready-made
  strategies as the ``strategy`` argument when applying a backoff.

When you apply a backoff strategy, you must supply a ``strategy`` argument which
can accept either a class that inherits from
:class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`, or
an *instance* of a class that inherits from
:class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`.

Passing a class will use the default configuration for the backoff strategy,
while passing an instance will let you modify that configuration. For example:

.. code-block:: python

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   strategy = strategies.Exponential)

will call ``some_function()`` with an
:class:`Exponential <backoff_utils.strategies.Exponential>` strategy applying its
default settings, while:

.. code-block:: python

  my_strategy = strategies.Polynomial(exponent = 3, scale_factor = 0.5)

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   strategy = my_strategy)

will call ``some_function()`` with a
:class:`Polynomial <backoff_utils.strategies.Polynomial>` strategy using an
exponent of 3 and a :term:`scale factor` of 0.5.

---------------

Strategy Features
=====================

.. _jitter:

Random Jitter
----------------

All strategies support using a random :term:`jitter`.

You can deactivate the jitter on a strategy by instantiating it with the argument
``jitter = False``. For example:

.. code-block:: python

  my_strategy = strategies.Exponential(jitter = False)

will ensure that no jitter is applied.

.. hint::

  By default, all strategies apply a random :term:`jitter` unless explicitly
  deactivated.

.. _minimum-delay:

Minimum Delay
--------------

While each strategy calculates its delay based on its own logic, you can ensure
that the delay returned is always a certain minimum number of seconds. You can apply a
minimum by instantiating a strategy with the ``minimum`` argument. For example:

.. code-block:: python

  my_strategy = strategies.Exponential(minimum = 5)

will ensure that at least 5 seconds will pass between retry attempts.

.. hint::

  By default, there is no minimum.

.. _scale-factor:

Scale Factor
--------------

Certain strategies - like the :class:`Polynomial <backoff_utils.strategies.Polynomial>`
strategy - can rapidly lead to very long delays between retry attempts. To offset
this, while still retaining the shape of the curve between retry attempts, each
strategy has a
:func:`scale_factor <backoff_utils.strategies.BackoffStrategy.scale_factor>` property
which is multipled by the "unadjusted" delay. This can be used to reduce (or increase)
the size (technically the magnitude) of the delay.

To apply a :term:`scale factor`, pass it as the ``scale_factor`` argument when
instantiating the strategy. For example:

.. code-block:: python

  my_strategy = strategies.Exponential(scale_factor = 0.5)

will ensure that whatever delay is calculated will always be reduced by 50% before
being applied.

.. hint::

  The :term:`scale factor` defaults to a value of ``1.0``.

---------------

Supported Strategies
======================

The library comes with five commonly-used backoff/retry strategies:

  * :ref:`Exponential <exponential-backoff>`
  * :ref:`Fibonaccial <fibonacci-backoff>`
  * :ref:`Fixed <fixed-backoff>`
  * :ref:`Linear <linear-backoff>`
  * :ref:`Polynomial <polynomial-backoff>`

However, you can also create your own :ref:`custom strategies <custom-strategies>`
by inheriting from :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`.

.. _exponential-backoff:

Exponential
--------------

The base delay time is calculated as:

.. math::

  2^a

where :math:`a` is the number of unsuccessful attempts that have been made.

.. _fibonacci-backoff:

Fibonacci
------------

The base delay time is returned as the Fibonacci number corresponding to the
current attempt.

.. _fixed-backoff:

Fixed
--------

The base delay time is calculated as a fixed value determined by the attempt
number.

To configure the sequence, instantiate the strategy passing an iterable to
``sequence`` like in the example below:

.. code-block:: python

  my_strategy = strategies.Fixed(sequence = [2, 4, 6, 8])

.. note::

  If the number of attempts exceeds the length of the sequence, the last delay
  in the sequence will be repeated.

.. tip::

  If no sequence is given, by default each base delay will be 1 second long.


.. _linear-backoff:

Linear
--------

The base delay time is equal to the attempt count.

.. _polynomial-backoff:

Polynomial
------------

The base delay time is calculated as:

.. math::

  a^e

where:

  * :math:`a` is the number of unsuccessful attempts that have been made,
  * :math:`e` is the ``exponent`` configured for the strategy.

To set the exponent, pass ``exponent`` as an argument to the class as follows:

.. code-block:: python

  my_strategy = strategies.Polynomial(exponent = 2)

will calculate the base delay as

.. math::

  a^2

where :math:`a` is the number of unsuccessful attempts that have been made.

---------------

.. _custom-strategies:

Creating Your Own Strategies
===============================

You can create your own custom backoff strategy by subclassing from
:class:`strategies.BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`.
When you do so, you will need to define your own ``time_to_sleep`` property which
returns a :class:`float <python:float>`.

For example:

.. code-block:: python

  import random
  from backoff_utils import strategies

  class MyCustomStrategy(strategies.BackoffStrategy):
    """This is a custom strategy that will always wait a random number of
    milliseconds."""

    @property
    def time_to_sleep(self):
      return random.random()

The custom strategy created above will always wait a random number of milliseconds,
regardless of anything else. You can make your classes as complicated as they
need to be, and use whatever logic you choose.
