# modules/logger.py
import os
import sys
from pathlib import Path
from datetime import datetime

class SmartLogger:
    def __init__(self, log_filename="activity.log"):
        # 1. Xác định thư mục gốc của dự án (Root Directory)
        # Nếu là file .py: Path(__file__) là đường dẫn file logger.py
        # Nếu là file .exe: sys.executable là đường dẫn file .exe
        if getattr(sys, 'frozen', False):
            # Nếu đang chạy từ file .exe
            base_dir = Path(sys.executable).parent
        else:
            # Nếu đang chạy từ file .py (nằm trong thư mục modules/)
            base_dir = Path(__file__).resolve().parent.parent

        # 2. Thiết lập đường dẫn tuyệt đối cho file log
        self.log_path = base_dir / "logs" / log_filename
        
        # 3. Tạo thư mục logs nếu chưa có
        self.ensure_log_directory()

    def ensure_log_directory(self):
        log_dir = self.log_path.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ghi log với đường dẫn tuyệt đối đã xác định
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")