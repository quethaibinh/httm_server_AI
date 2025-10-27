from pyparsing import List
from dto.review_response import ReviewResponse
from repository.review_repository import ReviewRepository
from repository.review_aspect_repository import ReviewAspectRepository
from model.review_aspect import ReviewAspect
from model.review import Review

class ReviewService:
    def __init__(self, reviewRepo: ReviewRepository, reviewAspectRepo: ReviewAspectRepository):
        self.reviewRepo = reviewRepo
        self.reviewAspectRepo = reviewAspectRepo

    def saveData(self, reviewResponses: List[ReviewResponse]):
        reviewNumbers = self.reviewRepo.save(reviewResponses)
        revewAspectNumber = self.reviewAspectRepo.save(reviewResponses)     
        print(f"[ReviewService] Saved {reviewNumbers} reviews and {revewAspectNumber} review aspects.")