***********************
Backoff-Utils
***********************

**Python Library for Backoff/Retry Strategies**

.. list-table::
  :widths: 10 90
  :header-rows: 1

  * - Branch
    - Unit Tests
  * - `latest <https://github.com/insightindustry/backoff-utils/tree/master>`_
    -
      .. image:: https://travis-ci.org/insightindustry/backoff-utils.svg?branch=latest
        :target: https://travis-ci.org/insightindustry/backoff-utils
        :alt: Build Status (Travis CI)

      .. image:: https://codecov.io/gh/insightindustry/backoff-utils/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/insightindustry/backoff-utils
        :alt: Code Coverage Status (Codecov)

      .. image:: https://readthedocs.org/projects/backoff-utils/badge/?version=latest
        :target: http://backoff-utils.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status (ReadTheDocs)

  * - `v. 1.0.0 <https://github.com/insightindustry/backoff-utils/tree/v.1.0.0>`_
    -
      .. image:: https://travis-ci.org/insightindustry/backoff-utils.svg?branch=v.1.0.0
        :target: https://travis-ci.org/insightindustry/backoff-utils
        :alt: Build Status (Travis CI)

      .. image:: https://codecov.io/gh/insightindustry/backoff-utils/branch/v.1.0.0/graph/badge.svg
        :target: https://codecov.io/gh/insightindustry/backoff-utils
        :alt: Code Coverage Status (Codecov)

      .. image:: https://readthedocs.org/projects/backoff-utils/badge/?version=v.1.0.0
        :target: http://backoff-utils.readthedocs.io/en/latest/?badge=v.1.0.0
        :alt: Documentation Status (ReadTheDocs)

  * - `develop <https://github.com/insightindustry/backoff-utils/tree/develop>`_
    -
      .. image:: https://travis-ci.org/insightindustry/backoff-utils.svg?branch=develop
        :target: https://travis-ci.org/insightindustry/backoff-utils
        :alt: Build Status (Travis CI)

      .. image:: https://codecov.io/gh/insightindustry/backoff-utils/branch/develop/graph/badge.svg
        :target: https://codecov.io/gh/insightindustry/backoff-utils
        :alt: Code Coverage Status (Codecov)

      .. image:: https://readthedocs.org/projects/backoff-utils/badge/?version=develop
        :target: http://backoff-utils.readthedocs.io/en/latest/?badge=develop
        :alt: Documentation Status (ReadTheDocs)

**Backoff-Utils** is a Python library that provides Python functions and decorators
that apply various backoff / retry strategies to your Python function and method
calls.

The library has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.4, 3.5, and 3.6.

**COMPLETE DOCUMENTATION ON READTHEDOCS:** http://backoff-utils.readthedocs.io/en/latest

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

--------------

Installation
==================

To install **Backoff-Utils**, just execute:

.. code:: bash

  $ pip install backoff-utils

Importing
-------------

Once installed, to import **Backoff-Utils** into your project you can use:

.. code-block:: python

  #: Import the backoff() function.
  from backoff_utils import backoff

  #: Import the @apply_backoff() decorator.
  from backoff_utils import apply_backoff

  #: Import backoff strategies.
  from backoff_utils import strategies

Dependencies
---------------

By design, **Backoff-Utils** are designed to rely on minimal dependencies.
The only dependency they have outside of the Python standard library is:

* `validator-collection <https://github.com/insightindustry/validator-collection/>`_
  which provides for robust validation functionality.

  This library in turn has one external dependency when installed under Python 2.7:

  * `regex <https://pypi.python.org/pypi/regex>`_ which is a drop-in replacement for
    Python's (buggy) standard ``re`` module.

------------------

Hello, World Example
========================

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

------------

Why Backoff-Utils?
======================

.. epigraph::

  *Because now and again, stuff breaks.*

Often, when making external API calls to third-party systems, something goes
wrong. The internet might glitch. The API we're calling might timeout. Gremlins
might eat your packets. Any number of things can go wrong, and Murphy's law tells
us that they will.

Which is why we need backoff strategies. Basically, these are techniques
that we can use to retry function calls after a given delay - and keep retrying
them until either the function call works, or until we've tried so many times that
we just give up and handle the error.

This library is meant to be an incredibly simple utility that provides a number
of easy-to-use backoff strategies. Its core API is to expose:

  * the ``backoff()`` function, which lets you apply
    a given backoff strategy to any Python function call, and;
  * the ``@apply_backoff()`` decorator, which lets
    you decorate any function or method call so that a given backoff strategy is
    *always* applied when the decorated function/method is called.

----------------

Library Features
==================

Supported Strategies
---------------------

The library supports five of the most-common backoff strategies that we've come
across:

* Exponential
* Fibonacci
* Fixed
* Linear
* Polynomial

In addtion, you can also create your own custom strategies as well.

**For more information about the backoff strategies supported, please see:**
`Strategies Explained <https://backoff-utils.readthedocs.io/en/latest/strategies.html>`_

Additional Features
----------------------

In addition to the basic strategies, the library also supports:

* random jitter
* argument-adjustment on retry
* selective exception capture
* chained backoff strategies
* failure handlers
* success handlers
* cut-off after max delay
* cut-off after max tries
* scaling
* minimum delay

**For more information about the backoff strategies supported, please see:**
`Using the Library <https://backoff-utils.readthedocs.io/en/latest/using.html>`_

-------------

Feedback, Support, and Contributing
====================================

We're happy to maintain this library going forward, and would always love to
hear users' feedback - especially if you're running into issues.

Please report issues or questions on the
`project's Github page <https://github.com/insightindustry/backoff-utils/issues>`_

**For more information on contributing to the Backoff-Utils library, please see:**
`Contributor Guide <https://backoff-utils.readthedocs.io/en/latest/contributing.html>`_
