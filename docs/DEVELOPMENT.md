# Phát triển PADOrganizer

Tài liệu này dành cho người muốn chạy từ mã nguồn, chỉnh sửa hoặc phát hành PADOrganizer. Người dùng thông thường chỉ cần làm theo [README](../README.md).

## Chạy từ mã nguồn

Yêu cầu Python 3.9 trở lên.

### Windows

```powershell
git clone https://github.com/padduwcs/PADOrganizer.git
cd PADOrganizer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

### Linux

```bash
git clone https://github.com/padduwcs/PADOrganizer.git
cd PADOrganizer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Khi chạy trên Linux, cấu hình, log và thùng rác nội bộ được ghi vào các thư mục XDG của người dùng, không ghi vào repository.

## Kiểm thử

```bash
python -m unittest discover -s tests -v
```

Trong máy không có display server:

```bash
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -v
```

## Đóng gói Windows

Tạo `dist/PADOrganizer.exe`:

```bat
build.bat
```

Để tạo Installer và bản portable, cài Inno Setup 6 rồi chạy:

```bat
build_release.bat 1.2.0
```

Kết quả:

```text
release/PADOrganizer-Setup-v1.2.0.exe
release/PADOrganizer-portable-v1.2.0.exe
release/SHA256SUMS.txt
```

Installer cài theo từng người dùng vào `%LOCALAPPDATA%\Programs\PADOrganizer` và không yêu cầu quyền Administrator.

## Đóng gói Linux

Linux artifact phải được build trên Linux; PyInstaller không cross-compile từ Windows. Script hỗ trợ Ubuntu 22.04 trở lên và tạo cả DEB lẫn AppImage cho `x86_64`:

```bash
APPIMAGETOOL=/path/to/appimagetool-x86_64.AppImage \
  bash scripts/build_linux.sh 1.2.0
```

Máy build cần `dpkg-deb`, `appimagetool` và các thư viện runtime Qt được khai báo trong `packaging/linux/debian/control`. GitHub Actions tự chuẩn bị toàn bộ môi trường này.

Kết quả:

```text
release/padorganizer_1.2.0_amd64.deb
release/PADOrganizer-v1.2.0-x86_64.AppImage
release/SHA256SUMS.txt
```

Kiểm tra nhanh executable đã đóng gói:

```bash
xvfb-run -a dist/PADOrganizer/PADOrganizer --smoke-test
```

## Phiên bản và phát hành

Trước khi build, cập nhật `APP_VERSION` trong `version.py`. Script sẽ từ chối build nếu phiên bản truyền vào không khớp:

```bash
python scripts/check_version.py 1.2.0
```

Workflow `.github/workflows/release.yml` có ba giai đoạn:

1. Kiểm tra version từ tag hoặc input thủ công.
2. Build và test độc lập trên Windows và Ubuntu 22.04; AppImage và gói DEB đều được chạy smoke test sau khi đóng gói.
3. Gộp bốn artifact, tạo một `SHA256SUMS.txt`, rồi xuất bản GitHub Release.

Chạy workflow thủ công từ tab **Actions** chỉ tạo artifact thử nghiệm, không tạo Release. Khi đã kiểm tra xong, phát hành bằng tag mới:

```bash
git tag -a v1.3.0 -m "PADOrganizer v1.3.0"
git push origin main
git push origin v1.3.0
```

Mỗi Release gồm:

```text
PADOrganizer-Setup-v1.3.0.exe
PADOrganizer-portable-v1.3.0.exe
padorganizer_1.3.0_amd64.deb
PADOrganizer-v1.3.0-x86_64.AppImage
SHA256SUMS.txt
```

## Cấu trúc phát hành

```text
PADOrganizer/
├── assets/                         # Icon bitmap dùng trên Linux
├── installer/PADOrganizer.iss      # Inno Setup cho Windows
├── packaging/linux/                # Desktop entry, launcher và metadata DEB
├── scripts/build_linux.sh          # Build DEB và AppImage
├── scripts/check_version.py        # Kiểm tra version đa nền tảng
├── scripts/new_checksums.py        # Tạo manifest SHA-256 đa nền tảng
├── PADOrganizer.spec               # PyInstaller one-file cho Windows
├── PADOrganizer-linux.spec         # PyInstaller one-dir cho Linux
├── build.bat                       # Build Windows portable
├── build_installer.bat             # Build Windows Installer
└── build_release.bat               # Build bộ phát hành Windows
```

`config.json`, `logs/`, `PADOrganizer_Trash/`, `build/`, `dist/` và `release/` là dữ liệu sinh ra khi chạy hoặc build, không được đưa vào Git.
