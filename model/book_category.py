from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class BookCategory(Base):
    __tablename__ = "book_category"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)

    category = relationship("Category", back_populates="book_categories")
    book = relationship("Book", back_populates="book_categories")