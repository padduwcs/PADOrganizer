import json
from copy import deepcopy
from pathlib import Path

from .platform_paths import APPLICATION_DIR, CONFIG_DIR, PAD_TRASH_DIR


BASE_DIR = APPLICATION_DIR

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
    "sort_by_date": False,
    "theme": "light",
    "language": "vi",
}

class ConfigManager:
    def __init__(self, filename="config.json", config_dir=None):
        self.config_path = Path(config_dir or CONFIG_DIR) / filename
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
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
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

    def get_theme(self):
        theme = self.config.get("theme", DEFAULT_CONFIG["theme"])
        return theme if theme in {"light", "dark"} else DEFAULT_CONFIG["theme"]

    def set_theme(self, theme):
        self.config["theme"] = theme if theme in {"light", "dark"} else "light"
        self.save_config()

    def get_language(self):
        language = self.config.get("language", DEFAULT_CONFIG["language"])
        return language if language in {"vi", "en"} else DEFAULT_CONFIG["language"]

    def set_language(self, language):
        self.config["language"] = language if language in {"vi", "en"} else "vi"
        self.save_config()
