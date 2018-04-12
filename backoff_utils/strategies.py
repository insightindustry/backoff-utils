# -*- coding: utf-8 -*-

"""
backoff_utils.strategies
#########################

Defines the different backoff strategies that can be applied using the **Backoff-Utils**
library.

"""
import abc
import time
import random

import validator_collection as validators


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


@add_metaclass(abc.ABCMeta)
class BackoffStrategy(object):
    """Abstract Base Class that defines the standard interface exposed by all
    backoff strategies supported by the library."""

    IS_INSTANTIATED = False

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __init__(self,
                 attempt,
                 jitter = True,
                 scale_factor = 1.0,
                 *args,
                 **kwargs):
        """Create an instance of the :class:`BackoffStrategy`.

        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :ref:`int <python:int>`

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :ref:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :ref:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale. Defaults to ``1.0``.
        :type scale_factor: :ref:`float <python:float>`

        """
        self.attempt = validators.integer(attempt)
        self.jitter = bool(jitter)
        self.scale_factor = validators.float(scale_factor)
        self.IS_INSTANTIATED = True

        for kwarg in kwargs:
            if hasattr(self, kwarg):
                try:
                    setattr(self, kwarg, kwargs[kwarg])
                except AttributeError:
                    pass

        super(BackoffStrategy, self).__init__(*args)

    @property
    @abc.abstractmethod
    def time_to_sleep(self):
        """The base number of seconds to delay before allowing a retry.

        :rtype: :ref:`float <python:float>`
        """
        pass

    @classmethod
    def delay(cls,
              attempt,
              jitter = True,
              scale_factor = 1.0):
        """Delay for a set period of time based on the ``attempt``.

        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :ref:`int <python:int>`

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :ref:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :ref:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale. Defaults to ``1.0``.
        :type scale_factor: :ref:`float <python:float>`

        """
        attempt = validators.integer(attempt)
        scale_factor = validators.float(scale_factor)
        if cls.IS_INSTANTIATED:
            cls.attempt = attempt
            cls.jitter = bool(jitter)
            cls.scale_factor = scale_factor
        else:
            cls = cls(attempt,
                      jitter = jitter,
                      scale_factor = scale_factor)

        if cls.jitter:
            time_to_sleep = cls.time_to_sleep + random.random()
        else:
            time_to_sleep = cls.time_to_sleep

        time_to_sleep = time_to_sleep * cls.scale_factor

        time.sleep(time_to_sleep)


class Exponential(BackoffStrategy):
    """Implements the :term:`exponential backoff` strategy.

    The base delay time is calculated as: :math:`2^self.attempt`
    """

    @property
    def time_to_sleep(self):
        return float(2**self.attempt)


class Fibonacci(BackoffStrategy):
    """Implements the :term:`fibonacci backoff` strategy.

    The base delay time is returned as the Fibonacci number corresponding to the
    current attempt.

    """

    @classmethod
    def _get_sub_value(cls, input):
        """Return the Fibonacci number given the ``input``.

        :param input: The input whose Fibonacci number should be returned.
        :type input: :ref:`int <python:int>`
        """
        input = validators.integer(input)
        if input < 1:
            return 1

        return cls._get_sub_value(input - 1) + cls._get_sub_value(input - 2)

    @property
    def time_to_sleep(self):
        return self._get_sub_value(self.attempt)


class Fixed(BackoffStrategy):
    """Implements the :term:`fixed backoff` strategy.

    The base delay time is calculated as a fixed value determined by the attempt
    number.
    """
    def __init__(self,
                 attempt,
                 sequence = None,
                 scale_factor = 1.0,
                 jitter = True,
                 *args,
                 **kwargs):
        """Create an instance of the :class:`BackoffStrategy`.

        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :ref:`int <python:int>`

        :param sequence: The sequence of base delay times to return based on the
          attempt number.
        :type sequence: iterable

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :ref:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :ref:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale. Defaults to ``1.0``.
        :type scale_factor: :ref:`float <python:float>`

        """
        sequence = validators.iterable(sequence)
        self.sequence = [validators.integer(x) for x in sequence]

        super(Fixed, self).__init__(attempt,
                                    *args,
                                    scale_factor = scale_factor,
                                    jitter = jitter,
                                    **kwargs)

    @property
    def time_to_sleep(self):
        return self.sequence[self.attempt]


class Polynomial(BackoffStrategy):
    """Implements the :term:`polynomial backoff` strategy.

    The base delay time is calculated as: :math:`self.attempt^self.exponent`
    """

    def __init__(self,
                 attempt,
                 jitter = True,
                 exponent = 1,
                 *args,
                 **kwargs):
        """Create an instance of the :class:`BackoffStrategy`.

        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :ref:`int <python:int>`

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :ref:`bool <python: bool>`

        :param exponent: The exponent to apply when calculating the base delay.
          Defaults to 1.
        :type exponent: :ref:`int <python:int>`

        """
        self.exponent = validators.integer(exponent)

        super(Polynomial, self).__init__(attempt,
                                         *args,
                                         jitter = jitter,
                                         **kwargs)

    @property
    def time_to_sleep(self):
        return float(self.attempt**self.exponent)


class Linear(BackoffStrategy):
    """Implements the :term:`fixed backoff` strategy.

    The base delay time is equal to the attempt count.
    """
    @property
    def time_to_sleep(self):
        return self.attempt
