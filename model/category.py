from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Category():
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    name = Column(String(255))

    book_categories = relationship("BookCategory", back_populates="category")