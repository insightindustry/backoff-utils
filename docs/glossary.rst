**********
Glossary
**********

.. glossary::

  Backoff Strategy
    An algorithm that determines how to delay between repeated attempts to
    perform an operation that has initially failed.

  Exponential Backoff
    A strategy whereby an operation is retried on failure given a randomized
    delay that raises 2 to the power of the number of attempts that have been
    made.

  Fibonaccial Backoff
    A strategy whereby an operation is retried on failure after delays which
    grow as per the Fibonacci sequence.

  Fixed Backoff
    A strategy whereby an operation is retried on failure after an explicitly
    specified delay.

  Jitter
    A random delay between 0 and 1 second in length that can optionally be
    added to the delay produced by a given backoff strategy.

  Linear Backoff
    A strategy whereby an operation is retried on failure with a monotonic
    (linearly-growing) delay.

  Polynomial Backoff
    A strategy where an operation is retried on failure with a delay
    that grows by a factor of the number of attempts that have been made.

  Scale Factor
    The delay determined by the backoff strategy is multipled by this value
    before the delay is applied. By default, this is set to 1.
