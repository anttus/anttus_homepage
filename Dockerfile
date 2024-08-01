# syntax=docker/dockerfile:1

FROM python:slim-bookworm AS builder

LABEL Name="Anttu's homepage" Version="2.1"

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root && rm -rf ${POETRY_CACHE_DIR}

FROM python:slim-bookworm AS runtime

ENV VIRTUAL_ENV=/.venv \
	PATH="/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./

EXPOSE 5050

CMD [ "gunicorn", "-k", "main.MyUvicornWorker", "main:app", "--config", "gunicorn.config.py", "--access-logfile", "-", "--forwarded-allow-ips", "'*'"]
