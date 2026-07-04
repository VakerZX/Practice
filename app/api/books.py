"""
Роуты уровня /books.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import BookCreate, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookOut])
def list_books(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    books = crud.get_books(db, skip=skip, limit=limit)
    if category_id is not None:
        books = [b for b in books if b.category_id == category_id]
    return books


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    # Проверяем, что категория существует, прежде чем создавать книгу
    category = crud.get_category(db, payload.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail="Указанная категория не существует")

    return crud.create_book(
        db,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        url=payload.url or "",
    )


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    # Если меняют категорию — проверим, что новая категория существует
    if payload.category_id is not None:
        category = crud.get_category(db, payload.category_id)
        if category is None:
            raise HTTPException(status_code=400, detail="Указанная категория не существует")

    fields = payload.model_dump(exclude_unset=True)
    book = crud.update_book(db, book_id, **fields)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return None
