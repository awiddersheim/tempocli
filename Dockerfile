FROM python:3.10-slim-bullseye as base

MAINTAINER Andrew Widdersheim <amwiddersheim@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /tempocli
COPY . .

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
        git \
    && pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
    && pip install --no-cache-dir --editable . \
    && useradd --no-create-home --system tempocli \
    && rm -rf .git \
    && apt-get -y remove \
        git \
    && apt-get clean autoremove \
    && rm -rf /var/lib/apt/lists/*

FROM base as prod

WORKDIR /templates

USER tempocli

ENTRYPOINT ["tempocli"]
CMD ["--help"]

FROM base as test

RUN SETUPTOOLS_SCM_PRETEND_VERSION="0.0.1" pip install --no-cache-dir --editable .[dev]
