FROM python:3.10-alpine3.14
LABEL maintainer="Sagun Devkota"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache mariadb-connector-c-dev build-base mariadb-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

COPY ./app /app

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user
ENV PATH="/py/bin:$PATH"

USER django-user