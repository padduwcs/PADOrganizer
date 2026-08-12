import tempfile
import unittest
from pathlib import Path

from modules.config_manager import ConfigManager
from modules.logger import PADLogger
from modules.platform_paths import resolve_application_paths


class PlatformPathTests(unittest.TestCase):
    def test_linux_paths_follow_xdg_environment(self):
        paths = resolve_application_paths(
            platform_name="linux",
            environment={
                "XDG_CONFIG_HOME": "/tmp/pad-config",
                "XDG_DATA_HOME": "/tmp/pad-data",
                "XDG_STATE_HOME": "/tmp/pad-state",
            },
            home="/home/example",
            frozen=True,
            executable="/opt/padorganizer/PADOrganizer",
            bundle_dir="/opt/padorganizer/resources",
        )

        self.assertEqual(paths.config_file, Path("/tmp/pad-config/PADOrganizer/config.json"))
        self.assertEqual(paths.trash_dir, Path("/tmp/pad-data/PADOrganizer/PADOrganizer_Trash"))
        self.assertEqual(paths.log_dir, Path("/tmp/pad-state/PADOrganizer/logs"))
        self.assertEqual(paths.application_dir.name, "padorganizer")

    def test_linux_paths_use_xdg_defaults(self):
        paths = resolve_application_paths(
            platform_name="linux",
            environment={},
            home="/home/example",
            frozen=False,
        )

        self.assertEqual(paths.config_dir, Path("/home/example/.config/PADOrganizer"))
        self.assertEqual(paths.data_dir, Path("/home/example/.local/share/PADOrganizer"))
        self.assertEqual(paths.state_dir, Path("/home/example/.local/state/PADOrganizer"))

    def test_windows_keeps_data_beside_executable(self):
        paths = resolve_application_paths(
            platform_name="win32",
            environment={},
            home="C:/Users/example",
            frozen=True,
            executable="C:/Apps/PADOrganizer/PADOrganizer.exe",
            bundle_dir="C:/Temp/bundle",
        )

        self.assertEqual(paths.config_dir, paths.application_dir)
        self.assertEqual(paths.data_dir, paths.application_dir)
        self.assertEqual(paths.state_dir, paths.application_dir)

    def test_config_and_logger_create_parent_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manager = ConfigManager(config_dir=root / "config")
            manager.set_theme("dark")
            logger = PADLogger(log_dir=root / "state" / "logs")
            logger.log("test")

            self.assertTrue((root / "config" / "config.json").is_file())
            self.assertTrue((root / "state" / "logs" / "activity.log").is_file())


if __name__ == "__main__":
    unittest.main()
