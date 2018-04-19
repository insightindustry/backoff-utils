# -*- coding: utf-8 -*-

"""Tests for backoff_utils._backoff"""
from datetime import datetime

import pytest

import backoff_utils.strategies as strategies

from backoff_utils._backoff import backoff

_attempts = 0
_was_successful = False


def divide_by_zero_function(trying_again):
    """Raise a ZeroDivisionError counting attempts."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    if trying_again is True:
        _attempts += 1
        raise ZeroDivisionError('Failed on Subsequent Attempt')
    else:
        _attempts = 0
        raise ZeroDivisionError()


def when_successful(value):
    """Update the global ``_was_successful`` value to True."""
    global _was_successful                                                      # pylint: disable=W0603,C0103
    _was_successful = True

def successful_function(trying_again, max_tries):
    """A successful function which returns a value."""
    global _attempts                                                            # pylint: disable=W0603,C0103

    if trying_again is True:
        _attempts += 1
    else:
        _attempts = 0

    if _attempts >= max_tries:
        return 123

    raise ZeroDivisionError()


def on_failure_function(error,
                        message = None,
                        stacktrace = None):
    raise AttributeError(message)


@pytest.mark.parametrize("failure, strategy, max_tries, max_delay, retry_execute", [
    (None, strategies.Exponential, 1, None, None),
    (None, strategies.Exponential, 3, None, None),
    (None, strategies.Exponential, 1, 3, None),
    (None, strategies.Exponential, 3, 5, None),
    (None, strategies.Exponential(jitter = False), 1, None, None),
    (None, strategies.Exponential(scale_factor = 3), 3, None, None),


    (None, strategies.Exponential, 1, None, divide_by_zero_function),
    (None, strategies.Exponential, 3, None, divide_by_zero_function),
    (None, strategies.Exponential, 1, 3, divide_by_zero_function),
    (None, strategies.Exponential, 3, 5, divide_by_zero_function),

    (None, strategies.Fibonacci, 1, None, None),
    (None, strategies.Fibonacci, 3, None, None),
    (None, strategies.Fibonacci, 1, 3, None),
    (None, strategies.Fibonacci, 3, 5, None),

    (None, strategies.Fixed, 1, None, None),
    (None, strategies.Fixed, 3, None, None),
    (None, strategies.Fixed, 1, 3, None),
    (None, strategies.Fixed, 3, 5, None),
    (None, strategies.Fixed(sequence = [2, 3, 4, 5]), 3, None, None),

    (None, strategies.Linear, 1, None, None),
    (None, strategies.Linear, 3, None, None),
    (None, strategies.Linear, 1, 3, None),
    (None, strategies.Linear, 3, 5, None),

    (None, strategies.Polynomial, 1, None, None),
    (None, strategies.Polynomial, 3, None, None),
    (None, strategies.Polynomial, 1, 3, None),
    (None, strategies.Polynomial, 3, 5, None),
    (None, strategies.Polynomial(exponent = 2), 3, None, None),


    (TypeError, 'invalid-value', 1, None, None),
    (TypeError, strategies.Exponential, 1, None, 'not-a-callable'),
])
def test_backoff_basic(failure, strategy, max_tries, max_delay, retry_execute):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    if not failure:
        with pytest.raises(ZeroDivisionError) as excinfo:
            start_time = datetime.utcnow()
            backoff(to_execute = divide_by_zero_function,
                    args = [False],
                    kwargs = None,
                    strategy = strategy,
                    retry_execute = retry_execute,
                    retry_args = [True],
                    retry_kwargs = None,
                    max_tries = max_tries,
                    max_delay = max_delay,
                    catch_exceptions = [type(ZeroDivisionError())],
                    on_failure = None,
                    on_success = None)
        end_time = datetime.utcnow()
        elapsed_time = start_time - end_time
        elapsed_time = elapsed_time.total_seconds()
        if max_delay is not None:
            assert elapsed_time <= max_delay
            assert _attempts <= max_tries
        else:
            assert _attempts == max_tries
        assert 'Subsequent Attempt' in str(excinfo.value)
    else:
        with pytest.raises(failure):
            start_time = datetime.utcnow()
            backoff(to_execute = divide_by_zero_function,
                    args = [False],
                    kwargs = None,
                    strategy = strategy,
                    retry_execute = retry_execute,
                    retry_args = [True],
                    retry_kwargs = None,
                    max_tries = max_tries,
                    max_delay = max_delay,
                    catch_exceptions = [type(ZeroDivisionError())],
                    on_failure = None,
                    on_success = None)
        end_time = datetime.utcnow()
        elapsed_time = start_time - end_time
        elapsed_time = elapsed_time.total_seconds()

    _attempts = 0


@pytest.mark.parametrize("strategy, max_tries, on_failure", [
    (strategies.Exponential, 1, ValueError),
    (strategies.Exponential, 3, ValueError)
])
def test_backoff_on_failure_exception(strategy, max_tries, on_failure):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    global _was_successful                                                      # pylint: disable=W0603,C0103

    with pytest.raises(on_failure) as excinfo:
        backoff(to_execute = divide_by_zero_function,
                args = [False],
                kwargs = None,
                strategy = strategy,
                retry_execute = None,
                retry_args = [True],
                retry_kwargs = None,
                max_tries = max_tries,
                catch_exceptions = [type(ZeroDivisionError())],
                on_failure = on_failure,
                on_success = None)
    assert _attempts == max_tries
    assert _was_successful is False
    _attempts = 0
    _was_successful = False


@pytest.mark.parametrize("strategy, max_tries, on_failure", [
    (strategies.Exponential, 1, on_failure_function),
    (strategies.Exponential, 3, on_failure_function)
])
def test_backoff_on_failure_function(strategy, max_tries, on_failure):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    global _was_successful                                                      # pylint: disable=W0603,C0103

    with pytest.raises(AttributeError) as excinfo:
        backoff(to_execute = divide_by_zero_function,
                args = [False],
                kwargs = None,
                strategy = strategy,
                retry_execute = None,
                retry_args = [True],
                retry_kwargs = None,
                max_tries = max_tries,
                catch_exceptions = [type(ZeroDivisionError())],
                on_failure = on_failure,
                on_success = None)
    assert _attempts == max_tries
    assert _was_successful is False
    _attempts = 0
    _was_successful = False



@pytest.mark.parametrize("strategy, max_tries, on_success", [
    (strategies.Exponential, 1, when_successful),
    (strategies.Exponential, 3, when_successful)
])
def test_backoff_on_success(strategy, max_tries, on_success):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    global _was_successful                                                      # pylint: disable=W0603,C0103

    return_value = backoff(to_execute = successful_function,
                           args = [False, max_tries],
                           kwargs = None,
                           strategy = strategy,
                           retry_execute = None,
                           retry_args = [True, max_tries],
                           retry_kwargs = None,
                           max_tries = max_tries,
                           catch_exceptions = [type(ZeroDivisionError())],
                           on_failure = None,
                           on_success = on_success)
    assert _attempts == max_tries
    assert _was_successful is True
    assert return_value == successful_function(True, max_tries)
    _attempts = 0
    _was_successful = False
