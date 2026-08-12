import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.check_version import source_version
from scripts.new_checksums import sha256


class ReleaseToolTests(unittest.TestCase):
    def test_source_version_reads_semantic_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "version.py").write_text('APP_VERSION = "2.4.6"\n', encoding="utf-8")
            self.assertEqual(source_version(root), "2.4.6")

    def test_sha256_streams_file_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.bin"
            content = b"PADOrganizer release artifact"
            path.write_bytes(content)
            self.assertEqual(sha256(path), hashlib.sha256(content).hexdigest())


if __name__ == "__main__":
    unittest.main()
