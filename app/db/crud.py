"""
CRUD-функции (Create, Read, Update, Delete) для таблиц categories и books.
"""

from sqlalchemy.orm import Session

from app.db.models import Book, Category


# ---------- CATEGORY CRUD ----------

def create_category(db: Session, title: str) -> Category:
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, new_title: str) -> Category | None:
    category = get_category(db, category_id)
    if category is None:
        return None
    category.title = new_title
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if category is None:
        return False
    db.delete(category)
    db.commit()
    return True


# ---------- BOOK CRUD ----------

def create_book(
    db: Session,
    title: str,
    description: str,
    price: float,
    category_id: int,
    url: str = "",
) -> Book:
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, **fields) -> Book | None:
    """
    Обновляет переданные поля книги.
    Пример: update_book(db, 1, price=999.0, title="Новое название")
    """
    book = get_book(db, book_id)
    if book is None:
        return None
    for key, value in fields.items():
        if hasattr(book, key):
            setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = get_book(db, book_id)
    if book is None:
        return False
    db.delete(book)
    db.commit()
    return True
