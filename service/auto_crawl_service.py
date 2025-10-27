# service/crawler_service.py
import random
import time
import re
from datetime import datetime
import requests
from sqlalchemy.orm import Session
from typing import List
from model.book import Book
from dto.review_response import ReviewResponse
from repository.book_repository import BookRepository

class AutoCrawlService:
    def __init__(self, book_repo: BookRepository, db: Session, max_pages: int = 5, delay_range=(1.5, 3.0)):
        self.max_pages = max_pages
        self.delay_range = delay_range
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; rv:118.0) Gecko/20100101 Firefox/118.0"
        ]
        self.vietnamese_chars = set("ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ")
        self.book_repo = book_repo
        self.db = db

    def _get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://tiki.vn/"
        }

    def get_all_booḳ̣(self) -> List[Book]:
        return self.book_repo.get_all_products()

    def crawl_reviews_for_product(self, product: Book) -> List[ReviewResponse]:
        reviews = []
        headers = self._get_headers()
        for page in range(1, self.max_pages + 1):
            print(f"[Crawler] Crawling reviews for product {product.id} (page {page})...")
            url = f"https://tiki.vn/api/v2/reviews?product_id={product.id}&page={page}&limit=20"
            try:
                res = requests.get(url, headers=headers, timeout=10)
            except Exception as e:
                print(f"[Crawler] Request error for product {product.id}: {e}")
                break

            if res.status_code == 403:
                print(f"[Crawler] 403 Forbidden for product {product.id} (page {page}), stop this product.")
                break
            if res.status_code != 200:
                print(f"[Crawler] Status {res.status_code} for product {product.id} (page {page}), stop.")
                break

            try:
                data = res.json()
                # print(f"data: {data}")
            except Exception as e:
                print(f"[Crawler] JSON decode error: {e}")
                break

            items = data.get("data", [])
            if not items:
                break

            for it in items:
                timestamp = it.get("created_at")
                if isinstance(timestamp, (int, float)):
                    created_at = datetime.fromtimestamp(timestamp).isoformat()
                else:
                    created_at = str(timestamp or "")

                response = ReviewResponse(
                    book_id=product.id,
                    book_name=product.name,
                    review_id=it.get("id"),
                    rating=it.get("rating"),
                    raw_content=it.get("content", ""),
                    created_at=created_at,
                    customer_name=it.get("created_by", {}).get("name"),
                    sentiment_overall=None,
                )
                reviews.append(response)

            time.sleep(random.uniform(*self.delay_range))

        return reviews
    

    def clean_text(self, text: str) -> str:
        if not text:
            return None
        text = re.sub(r'<.*?>', '', text)            # remove html
        text = re.sub(r'[^\w\sÀ-ỹ]', ' ', text)     # keep letters/numbers
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.lower()
        if len(text.split()) < 3:
            return None
        return text

    def is_vietnamese(self, text: str) -> bool:
        return any(ch in self.vietnamese_chars for ch in text)

    def filter_and_clean(self, raw_reviews: List[ReviewResponse]) -> List[ReviewResponse]:
        cleaned = []
        for r in raw_reviews:
            cleaned_text = self.clean_text(r.raw_content)
            if not cleaned_text:
                continue
            if not self.is_vietnamese(cleaned_text):
                continue
            r.raw_content = cleaned_text
            cleaned.append(r)
        return cleaned