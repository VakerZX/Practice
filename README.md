# Octagon Books API

Учебный проект: REST API для книг и категорий на **FastAPI** + **SQLAlchemy** + **PostgreSQL**.

## Стек

- Python 3
- PostgreSQL
- SQLAlchemy (ORM)
- FastAPI + Uvicorn
- Pydantic (валидация данных)

## Структура проекта

```
app/
  main.py             # точка входа FastAPI, подключение роутеров, /health
  schemas.py          # Pydantic-схемы запросов/ответов
  print_db.py         # отладочный скрипт вывода данных из БД в консоль
  init_db.py           # наполнение БД тестовыми данными
  api/
    categories.py      # CRUD-роуты /categories
    books.py            # CRUD-роуты /books (+ фильтр по category_id)
  db/
    db.py                # подключение к БД, сессия, get_db()
    models.py            # модели Category и Book
    crud.py               # функции CRUD к БД
requirements.txt
.env                    # параметры подключения к БД (не коммитить в открытом виде на проде)
.gitignore
```

## Установка и запуск

### 1. PostgreSQL

Установи PostgreSQL (в WSL/Ubuntu) и создай пользователя и базу:

```bash
sudo apt update && sudo apt install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql
```

В консоли `psql`:

```sql
CREATE USER octagon WITH PASSWORD '12345';
CREATE DATABASE octagon_db OWNER octagon;
\q
```

Подключиться к своей базе можно так (peer-аутентификация по умолчанию требует `-h localhost`):

```bash
psql -h localhost -U octagon -d octagon_db
```

### 2. Виртуальное окружение и зависимости

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Переменные окружения

Файл `.env` в корне проекта уже содержит параметры подключения:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345
```

### 4. Наполнение БД тестовыми данными (опционально)

```bash
python -m app.init_db
```

Создаст 2 категории и по несколько книг в каждой.

### 5. Запуск API

```bash
uvicorn app.main:app --reload
```

После запуска доступны:

- `http://127.0.0.1:8000/health` — проверка, что сервис жив
- `http://127.0.0.1:8000/docs` — интерактивная Swagger-документация со всеми эндпоинтами

## Эндпоинты

### Categories

| Метод  | Путь                  | Описание                        |
|--------|-----------------------|----------------------------------|
| GET    | /categories/           | список категорий                |
| GET    | /categories/{id}       | категория по id                 |
| POST   | /categories/           | создать категорию                |
| PUT    | /categories/{id}       | обновить категорию                |
| DELETE | /categories/{id}       | удалить категорию                 |

### Books

| Метод  | Путь                              | Описание                                    |
|--------|-----------------------------------|-----------------------------------------------|
| GET    | /books/                            | список книг                                   |
| GET    | /books/?category_id={id}           | список книг, отфильтрованный по категории     |
| GET    | /books/{id}                        | книга по id                                   |
| POST   | /books/                            | создать книгу (проверяется, что категория существует) |
| PUT    | /books/{id}                        | обновить книгу                                 |
| DELETE | /books/{id}                        | удалить книгу                                  |

## Проверка через psql

После запросов через API можно свериться напрямую с базой:

```bash
psql -h localhost -U octagon -d octagon_db
SELECT * FROM categories;
SELECT * FROM books;
```

## Скриншоты

Скриншоты работы (`/docs`, успешный запрос, вывод `psql`) находятся в папке `examples/`.
