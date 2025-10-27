# controller/schedule_controller.py
import random
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from database import SessionLocal
from repository.book_repository import BookRepository
from repository.review_aspect_repository import ReviewAspectRepository
from repository.review_repository import ReviewRepository
from service.auto_crawl_service import AutoCrawlService
from dto.review_response import CollectStatus
from service.handle_data_service import HandleDataService
from service.review_service import ReviewService

class ScheduleController:
    def __init__(self, interval_days: int = 1):
        self.db = SessionLocal()
        self.book_repo = BookRepository(self.db)
        self.review_repo = ReviewRepository(self.db)
        self.review_aspect_repo = ReviewAspectRepository(self.db)
        self.crawler = AutoCrawlService(self.book_repo, self.db)
        self.handle_data_service = HandleDataService()
        self.review_service = ReviewService(self.review_repo, self.review_aspect_repo)
        self.scheduler = BackgroundScheduler()
        self.status = CollectStatus()
        self.interval_days = interval_days

    def collect_all_once(self):
        print(f"[ScheduleController] Start collect at {datetime.now()}")
        self.status.running = True
        total_collected = 0
        products = self.crawler.get_all_booḳ̣()
        print(f"\n[ScheduleController] Found {len(products)} products to collect.")
        for p in products:
            all_cleaned = []
            print(f"\n Đang thu thập review cho: {p.name} (ID={p.id})")
            raw = self.crawler.crawl_reviews_for_product(p)
            print(f"dữ liệu crawl: có {len(raw)} review.")
            cleaned = self.crawler.filter_and_clean(raw)
            print(f"Sau làm sạch: còn {len(cleaned)} review hợp lệ.")
            all_cleaned.extend(cleaned)
            overall_response = self.handle_data_service.handle_review_overall(all_cleaned)
            response = self.handle_data_service.handle_review_aspect(overall_response)
            self.review_service.saveData(response)
            print("Nghỉ 5 giây trước khi chuyển sang sản phẩm tiếp theo...")
            time.sleep(random.uniform(5, 10))
        print(f"[ScheduleController] Done collect at {datetime.now()}, saved {total_collected}")

    def start(self):
        # chạy 1 lần khi start app (có thể comment nếu không muốn)
        self.collect_all_once()
        # lập lịch hàng ngày
        self.scheduler.add_job(self.collect_all_once, 'interval', days=self.interval_days)
        self.scheduler.start()
        print("[ScheduleController] Scheduler started")

    def stop(self):
        self.scheduler.shutdown(wait=False)

    def get_status(self):
        return self.status
    
    def __del__(self):
        if self.db:
            self.db.close()