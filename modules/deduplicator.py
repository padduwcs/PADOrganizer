# modules/deduplicator.py
import hashlib
from pathlib import Path

from .safety import list_candidate_files


class Deduplicator:
    @staticmethod
    def hash_file(file_path: Path, block_size=65536) -> str:
        hasher = hashlib.blake2b()
        try:
            with open(file_path, 'rb') as afile:
                buf = afile.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(block_size)
            return hasher.hexdigest()
        except Exception:
            return None

    def find_duplicates(self, target_dir: Path, progress_callback=None, excluded_paths=()):
        # Only files that share a size can be identical, so group by size before hashing.
        # Empty files are skipped: they carry no content worth deduplicating.
        sizes = {}
        for f in list_candidate_files(target_dir, excluded_paths):
            try:
                size = f.stat().st_size
            except OSError:
                continue
            if size > 0:
                sizes.setdefault(size, []).append(f)

        files_to_hash = [f for group in sizes.values() if len(group) > 1 for f in group]
        total_files = len(files_to_hash)

        hashes = {}
        for i, file_path in enumerate(files_to_hash):
            file_hash = self.hash_file(file_path)
            if file_hash:
                hashes.setdefault(file_hash, []).append(file_path)

            if progress_callback:
                progress_callback(i + 1, total_files, file_path.name)

        return [file_list for file_list in hashes.values() if len(file_list) > 1]
