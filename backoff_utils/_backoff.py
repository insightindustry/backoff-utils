# -*- coding: utf-8 -*-

"""
backoff_utils._backoff
#########################

Implements the ``backoff()`` function which executes a function/method call
and retries on failure based on arguments passed to the ``backoff()`` function.

"""
import os
from datetime import datetime
import sys

from validator_collection import validators, checkers

import backoff_utils.strategies as strategies

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)


DEFAULT_MAX_TRIES = os.environ.get('BACKOFF_DEFAULT_TRIES', 3)
DEFAULT_MAX_DELAY = os.environ.get('BACKOFF_DEFAULT_DELAY', None)


class BackoffTimeoutError(Exception):
    """Error that is raised if a backoff strategy timed out without raising
    a different exception."""
    pass


def _handle_failure(on_failure = None,
                    error = None):
    """Handle the failure of a function called by :ref:`backoff`.

    :param on_failure: The :class:`Exception <python:Exception>` or function to call
      when all retry attempts have failed. If :class:`None <python:None>`, will raise the last-caught
      :class:`Exception <python:Exception>`. If an :class:`Exception <python:Exception>`,
      will raise the exception with the same message as the last-caught exception.
      If a function, will call the function and pass the last-raised exception, its
      message, and stacktrace to the function. Defaults to :class:`None <python:None>`.
    :type on_failure: :class:`Exception <python:Exception>` / function / :class:`None <python:None>`

    :param error: The :class:`Exception <python:Exception>` that was raised. Defaults
      to :class:`Exception <python:Exception>`.
    :type error: :class:`Exception <python:Exception>`
    """
    if error is None:
        error = Exception

    is_on_failure_an_exception = False
    if is_py2:
        if isinstance(on_failure, Exception):
            is_on_failure_an_exception = True
        elif checkers.is_type(on_failure, 'type'):
            is_on_failure_an_exception = isinstance(on_failure(), Exception)
        else:
            is_on_failure_an_exception = False
    else:
        is_on_failure_an_exception = checkers.is_type(on_failure,
                                                      ('type', 'Exception')) and \
                                     hasattr(on_failure, '__cause__')


    if on_failure is None:
        raise error
    elif is_on_failure_an_exception:
        raise on_failure(error.args[0])
    else:
        try:
            on_failure(error, error.args[0], sys.exc_info()[2])
        except Exception as nested_error:
            raise nested_error



