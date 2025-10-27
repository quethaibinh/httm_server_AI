from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class BookAuthor():
    __tablename__ = "book_author"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    book = relationship("Book", back_populates="book_authors")
    author = relationship("Author", back_populates="book_authors")