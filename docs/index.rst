.. Backoff-Utils documentation master file, created by
   sphinx-quickstart on Wed Apr 11 11:51:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################################
Backoff-Utils - Python Library for Backoff/Retry Strategies
####################################################################

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

.. contents::
  :depth: 3
  :backlinks: entry

The **Backoff-Utils** is a Python library that provides Python functions and decorators
to help apply various backoff / retry strategies to your Python function and method
calls.

Installation
====================================

To install **Backoff-Utils**, just execute:

.. code:: bash

  $ pip install backoff-utils

Hello, World Example
=========================

.. code:: python

  from backoff_utils import strategies

  # Using a Function Call
  from backoff_utils import backoff

  def some_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = backoff(some_function,
                   strategy = strategies.exponential,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3)

  # Using a Decorator
  from backoff_utils import backoff

  @apply_backoff(max_tries = 3, strategy = strategies.exponential)
  def some_decorated_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

    result = some_decorated_function('value1', 'value2', kwarg1 = 'value3')


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
