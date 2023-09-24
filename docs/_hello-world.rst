.. code:: python

  from backoff_utils import strategies

  # Using a Function Call
  from backoff_utils import backoff

  def some_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = backoff(some_function,
                   args = ['value1', 'value2'],
                   kwargs = { 'kwarg1': 'value3' },
                   max_tries = 3,
                   max_delay = 3600,
                   strategy = strategies.Exponential)

  # Using a Decorator
  from backoff_utils import apply_backoff

  @apply_backoff(strategy = strategies.Exponential, max_tries = 3, max_delay = 3600)
  def some_decorated_function(arg1, arg2, kwarg1 = None):
      # your code goes here
      pass

  result = some_decorated_function('value1', 'value2', kwarg1 = 'value3')
