"""
Модуль подключения к базе данных PostgreSQL через SQLAlchemy.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Загружаем переменные окружения из файла .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "octagon_db")
DB_USER = os.getenv("DB_USER", "octagon")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# echo=True удобно на этапе отладки — в консоли видно все SQL-запросы
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    """
    Генератор сессии подключения к БД.
    Используется как контекст: сессия закрывается автоматически.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Создаёт все таблицы, описанные в models.py, если их ещё нет.
    """
    # Импорт моделей нужен здесь, чтобы Base "увидел" все таблицы
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
