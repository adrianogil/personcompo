FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VERSION=1.7.1

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

CMD ["python", "-m", "personcompo.dominoes.dominoesgame"]
