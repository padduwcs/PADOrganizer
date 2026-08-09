import json
import sys
from copy import deepcopy
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()
PAD_TRASH_DIR = BASE_DIR / "PADOrganizer_Trash"

DEFAULT_CONFIG = {
    "file_map": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".md"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executables": [".exe", ".msi", ".bat", ".cmd", ".sh"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".cs", ".php", ".json", ".xml"],
        "Design": [".psd", ".ai", ".xd", ".fig", ".sketch"],
        "Books": [".epub", ".mobi", ".azw3"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
        "Archives": [".iso", ".dmg", ".torrent"],
        "Others": [".apk", ".bak", ".tmp"]
    },
    "sort_by_date": False
}

class ConfigManager:
    def __init__(self, filename="config.json"):
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).parent
        else:
            self.base_dir = Path(__file__).resolve().parent.parent
            
        self.config_path = self.base_dir / filename
        self.config = self.load_config()

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return deepcopy(DEFAULT_CONFIG)

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_file_map(self):
        return deepcopy(self.config.get("file_map", DEFAULT_CONFIG["file_map"]))

    def set_file_map(self, file_map):
        self.config["file_map"] = deepcopy(file_map)
        self.save_config()
        
    def is_sort_by_date_enabled(self):
        return self.config.get("sort_by_date", False)
        
    def set_sort_by_date(self, enabled: bool):
        self.config["sort_by_date"] = enabled
        self.save_config()
