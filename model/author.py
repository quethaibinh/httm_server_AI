from sqlalchemy import Column, Date, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Author():
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date)
    national = Column(String(255))
    description = Column(String(255))

    book_authors = relationship("BookAuthor", back_populates="author")