By design, **Backoff-Utils** are designed to rely on minimal dependencies.
The only dependency they have outside of the Python standard library is:

* `validator-collection <https://github.com/insightindustry/validator-collection/>`_
  which provides for robust validation functionality.

  This library in turn has one external dependency when installed under Python 2.7:

  * `regex <https://pypi.python.org/pypi/regex>`_ which is a drop-in replacement for
    Python's (buggy) standard :class:`re <python:re>` module.
