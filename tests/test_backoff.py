# -*- coding: utf-8 -*-

"""Tests for backoff_utils._backoff"""

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

def successful_function(trying_again):
    """A successful function which returns a value."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    if trying_again is True:
        _attempts += 1
        return 123
    else:
        _attempts = 0
        raise ZeroDivisionError()


def on_failure_function(error,
                        message = None,
                        stacktrace = None):
    raise AttributeError(message)


@pytest.mark.parametrize("strategy, max_tries", [
    (strategies.ExponentialBackoff, 1),
    (strategies.ExponentialBackoff, 3)
])
def test_backoff_basic(strategy, max_tries):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    with pytest.raises(ZeroDivisionError) as excinfo:
        backoff(to_execute = divide_by_zero_function,
                args = [False],
                kwargs = None,
                strategy = strategy,
                retry_execute = None,
                retry_args = [True],
                retry_kwargs = None,
                max_tries = max_tries,
                catch_exceptions = [type(ZeroDivisionError())],
                on_failure = None,
                on_success = None)
    assert 'Subsequent Attempt' in str(excinfo.value)
    assert _attempts == max_tries
    _attempts = 0


@pytest.mark.parametrize("strategy, max_tries, on_failure", [
    (strategies.ExponentialBackoff, 1, ValueError),
    (strategies.ExponentialBackoff, 3, ValueError)
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
    (strategies.ExponentialBackoff, 1, on_failure_function),
    (strategies.ExponentialBackoff, 3, on_failure_function)
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
    (strategies.ExponentialBackoff, 1, when_successful),
    (strategies.ExponentialBackoff, 3, when_successful)
])
def test_backoff_on_success(strategy, max_tries, on_success):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    global _was_successful                                                      # pylint: disable=W0603,C0103

    return_value = backoff(to_execute = successful_function,
                           args = [False],
                           kwargs = None,
                           strategy = strategy,
                           retry_execute = None,
                           retry_args = [True],
                           retry_kwargs = None,
                           max_tries = max_tries,
                           catch_exceptions = [type(ZeroDivisionError())],
                           on_failure = None,
                           on_success = on_success)
    assert _attempts == max_tries
    assert _was_successful is True
    assert return_value == successful_function(True)
    _attempts = 0
    _was_successful = False
