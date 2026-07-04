"""
Точка входа FastAPI-приложения.

Запуск (из корня проекта, с активированным venv):
    uvicorn app.main:app --reload

Документация Swagger будет доступна по адресу:
    http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import books, categories
from app.db.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняется при старте приложения: поднимаем подключение к БД
    # и создаём таблицы, если их ещё нет
    init_db()
    yield
    # Здесь можно было бы закрывать соединения при остановке приложения


app = FastAPI(
    title="Octagon Books API",
    description="Простой CRUD API для книг и категорий на FastAPI + SQLAlchemy + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)
