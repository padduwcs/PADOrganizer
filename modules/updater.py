import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from version import APP_VERSION


LATEST_RELEASE_API = "https://api.github.com/repos/padduwcs/PADOrganizer/releases/latest"
RELEASES_URL = "https://github.com/padduwcs/PADOrganizer/releases/latest"
API_VERSION = "2026-03-10"
REQUEST_TIMEOUT = 20
INSTALL_MARKER = "installed.marker"
_VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


class UpdateError(Exception):
    """An update could not be checked or prepared safely."""


class IntegrityError(UpdateError):
    """The downloaded installer did not match its published SHA-256."""


@dataclass(frozen=True)
class ReleaseInfo:
    version: str
    notes: str
    page_url: str
    installer_name: str
    installer_url: str
    installer_size: int
    installer_sha256: str


def parse_version(value):
    match = _VERSION_PATTERN.fullmatch(str(value).strip())
    if not match:
        raise ValueError(f"Phiên bản không hợp lệ: {value}")
    return tuple(int(part) for part in match.groups())


def is_newer_version(candidate, current=APP_VERSION):
    return parse_version(candidate) > parse_version(current)


def is_installed_build():
    if not getattr(sys, "frozen", False):
        return False
    base_dir = Path(sys.executable).resolve().parent
    return (base_dir / INSTALL_MARKER).is_file() or any(base_dir.glob("unins*.exe"))


def _request(url):
    return Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"PADOrganizer/{APP_VERSION}",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )


def _validate_github_url(url):
    parsed = urlparse(str(url))
    if parsed.scheme != "https" or parsed.hostname not in {"github.com", "api.github.com"}:
        raise UpdateError("GitHub trả về một đường dẫn tải xuống không hợp lệ.")
    return str(url)


def _friendly_network_error(exc):
    if isinstance(exc, HTTPError):
        if exc.code in {403, 429}:
            return UpdateError("GitHub đang giới hạn yêu cầu. Vui lòng thử lại sau.")
        if exc.code == 404:
            return UpdateError("Chưa tìm thấy bản phát hành công khai trên GitHub.")
        return UpdateError(f"GitHub phản hồi lỗi HTTP {exc.code}.")
    if isinstance(exc, URLError):
        return UpdateError("Không thể kết nối GitHub. Hãy kiểm tra Internet và thử lại.")
    if isinstance(exc, TimeoutError):
        return UpdateError("Kết nối GitHub quá thời gian chờ. Vui lòng thử lại.")
    return UpdateError("Không thể hoàn tất kết nối cập nhật.")


def _read_url(url, opener, timeout=REQUEST_TIMEOUT):
    try:
        with opener(_request(url), timeout=timeout) as response:
            return response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise _friendly_network_error(exc) from exc


def _checksum_from_manifest(content, installer_name):
    for raw_line in content.decode("utf-8-sig", errors="replace").splitlines():
        parts = raw_line.strip().split(None, 1)
        if len(parts) != 2:
            continue
        digest, filename = parts
        filename = filename.lstrip("*").strip()
        if filename == installer_name and re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            return digest.lower()
    return ""


