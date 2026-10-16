import json
import tempfile
import unittest
from pathlib import Path

from modules.config_manager import DEFAULT_CONFIG, ConfigManager, sanitize_config


class ConfigManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp.name)
        self.config_path = self.config_dir / "config.json"

    def tearDown(self):
        self.temp.cleanup()

    def write_raw(self, text):
        self.config_path.write_text(text, encoding="utf-8")

    def test_round_trip_keeps_custom_rules(self):
        manager = ConfigManager(config_dir=self.config_dir)
        manager.set_file_map({"Photos": [".jpg"]})
        manager.set_theme("dark")

        reloaded = ConfigManager(config_dir=self.config_dir)

        self.assertEqual(reloaded.get_file_map(), {"Photos": [".jpg"]})
        self.assertEqual(reloaded.get_theme(), "dark")
        self.assertEqual(list(self.config_dir.glob("*.tmp")), [])

    def test_non_object_json_falls_back_to_defaults(self):
        self.write_raw("[1, 2, 3]")
        manager = ConfigManager(config_dir=self.config_dir)

        self.assertEqual(manager.get_file_map(), DEFAULT_CONFIG["file_map"])
        self.assertFalse(manager.is_sort_by_date_enabled())

    def test_corrupt_json_is_backed_up(self):
        self.write_raw('{"file_map": {"Photos": [".jpg"]')
        manager = ConfigManager(config_dir=self.config_dir)

        self.assertEqual(manager.get_file_map(), DEFAULT_CONFIG["file_map"])
        backup = self.config_dir / "config.json.broken"
        self.assertTrue(backup.exists())
        self.assertIn("Photos", backup.read_text(encoding="utf-8"))

    def test_invalid_values_are_replaced_and_extensions_normalized(self):
        self.write_raw(
            json.dumps(
                {
                    "file_map": {"Photos": ["JPG", ".Png", ".png", 7], "Broken": "jpg", "": [".x"]},
                    "sort_by_date": "yes",
                    "theme": "neon",
                    "language": "en",
                    "custom": 1,
                }
            )
        )
        manager = ConfigManager(config_dir=self.config_dir)

        self.assertEqual(manager.get_file_map(), {"Photos": [".jpg", ".png"]})
        self.assertFalse(manager.is_sort_by_date_enabled())
        self.assertEqual(manager.get_theme(), "light")
        self.assertEqual(manager.get_language(), "en")
        self.assertEqual(manager.config["custom"], 1)

    def test_empty_file_map_uses_defaults(self):
        config = sanitize_config({"file_map": {}})
        self.assertEqual(config["file_map"], DEFAULT_CONFIG["file_map"])


if __name__ == "__main__":
    unittest.main()
