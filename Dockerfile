FROM python:3.7

MAINTAINER Andrew Widdersheim <amwiddersheim@gmail.com>

WORKDIR /tempocli

COPY . .

RUN pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
    && pip install --no-cache-dir . \
    && useradd \
        --no-create-home \
        --system \
        tempocli

USER tempocli

ENTRYPOINT ["tempocli"]
CMD ["--help"]