def backoff(to_execute,
            args = None,
            kwargs = None,
            strategy = None,
            retry_execute = None,
            retry_args = None,
            retry_kwargs = None,
            max_tries = None,
            max_delay = None,
            catch_exceptions = None,
            on_failure = None,
            on_success = None):
    """Retry a function call multiple times with a delay per the strategy given.

    :param to_execute: The function call that is to be attempted.
    :type to_execute: callable

    :param args: The positional arguments to pass to the function on the first attempt.

      If ``retry_args`` is :class:`None <python:None>`, will re-use these
      arguments on retry attempts as well.
    :type args: iterable / :class:`None <python:None>`.

    :param kwargs: The keyword arguments to pass to the function on the first attempt.

      If ``retry_kwargs`` is :class:`None <python:None>`, will re-use these keyword
      arguments on retry attempts as well.
    :type kwargs: :class:`dict <python:dict>` / :class:`None <python:None>`

    :param strategy: The :class:`BackoffStrategy` to use when determining the
      delay between retry attempts.

      If :class:`None <python:None>`, defaults to :class:`Exponential`.
    :type strategy: :class:`BackoffStrategy`

    :param retry_execute: The function to call on retry attempts.

      If :class:`None <python:None>`, will retry ``to_execute``.

      Defaults to :class:`None <python:None>`.
    :type retry_execute: callable / :class:`None <python:None>`

    :param retry_args: The positional arguments to pass to the function on retry attempts.

      If :class:`None <python:None>`, will re-use ``args``.

      Defaults to :class:`None <python:None>`.
    :type retry_args: iterable / :class:`None <python:None>`

    :param retry_kwargs: The keyword arguments to pass to the function on retry attempts.

      If :class:`None <python:None>`, will re-use ``kwargs``.

      Defaults to :class:`None <python:None>`.
    :type subsequent_kwargs: :class:`dict <python:dict>` / :class:`None <python:None>`

    :param max_tries: The maximum number of times to attempt the call.

      If :class:`None <python:None>`, will apply an environment variable
      ``BACKOFF_DEFAULT_TRIES``. If that environment variable is not set, will
      apply a default of ``3``.
    :type max_tries: int / :class:`None <python:None>`

    :param max_delay: The maximum number of seconds to wait befor giving up
      once and for all. If :class:`None <python:None>`, will apply an environment variable
      ``BACKOFF_DEFAULT_DELAY`` if that environment variable is set. If it is not
      set, will not apply a max delay at all.
    :type max_delay: :class:`None <python:None>` / int

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
      :class:`exception <python:Exception>`.

      If an :class:`exception <python:Exception>`, will raise the exception with
      the same message as the last-caught exception.

      If a function, will call the function and pass the last-raised exception, its
      message, and stacktrace to the function.

      Defaults to :class:`None <python:None>`.
    :type on_failure: :class:`Exception <python:Exception>` / function /
      :class:`None <python:None>`

    :param on_success: The function to call when the operation was successful.
      The function receives the result of the ``to_execute`` or ``retry_execute``
      function that was successful, and is called before that result is returned
      to whatever code called the backoff function. If :class:`None <python:None>`,
      will just return the result of ``to_execute`` or ``retry_execute`` without
      calling a handler.

      Defaults to :class:`None <python:None>`.
    :type on_success: callable / :class:`None <python:None>`

    :returns: The result of the attempted function.

    Example:

    .. code-block:: python

      from backoff_utils import backoff

      def some_function(arg1, arg2, kwarg1 = None):
          # Function does something
          pass

      result = backoff(some_function,
                       args = ['value1', 'value2'],
                       kwargs = { 'kwarg1': 'value3' },
                       max_tries = 3,
                       max_delay = 30,
                       strategy = strategies.Exponential)

    """
    # pylint: disable=too-many-branches,too-many-statements

    if to_execute is None:
        raise ValueError('to_execute cannot be None')
    elif not checkers.is_callable(to_execute):
        raise TypeError('to_execute must be callable')

    if strategy is None:
        strategy = strategies.Exponential

    if not hasattr(strategy, 'IS_INSTANTIATED'):
        raise TypeError('strategy must be a BackoffStrategy or descendent')
    if not strategy.IS_INSTANTIATED:
        test_strategy = strategy(attempt = 0)
    else:
        test_strategy = strategy

    if not checkers.is_type(test_strategy, 'BackoffStrategy'):
        raise TypeError('strategy must be a BackoffStrategy or descendent')

    if args:
        args = validators.iterable(args)
    if kwargs:
        kwargs = validators.dict(kwargs)

    if retry_execute is None:
        retry_execute = to_execute
    elif not checkers.is_callable(retry_execute):
        raise TypeError('retry_execute must be None or a callable')

    if not retry_args:
        retry_args = args
    else:
        retry_args = validators.iterable(retry_args)

    if not retry_kwargs:
        retry_kwargs = kwargs
    else:
        retry_kwargs = validators.dict(retry_kwargs)

    if max_tries is None:
        max_tries = DEFAULT_MAX_TRIES

    max_tries = validators.integer(max_tries)

    if max_delay is None:
        max_delay = DEFAULT_MAX_DELAY

    if catch_exceptions is None:
        catch_exceptions = [type(Exception())]
    else:
        if not checkers.is_iterable(catch_exceptions):
            catch_exceptions = [catch_exceptions]

        catch_exceptions = validators.iterable(catch_exceptions)

    if on_failure is not None and not checkers.is_callable(on_failure):
        raise TypeError('on_failure must be None or a callable')

    if on_success is not None and not checkers.is_callable(on_success):
        raise TypeError('on_success must be None or a callable')

    cached_error = None

    return_value = None
    returned = False
    failover_counter = 0
    start_time = datetime.utcnow()
    while failover_counter <= (max_tries):
        elapsed_time = (datetime.utcnow() - start_time).total_seconds()
        if max_delay is not None and elapsed_time >= max_delay:
            if cached_error is None:
                raise BackoffTimeoutError('backoff timed out after:'
                                          ' {}s'.format(elapsed_time))
            else:
                _handle_failure(on_failure, cached_error)
        if failover_counter == 0:
            try:
                if args is not None and kwargs is not None:
                    return_value = to_execute(*args, **kwargs)
                elif args is not None:
                    return_value = to_execute(*args)
                elif kwargs is not None:
                    return_value = to_execute(**kwargs)
                else:
                    return_value = to_execute()
                returned = True
                break
            except Exception as error:                                          # pylint: disable=broad-except
                if type(error) in catch_exceptions:
                    cached_error = error
                    strategy.delay(failover_counter)
                    failover_counter += 1
                    continue
                else:
                    _handle_failure(on_failure = on_failure,
                                    error = error)
                    return
        else:
            try:
                if retry_args is not None and retry_kwargs is not None:
                    return_value = retry_execute(*retry_args, **retry_kwargs)
                elif retry_args is not None:
                    return_value = retry_execute(*retry_args)
                elif retry_kwargs is not None:
                    return_value = retry_execute(**retry_kwargs)
                else:
                    return_value = retry_execute()
                returned = True
                break
            except Exception as error:                                          # pylint: disable=broad-except
                if type(error) in catch_exceptions:
                    strategy.delay(failover_counter)
                    cached_error = error
                    failover_counter += 1
                    continue
                else:
                    _handle_failure(on_failure = on_failure,
                                    error = error)
                    return

    if not returned:
        _handle_failure(on_failure = on_failure,
                        error = cached_error)
        return
    elif returned and on_success is not None:
        on_success(return_value)

    return return_value
