# -*- coding: utf-8 -*-

"""
backoff_utils._decoratory
#########################

Implements the ``@apply_backoff()`` decorator which can be applied to
function/method calls and retries on failure based on arguments passed to the
``backoff()`` function.

"""
from functools import wraps

from backoff_utils._backoff import backoff

def apply_backoff(strategy = None,
                  max_tries = None,
                  catch_exceptions = None,
                  on_failure = None,
                  on_success = None):
    """Decorator that applies a backoff strategy to a decorated function/method.

    :param strategy: The :class:`BackoffStrategy` to use when determining the
      delay between retry attempts. If ``None``, defaults to
      :ref:`exponential <ExponentialBackoff>`.
    :type strategy: :class:`BackoffStrategy`

    :param max_tries: The maximum number of times to attempt the call. Defaults to ``3``.
    :type max_tries: int

    :param catch_exceptions: The ``type(exception)`` to catch and retry. If
      ``None``, will catch all exceptions. Defaults to ``None``.
    :type catch_exceptions: iterable of form ``[type(exception()), ...]``

    :param on_failure: The :ref:`exception <python:Exception>` or function to call
      when all retry attempts have failed. If ``None``, will raise the last-caught
      :ref:`exception <python:Exception>`. If an :ref:`exception <python:Exception>`,
      will raise the exception with the same message as the last-caught exception.
      If a function, will call the function and pass the last-raised exception, its
      message, and stacktrace to the function. Defaults to ``None``.
    :type on_failure: :ref:`Exception <python:Exception>` / function / ``None``

    :param on_success: The function to call when the operation was successful.
      The function receives the result of the ``to_execute`` or ``retry_execute``
      function that was successful, and is called before that result is returned
      to whatever code called the backoff function. If ``None``, will just return
      the result of ``to_execute`` or ``retry_execute`` without calling a handler.
      Defaults to ``None``.
    :type on_success: callable / ``None``

    Example:

    .. code:: python

      @apply_backoff(strategy = strategies.ExponentialBackoff,
                     max_tries = 5)
      def some_function(arg1, arg2, kwarg1 = None):
          pass

      result = some_function('value1', 'value2', kwarg1 = 'value3')


    """
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return backoff(to_execute = func,
                           args = args,
                           kwargs = kwargs,
                           strategy = strategy,
                           max_tries = max_tries,
                           catch_exceptions = catch_exceptions,
                           on_failure = on_failure,
                           on_success = on_success)
        return wrapper

    return real_decorator
