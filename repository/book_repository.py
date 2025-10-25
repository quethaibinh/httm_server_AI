# repository/product_repository.py
from typing import List
from sqlalchemy.orm import Session

from model.book import Book

class BookRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[Book]:
        return self.db.query(Book).all()
    

