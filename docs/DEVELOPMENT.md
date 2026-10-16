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

## Kiểm tra mã nguồn

`requirements-dev.txt` cài sẵn `ruff`. Cấu hình trong `ruff.toml` chỉ bắt lỗi thật (cú pháp, tên chưa định nghĩa, import thừa) và không thay đổi định dạng mã:

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
```

GitHub Actions chạy bước này trước khi build bản phát hành.

## Quy tắc an toàn khi xử lý tệp

Mọi thao tác sắp xếp và tìm tệp trùng đều lấy danh sách tệp qua `modules/safety.py`:

- Chỉ xử lý tệp nằm trực tiếp trong thư mục đã chọn; bỏ qua thư mục con, symlink, tệp bắt đầu bằng `.` và tệp có thuộc tính Hidden/System trên Windows.
- Bỏ qua chính file chương trình đang chạy cùng `config.json`/`activity.log` cũ.
- Không cho chọn thư mục ứng dụng, thư mục gốc của ổ đĩa, thư mục Home và thư mục hệ thống (`C:\Windows`, `Program Files`, `ProgramData`, `/usr`, `/etc`…).
- Tìm tệp trùng chỉ băm những tệp có cùng kích thước và bỏ qua tệp 0 byte.

Khi thêm tính năng mới có động tới tệp người dùng, hãy dùng lại `list_candidate_files` thay vì tự duyệt thư mục.

## Đóng gói Windows

Tạo `dist/PADOrganizer.exe`:

```bat
build.bat
```

Để tạo Installer và bản portable, cài Inno Setup 6 rồi chạy:

```bat
build_release.bat 1.3.0
```

Kết quả:

```text
release/PADOrganizer-Setup-v1.3.0.exe
release/PADOrganizer-portable-v1.3.0.exe
release/SHA256SUMS.txt
```

Installer cài theo từng người dùng vào `%LOCALAPPDATA%\Programs\PADOrganizer` và không yêu cầu quyền Administrator.

## Đóng gói Linux

Linux artifact phải được build trên Linux; PyInstaller không cross-compile từ Windows. Script hỗ trợ Ubuntu 22.04 trở lên và tạo cả DEB lẫn AppImage cho `x86_64`:

```bash
APPIMAGETOOL=/path/to/appimagetool-x86_64.AppImage \
  bash scripts/build_linux.sh 1.3.0
```

Máy build cần `dpkg-deb`, `appimagetool` và các thư viện runtime Qt được khai báo trong `packaging/linux/debian/control`. GitHub Actions tự chuẩn bị toàn bộ môi trường này.

Kết quả:

```text
release/padorganizer_1.3.0_amd64.deb
release/PADOrganizer-v1.3.0-x86_64.AppImage
release/SHA256SUMS.txt
```

Kiểm tra nhanh executable đã đóng gói:

```bash
xvfb-run -a dist/PADOrganizer/PADOrganizer --smoke-test
```

## Logo và icon

`assets/logo.png` (1024×1024, nền trong suốt) là ảnh gốc của mọi icon. Sau khi thay logo, tạo lại icon bằng:

```bash
python -m pip install pillow
python scripts/build_icons.py
```

Script ghi đè `logo.ico` (Windows), `assets/padorganizer.png` (256 px, Linux và logo trong giao diện) và `assets/padorganizer-512.png` (Linux HiDPI). `assets/banner.png` dùng cho README; `assets/social-preview.png` (1280×640) dùng làm ảnh xem trước khi chia sẻ liên kết, tải lên tại **Settings → General → Social preview** của repository.

## Tích hợp liên tục

`.github/workflows/ci.yml` chạy `ruff` và toàn bộ test trên Windows lẫn Ubuntu cho mỗi lần push lên `main` và mỗi Pull Request.

## Phiên bản và phát hành

Trước khi phát hành:

1. Cập nhật `APP_VERSION` trong `version.py`.
2. Thêm mục `## [X.Y.Z] - YYYY-MM-DD` vào đầu [CHANGELOG.md](../CHANGELOG.md). Nội dung mục này trở thành ghi chú phát hành trên GitHub và hiển thị trong hộp thoại **Có gì mới** của ứng dụng.

Script sẽ từ chối build nếu phiên bản truyền vào không khớp `version.py`, và test sẽ báo lỗi nếu CHANGELOG thiếu mục cho phiên bản hiện tại:

```bash
python scripts/check_version.py 1.3.0
python scripts/release_notes.py 1.3.0 release-notes.md
```

Workflow `.github/workflows/release.yml` có ba giai đoạn:

1. Kiểm tra version từ tag hoặc input thủ công, rồi chạy lint.
2. Build và test độc lập trên Windows và Ubuntu 22.04; AppImage và gói DEB đều được chạy smoke test sau khi đóng gói.
3. Gộp bốn artifact, tạo một `SHA256SUMS.txt`, lấy ghi chú từ CHANGELOG rồi xuất bản GitHub Release.

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
├── assets/logo.png                 # Logo gốc, nguồn để tạo mọi icon
├── assets/                         # Icon PNG, banner README và ảnh social preview
├── docs/images/                    # Ảnh chụp màn hình cho README
├── installer/PADOrganizer.iss      # Inno Setup cho Windows
├── packaging/linux/                # Desktop entry, launcher và metadata DEB
├── modules/safety.py               # Bộ lọc tệp và thư mục được phép xử lý
├── scripts/build_icons.py          # Tạo logo.ico và icon PNG từ assets/logo.png
├── scripts/build_linux.sh          # Build DEB và AppImage
├── scripts/check_version.py        # Kiểm tra version đa nền tảng
├── scripts/new_checksums.py        # Tạo manifest SHA-256 đa nền tảng
├── scripts/release_notes.py        # Lấy ghi chú phát hành từ CHANGELOG.md
├── CHANGELOG.md                    # Nhật ký thay đổi theo phiên bản
├── ruff.toml                       # Cấu hình lint
├── PADOrganizer.spec               # PyInstaller one-file cho Windows
├── PADOrganizer-linux.spec         # PyInstaller one-dir cho Linux
├── build.bat                       # Build Windows portable
├── build_installer.bat             # Build Windows Installer
└── build_release.bat               # Build bộ phát hành Windows
```

`config.json`, `logs/`, `PADOrganizer_Trash/`, `build/`, `dist/` và `release/` là dữ liệu sinh ra khi chạy hoặc build, không được đưa vào Git.
