*************************************
API Reference
*************************************

.. contents::
  :local:
  :depth: 2
  :backlinks: entry

------

.. _backoff:

:func:`backoff() <backoff_utils._backoff.backoff>` Function
===============================================================

.. autofunction:: backoff_utils._backoff.backoff

-----

.. _apply_backoff:

:func:`@apply_backoff() <backoff_utils._decorator.apply_backoff>` Decorator
==============================================================================

.. autofunction:: backoff_utils._decorator.apply_backoff

------

Strategies
=============

.. module:: backoff_utils.strategies

Exponential
-------------

.. autoclass:: backoff_utils.strategies.Exponential

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <BackoffStrategy.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: Exponential.delay

-------------

Fibonacci
------------

.. autoclass:: backoff_utils.strategies.Fibonacci

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <Fibonacci.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: Fibonacci.delay

--------------

Fixed
---------

.. autoclass:: backoff_utils.strategies.Fixed

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <Fixed.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: sequence
  :annotation: = None

  The sequence of base delay times (in seconds) to return based on the attempt number.

  .. note::

    If the number of attempts exceeds the length of the sequence, the last delay
    in the sequence will be repeated.

  .. tip::

    If no sequence is given, by default each base delay will be 1 second long.

  :rtype: iterable of numbers / :class:`None <python:NoneType>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: Fixed.delay

-------------

Linear
---------

.. autoclass:: backoff_utils.strategies.Linear

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <Linear.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: Linear.delay

------------

Polynomial
-------------

.. autoclass:: backoff_utils.strategies.Polynomial

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: exponent
  :annotation: = 1.0

  The exponent to apply when calculating the base delay. Defaults to ``1.0``.

  :rtype: :class:`float <python:float>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <Fixed.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: Polynomial.delay

-------------------

Meta-classes
===============

BackoffStrategy
-----------------------------

.. autoclass:: backoff_utils.strategies.BackoffStrategy

Class Attributes
^^^^^^^^^^^^^^^^^

.. attribute:: IS_INSTANTIATED
  :annotation: = False

  Indicates whether the object is an instance of the strategy, or merely its
  class object.

  :rtype: :class:`bool <python:bool>`

Properties
^^^^^^^^^^^

.. attribute:: attempt
  :annotation: = None

  The number of the attempt that the strategy is currently evaluating.

  :rtype: :class:`int <python:int>` / :class:`None <python:NoneType>`

.. attribute:: minimum
  :annotation: = 0.0

  The minimum delay to apply, expressed in seconds.

  :rtype: :class:`float <python:float>`

.. attribute:: jitter
  :annotation: = True

  If ``True``, will add a random :class:`float <python:float>` between 0 and 1 to
  the delay.

  :rtype: :class:`bool <python:bool>`

.. attribute:: scale_factor
  :annotation: = 1.0

  A factor by which the :func:`time_to_sleep <BackoffStrategy.time_to_sleep>` is
  multiplied to adjust its scale.

  :rtype: :class:`float <python:float>`

.. attribute:: time_to_sleep
  :annotation: = 0.0 (read-only)

  The base number of seconds to delay before allowing a retry.

  :rtype: :class:`float <python:float>`

Class Methods
^^^^^^^^^^^^^^^^

.. automethod:: BackoffStrategy.delay
