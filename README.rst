TempoCLI
========

Command line interface for interacting with Tempo.

|Status| |PackageVersion| |PythonVersions|

Introduction
------------

Ease repetitive Tempo tasks by using templates to fill in recurring
items without having to use web interface. Templates are yaml formatted
files that are semi-flexible in allowing what can be created.

::

    ----
    author: foo

    issues:
      # Will use current date if one can't be determined.
      - issue: INT-8
        time_spent: 30m
        start_time: "9:30AM"

      # Can specify day of week easily.
      - issue: INT-10
        time_spent: 1h
        start_time: Monday at 9AM

      # Full on datetime with author override.
      - issue: INT-11
        time_spent: 90s
        start_time: "2018-08-05 11:00:00"
        author: bar

      # Pass in extras that aren't exposed in DSL.
      # https://tempo-io.github.io/tempo-api-docs/#worklogs
      - issue: INT-11
        time_spent: 1h
        start_time: 8am
        extras:
          remainingEstimateSeconds: 300


Installation
------------

::

    $ pip install tempocli
    $ pip install --upgrade tempocli

Running
-------

::

    tempocli --config <config> create --template <template>

Configuration
-------------

By default, ``~/.tempocli.yml`` is the path used for the configuration
file but that can be changed with the ``--config`` option during
invocation. The configuration file should look like this::

    ---
    url: https://api.tempo.io/2/
    token: <token>

It is also possible to specify the token using the ``TEMPOCLI_TOKEN``
environment variable.

Development
-----------

::

    $ pip install -e .
    $ tempocli --help


Testing
-------

::

    # Install development packages (preferably in a virtualenv)
    $ pip install -e .[dev]

    # Run tests
    $ pytest

    # Run tests for available Python interpreters
    $ tox

    # Linting
    $ tox -e flake8


.. |PackageVersion| image:: https://img.shields.io/pypi/v/tempocli.svg?style=flat
    :alt: PyPI version
    :target: https://pypi.org/project/tempocli

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/tempocli.svg
    :alt: Supported Python versions
    :target: https://pypi.org/project/tempocli

.. |Status| image:: https://img.shields.io/circleci/project/github/awiddersheim/tempocli/master.svg
    :alt: Build
    :target: https://circleci.com/gh/awiddersheim/tempocli
