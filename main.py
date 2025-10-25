# main.py
from fastapi import FastAPI
from controller.schedule_controller import ScheduleController
from dto.review_response import CollectStatus
import uvicorn
from database import Base, engine
from model import *

app = FastAPI(title="Auto Collector FastAPI")

# Tự động tạo bảng dựa trên các lớp ORM đã định nghĩa
# Base.metadata.create_all(bind=engine)

# Khởi tạo controller singleton
schedule_controller = ScheduleController(interval_days=1)

@app.on_event("startup")
def startup_event():
    # Start scheduler khi FastAPI khởi động
    schedule_controller.start()

@app.on_event("shutdown")
def shutdown_event():
    schedule_controller.stop()

@app.get("/")
def root():
    return {"message": "Auto Collector is running"}

@app.get("/status")
def status():
    return schedule_controller.get_status().dict()

@app.post("/trigger")
def trigger_collection():
    # trigger thủ công
    schedule_controller.collect_all_once()
    return {"message": "Manual collection triggered", "last_run": schedule_controller.get_status().last_run}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
