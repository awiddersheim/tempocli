# TempoCLI

Command line interface for interacting with Tempo.

[![PyPI version](https://img.shields.io/pypi/v/tempocli.svg)](https://pypi.org/project/tempocli)
[![Python Versions](https://img.shields.io/pypi/pyversions/tempocli.svg)](https://pypi.org/project/tempocli)
[![Build Status](https://img.shields.io/circleci/project/github/awiddersheim/tempocli/master.svg)](https://circleci.com/gh/awiddersheim/tempocli)
[![License](https://img.shields.io/pypi/l/tempocli.svg)](https://github.com/awiddersheim/tempocli/blob/master/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/awiddersheim/tempocli.svg)](https://hub.docker.com/r/awiddersheim/tempocli)

## Introduction

Ease repetitive Tempo tasks by using templates to fill in recurring
items without having to use web interface. Templates are yaml formatted
files that are semi-flexible in allowing what can be created.

The `author_account_id` can be obtained by going to your profile in
JIRA and copying the ID from the URL.

```
----
author_account_id: foo

issues:
  # Will use current date if one can't be determined.
  - issue: INT-8
    time_spent: 30m
    start_time: "9:30AM"

  # Can specify day of week easily.
  - issue: INT-10
    time_spent: 1h
    start_time: Monday at 9AM

  # Full on datetime with override.
  - issue: INT-11
    time_spent: 90s
    start_time: "2018-08-05 11:00:00"
    author_account_id: bar

  # Pass in extras that aren't exposed in DSL.
  # https://tempo-io.github.io/tempo-api-docs/#worklogs
  - issue: INT-11
    time_spent: 1h
    start_time: 8am
    extras:
      remainingEstimateSeconds: 300
```

## Installation

```
$ pip install tempocli
$ pip install --upgrade tempocli
```

## Running

```
$ tempocli --config <config> create --template <template>
```

## Configuration

By default, `~/.tempocli.yml` is the path used for the configuration
file but that can be changed with the `--config` option during
invocation. The configuration file should look like this:

```
---
token: <token>
```

It is also possible to specify the token using the `TEMPOCLI_TOKEN`
environment variable.

## Docker

```
$ docker pull awiddersheim/tempocli
$ docker run \
    --rm \
    --tty \
    --interactive \
    --volume ~/.tempocli.yml:/home/tempocli/.tempocli.yml:ro \
    --volume /some/dir/with/templates:/templates:ro \
    awiddersheim/tempocli \
    create --template /templates/template.yml
```

## Development

```
$ pip install -e .
$ tempocli --help
```


## Testing

```
# Install development packages (preferably in a virtualenv)
$ pip install -e .[dev]

# Run tests
$ pytest

# Run tests for all available Python interpreters
$ tox

# Linting
$ flake8

# Can also lint in tox as well
$ tox -e flake8
```
