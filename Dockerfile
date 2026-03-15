FROM python:3.13-slim

WORKDIR /reststudy

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "until python -c \"import socket; socket.create_connection(('db', 5432), 2)\"; do echo 'Waiting for postgres...'; sleep 2; done; python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]