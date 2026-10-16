# modules/classifier.py
import shutil
from pathlib import Path
from datetime import datetime


FALLBACK_CATEGORY = "Others"


def normalize_extension(value) -> str:
    """Return a lowercase extension with a leading dot, or "" for blank input."""
    value = str(value).strip().lower()
    if value and not value.startswith("."):
        value = f".{value}"
    return value


def build_extension_index(file_map) -> dict:
    """Map each normalized extension to the first category that claims it."""
    index = {}
    for category, extensions in file_map.items():
        for extension in extensions:
            index.setdefault(normalize_extension(extension), category)
    index.pop("", None)
    return index


def categorize(extension, extension_index) -> str:
    return extension_index.get(normalize_extension(extension), FALLBACK_CATEGORY)


class FileMover:
    def __init__(self):
        self.histories = []
        self.current_batch = []

    def start_batch(self):
        self.current_batch = []

    def end_batch(self):
        if self.current_batch:
            self.histories.append(self.current_batch)
            self.current_batch = []

    def has_history(self):
        return len(self.histories) > 0

    @staticmethod
    def get_unique_path(path: Path) -> Path:
        counter = 1
        new_path = path
        while new_path.exists():
            new_path = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            counter += 1
        return new_path

    def move_file(self, source: Path, destination_folder: Path, sort_by_date: bool = False):
        final_dest = destination_folder
        if sort_by_date:
            try:
                mtime = source.stat().st_mtime
                dt = datetime.fromtimestamp(mtime)
                year_month = dt.strftime("%Y-%m")
                final_dest = destination_folder / year_month
            except Exception:
                pass
                
        final_dest.mkdir(parents=True, exist_ok=True)

        target_path = self.get_unique_path(final_dest / source.name)
        shutil.move(str(source), str(target_path))
        
        self.current_batch.append((source, target_path))
        return target_path
        
    def undo_last_operation(self, logger=None):
        """Khôi phục lại thao tác gần nhất"""
        if not self.histories:
            return 0, 0
            
        last_batch = self.histories.pop()
        success_count = 0
        error_count = 0
        directories_to_check = set()
        
        for original_path, current_path in last_batch:
            try:
                if current_path.exists():
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                    undo_path = self.get_unique_path(original_path)
                    shutil.move(str(current_path), str(undo_path))
                    directories_to_check.add(current_path.parent)
                    
                    if logger:
                        logger.log(f"UNDO SUCCESS: {current_path.name} -> {undo_path}")
                    success_count += 1
            except Exception as e:
                if logger:
                    logger.log(f"UNDO ERROR: Lỗi khi khôi phục {current_path.name} - {e}")
                error_count += 1
                
        for d in directories_to_check:
            try:
                if d.exists() and d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
                    if d.parent.exists() and d.parent.is_dir() and not any(d.parent.iterdir()):
                        d.parent.rmdir()
            except Exception:
                pass
        
        return success_count, error_count

    def discard_files(self, files, trash_dir: Path, permanent=False, logger=None, progress_callback=None):
        """Trash (undoable) or permanently delete files; return (success, errors)."""
        success_count = 0
        error_count = 0
        total = len(files)
        if not permanent:
            trash_dir.mkdir(parents=True, exist_ok=True)
            self.start_batch()

        for index, file_path in enumerate(files):
            try:
                if permanent:
                    file_path.unlink()
                    message = f"PERMANENT DELETED: {file_path.name}"
                else:
                    new_path = self.move_file(file_path, trash_dir, sort_by_date=False)
                    message = f"TRASHED: {file_path.name} -> {new_path.name}"
                success_count += 1
            except Exception as e:
                prefix = "PERM DELETE ERROR" if permanent else "TRASH ERROR"
                message = f"{prefix}: {file_path.name} - {e}"
                error_count += 1
            if logger:
                logger.log(message)
            if progress_callback:
                progress_callback(index + 1, total, file_path.name)

        if not permanent:
            self.end_batch()
        return success_count, error_count
