# repository/review_repository.py
import pandas as pd
from typing import List
from dto.review_response import ReviewResponse

class ReviewRepository:
    def __init__(self, output_path: str = "clean_reviews.xlsx"):
        self.output_path = output_path

    def save_reviews_to_excel(self, reviews: List[ReviewResponse]):
        if not reviews:
            return 0
        df = pd.DataFrame([r.to_dict() for r in reviews])
        # nếu file tồn tại, gộp (append) và drop duplicate
        try:
            old = pd.read_excel(self.output_path)
            df = pd.concat([old, df], ignore_index=True).drop_duplicates(subset=["review_id"])
        except Exception:
            pass
        df.to_excel(self.output_path, index=False)
        return len(df)
