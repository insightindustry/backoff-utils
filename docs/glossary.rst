###########
Glossary
###########

.. |br| raw:: html

  <br/>

.. glossary::

  Exponential Backoff
    A strategy whereby an operation is retried on failure given a randomized
    delay factored by the number of failed attempts.

  Fibonaccial Backoff
    A strategy whereby an operation is retried on failure after delays which
    grow as per the Fibonacci sequence.

  Fixed Backoff
    A strategy whereby an operation is retried on failure after an explicitly
    specified delay.

  Linear Backoff
    A strategy whereby an operation is retried on failure with a monotonic
    (linearly-growing) delay.

  Polynomial Backoff
    A strategy where an operation is retried on failure with a randomized delay
    factored according to a polynomial.
