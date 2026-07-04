"""
Отладочный скрипт (перенесён из задания 5): читает данные из БД
и выводит их на экран в консоль — без API, напрямую через crud.py.

Запуск (из корня проекта, с активированным venv):
    python -m app.print_db
"""

from app.db import crud
from app.db.db import SessionLocal


def main():
    db = SessionLocal()
    try:
        categories = crud.get_categories(db)

        if not categories:
            print("В базе данных пока нет категорий. Сначала запустите init_db.py")
            return

        for category in categories:
            print(f"\nКатегория: {category.title} (id={category.id})")
            print("-" * 40)

            books = [book for book in category.books]
            if not books:
                print("  (в этой категории пока нет книг)")
                continue

            for book in books:
                print(f"  • {book.title}")
                print(f"    Цена: {book.price} руб.")
                print(f"    Описание: {book.description}")
                print(f"    Ссылка: {book.url or '(пусто)'}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
