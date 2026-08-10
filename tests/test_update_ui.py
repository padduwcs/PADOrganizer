import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QScrollArea

from main import AppMessageDialog, FittedLabel, MainWindow, UpdateCheckThread
from modules.config_manager import ConfigManager
from modules.i18n import get_language, set_language
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

    def test_theme_and_language_switch_apply_immediately(self):
        with patch.object(ConfigManager, "save_config"):
            window = MainWindow()
            initial_theme = window.current_theme
            window.toggle_theme()
            expected_theme = "dark" if initial_theme == "light" else "light"
            self.assertEqual(window.current_theme, expected_theme)
            self.assertEqual(window.config_manager.get_theme(), expected_theme)
            self.assertEqual(self.app.property("theme"), expected_theme)

            initial_language = get_language()
            window.toggle_language()
            expected_language = "en" if initial_language == "vi" else "vi"
            self.assertEqual(get_language(), expected_language)
            self.assertEqual(window.config_manager.get_language(), expected_language)
            expected_title = (
                "Organize files."
                if expected_language == "en"
                else "Sắp xếp tệp."
            )
            page_titles = [
                label.text()
                for label in window.findChildren(QLabel, "PageTitle")
            ]
            self.assertEqual(page_titles, [expected_title])
            window.close()
        set_language("vi")

    def test_compact_layout_never_overflows_horizontally(self):
        with patch.object(ConfigManager, "save_config"):
            window = MainWindow()
            window.resize(980, 700)
            window.show()
            self.app.processEvents()
            scroll = window.findChild(QScrollArea, "MainScroll")
            self.assertEqual(scroll.horizontalScrollBar().maximum(), 0)

            window.toggle_language()
            self.app.processEvents()
            self.assertEqual(scroll.horizontalScrollBar().maximum(), 0)
            window.close()
        set_language("vi")

    def test_primary_cards_use_short_titles_and_tooltips(self):
        with (
            patch.object(ConfigManager, "save_config"),
            patch.object(ConfigManager, "get_language", return_value="vi"),
        ):
            window = MainWindow()
            card_titles = window.findChildren(QLabel, "CardTitle")
            self.assertEqual(
                [label.text() for label in card_titles],
                ["Chọn thư mục", "Tùy chọn sắp xếp"],
            )
            self.assertTrue(all(not label.wordWrap() for label in card_titles))
            self.assertIn("trực tiếp", card_titles[0].toolTip())
            visible_copy = [label.text() for label in window.findChildren(QLabel)]
            self.assertNotIn(
                "Chỉ các tệp nằm trực tiếp trong thư mục được xử lý.",
                visible_copy,
            )

            window.toggle_language()
            self.assertEqual(
                [label.text() for label in card_titles],
                ["Choose folder", "Organization options"],
            )
            self.assertIn("directly", card_titles[0].toolTip())
            window.close()
        set_language("vi")

    def test_folder_metric_fits_in_both_languages(self):
        with (
            patch.object(ConfigManager, "save_config"),
            patch.object(ConfigManager, "get_language", return_value="vi"),
        ):
            window = MainWindow()
            window.show()
            self.app.processEvents()
            value = window.hero_folder_value
            self.assertIsInstance(value, FittedLabel)

            for expected_text in ("Chưa chọn", "Not selected"):
                self.assertEqual(value.text(), expected_text)
                fitted_width = QFontMetrics(value.fitted_font()).horizontalAdvance(value.text())
                self.assertLessEqual(fitted_width, value.contentsRect().width())
                window.toggle_language()
                self.app.processEvents()

            window.close()
        set_language("vi")


if __name__ == "__main__":
    unittest.main()
