# -*- coding: utf-8 -*-

"""Tests for backoff_utils._backoff"""
from datetime import datetime

import pytest

import backoff_utils.strategies as strategies

from backoff_utils._decorator import apply_backoff

_attempts = 0
_was_successful = False


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


@pytest.mark.parametrize("failure, strategy, max_tries, max_delay", [
    (None, strategies.Exponential, 1, None),
    (None, strategies.Exponential, 3, None),

    (None, strategies.Exponential, 1, None),
    (None, strategies.Exponential, 3, None),
    (None, strategies.Exponential, 1, 3),
    (None, strategies.Exponential, 3, 5),
    (None, strategies.Exponential(jitter = False), 1, None),
    (None, strategies.Exponential(scale_factor = 3), 3, None),

    (None, strategies.Fibonacci, 1, None),
    (None, strategies.Fibonacci, 3, None),
    (None, strategies.Fibonacci, 1, 3),
    (None, strategies.Fibonacci, 3, 5),

    (None, strategies.Fixed, 1, None),
    (None, strategies.Fixed, 3, None),
    (None, strategies.Fixed, 1, 3),
    (None, strategies.Fixed, 3, 5),
    (None, strategies.Fixed(sequence = [2, 3, 4, 5]), 3, None),

    (None, strategies.Linear, 1, None),
    (None, strategies.Linear, 3, None),
    (None, strategies.Linear, 1, 3),
    (None, strategies.Linear, 3, 5),

    (None, strategies.Polynomial, 1, None),
    (None, strategies.Polynomial, 3, None),
    (None, strategies.Polynomial, 1, 3),
    (None, strategies.Polynomial, 3, 5),
    (None, strategies.Polynomial(exponent = 2), 3, None),

    (TypeError, 'invalid-value', 1, None),
])
def test_apply_backoff(failure, strategy, max_tries, max_delay):
    """Test the :ref:`backoff_utils._backoff.backoff` function."""
    global _attempts                                                            # pylint: disable=W0603,C0103

    @apply_backoff(strategy = strategy,
                   max_tries = max_tries,
                   max_delay = max_delay,
                   catch_exceptions = [type(ZeroDivisionError())],
                   on_failure = None,
                   on_success = None)
    def divide_by_zero_function():
        """Raise a ZeroDivisionError counting attempts."""
        global _attempts                                                            # pylint: disable=W0603,C0103
        if _attempts > 0:
            _attempts += 1
            raise ZeroDivisionError('Failed on Subsequent Attempt')
        else:
            _attempts += 1
            raise ZeroDivisionError()

    if not failure:
        with pytest.raises(ZeroDivisionError) as excinfo:
            start_time = datetime.utcnow()
            divide_by_zero_function()

        end_time = datetime.utcnow()
        elapsed_time = start_time - end_time
        elapsed_time = elapsed_time.total_seconds()
        if max_delay is not None:
            assert elapsed_time <= max_delay
            assert _attempts <= (max_tries + 1)
        else:
            assert _attempts == (max_tries + 1)
        if max_tries > 1:
            assert 'Subsequent Attempt' in str(excinfo.value)
    else:
        with pytest.raises(failure):
            start_time = datetime.utcnow()
            divide_by_zero_function()
        end_time = datetime.utcnow()
        elapsed_time = start_time - end_time
        elapsed_time = elapsed_time.total_seconds()

    _attempts = 0
