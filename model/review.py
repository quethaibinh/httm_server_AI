from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

if TYPE_CHECKING:
    from .book import Book

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    raw_text = Column(Text)
    rating = Column(Float)
    source = Column(String(255))
    created_at = Column(DateTime)
    status = Column(String(255))
    sentiment = Column(String(255))

    book = relationship("Book", back_populates="reviews")
    aspects = relationship("ReviewAspect", back_populates="review", cascade="all, delete-orphan")