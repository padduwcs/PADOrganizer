import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from modules.classifier import FileMover, build_extension_index, categorize, normalize_extension


class CategorizeTests(unittest.TestCase):
    def test_extensions_match_case_insensitively(self):
        index = build_extension_index({"Images": [".JPG", "png"], "Documents": [".pdf"]})

        self.assertEqual(categorize(".jpg", index), "Images")
        self.assertEqual(categorize(".PNG", index), "Images")
        self.assertEqual(categorize(".Pdf", index), "Documents")

    def test_unknown_or_missing_extension_falls_back_to_others(self):
        index = build_extension_index({"Images": [".jpg"]})

        self.assertEqual(categorize(".xyz", index), "Others")
        self.assertEqual(categorize("", index), "Others")

    def test_first_category_wins_for_duplicate_extension(self):
        index = build_extension_index({"Images": [".svg"], "Design": [".svg"]})
        self.assertEqual(categorize(".svg", index), "Images")

    def test_normalize_extension(self):
        self.assertEqual(normalize_extension(" JPG "), ".jpg")
        self.assertEqual(normalize_extension(".Tar"), ".tar")
        self.assertEqual(normalize_extension("  "), "")


class FileMoverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.mover = FileMover()

    def tearDown(self):
        self.temp.cleanup()

    def test_name_conflicts_get_numbered_suffix(self):
        destination = self.root / "Images"
        destination.mkdir()
        (destination / "photo.jpg").write_bytes(b"existing")
        source = self.root / "photo.jpg"
        source.write_bytes(b"new")

        self.mover.start_batch()
        moved = self.mover.move_file(source, destination)
        self.mover.end_batch()

        self.assertEqual(moved.name, "photo_1.jpg")
        self.assertEqual((destination / "photo.jpg").read_bytes(), b"existing")
        self.assertEqual(moved.read_bytes(), b"new")

    def test_undo_restores_files_and_removes_empty_date_folders(self):
        source = self.root / "photo.jpg"
        source.write_bytes(b"jpg")
        timestamp = datetime(2024, 5, 17, 12, 0).timestamp()
        os.utime(source, (timestamp, timestamp))

        self.mover.start_batch()
        moved = self.mover.move_file(source, self.root / "Images", sort_by_date=True)
        self.mover.end_batch()

        self.assertEqual(moved, self.root / "Images" / "2024-05" / "photo.jpg")
        self.assertTrue(self.mover.has_history())

        success, errors = self.mover.undo_last_operation()

        self.assertEqual((success, errors), (1, 0))
        self.assertEqual(source.read_bytes(), b"jpg")
        self.assertFalse((self.root / "Images").exists())
        self.assertFalse(self.mover.has_history())

    def test_discard_to_trash_is_undoable(self):
        trash = self.root / "Trash"
        duplicate = self.root / "copy.txt"
        duplicate.write_text("same")
        progress = []

        success, errors = self.mover.discard_files(
            [duplicate], trash, progress_callback=lambda *args: progress.append(args)
        )

        self.assertEqual((success, errors), (1, 0))
        self.assertEqual(progress, [(1, 1, "copy.txt")])
        self.assertTrue((trash / "copy.txt").exists())
        self.assertEqual(self.mover.undo_last_operation(), (1, 0))
        self.assertEqual(duplicate.read_text(), "same")

    def test_permanent_discard_deletes_and_counts_errors(self):
        existing = self.root / "copy.txt"
        existing.write_text("same")
        missing = self.root / "missing.txt"

        success, errors = self.mover.discard_files(
            [existing, missing], self.root / "Trash", permanent=True
        )

        self.assertEqual((success, errors), (1, 1))
        self.assertFalse(existing.exists())
        self.assertFalse((self.root / "Trash").exists())
        self.assertFalse(self.mover.has_history())


if __name__ == "__main__":
    unittest.main()
