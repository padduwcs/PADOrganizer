import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

import main
from main import DedupeDialog, MainWindow


class _MemoryLogger:
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

    def has_logs(self):
        return bool(self.messages)


class CleanupUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.window = MainWindow()
        self.window.logger = _MemoryLogger()

    def tearDown(self):
        self.window.is_busy = False
        self.window.close()
        self.temp.cleanup()

    def test_home_folder_is_rejected(self):
        with patch.object(main.QMessageBox, "warning") as warning:
            self.window.set_target_directory(str(Path.home()))

        warning.assert_called_once()
        self.assertEqual(self.window.target_dir, "")

    def test_dialog_returns_selection_without_touching_files(self):
        first = self.root / "a.txt"
        second = self.root / "copy_of_a.txt"
        first.write_text("same")
        second.write_text("same")

        dialog = DedupeDialog([[first, second]], self.window)
        with patch.object(main.QMessageBox, "question", return_value=main.QMessageBox.StandardButton.Yes):
            dialog.process_deletion(permanent=False)

        self.assertEqual(dialog.files_to_remove, [second])
        self.assertFalse(dialog.permanent)
        self.assertTrue(second.exists())

    def test_cleanup_runs_in_background_and_is_undoable(self):
        duplicate = self.root / "copy.txt"
        duplicate.write_text("same")
        trash = self.root / "Trash"

        with patch.object(main, "PAD_TRASH_DIR", trash), \
                patch.object(main.QMessageBox, "information") as information:
            self.window.run_cleanup([duplicate], permanent=False)
            self.assertTrue(self.window.is_busy)
            self.assertTrue(self.window.cleanup_worker.wait(5000))
            self.app.processEvents()

            information.assert_called_once()

        self.assertFalse(self.window.is_busy)
        self.assertFalse(duplicate.exists())
        self.assertTrue((trash / "copy.txt").exists())
        self.assertTrue(self.window.btn_undo.isEnabled())
        self.assertEqual(self.window.mover.undo_last_operation(), (1, 0))
        self.assertTrue(duplicate.exists())


if __name__ == "__main__":
    unittest.main()
