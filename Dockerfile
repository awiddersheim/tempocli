FROM python:3.7-alpine as base

MAINTAINER Andrew Widdersheim <amwiddersheim@gmail.com>

WORKDIR /tempocli
COPY . .

RUN apk add --no-cache --virtual .build-deps \
        coreutils \
        git \
    && pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
    && export SETUPTOOLS_SCM_PREVIOUS_TAG="$(git tag | sort -V | grep "^v.*" | grep -v ".dev" | tail -n 1)" \
    && pip install --no-cache-dir . \
    && adduser -H -S tempocli

FROM base as prod

RUN rm -rf /tempocli \
    && apk del .build-deps

WORKDIR /templates

USER tempocli

ENTRYPOINT ["tempocli"]
CMD ["--help"]

FROM base as test

RUN pip install --no-cache-dir --editable .[dev]
