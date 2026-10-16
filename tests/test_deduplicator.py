import tempfile
import unittest
from pathlib import Path

from modules.deduplicator import Deduplicator


class DeduplicatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.root / name
        path.write_bytes(content)
        return path

    def groups(self):
        return [sorted(path.name for path in group) for group in Deduplicator().find_duplicates(self.root)]

    def test_identical_files_are_grouped(self):
        self.write("a.txt", b"same content")
        self.write("b.txt", b"same content")
        self.write("c.txt", b"other")

        self.assertEqual(self.groups(), [["a.txt", "b.txt"]])

    def test_same_size_but_different_content_is_not_duplicate(self):
        self.write("a.bin", b"aaaa")
        self.write("b.bin", b"bbbb")

        self.assertEqual(self.groups(), [])

    def test_empty_files_are_ignored(self):
        self.write("empty1.txt", b"")
        self.write("empty2.txt", b"")

        self.assertEqual(self.groups(), [])

    def test_hidden_files_are_ignored(self):
        self.write("visible.txt", b"same")
        self.write(".hidden.txt", b"same")

        self.assertEqual(self.groups(), [])

    def test_only_size_matches_are_hashed(self):
        self.write("unique.txt", b"one of a kind")
        self.write("a.txt", b"dup")
        self.write("b.txt", b"dup")
        progress = []

        Deduplicator().find_duplicates(self.root, lambda *args: progress.append(args))

        self.assertEqual(len(progress), 2)
        self.assertEqual(progress[-1][:2], (2, 2))


if __name__ == "__main__":
    unittest.main()
