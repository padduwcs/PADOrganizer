# modules/classifier.py
import shutil
from pathlib import Path
from datetime import datetime

class FileMover:
    @staticmethod
    def get_unique_path(path: Path) -> Path:
        """Nếu file đã tồn tại, thêm hậu tố (1), (2)... để tránh ghi đè."""
        counter = 1
        new_path = path
        while new_path.exists():
            new_path = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            counter += 1
        return new_path

    def move_file(self, source: Path, destination_folder: Path):
        if not destination_folder.exists():
            destination_folder.mkdir(parents=True)
        
        target_path = self.get_unique_path(destination_folder / source.name)
        shutil.move(str(source), str(target_path))
        return target_path