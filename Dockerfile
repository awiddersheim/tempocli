FROM python:3.7

MAINTAINER Andrew Widdersheim <amwiddersheim@gmail.com>

WORKDIR /tempocli

COPY . .

RUN pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
    && export SETUPTOOLS_SCM_PREVIOUS_TAG="$(git tag | sort -V | grep "^v.*" | grep -v ".dev" | tail -n 1)" \
    && pip install --no-cache-dir . \
    && useradd \
        --no-create-home \
        --system \
        tempocli \
    && rm -rf /tempocli

WORKDIR /templates

USER tempocli

ENTRYPOINT ["tempocli"]
CMD ["--help"]
