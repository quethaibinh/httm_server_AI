# repository/review_repository.py
import pandas as pd
from typing import List

from sqlalchemy.orm import Session
from dto.review_response import ReviewResponse
from model.review import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, reviewResponses: List[ReviewResponse]):
        incoming_ids = {r.review_id for r in reviewResponses}
        existing_ids = {
            rid for (rid,) in self.db.query(Review.id)
            .filter(Review.id.in_(incoming_ids))
            .all()
        }

        reviews = []
        for reviewResponse in reviewResponses:
            if reviewResponse.review_id not in existing_ids:
                reviews.append(Review(
                    id = reviewResponse.review_id,
                    book_id = reviewResponse.book_id,
                    raw_text = reviewResponse.raw_content,
                    rating = reviewResponse.rating,
                    source = reviewResponse.customer_name,
                    created_at = reviewResponse.created_at,
                    sentiment = reviewResponse.sentiment_overall
                ))
        self.db.bulk_save_objects(reviews)
        self.db.commit()
        return len(reviews)
