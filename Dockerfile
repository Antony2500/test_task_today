FROM python:3.10-buster as builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR .
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.10-slim-buster

ENV VIRTUAL_ENV=./.venv \
    PATH="/./.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR ./

RUN apt update && \
    apt install -y postgresql-client


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
