FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# установка poetry
RUN pip install poetry

# отключаем виртуальное окружение
RUN poetry config virtualenvs.create false

# копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# устанавливаем зависимости
RUN poetry install --no-root

# копируем проект
COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]