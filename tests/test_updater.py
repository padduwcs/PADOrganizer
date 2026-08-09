import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from modules.updater import (
    IntegrityError,
    UpdateError,
    download_installer,
    fetch_latest_release,
    is_newer_version,
    parse_version,
)


class FakeResponse:
    def __init__(self, content, headers=None):
        self._stream = io.BytesIO(content)
        self.headers = headers or {}

    def read(self, size=-1):
        return self._stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class UpdaterTests(unittest.TestCase):
    def test_version_comparison(self):
        self.assertEqual(parse_version("v1.2.3"), (1, 2, 3))
        self.assertTrue(is_newer_version("1.1.0", "1.0.9"))
        self.assertFalse(is_newer_version("1.0.0", "1.0.0"))
        with self.assertRaises(ValueError):
            parse_version("1.0")

    def test_fetch_release_uses_asset_digest(self):
        installer = b"installer"
        digest = hashlib.sha256(installer).hexdigest()
        payload = {
            "tag_name": "v1.2.0",
            "html_url": "https://github.com/padduwcs/PADOrganizer/releases/tag/v1.2.0",
            "body": "Release notes",
            "assets": [
                {
                    "name": "PADOrganizer-Setup-v1.2.0.exe",
                    "browser_download_url": "https://github.com/example/installer.exe",
                    "size": len(installer),
                    "digest": f"sha256:{digest}",
                }
            ],
        }

        def opener(request, timeout=0):
            del request, timeout
            return FakeResponse(json.dumps(payload).encode("utf-8"))

        release = fetch_latest_release(opener=opener)
        self.assertEqual(release.version, "1.2.0")
        self.assertEqual(release.installer_sha256, digest)

    def test_fetch_release_falls_back_to_checksum_manifest(self):
        digest = "a" * 64
        payload = {
            "tag_name": "v1.2.0",
            "html_url": "https://github.com/padduwcs/PADOrganizer/releases/tag/v1.2.0",
            "assets": [
                {
                    "name": "PADOrganizer-Setup-v1.2.0.exe",
                    "browser_download_url": "https://github.com/example/installer.exe",
                    "size": 10,
                },
                {
                    "name": "SHA256SUMS.txt",
                    "browser_download_url": "https://github.com/example/checksums.txt",
                },
            ],
        }
        responses = [
            FakeResponse(json.dumps(payload).encode("utf-8")),
            FakeResponse(f"{digest}  PADOrganizer-Setup-v1.2.0.exe\n".encode("utf-8")),
        ]

        def opener(request, timeout=0):
            del request, timeout
            return responses.pop(0)

        release = fetch_latest_release(opener=opener)
        self.assertEqual(release.installer_sha256, digest)

    def test_fetch_release_requires_installer(self):
        payload = {
            "tag_name": "v1.2.0",
            "html_url": "https://github.com/padduwcs/PADOrganizer/releases/tag/v1.2.0",
            "assets": [],
        }

        def opener(request, timeout=0):
            del request, timeout
            return FakeResponse(json.dumps(payload).encode("utf-8"))

        with self.assertRaises(UpdateError):
            fetch_latest_release(opener=opener)

    def test_download_verifies_checksum(self):
        content = b"valid installer contents"
        digest = hashlib.sha256(content).hexdigest()
        release = type(
            "Release",
            (),
            {
                "installer_name": "PADOrganizer-Setup-v1.2.0.exe",
                "installer_url": "https://github.com/example/installer.exe",
                "installer_size": len(content),
                "installer_sha256": digest,
            },
        )()

        def opener(request, timeout=0):
            del request, timeout
            return FakeResponse(content, {"Content-Length": str(len(content))})

        with tempfile.TemporaryDirectory() as directory:
            path = download_installer(release, opener=opener, destination_dir=directory)
            self.assertEqual(path.read_bytes(), content)

    def test_download_rejects_invalid_checksum(self):
        content = b"tampered installer"
        release = type(
            "Release",
            (),
            {
                "installer_name": "PADOrganizer-Setup-v1.2.0.exe",
                "installer_url": "https://github.com/example/installer.exe",
                "installer_size": len(content),
                "installer_sha256": "0" * 64,
            },
        )()

        def opener(request, timeout=0):
            del request, timeout
            return FakeResponse(content, {"Content-Length": str(len(content))})

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(IntegrityError):
                download_installer(release, opener=opener, destination_dir=directory)
            self.assertFalse(any(Path(directory).glob("*.exe")))


if __name__ == "__main__":
    unittest.main()
