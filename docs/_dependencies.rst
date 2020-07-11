By design, **Backoff-Utils** are designed to rely on minimal dependencies.
The only dependency they have outside of the Python standard library is:

* `validator-collection <https://github.com/insightindustry/validator-collection/>`_
  which provides for robust validation functionality.

  This library in turn has two external dependencies:
  * `jsonschema <https://pypi.org/project/jsonschema/>`_, and
  * (when installed under Python 2.7) `regex <https://pypi.python.org/pypi/regex>`_
    which is a drop-in replacement for Python 2.7's (buggy) standard
    :class:`re <python:re>` module.
