import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton

from main import AppMessageDialog, MainWindow, UpdateCheckThread
from version import APP_VERSION


class UpdateUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_update_check_is_manual_and_displays_version(self):
        with patch.object(UpdateCheckThread, "start") as start:
            window = MainWindow()
            self.assertIsNone(window.pending_update_release)
            start.assert_not_called()

            version_label = window.findChild(QLabel, "VersionLabel")
            self.assertIsNotNone(version_label)
            self.assertIn(APP_VERSION, version_label.text())

            window.btn_check_updates.click()
            start.assert_called_once()
            window.is_busy = False
            window.close()

    def test_custom_message_dialog_uses_localized_actions(self):
        dialog = AppMessageDialog(
            "Bảo trì dữ liệu",
            "Xóa toàn bộ nhật ký hoạt động?",
            "Nội dung xác nhận.",
            "Xóa nhật ký",
            "Giữ lại",
            variant="danger",
        )
        buttons = {button.text(): button for button in dialog.findChildren(QPushButton)}
        self.assertIn("Xóa nhật ký", buttons)
        self.assertIn("Giữ lại", buttons)
        self.assertEqual(buttons["Xóa nhật ký"].objectName(), "MessageDanger")
        self.assertTrue(dialog.windowFlags() & Qt.WindowType.FramelessWindowHint)
        dialog.close()


if __name__ == "__main__":
    unittest.main()
