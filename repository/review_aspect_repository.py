from pyparsing import List
from sqlalchemy.orm import Session
from dto.review_response import ReviewResponse
from model.review_aspect import ReviewAspect


class ReviewAspectRepository:
    def __init__(self, db: Session):
        self.db_session = db

    def save(self, reviewResponses: List[ReviewResponse]):

        incoming_ids = {r.review_id for r in reviewResponses}
        existing_ids = {
            rid for (rid,) in self.db_session.query(ReviewAspect.review_id)
            .filter(ReviewAspect.review_id.in_(incoming_ids))
            .all()
        }
        reviewAspects = []
        for reviewResponse in reviewResponses:
            if reviewResponse.review_id not in existing_ids:
                for aspectSentiment in reviewResponse.sentiment_aspects:
                    reviewAspects.append(
                        ReviewAspect(
                            aspect_code = aspectSentiment.aspect_name,
                            sentiment = aspectSentiment.sentiment_label,
                            created_at = reviewResponse.created_at,
                            review_id = reviewResponse.review_id,
                            book_id = reviewResponse.book_id
                        )
                    )
        self.db_session.bulk_save_objects(reviewAspects)
        self.db_session.commit()
        return len(reviewAspects)