import os
import sys
import tempfile
import unittest
from pathlib import Path

from modules.safety import classify_target_directory, is_hidden_or_system, list_candidate_files


def _set_windows_hidden(path):
    import ctypes

    FILE_ATTRIBUTE_HIDDEN = 0x2
    if not ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN):
        raise OSError("SetFileAttributesW failed")


class CandidateFileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def names(self, **kwargs):
        return sorted(path.name for path in list_candidate_files(self.root, **kwargs))

    def test_lists_only_visible_direct_files(self):
        (self.root / "photo.jpg").write_bytes(b"jpg")
        (self.root / ".bashrc").write_text("export PATH")
        (self.root / "config.json").write_text("{}")
        (self.root / "activity.log").write_text("log")
        (self.root / "Nested").mkdir()
        (self.root / "Nested" / "inner.txt").write_text("inner")

        self.assertEqual(self.names(), ["photo.jpg"])

    def test_excluded_paths_are_skipped(self):
        keep = self.root / "keep.txt"
        skip = self.root / "PADOrganizer.exe"
        keep.write_text("keep")
        skip.write_bytes(b"MZ")

        self.assertEqual(self.names(excluded_paths=[skip]), ["keep.txt"])

    def test_symlinks_are_skipped(self):
        target = self.root / "real.txt"
        target.write_text("real")
        try:
            os.symlink(target, self.root / "link.txt")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks are not available for this user")

        self.assertEqual(self.names(), ["real.txt"])

    @unittest.skipUnless(sys.platform == "win32", "Windows file attributes")
    def test_windows_hidden_attribute_is_skipped(self):
        hidden = self.root / "desktop.ini"
        hidden.write_text("[.ShellClassInfo]")
        _set_windows_hidden(hidden)
        (self.root / "visible.txt").write_text("visible")

        self.assertTrue(is_hidden_or_system(hidden))
        self.assertEqual(self.names(), ["visible.txt"])

    def test_dotfiles_are_hidden_on_every_platform(self):
        self.assertTrue(is_hidden_or_system(Path(".profile"), platform_name="linux"))
        self.assertFalse(is_hidden_or_system(Path("report.pdf"), platform_name="linux"))


class TargetDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home" / "user"
        self.home.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def classify(self, path, platform_name="linux", environment=None, protected=()):
        return classify_target_directory(
            path,
            protected,
            platform_name=platform_name,
            environment=environment or {},
            home=self.home,
        )

    def test_regular_user_folder_is_allowed(self):
        downloads = self.home / "Downloads"
        downloads.mkdir()
        self.assertIsNone(self.classify(downloads))

    def test_app_directories_are_protected(self):
        app_dir = self.root / "app"
        app_dir.mkdir()
        self.assertEqual(self.classify(app_dir, protected=[app_dir]), "protected")

    def test_drive_root_and_home_are_system(self):
        self.assertEqual(self.classify(Path(self.root.anchor)), "system")
        self.assertEqual(self.classify(self.home), "system")

    def test_posix_system_trees_are_blocked_with_descendants(self):
        self.assertEqual(self.classify(Path("/usr/lib/python3")), "system")
        self.assertEqual(self.classify(Path("/var")), "system")
        self.assertIsNone(self.classify(Path("/var/www/site")))

    def test_windows_system_folders_come_from_environment(self):
        windows_dir = self.root / "Windows"
        program_files = self.root / "Program Files"
        environment = {"SystemRoot": str(windows_dir), "ProgramFiles": str(program_files)}

        self.assertEqual(
            self.classify(windows_dir / "System32", "win32", environment), "system"
        )
        self.assertEqual(self.classify(program_files, "win32", environment), "system")
        self.assertIsNone(self.classify(self.root / "Photos", "win32", environment))


if __name__ == "__main__":
    unittest.main()
