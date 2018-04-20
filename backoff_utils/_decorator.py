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
                  max_delay = None,
                  catch_exceptions = None,
                  on_failure = None,
                  on_success = None):
    """Decorator that applies a backoff strategy to a decorated function/method.

    :param strategy: The :class:`BackoffStrategy` to use when determining the
      delay between retry attempts. If :class:`None <python:None>`, defaults to
      :class:`Exponential <Exponential>`.
    :type strategy: :class:`BackoffStrategy`

    :param max_tries: The maximum number of times to attempt the call.

      If :class:`None <python:None>`, will apply an environment variable
      ``BACKOFF_DEFAULT_TRIES``. If that environment variable is not set, will
      apply a default of ``3``.
    :type max_tries: :class:`int <python:int>` / :class:`None <python:None>`

    :param max_delay: The maximum number of seconds to wait befor giving up once
      and for all.

      If :class:`None <python:None>`, will apply an environment variable
      ``BACKOFF_DEFAULT_DELAY`` if that environment variable is set. If it is not
      set, will not apply a max delay at all.
    :type max_delay: :class:`None <python:None>` / class:`int <python:int>`

    :param catch_exceptions: The ``type(exception)`` to catch and retry. If
      :class:`None <python:None>`, will catch all exceptions.

      Defaults to :class:`None <python:None>`.

      .. caution::

        The iterable must contain one or more types of exception *instances*, and not
        class objects. For example:

        .. code-block:: python

          # GOOD:
          catch_exceptions = (type(ValueError()), type(TypeError()))

          # BAD:
          catch_exceptions = (type(ValueError), type(ValueError))

          # BAD:
          catch_exceptions = (ValueError, TypeError)

          # BAD:
          catch_exceptions = (ValueError(), TypeError())

    :type catch_exceptions: iterable of form ``[type(exception()), ...]``

    :param on_failure: The :class:`exception <python:Exception>` or function to call
      when all retry attempts have failed.

      If :class:`None <python:None>`, will raise the last-caught
      :class:`Exception <python:Exception>`.

      If an :class:`Exception <python:Exception>`, will raise the exception with
      the same message as the last-caught exception.

      If a function, will call the function and pass the last-raised exception, its
      message, and stacktrace to the function.

      Defaults to :class:`None <python:None>`.
    :type on_failure: :class:`Exception <python:Exception>` / function /
      :class:`None <python:None>`

    :param on_success: The function to call when the operation was successful.

      The function receives the result of the decorated function, and is called
      before that result is returned to whatever code called the decorated function.

      If :class:`None <python:None>`, will just return the result of the decorated
      function without calling a handler.

      Defaults to :class:`None <python:None>`.
    :type on_success: callable / :class:`None <python:None>`

    Example:

    .. code:: python

      @apply_backoff(strategy = strategies.ExponentialBackoff,
                     max_tries = 5,
                     max_delay = 30)
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
                           max_delay = max_delay,
                           catch_exceptions = catch_exceptions,
                           on_failure = on_failure,
                           on_success = on_success)
        return wrapper

    return real_decorator
