# model/entities.py
from typing import Optional

class Product:
    def __init__(self, product_id: int, name: str, category: Optional[str]=None, source: str="tiki"):
        self.product_id = int(product_id)
        self.name = name
        self.category = category
        self.source = source

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "source": self.source
        }

class Review:
    def __init__(self, review_id: int, product_id: int, rating: int, content: str, created_at: str, customer_name: Optional[str]=None):
        self.review_id = review_id
        self.product_id = product_id
        self.rating = rating
        self.content = content
        self.created_at = created_at
        self.customer_name = customer_name

    def to_dict(self):
        return {
            "review_id": self.review_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "content": self.content,
            "created_at": self.created_at,
            "customer_name": self.customer_name
        }
