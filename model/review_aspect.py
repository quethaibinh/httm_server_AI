from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

if TYPE_CHECKING:
    from .book import Book
    from .review import Review

class ReviewAspect(Base):
    __tablename__ = "review_aspect"

    id = Column(Integer, primary_key=True, index=True)
    sentiment = Column(String(255))
    created_at = Column(DateTime(timezone=True))
    aspect_code = Column(String, nullable=False)
    review_id = Column(Integer, ForeignKey("review.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)

    review = relationship("Review", back_populates="aspects")
    book = relationship("Book", back_populates="review_aspects")