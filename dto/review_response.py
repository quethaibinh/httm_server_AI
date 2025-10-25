# model/dto.py
from typing import Any, Optional

from pydantic import BaseModel, Field

class AspectSentiment(BaseModel):
    aspect_name: str
    sentiment_label: str
    # confidence: float | None = None
    # extra_metadata: dict[str, Any] | None = None


class ReviewResponse(BaseModel):
    book_id: int
    book_name: str
    rating: float | None = None
    raw_content: str
    created_at: str
    customer_name: Optional[str] = None
    sentiment_overall: Optional[str] = None
    sentiment_aspects: list[AspectSentiment] = Field(default_factory=list)

    def add_overall_sentiment(self, label: str) -> None:
        self.sentiment_overall = label

    def add_aspect_sentiment(self, aspect: AspectSentiment) -> None:
        self.sentiment_aspects.append(aspect)

class CollectStatus(BaseModel):
    last_run: Optional[str] = None
    total_collected: int = 0
    running: bool = False
