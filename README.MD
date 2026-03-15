# RESTstudy

## Описание

RESTstudy — backend-часть LMS-системы, разработанная на Django REST Framework.  
Проект предоставляет API для работы с курсами, уроками и пользователями.

В проекте используются:

- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
- GitHub Actions (CI/CD)

Проект находится в стадии разработки.

---

## Установка

### 1. Клонирование репозитория

```
git clone https://github.com/AndTiho/RESTstudy.git
cd RESTstudy
```

### 2. Установка Docker

Необходимо установить Docker.

Проверить установку:

```
docker --version
```

---

## Сборка Docker-образа

```
docker build -t reststudy .
```

---

## Запуск контейнера

```
docker run -p 8000:8000 reststudy
```

После запуска приложение будет доступно по адресу:

```
http://localhost:8000
```

---

## Проверка работоспособности

### Проверка API

Открыть в браузере:

```
http://localhost:8000
```

Если API отвечает — приложение работает.

---

### Проверка контейнеров

```
docker ps
```

---

## Проверка PostgreSQL

Подключиться к контейнеру базы данных:

```
docker exec -it db psql -U postgres
```

Список баз данных:

```sql
\l
```

---

## Проверка Redis

Подключение к Redis:

```
docker exec -it redis redis-cli
```

Проверка соединения:

```
ping
```

Ответ должен быть:

```
PONG
```

---

## Проверка Celery Worker

Просмотр логов:

```
docker logs celery
```

---

## Проверка Celery Beat

Просмотр логов:

```
docker logs celery-beat
```

---

## Деплой на удалённый сервер

Для автоматического деплоя используется GitHub Actions.

Workflow выполняет следующие шаги:

1. Сборка Docker-образа
2. Публикация образа в Docker Hub
3. Подключение к серверу по SSH
4. Загрузка нового Docker-образа
5. Остановка старых контейнеров
6. Запуск новых контейнеров приложения, Celery и Celery Beat

После выполнения workflow новая версия приложения автоматически разворачивается на сервере.

---

## Проверка деплоя

На сервере:

```
docker ps
```

Просмотр логов:

```
docker logs myapp
docker logs celery
docker logs celery-beat
```

---

## Документация API

Swagger:

```
http://localhost:8000/swagger/
```

ReDoc:

```
http://localhost:8000/redoc/
```

---

## Лицензия

Проект распространяется без лицензии.