def fetch_latest_release(opener=None, timeout=REQUEST_TIMEOUT):
    opener = opener or urlopen
    try:
        payload = json.loads(_read_url(LATEST_RELEASE_API, opener, timeout).decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise UpdateError("GitHub trả về dữ liệu phiên bản không hợp lệ.") from exc

    tag_name = str(payload.get("tag_name", ""))
    try:
        parse_version(tag_name)
    except ValueError as exc:
        raise UpdateError("Bản phát hành mới nhất không có số phiên bản hợp lệ.") from exc

    version = tag_name.lstrip("v")
    installer_name = f"PADOrganizer-Setup-v{version}.exe"
    assets = payload.get("assets") or []
    installer = next((asset for asset in assets if asset.get("name") == installer_name), None)
    if installer is None:
        raise UpdateError(f"Bản phát hành v{version} chưa có file Installer phù hợp.")

    installer_url = _validate_github_url(installer.get("browser_download_url", ""))
    digest_value = str(installer.get("digest") or "")
    installer_sha256 = ""
    if digest_value.lower().startswith("sha256:"):
        candidate = digest_value.split(":", 1)[1]
        if re.fullmatch(r"[0-9a-fA-F]{64}", candidate):
            installer_sha256 = candidate.lower()

    if not installer_sha256:
        checksum_asset = next(
            (asset for asset in assets if asset.get("name") == "SHA256SUMS.txt"),
            None,
        )
        if checksum_asset is not None:
            checksum_url = _validate_github_url(checksum_asset.get("browser_download_url", ""))
            installer_sha256 = _checksum_from_manifest(
                _read_url(checksum_url, opener, timeout), installer_name
            )

    if not installer_sha256:
        raise UpdateError("Không tìm thấy mã SHA-256 để xác minh Installer.")

    page_url = _validate_github_url(payload.get("html_url", RELEASES_URL))
    return ReleaseInfo(
        version=version,
        notes=str(payload.get("body") or "Không có ghi chú cho phiên bản này."),
        page_url=page_url,
        installer_name=installer_name,
        installer_url=installer_url,
        installer_size=int(installer.get("size") or 0),
        installer_sha256=installer_sha256,
    )


def _clean_old_downloads(update_dir, keep_name):
    for pattern in ("*.part", "PADOrganizer-Setup-v*.exe"):
        for path in update_dir.glob(pattern):
            if path.name == keep_name:
                continue
            try:
                path.unlink()
            except OSError:
                pass


def download_installer(release, progress_callback=None, opener=None, destination_dir=None):
    opener = opener or urlopen
    update_dir = Path(destination_dir or Path(tempfile.gettempdir()) / "PADOrganizer" / "updates")
    update_dir.mkdir(parents=True, exist_ok=True)
    destination = update_dir / release.installer_name
    partial = destination.with_suffix(destination.suffix + ".part")
    _clean_old_downloads(update_dir, destination.name)

    hasher = hashlib.sha256()
    downloaded = 0
    try:
        with opener(_request(release.installer_url), timeout=REQUEST_TIMEOUT) as response:
            total = int(response.headers.get("Content-Length") or release.installer_size or 0)
            with open(partial, "wb") as output:
                while True:
                    chunk = response.read(1024 * 256)
                    if not chunk:
                        break
                    output.write(chunk)
                    hasher.update(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)
    except (HTTPError, URLError, TimeoutError) as exc:
        try:
            partial.unlink()
        except OSError:
            pass
        raise _friendly_network_error(exc) from exc
    except OSError as exc:
        try:
            partial.unlink()
        except OSError:
            pass
        raise UpdateError("Không thể lưu Installer vào thư mục tạm của Windows.") from exc

    actual_sha256 = hasher.hexdigest().lower()
    if actual_sha256 != release.installer_sha256.lower():
        try:
            partial.unlink()
        except OSError:
            pass
        raise IntegrityError("Installer tải xuống không khớp mã SHA-256 và đã bị loại bỏ.")

    try:
        partial.replace(destination)
    except OSError as exc:
        raise UpdateError("Không thể hoàn tất file Installer đã tải.") from exc
    return destination


def launch_installer(installer_path):
    path = Path(installer_path).resolve()
    if sys.platform != "win32" or not path.is_file():
        raise UpdateError("Không thể mở Installer đã tải trên thiết bị này.")
    try:
        subprocess.Popen(
            [str(path), "/CLOSEAPPLICATIONS", "/NORESTART", "/NORESTARTAPPLICATIONS"],
            close_fds=True,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
    except OSError as exc:
        raise UpdateError("Windows không thể khởi chạy Installer đã tải.") from exc
