FROM python:3.10-slim-bullseye as base

MAINTAINER Andrew Widdersheim <amwiddersheim@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /tempocli
COPY setup.py README.md .

RUN pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
    && mkdir -p tempocli \
    && SETUPTOOLS_SCM_PRETEND_VERSION="0.0.1" pip install --no-cache-dir --editable . \
    && useradd --no-create-home --system tempocli

COPY . .

ARG SETUPTOOLS_SCM_PRETEND_VERSION

RUN pip install --no-cache-dir --editable .

FROM base as prod

WORKDIR /templates

USER tempocli

ENTRYPOINT ["tempocli"]
CMD ["--help"]

FROM base as test

RUN pip install --no-cache-dir --editable .[dev]
