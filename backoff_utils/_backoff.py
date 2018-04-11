# -*- coding: utf-8 -*-

"""
backoff_utils._backoff
#########################

Implements the ``backoff()`` function which executes a function/method call
and retries on failure based on arguments passed to the ``backoff()`` function.

"""
import sys

import backoff_utils.validators as validators

from backoff_utils.strategies import ExponentialBackoff


def backoff(to_execute,
            args = None,
            kwargs = None,
            strategy = None,
            retry_execute = None,
            retry_args = None,
            retry_kwargs = None,
            max_tries = 3,
            catch_exceptions = None,
            on_failure = None,
            on_success = None):
    """Retry a function call multiple times with a delay per the strategy given.

    :param to_execute: The function call that is to be attempted.
    :type to_execute: callable

    :param args: The positional arguments to pass to the function on the
      first attempt. If ``retry_args`` is ``None``, will re-use these
      arguments on retry attempts as well.
    :type args: iterable / ``None``.

    :param kwargs: The keyword arguments to pass to the function on the
      first attempt. If ``retry_kwargs`` is ``None``, will re-use these keyword
      arguments on retry attempts as well.
    :type kwargs: :ref:`dict <python:dict>` / ``None``

    :param strategy: The :class:`BackoffStrategy` to use when determining the
      delay between retry attempts. If ``None``, defaults to
      :ref:`exponential <ExponentialBackoff>`.
    :type strategy: :class:`BackoffStrategy`

    :param retry_execute: The function to call on retry attempts. If ``None``,
      will retry ``to_execute``. Defaults to ``None``.
    :type retry_execute: callable / ``None``

    :param retry_args: The positional arguments to pass to the function on
      retry attempts. If ``None``, will re-use ``args``. Defaults to ``None``.
    :type retry_args: iterable / ``None``

    :param retry_kwargs: The keyword arguments to pass to the function on
      retry attempts. If ``None``, will re-use ``kwargs``. Defaults to ``None``.
    :type subsequent_kwargs: :ref:`dict <python:dict>` / ``None``

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

    :returns: The result of the attempted function.

    """
    # pylint: disable=too-many-branches

    if to_execute is None:
        raise ValueError('to_execute cannot be None')
    elif not validators.is_callable(to_execute):
        raise TypeError('to_execute must be callable')

    if strategy is None:
        strategy = ExponentialBackoff
    elif not validators.is_type(strategy, 'BackoffStrategy'):
        raise TypeError('strategy must be a BackoffStrategy or descendent')

    if args is not None:
        args = validators.iterable(args)
    if kwargs is not None:
        kwargs = validators.dict(kwargs)

    if retry_execute is None:
        retry_execute = to_execute
    elif not validators.is_callable(retry_execute):
        raise TypeError('retry_execute must be None or a callable')

    if retry_args is None:
        retry_args = args
    else:
        retry_args = validators.iterable(retry_args)

    if retry_kwargs is None:
        retry_kwargs = kwargs
    else:
        retry_kwargs = validators.dict(retry_kwargs)

    max_tries = validators.integer(max_tries)

    if catch_exceptions is None:
        catch_exceptions = (type(Exception()))

    if on_failure is not None and not validators.is_callable(on_failure):
        raise TypeError('on_failure must be None or a callable')

    if on_success is not None and not validators.is_callable(on_success):
        raise TypeError('on_success must be None or a callable')

    return_value = None
    failover_counter = 0
    while failover_counter < (max_tries + 1):
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
                break
            except Exception as error:                                          # pylint: disable=broad-except
                if type(error) in catch_exceptions:
                    strategy.delay(failover_counter)
                    failover_counter += 1
                    continue
                elif on_failure is None:
                    raise error
                elif validators.is_type(on_failure, 'Exception'):
                    raise on_failure(error.args[0])
                else:
                    on_failure(error, error.args[0], sys.exc_info()[2])
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
                break
            except Exception as error:                                          # pylint: disable=broad-except
                if type(error) in catch_exceptions:
                    strategy.delay(failover_counter)
                    failover_counter += 1
                    continue
                elif on_failure is None:
                    raise error
                elif validators.is_type(on_failure, 'Exception'):
                    raise on_failure(error.args[0])
                else:
                    on_failure(error, error.args[0], sys.exc_info()[2])
                    return

        if on_success is not None:
            on_success(return_value)

        return return_value
