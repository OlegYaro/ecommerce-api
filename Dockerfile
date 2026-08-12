FROM python:3.14-slim

ENV POETRY_VERSION=2.4.1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root && rm -rf "${POETRY_CACHE_DIR}"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
