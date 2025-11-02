from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Protocol, Union

from dto.review_response import AspectSentiment, ReviewResponse
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


ASPECT_KEYWORDS = {
    "noi_dung": [
        "nội dung", "ý nghĩa", "câu chuyện", "kiến thức", "bài học", "chủ đề", "tác giả", "dịch", "dich" "dịch thuật", "phong cách viết",
        "chiêm nghiệm", "bản dịch", "thông điệp", "tâm lý học", "giá trị", "bổ ích", "hấp dẫn", "ok", "oke", "dễ hiểu", "khó hiểu",
        "sâu sắc", "truyền tải", "chi tiết", "lời văn", "cảm nhận", "đáng đọc", "hay", "chán", "nhàm chán", "lỗi chính tả", "sai chính tả"
    ],
    "hinh_thuc": [
        "bìa", "giấy", "in ấn", "chất lượng giấy", "trang sách", "hình ảnh", "minh họa", "mực in", "đóng gói", "bọc sách", "xinh", "xinhh", "thơm"
        "bẩn", "rách", "xước", "móp", "cũ", "mới", "đẹp", "dày", "mỏng", "seal", "ố", "bụi", "sạch", "bong keo", "gấp góc", "bìa cứng", "bìa mềm"
    ],
    "gia_ca": [
        "giá", "giá cả", "giá tiền", "đắt", "rẻ", "khuyến mãi", "sale", "giá tốt", "đáng tiền", "đắt đỏ", "giảm giá", "niêm yết"
    ],
    "giao_hang": [
        "giao hàng", "ship", "vận chuyển", "đóng gói", "nhận hàng", "thời gian giao", "chuyển phát", "freeship", "shop", "tiki", "hoa toc", "hỏa tốc"
    ],
    "dich_vu": [
        "đổi trả", "hỗ trợ", "dịch vụ", "chăm sóc khách hàng", "tư vấn", "phản hồi", "hoàn tiền", "nhan", "nhắn"
    ]
}

def detect_aspects(text: str, keywords: Dict[str, List[str]] = ASPECT_KEYWORDS) -> List[str]:
    """Trả về danh sách aspect được detect theo keyword matching (weak heuristic)."""
    text_lower = text.lower()
    found = []
    for aspect, kw_list in keywords.items():
        for kw in kw_list:
            if kw.lower() in text_lower:
                found.append(aspect)
                break
    return found

class PredictionModel(Protocol):
    """Common interface for sentiment classifier implementations."""

    def predict(self, text: str):
        ...


class TransformersTextClassifier:
    """Wraps a local Hugging Face checkpoint using the transformers pipeline."""

    def __init__(self, model_dir: Union[str, Path], *, device: int | None = None) -> None:
        model_dir = Path(model_dir).resolve()
        if not model_dir.exists():
            raise FileNotFoundError(f"Model directory not found: {model_dir}")

        self._tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self._model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        # device = -1 means CPU, otherwise pass GPU index
        pipeline_device = device if device is not None else -1
        self._pipeline = pipeline(
            "text-classification",
            model=self._model,
            tokenizer=self._tokenizer,
            device=pipeline_device,
            truncation=True,
        )
        tokenizer_max = getattr(self._tokenizer, "model_max_length", None)
        model_max = getattr(self._model.config, "max_position_embeddings", None)
        candidates = [val for val in (tokenizer_max, model_max) if isinstance(val, int) and val > 0]
        if candidates:
            self._max_length = max(8, min(candidates) - 2)
        else:
            self._max_length = None

    def predict(self, text: str):
        if not text:
            return []

        generation_kwargs = {"truncation": True}
        if self._max_length is not None:
            generation_kwargs["max_length"] = self._max_length

        outputs = self._pipeline(text, **generation_kwargs)
        # transformers returns list of dicts; normalise to list for callers
        if isinstance(outputs, dict):
            outputs = [outputs]
        return outputs


class HandleDataService:
    """Service responsible for sentiment inference using AI models."""

    def __init__(
        self,
        overall_model: Union[PredictionModel, str, Path, None] = None,
        aspect_model: Union[PredictionModel, str, Path, None] = None,
        *,
        device: int | None = None,
    ) -> None:
        base_dir = Path(__file__).resolve().parent.parent / "model_AI"

        if overall_model is None:
            overall_model = base_dir / "model_overall"
        if isinstance(overall_model, (str, Path)):
            self._overall_model = TransformersTextClassifier(overall_model, device=device)
        else:
            self._overall_model = overall_model

        if aspect_model is None:
            aspect_model = base_dir / "model__aspect"
        if isinstance(aspect_model, (str, Path)):
            self._aspect_model = TransformersTextClassifier(aspect_model, device=device)
        else:
            self._aspect_model = aspect_model

    def handle_review_overall(self, reviews: Iterable[ReviewResponse]) -> list[ReviewResponse]:
        response = []
        for review in reviews:
            predictions = self._overall_model.predict(review.raw_content)
            label = ""
            if predictions:
                top = predictions[0]
                if isinstance(top, dict):
                    label = top.get("label", "")
                else:
                    label = str(top)
            review.add_overall_sentiment(label)
            response.append(review)
        return response

    def handle_review_aspect(self, reviews: Iterable[ReviewResponse]) -> list[ReviewResponse]:
        enriched = []
        for review in reviews:
            aspects = detect_aspects(review.raw_content)  # ['noi_dung', 'gia_ca', ...]
            for asp in aspects:
                input_text = f"{review.raw_content} [SEP] {asp}"
                pred = self._aspect_model.predict(input_text)[0]  # ví dụ {'label': 'POSITIVE', 'score': 0.87}
                label = pred.get("label") or pred.get("sentiment") or pred.get("sentiment_label")
                review.add_aspect_sentiment(AspectSentiment(aspect_name=asp, sentiment_label=label))
            enriched.append(review)
        return enriched