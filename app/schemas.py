"""
Pydantic-схемы: что API принимает на вход и что возвращает наружу.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------- CATEGORY ----------

class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    """Схема для создания категории."""
    pass


class CategoryUpdate(BaseModel):
    """Схема для обновления категории (все поля опциональны)."""
    title: Optional[str] = None


class CategoryOut(CategoryBase):
    """Схема ответа — то, что отдаём клиенту."""
    id: int

    # Позволяет строить схему прямо из объекта SQLAlchemy (аналог orm_mode в Pydantic v1)
    model_config = ConfigDict(from_attributes=True)


# ---------- BOOK ----------

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = ""
    category_id: int


class BookCreate(BookBase):
    """Схема для создания книги."""
    pass


class BookUpdate(BaseModel):
    """Схема для обновления книги (все поля опциональны)."""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None


class BookOut(BookBase):
    """Схема ответа — то, что отдаём клиенту."""
    id: int

    model_config = ConfigDict(from_attributes=True)
