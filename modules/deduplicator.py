# modules/deduplicator.py
import hashlib
from pathlib import Path

class Deduplicator:
    @staticmethod
    def hash_file(file_path: Path, block_size=65536) -> str:
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as afile:
                buf = afile.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(block_size)
            return hasher.hexdigest()
        except Exception:
            return None

    def find_duplicates(self, target_dir: Path, progress_callback=None):
        hashes = {}
        duplicates = []
        
        all_files = []
        for f in target_dir.iterdir():
            if f.is_file():
                all_files.append(f)
                
        total_files = len(all_files)
        
        for i, file_path in enumerate(all_files):
            file_hash = self.hash_file(file_path)
            if file_hash:
                if file_hash in hashes:
                    hashes[file_hash].append(file_path)
                else:
                    hashes[file_hash] = [file_path]
            
            if progress_callback:
                progress_callback(i + 1, total_files, file_path.name)
                
        for file_hash, file_list in hashes.items():
            if len(file_list) > 1:
                duplicates.append(file_list)
                
        return duplicates
