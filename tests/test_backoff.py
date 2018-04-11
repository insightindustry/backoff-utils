# -*- coding: utf-8 -*-

"""Tests for backoff_utils._backoff"""

import pytest

import backoff_utils.strategies as strategies

from backoff_utils._backoff import backoff

_attempts = 0


def divide_by_zero_function(trying_again):
    """Raise a ZeroDivisionError counting attempts."""
    global _attempts                                                            # pylint: disable=W0603,C0103
    if trying_again is True:
        _attempts += 1
        raise ZeroDivisionError('Failed on Subsequent Attempt')
    else:
        _attempts = 0
        raise ZeroDivisionError()


@pytest.mark.parametrize("strategy, max_tries", [
    (strategies.ExponentialBackoff, 1),
    (strategies.ExponentialBackoff, 3)
])
def test_backoff(strategy, max_tries):
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
