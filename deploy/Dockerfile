FROM python:slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Requirements
RUN python -m pip install --upgrade setuptools && \
    python -m pip install --upgrade pip && \
    python -m pip install poetry==1.1.4
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
RUN poetry config virtualenvs.create false && \
    poetry install

# Scripts
COPY ./deploy/scripts/* /

COPY ./ /app

RUN chmod +x /is_postgres_ready.py && \
    chmod +x /entrypoint && \
    chmod +x /start

CMD ["/entrypoint", "/start"]