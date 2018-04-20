********************
Using the Library
********************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

---------------

Why are Backoff Strategies useful?
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

How does this library help?
=============================

**This library provides a simple one-line approach to using backoff strategies in your code.**

It provides a simple function (:func:`backoff() <backoff_utils._backoff.backoff>`)
and a simple decorator (:func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>`)
that let you easily retry problematic functions using five different configurable
:doc:`strategies <strategies>`.

---------------

Installing the Library
========================

To install **Backoff-Utils**, just execute:

.. code-block:: bash

  $ pip install backoff-utils

Importing the Library
=======================

There are three parts to the library that you should be aware of:

#. The :func:`backoff() <backoff_utils._backoff.backoff>` function, which you can use to
   to apply a backoff strategy to a given function/method call inside your code.
#. The :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator, which you can
   use to always apply a backoff strategy to one of your function/methods.
#. The :doc:`strategies` module, which exposes
   the :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>` classes
   that you supply to the function and decorator, telling them how to delay between
   attempts. The specific strategies are:

   * :class:`strategies.Exponential <backoff_utils.strategies.Exponential>`
   * :class:`strategies.Fibonacci <backoff_utils.strategies.Fibonacci>`
   * :class:`strategies.Fixed <backoff_utils.strategies.Fixed>`
   * :class:`strategies.Linear <backoff_utils.strategies.Linear>`
   * :class:`strategies.Polynomial <backoff_utils.strategies.Polynomial>`

All three of these components are importable directly from the ``backoff_utils``
package as shown below:

.. code-block:: python

  #: Import everything
  from backoff_utils import backoff, apply_backoff, strategies

  #: Import the backoff() function.
  from backoff_utils import backoff

  #: Import the @apply_backoff() decorator.
  from backoff_utils import apply_backoff

  #: Import backoff strategies.
  from backoff_utils import strategies

.. _function-approach:

---------------

Using the Backoff Function Call
=================================

You use the :func:`backoff() <backoff_utils._backoff.backoff>` function when:

  * you want to call some other function/method using a backoff strategy, but that
    function/method is not decorated with
    :func:`@apply_backoff() <backoff_utils._decorator.backoff>`
  * you want to call some other function/method using a backoff strategy, but if that
    call fails, you want to retry using a different call.

.. tip::

  The function approach is often used when we want to apply a backoff strategy
  to a function or method called in someone else's code, like in some imported
  third-party library.

  Since that code won't be using the
  :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>`
  decorator, if we want to apply a backoff strategy we'll need to use the
  :func:`backoff() <backoff_utils._backoff.backoff>` function.

Basic Usage
-------------

For example, let's imagine we have a function:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = value):
      # Function does stuff here

When our code calls ``some_function()``, we want to apply an
:class:`Exponential <backoff_utils.strategies.Exponential>` backoff strategy. We can do so
using:

.. code-block:: python

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   strategy = strategies.Exponential)

Let's breakdown what this does. First, it will try calling:

.. code-block:: python

  result = some_function('value1', 'value2', kwarg1 = 'value3')

If this raises an error, it will retry using an
:class:`Exponential <backoff_utils.strategies.Exponential>` delay. It will
continue to retry, until either it has made 3 attempts or 30 seconds have elapsed.
If this call is still failing after 3 attempts or 30 seconds, it will raise the
last :class:`Exception <python:Exception>` raised by ``some_function()``.

.. note::

  The ``strategy`` argument can accept either a class that inherits from
  :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`, or it can
  accept an *instance* of a class that inherits from
  :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`.

  Passing a class will use the default configuration for the backoff strategy,
  while passing an instance will let you modify that configuration. For example:

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

  .. seealso::

    For more information, please see: :doc:`Strategies Explained <strategies>`.

.. _max-delay:
.. _max-tries:

.. tip::

  If you don't supply a ``max_tries`` argument, the backoff strategy will look
  for a default max in the ``BACKOFF_DEFAULT_TRIES`` environment variable. If
  that environment variable doesn't exist, it will retry your call three times
  then fail.

  If you don't supply a ``max_delay``, the backoff strategy look for a default
  maximum delay in the ``BACKOFF_DEFAULT_DELAY`` environment variable. If that
  environment variable doesn't exist, it will keep retrying your call until it
  hits ``max_tries``.

And that's it!

.. seealso::

  For more detailed documentation, please see the :doc:`API Reference <api>` for the
  :func:`backoff() <backoff_utils._backoff.backoff>` function.

.. _argument-adjustment:

Alternative Fallbacks
-----------------------

The :func:`backoff() <backoff_utils._backoff.backoff>` function allows you to fallback to either
a different function or a different set of arguments after the first failure.

For example, let's imagine a situation where we have two functions:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

  def some_alternative_function(arg1, arg2, arg3, arg4):
      # Function does stuff.

Now, let's try to first call ``some_function()``, and if that doesn't work, we
can automatically try calling ``some_alternative_function()`` after our delay:

.. code-block:: python

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   retry_execute = some_alternative_function,
                   retry_args = ['value1', 'value2', 'value3', 'something else'],
                   retry_kwargs = {},
                   max_tries = 3,
                   max_delay = 30,
                   strategy = strategies.Exponential)

Let's breakdown what this will do. As before, first it will try calling:

.. code-block:: python

  result = some_function('value1', 'value2', kwarg1 = 'value3')

When that doesn't work, it will then try calling:

.. code-block:: python

  result = some_alternative_function('value1' ,'value2', 'value3', 'something else')

until either that is successful, or the strategy exceeds the maximum number of tries
or the maximum delay. If everything fails, then it will raise the
last :class:`Exception <python:exception>` raised by ``some_alternative_function()``.

.. _exception-handling:

Retrying on Specific Errors
-----------------------------

Not all errors are created equal. For some errors, we know with 100% certainty
that retrying a function/method call with the same parameters will produce the
exact same error every time. Which means there's no point to applying a backoff
strategy. However, certain errors may be caused by other factors...which means
that if we try again, the function/method call might just work.

This is often the cause when a function/method is making a call across a network
(like an HTTP request). Such a request might timeout because the API just happened
to be over-burdened when the first request was made. If you want a second, maybe
your next request will get through.

The :func:`backoff() <backoff_utils._backoff.backoff>` function allows you to only apply the
backoff strategy for a defined set of exceptions. If the function/method you're
trying raises an exception that isn't on the list? Then the call won't be retried.

Let's assume we have ``some_function()`` as follows:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

Now, let's further assume that ``some_function()`` will sometimes raise:

* :class:`TimeoutError <python:TimeoutError>`
* :class:`IOError <python:IOError>`
* :class:`NotImplementedError <python:NotImplementedError>`

If we get :class:`NotImplementedError <python:NotImplementedError>`, there's no
point in retrying: The same arguments will always produce the same error. But
the other two errors may just be a momentary glitch, and retrying after some
delay may work. Here's how we would do that:

.. code-block:: python

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   catch_exceptions = [type(TimeoutError), type(IOError)],
                   strategy = strategies.Exponential)

Now, when ``some_function('value1', 'value2', kwarg1 = 'value3')`` raises a
:class:`TimeoutError <python:TimeoutError>` or :class:`IOError <python:IOError>`,
the call will be retried up to 3 times or for 30 seconds (whichever comes first).
If the call raises any other exception, then the call will fail and bubble that
exception up to your code where you'll need to handle it.

.. caution::

  If ``catch_exceptions`` is not :class:`None <python:None>` (the default, which
  will catch all exceptions), then it is very important that the ``catch_exceptions`` argument
  always contain one or more ``type(Exception())`` values. For example:

  .. code-block:: python

    # GOOD: This will work.
    result = backoff(some_function,
                     args = ['value1', 'value2'],
                     kwargs = { 'kwarg1': 'value3' },
                     max_tries = 3,
                     max_delay = 30,
                     catch_exceptions = [type(TimeoutError()), type(IOError())],
                     strategy = strategies.Exponential)

    result = backoff(some_function,
                     args = ['value1', 'value2'],
                     kwargs = { 'kwarg1': 'value3' },
                     max_tries = 3,
                     max_delay = 30,
                     catch_exceptions = type(TimeoutError()),
                     strategy = strategies.Exponential)

    # BAD: This will not work.
    result = backoff(some_function,
                     args = ['value1', 'value2'],
                     kwargs = { 'kwarg1': 'value3' },
                     max_tries = 3,
                     max_delay = 30,
                     catch_exceptions = [TimeoutError, IOError],
                     strategy = strategies.Exponential)

    result = backoff(some_function,
                     args = ['value1', 'value2'],
                     kwargs = { 'kwarg1': 'value3' },
                     max_tries = 3,
                     max_delay = 30,
                     catch_exceptions = [type(TimeoutError), type(IOError)],
                     strategy = strategies.Exponential)

.. _failure-handling:

Handling Failures
-------------------

Sometimes, even after retrying stuff, your function/method call will still fail.
That's life. But when that happens, you might want to call some *other* function
or method to do something in response. You can do this by passing that
function/method to the :func:`backoff() <backoff_utils._backoff.backoff>` function
as the ``on_failure`` argument.

For example, let's imagine we have two functions:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

  def error_handler(*args, **kwargs):
      # Function does stuff.

We can have the backoff strategy call ``error_handler()`` when it has a final
failure - meaning after :func:`backoff() <backoff_utils._backoff.backoff>` has tried and failed
multiple times, after it has timed out, or if ``some_function()`` raises an
exception that is not listed in ``catch_exceptions``.

Here's how that would look:

.. code-block:: python

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   catch_exceptions = [type(TimeoutError()), type(IOError())],
                   on_failure = error_handler,
                   strategy = strategies.Exponential)

.. tip::

  If you pass a class that descends from :class:`Exception <python:Exception>`
  to ``on_failure``, that exception will be raised with the message of the
  last exception raised by ``some_function()``.

.. caution::

  If you are passing a custom function (*not* an :class:`Exception <python:Exception>`)
  to ``on_failure``, that custom function must accept three positional arguments:

  #. ``error`` - the last exception raised
  #. ``message`` - the message of the last exception raised
  #. ``traceback`` - the stack trace associated with the last exception raised

  If the ``on_failure`` function cannot accept those three positional arguments,
  or if the ``on_failure`` function itself fails, then the last exception raised
  will bubble up.

.. _success-handling:

Handling Success
------------------

So we've talked a lot about failures here. But sometimes, things work! When
the :func:`backoff() <backoff_utils._backoff.backoff>` function is successful, it will always
return the value back to where it was called. But sometimes, you want to fire a
success handler before that value is returned. You can do this by passing a
handler function to the :func:`backoff() <backoff_utils._backoff.backoff>` function's
``on_success`` argument.

Let's imagine we have the following:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

  def success_handler(value_on_success):
      # Function does stuff.

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 30,
                   catch_exceptions = [type(TimeoutError()), type(IOError())],
                   on_success = success_handler,
                   strategy = strategies.Exponential)

  # some more stuff happens here

Now, when ``some_function()`` is successful, *before* ``result`` is returned
to your code, the :func:`backoff() <backoff_utils._backoff.backoff>` function will call:

.. code-block:: python

  success_handler(result)

When ``success_handler()`` returns control, the :func:`backoff() <backoff_utils._backoff.backoff>`
function will return ``result`` and your code can continue.

.. caution::

  It is very important that your ``on_success`` function always accept a single
  ``result`` value. This will always be the value returned by function/method
  you were trying to call using a backoff strategy.

.. tip::

  A common pattern is to make your ``on_success`` function an asynchronous
  function. This can help parallelize your code to some extent, which means
  your code isn't waiting for your ``on_success`` handler to complete before
  continuing.

.. _decorator-approach:

Using the Decorator Approach
=================================

You use the :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator when you
want to *always* apply a particular backoff strategy to one of your functions or
methods.

Basic Usage
-------------

For example, let's imagine we have a function:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = value):
      # Function does stuff here

  result = some_function('value1', 'value2', kwarg1 = 'value3')

Whenever your code calls ``some_function()``, we want to apply an
:class:`Exponential <backoff_utils.strategies.Exponential>` backoff strategy for
a maximum of 5 tries provided they don't take longer than 30 seconds. Here's how we would do that:

.. code-block:: python

  @apply_backoff(strategies.Exponential, max_tries = 5, max_delay = 30)
  def some_function(arg1, arg2, kwarg1 = value):
      # Function does stuff here

  result = some_function('value1', 'value2', kwarg1 = 'value3')

That's it! Now, whenever you call ``some_function()``, the decorator will look
for an error, and if it catches one, will retry the call after an exponential
delay. It will keep retrying until it has tried five times, or until 30 seconds
have passed - whichever is first.

.. note::

  Just as when using the :ref:`function call approach <function-approach>`,
  you can pass the :class:`BackoffStrategy <backoff_utils.strategies.BackoffStrategy>`,
  the number of ``max_tries``, and ``max_delay`` to the
  :func:`@apply_backoff <backoff_utils._decorator.apply_backoff>` decorator.

.. seealso::

  For more detailed documentation, please see the :doc:`API Reference <api>` for the
  :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator.

Alternative Fallbacks
-----------------------

.. caution::

  The :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator does not
  support alternative fallbacks. If you want to use alternative fallbacks, then
  we suggest using the :ref:`function approach <function-approach>`.

Retrying on Specific Errors
-----------------------------

When using the :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator,
you can retry on specific errors by passing those error types to the decorator's
``catch_exceptions`` argument.

.. seealso::

  This works the same as the ``catch_exceptions`` argument when using the
  :ref:`function call approach <exception-handling>`.

Handling Failures
-------------------

.. seealso::

  When using the :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator,
  you can fire an ``on_failure`` handler by passing an ``on_failure`` argument
  just as you can for the :ref:`function call approach <failure-handling>`.

Handling Success
-------------------

.. seealso::

  When using the :func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` decorator,
  you can fire an ``on_success`` handler by passing an ``on_success`` argument
  just as you can for the :ref:`function call approach <success-handling>`.

---------------

.. _chaining-strategies:

Stacking / Nesting / Chaining Strategies
==================================================

Let's imagine that the function/method you want to call will raise two different
errors, and you want to apply a *different* backoff strategy for each error. Using
the library, that's fairly straightforward.

For example, let's imagine we have a function:

.. code-block:: python

  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

which sometimes raises a :class:`TimeoutError <python:TimeoutError>` and sometimes
an :class:`IOError <python:IOError>`.

Let's further assume that if it raises a :class:`TimeoutError <python:TimeoutError>`,
we want to apply an :class:`Exponential` strategy up to five times, but for an
:class:`IOError <python:IOError>` we want to apply a :class:`Linear` strategy up to
3 times.

Using the Function Approach
-----------------------------

Here's how we could do that using the function approach:

.. code-block:: python

  def backoff_for_timeout():
      return backoff(some_function,
                     args = ['value1', 'value2'],
                     kwargs = { 'kwarg1': 'value3' },
                     max_tries = 5,
                     catch_exceptions = [type(TimeoutError())],
                     strategy = strategies.Exponential)

  result = backoff(backoff_for_timeout,
                   max_tries = 3,
                   catch_exceptions = [type(IOError())],
                   strategy = strategies.Linear)

First, your code will call the :func:`backoff() <backoff_utils._backoff.backoff>` function
for ``backoff_for_timeout()``. It will be looking to catch any
:class:`IOError <python:IOError>` that ``backoff_for_timeout()`` raises. When it
catches one, it will retry up to three times using the :class:`Linear <backoff_utils.strategies.Linear>` strategy.

When the :func:`backoff() <backoff_utils._backoff.backoff>` function calls ``backoff_for_timeout()``,
that function will in turn call another :func:`backoff() <backoff_utils._backoff.backoff>` function
for ``some_function()``. It will be looking to catch any
:class:`TimeoutError <python:TimeoutError>` exceptions that ``some_function()`` raises.
When it catches one, it will retry up to five times using the
:class:`Exponential <backoff_utils.strategies.Exponential>` strategy.

At this point, if ``some_function()`` raises an :class:`IOError <python:IOError>`, however,
it will bubble up to the first :func:`backoff() <backoff_utils._backoff.backoff>` function, which
will catch and handle it.

Using the Decorator Approach
-------------------------------

Here's how we could do it using the :func:`@apply_backoff <backoff_utils._decorator.apply_backoff>`
decorator:

.. code-block:: python

  @apply_backoff(strategies.Linear, max_tries = 3, catch_exceptions = type(IOError))
  @apply_backoff(strategies.Exponential, max_tries = 5, catch_exceptions = type(TimeoutError))
  def some_function(arg1, arg2, kwarg1 = None):
      # Function does stuff.

  result = some_function('value1', 'value2', kwarg1 = 'value3')

Now, when your code calls ``some_function()``, it will first try to catch any
:class:`TimeoutError <python:TimeoutError>` raised by ``some_function()``. If it
catches one, it will retry ``some_function()`` up to 5 times using an
:class:`Exponential <backoff_utils.strategies.Exponential>` strategy.

If ``some_function()`` raises anything other than a
:class:`TimeoutError <python:TimeoutError>`, that error will bubble up to the *next*
decorator you've applied. That decorator looks for a :class:`IOError <python:IOError>`.
If it catches one, it will retry up to 3 times using a
:class:`Linear <backoff_utils.strategies.Linear>` strategy.
