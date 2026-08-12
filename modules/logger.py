from pathlib import Path
from datetime import datetime

from .platform_paths import LOG_DIR

class PADLogger:
    def __init__(self, log_filename="activity.log", log_dir=None):
        self.log_path = Path(log_dir or LOG_DIR) / log_filename
        self.ensure_log_directory()

    def ensure_log_directory(self):
        log_dir = self.log_path.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message):
        self.ensure_log_directory()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def has_logs(self):
        try:
            return self.log_path.exists() and self.log_path.stat().st_size > 0
        except OSError:
            return False

    def clear_logs(self):
        if not self.log_path.exists():
            return False

        self.log_path.unlink()
        try:
            self.log_path.parent.rmdir()
        except OSError:
            pass
        return True
