from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

if TYPE_CHECKING:
    from .review import Review
    from .review_aspect import ReviewAspect
    from .book_category import BookCategory
    from .book_author import BookAuthor

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255))
    description = Column(String(255))
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    thumbnail = Column(String(255))
    number_of_page = Column(Integer)
    language = Column(String(255))

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    review_aspects = relationship("ReviewAspect", back_populates="book", cascade="all, delete-orphan")
    # book_categories = relationship("BookCategory", back_populates="book", cascade="all, delete-orphan")
    # book_authors = relationship("BookAuthor", back_populates="book", cascade="all, delete-orphan")