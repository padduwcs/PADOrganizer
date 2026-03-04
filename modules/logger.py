# modules/logger.py
from datetime import datetime

class SmartLogger:
    def __init__(self, log_path="logs/activity.log"):
        self.log_path = log_path

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")