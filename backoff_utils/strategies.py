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


def _add_metaclass(metaclass):
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


@_add_metaclass(abc.ABCMeta)
class BackoffStrategy(object):
    """Abstract Base Class that defines the standard interface exposed by all
    backoff strategies supported by the library."""

    IS_INSTANTIATED = False

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __init__(self,
                 attempt = None,
                 minimum = 0.0,
                 jitter = True,
                 scale_factor = 1.0,
                 **kwargs):
        """
        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :class:`int <python:int>`

        :param minimum: The minimum delay to apply. Defaults to ``0``.
        :type minimum: number

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :class:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :func:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale. Defaults to ``1.0``.
        :type scale_factor: :class:`float <python:float>`

        """
        self.attempt = None
        if attempt is not None:
            self.attempt = validators.integer(attempt)
        self.minimum = minimum
        self.jitter = bool(jitter)
        self.scale_factor = validators.float(scale_factor)
        self.IS_INSTANTIATED = True

        for kwarg in kwargs:
            if hasattr(self, kwarg):
                try:
                    setattr(self, kwarg, kwargs[kwarg])
                except AttributeError:
                    pass

    @property
    @abc.abstractmethod
    def time_to_sleep(self):
        """The base number of seconds to delay before allowing a retry.

        :rtype: :class:`float <python:float>`
        """
        pass

    @classmethod
    def delay(cls,
              attempt,
              minimum = None,
              jitter = None,
              scale_factor = 1.0):
        """Delay for a set period of time based on the ``attempt``.

        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :class:`int <python:int>`

        :param minimum: The minimum number of seconds to delay.

          If :class:`None <python:None>`, will apply either the strategy's
          default or the instance's configured property.
        :type minimum: number

        :param jitter: If ``True``, will add a random float to the delay.

          If ``False``, will not.

          If :class:`None <python:None>`, will apply either the strategy's
          default or the instance's configured property.
        :type jitter: :class:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :func:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale.

          If :class:`None <python:None>`, will apply either the strategy's default
          or the instance's configured property.
        :type scale_factor: :class:`float <python:float>`

        """
        attempt = validators.integer(attempt)
        scale_factor = validators.float(scale_factor)
        if cls.IS_INSTANTIATED:
            cls.attempt = attempt
            if jitter is not None:
                cls.jitter = bool(jitter)
            if scale_factor is not None:
                cls.scale_factor = scale_factor
            if minimum is not None:
                cls.minimum = minimum
        elif minimum is not None:
            cls = cls(attempt,
                      minimum = minimum,
                      jitter = jitter,
                      scale_factor = scale_factor)
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

    The base delay time is calculated as:

    .. math::

        2^a

    where :math:`a` is the number of the current attempt being made.
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
        :type input: :class:`int <python:int>`
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
                 attempt = None,
                 sequence = None,
                 minimum = 0,
                 jitter = True,
                 scale_factor = 1.0,
                 **kwargs):
        """
        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :class:`int <python:int>`

        :param sequence: The sequence of base delay times to return based on the
          attempt number.
        :type sequence: iterable of numbers

        :param minimum: The minimum delay to apply. Defaults to ``0``.
        :type minimum: number

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :class:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :class:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale.

          Defaults to ``1.0``.
        :type scale_factor: :class:`float <python:float>`

        """
        if sequence is None:
            self.sequence = None
        else:
            sequence = validators.iterable(sequence)
            self.sequence = [validators.integer(x) for x in sequence]

        super(Fixed, self).__init__(attempt = attempt,
                                    minimum = minimum,
                                    jitter = jitter,
                                    scale_factor = scale_factor,
                                    **kwargs)

    @property
    def time_to_sleep(self):
        if not self.sequence:
            return 1

        if len(self.sequence) <= self.attempt:
            needs = self.attempt - len(self.sequence)
            sequence = [x for x in self.sequence]
            last_value = sequence[:-1]
            sequence.extend(last_value for x in range(0, needs))
        else:
            sequence = self.sequence

        return sequence[self.attempt]


class Linear(BackoffStrategy):
    """Implements the :term:`fixed backoff` strategy.

    The base delay time is equal to the attempt count.
    """
    @property
    def time_to_sleep(self):
        return self.attempt


class Polynomial(BackoffStrategy):
    """Implements the :term:`polynomial backoff` strategy.

    The base delay time is calculated as:

    .. math::
        a^e

    where:

      * :math:`a` is the number of attempts made
      * :math:`e` is the :func:`exponent <exponent>` property
    """

    def __init__(self,
                 attempt = None,
                 exponent = 1,
                 minimum = 0,
                 jitter = True,
                 scale_factor = 1.0,
                 **kwargs):
        """
        :param attempt: The number of the attempt that was last-attempted. This
          value is used by the strategy to determine the amount of time to delay
          before continuing.
        :type attempt: :class:`float <python:float>`

        :param exponent: The exponent to apply when calculating the base delay.
          Defaults to 1.
        :type exponent: :class:`int <python:int>`

        :param minimum: The minimum delay to apply. Defaults to ``0``.
        :type minimum: number

        :param jitter: If ``True``, will add a random float to the delay. Defaults
          to ``True``.
        :type jitter: :class:`bool <python: bool>`

        :param scale_factor: A factor by which the
          :class:`time_to_sleep <BackoffStrategy.time_to_sleep>` is multiplied to
          adjust its scale. Defaults to ``1.0``.
        :type scale_factor: :class:`float <python:float>`

        """
        self.exponent = validators.float(exponent)

        super(Polynomial, self).__init__(attempt = attempt,
                                         minimum = minimum,
                                         jitter = jitter,
                                         scale_factor = scale_factor,
                                         **kwargs)

    @property
    def time_to_sleep(self):
        return float(self.attempt**self.exponent)
