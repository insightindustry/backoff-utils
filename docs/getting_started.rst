*************************************
Getting Started
*************************************

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

Installation
====================================

.. include:: _installation.rst

Hello, World
===============

As a quick reference, here are some examples. Each of the examples below performs
up to three attempts, applying an :term:`exponential backoff` strategy with
default configuration:

.. include:: _hello-world.rst

-------------

Library Capabilities
=========================================

There are two ways in which you can apply a backoff/retry strategy using the
**Backoff-Utils**. Which approach you want to use will probably depend on your
code and your code conventions:

  * :ref:`using a function call <function-approach>`
  * :ref:`using a decorator <decorator-approach>`

Both of these approaches support the following backoff strategies:

  * :ref:`Exponential <exponential-backoff>`
  * :ref:`Fibonaccial <fibonacci-backoff>`
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
