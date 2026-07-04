"""
Скрипт первичного наполнения базы данных.

Запуск (из корня проекта, с активированным venv):
    python -m app.init_db
"""

from app.db import crud
from app.db.db import SessionLocal, init_db


def seed():
    # Создаём таблицы, если их ещё нет
    init_db()

    db = SessionLocal()
    try:
        # --- Категории ---
        fiction = crud.create_category(db, "Художественная литература")
        science = crud.create_category(db, "Научная литература")

        # --- Книги для категории "Художественная литература" ---
        crud.create_book(
            db,
            title="Мастер и Маргарита",
            description="Роман Михаила Булгакова о добре и зле, любви и предательстве.",
            price=650.0,
            category_id=fiction.id,
        )
        crud.create_book(
            db,
            title="Преступление и наказание",
            description="Роман Фёдора Достоевского о преступлении и муках совести.",
            price=590.0,
            category_id=fiction.id,
        )
        crud.create_book(
            db,
            title="Война и мир",
            description="Роман-эпопея Льва Толстого о судьбах людей на фоне войны 1812 года.",
            price=890.0,
            category_id=fiction.id,
        )

        # --- Книги для категории "Научная литература" ---
        crud.create_book(
            db,
            title="Краткая история времени",
            description="Стивен Хокинг о происхождении и устройстве Вселенной.",
            price=720.0,
            category_id=science.id,
        )
        crud.create_book(
            db,
            title="Эгоистичный ген",
            description="Ричард Докинз о теории эволюции с точки зрения генов.",
            price=680.0,
            category_id=science.id,
        )

        print("База данных успешно наполнена тестовыми данными.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
