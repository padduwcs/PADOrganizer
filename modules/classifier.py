# modules/classifier.py
import shutil
from pathlib import Path
from datetime import datetime

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
                
        if not final_dest.exists():
            final_dest.mkdir(parents=True)
        
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
                    if not original_path.parent.exists():
                        original_path.parent.mkdir(parents=True)
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