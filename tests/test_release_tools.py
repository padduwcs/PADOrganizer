import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.check_version import source_version
from scripts.new_checksums import sha256
from scripts.release_notes import release_notes


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

    def test_release_notes_extracts_only_requested_section(self):
        changelog = (
            "# Changelog\n\n"
            "## [2.0.0] - 2030-01-02\n\n### Added\n- New thing\n\n"
            "## [1.9.0] - 2029-12-01\n\n- Old thing\n\n"
            "[2.0.0]: https://example.com/compare\n"
        )
        self.assertEqual(release_notes(changelog, "2.0.0"), "### Added\n- New thing\n")
        self.assertEqual(release_notes(changelog, "1.9.0"), "- Old thing\n")
        with self.assertRaises(ValueError):
            release_notes(changelog, "3.0.0")

    def test_changelog_covers_current_version(self):
        root = Path(__file__).resolve().parent.parent
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(release_notes(changelog, source_version(root)).strip())


if __name__ == "__main__":
    unittest.main()
