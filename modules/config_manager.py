import json
import os
import shutil
from copy import deepcopy
from pathlib import Path

from .classifier import normalize_extension
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

__all__ = ["BASE_DIR", "DEFAULT_CONFIG", "PAD_TRASH_DIR", "ConfigManager", "sanitize_config"]


def _sanitize_file_map(value):
    """Return a cleaned category map, or None when nothing usable remains."""
    if not isinstance(value, dict):
        return None
    file_map = {}
    for category, extensions in value.items():
        if not isinstance(category, str) or not category.strip():
            continue
        if not isinstance(extensions, list):
            continue
        normalized = []
        for extension in extensions:
            if not isinstance(extension, str):
                continue
            extension = normalize_extension(extension)
            if extension and extension not in normalized:
                normalized.append(extension)
        file_map[category.strip()] = normalized
    return file_map or None


def sanitize_config(raw):
    """Merge a loaded config over the defaults, discarding values of the wrong type."""
    config = deepcopy(DEFAULT_CONFIG)
    if not isinstance(raw, dict):
        return config
    for key, value in raw.items():
        if key not in DEFAULT_CONFIG:
            config[key] = value
    file_map = _sanitize_file_map(raw.get("file_map"))
    if file_map is not None:
        config["file_map"] = file_map
    if isinstance(raw.get("sort_by_date"), bool):
        config["sort_by_date"] = raw["sort_by_date"]
    if raw.get("theme") in {"light", "dark"}:
        config["theme"] = raw["theme"]
    if raw.get("language") in {"vi", "en"}:
        config["language"] = raw["language"]
    return config


class ConfigManager:
    def __init__(self, filename="config.json", config_dir=None):
        self.config_path = Path(config_dir or CONFIG_DIR) / filename
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            return deepcopy(DEFAULT_CONFIG)
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return sanitize_config(json.load(f))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            self._backup_unreadable_config()
            return deepcopy(DEFAULT_CONFIG)

    def _backup_unreadable_config(self):
        # Keep the damaged file so custom rules can still be recovered by hand.
        try:
            shutil.copy2(self.config_path, self.config_path.with_name(self.config_path.name + ".broken"))
        except OSError:
            pass

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.config_path.with_name(self.config_path.name + ".tmp")
        try:
            with open(temporary, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporary, self.config_path)
        except BaseException:
            try:
                temporary.unlink()
            except OSError:
                pass
            raise

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
