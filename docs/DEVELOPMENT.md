# Phát triển PADOrganizer

Tài liệu này dành cho người muốn chạy từ mã nguồn, chỉnh sửa hoặc phát hành PADOrganizer. Người dùng thông thường chỉ cần làm theo [README](../README.md).

## Chạy từ mã nguồn

Yêu cầu Python 3.9 trở lên.

```powershell
git clone https://github.com/padduwcs/PADOrganizer.git
cd PADOrganizer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Trên macOS hoặc Linux, kích hoạt môi trường bằng:

```bash
source .venv/bin/activate
```

## Đóng gói cho Windows

Tạo `dist/PADOrganizer.exe`:

```bat
build.bat
```

Script ưu tiên Python trong `.venv` hoặc `venv`, sau đó mới tìm Python đã cài trên hệ thống.

## Tạo Installer và bộ phát hành

Cài [Inno Setup 6](https://jrsoftware.org/isdl.php), sau đó chạy:

```bat
build_release.bat 1.0.0
```

Kết quả trong `release/` gồm:

```text
PADOrganizer-Setup-v1.0.0.exe
PADOrganizer-portable-v1.0.0.exe
SHA256SUMS.txt
```

Nếu đã có `dist/PADOrganizer.exe` và chỉ cần tạo installer:

```bat
build_installer.bat 1.0.0
```

Installer cài theo từng người dùng vào `%LOCALAPPDATA%\Programs\PADOrganizer` và không yêu cầu quyền Administrator.

## Phát hành trên GitHub

Workflow `.github/workflows/release.yml` tự động build và tạo GitHub Release khi có tag dạng `vX.Y.Z`:

```bash
git tag -a v1.0.1 -m "PADOrganizer v1.0.1"
git push origin main
git push origin v1.0.1
```

Mỗi bản phát hành phải sử dụng một số phiên bản và tag mới. Có thể chạy workflow thủ công từ tab **Actions** để kiểm tra artefact mà không tạo Release.

## Cấu trúc chính

```text
PADOrganizer/
├── main.py                    # Giao diện và luồng ứng dụng
├── modules/                   # Phân loại, cấu hình, log và tìm tệp trùng
├── installer/PADOrganizer.iss # Cấu hình Inno Setup
├── scripts/New-Checksums.ps1  # Tạo mã SHA-256
├── PADOrganizer.spec          # Cấu hình PyInstaller
├── build.bat                  # Build bản portable
├── build_installer.bat        # Build installer
└── build_release.bat          # Build toàn bộ artefact phát hành
```

`config.json`, `logs/`, `PADOrganizer_Trash/`, `build/`, `dist/` và `release/` là dữ liệu sinh ra khi chạy hoặc build, không được đưa vào Git.
