# -*- coding: utf-8 -*-

"""
Backoff-Utils
#########################

A collection of Python functions and decorators that can be used to simply and
efficiently apply various backoff and retry strategies in your Python
code.

"""
from backoff_utils._backoff import backoff
from backoff_utils._decorator import apply_backoff


__all__ = [
    'backoff',
    'apply_backoff'
]
