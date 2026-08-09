# PADOrganizer

**Personal Archive Directory Organizer** — ứng dụng desktop giúp phân loại, sắp xếp và dọn dẹp tệp cá nhân bằng Python và PyQt6.

![PADOrganizer logo](logo.ico)

## Tính năng

- Tự động phân loại tệp vào các thư mục như `Images`, `Documents`, `Videos` theo quy tắc có thể tùy chỉnh.
- Tùy chọn sắp xếp tiếp theo mốc `Năm-Tháng`, ví dụ `Images/2026-05`.
- Giao diện desktop trực quan với tiến trình xử lý rõ ràng.
- Hoàn tác đợt di chuyển gần nhất và tự động dọn thư mục rỗng.
- Tìm tệp trùng lặp theo nội dung, cho phép chọn bản cần giữ.
- Chuyển tệp vào thùng rác nội bộ `PADOrganizer_Trash` để có thể lấy lại, hoặc xóa vĩnh viễn khi người dùng xác nhận.
- Chỉnh sửa quy tắc phân loại ngay trong giao diện.

## Trải nghiệm sử dụng

- Dashboard mới tập trung toàn bộ quy trình vào một màn hình, với hành động chính và trạng thái xử lý luôn rõ ràng.
- Kéo thả thư mục trực tiếp hoặc nhấn `Chọn thư mục`; số lượng tệp và tổng dung lượng được hiển thị tức thời.
- Bộ quy tắc dạng bảng hỗ trợ thêm, chỉnh sửa, xóa, kiểm tra phần mở rộng trùng và khôi phục mặc định.
- Màn hình xử lý bản trùng cho biết tệp sẽ bị tác động và dung lượng có thể giải phóng trước khi xác nhận.
- Mọi thao tác và nhật ký diễn ra cục bộ; người dùng có thể xóa nhật ký bất cứ lúc nào từ mục `Bảo trì`.

Phím tắt:

| Phím | Thao tác |
|---|---|
| `Ctrl+O` | Chọn thư mục |
| `Ctrl+Enter` | Tổ chức thư mục |
| `Ctrl+D` | Tìm tệp trùng |
| `Ctrl+Z` | Hoàn tác |
| `Ctrl+,` | Mở quy tắc phân loại |

## Tải và sử dụng trên Windows

Trong trang [Releases](https://github.com/padduwcs/PADOrganizer/releases), mỗi phiên bản cung cấp hai lựa chọn:

- `PADOrganizer-Setup-vX.Y.Z.exe`: bản cài đặt được khuyên dùng. Installer tạo shortcut và thêm PADOrganizer vào danh sách ứng dụng có thể gỡ cài đặt của Windows.
- `PADOrganizer-portable-vX.Y.Z.exe`: bản chạy trực tiếp, không cần cài đặt. Nên đặt tệp trong một thư mục riêng có quyền ghi thay vì chạy lâu dài từ `Downloads`.

Ứng dụng đã đóng gói không yêu cầu người dùng cài Python. Lần đầu tải về, Windows có thể hiển thị cảnh báo SmartScreen vì tệp phát hành chưa có chữ ký số. Chỉ tiếp tục nếu tệp được tải từ repository chính thức và mã SHA-256 khớp với `SHA256SUMS.txt` trong cùng bản phát hành.

Dữ liệu cục bộ gồm `config.json`, `logs/` và `PADOrganizer_Trash/` nằm cạnh ứng dụng. Cài phiên bản mới vào cùng vị trí sẽ giữ nguyên các dữ liệu này. Trình gỡ cài đặt cũng không tự động xóa dữ liệu do người dùng tạo; người dùng có thể xóa thư mục cài đặt còn lại nếu không muốn giữ chúng.

## Chạy từ mã nguồn

Yêu cầu Python 3.9 trở lên.

```bash
git clone https://github.com/padduwcs/PADOrganizer.git
cd PADOrganizer
python -m venv .venv
```

Kích hoạt môi trường ảo:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Cài thư viện và chạy ứng dụng:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Đóng gói cho Windows

### Bản portable

Chạy:

```bat
build.bat
```

Hoặc đóng gói thủ công:

```bash
python -m pip install -r requirements-dev.txt
python -m PyInstaller --clean PADOrganizer.spec
```

Tệp thực thi được tạo tại `dist/PADOrganizer.exe`.

### Installer và bộ tệp phát hành

Cài [Inno Setup 6](https://jrsoftware.org/isdl.php), sau đó chạy:

```bat
build_release.bat 1.0.0
```

Script sẽ tạo trong thư mục `release/`:

```text
PADOrganizer-Setup-v1.0.0.exe
PADOrganizer-portable-v1.0.0.exe
SHA256SUMS.txt
```

Nếu đã có `dist/PADOrganizer.exe` và chỉ muốn tạo installer:

```bat
build_installer.bat 1.0.0
```

Installer mặc định cài vào `%LOCALAPPDATA%\Programs\PADOrganizer`, không yêu cầu quyền Administrator. Lựa chọn này phù hợp với cách ứng dụng hiện lưu cấu hình và dữ liệu cạnh tệp thực thi.

## Phát hành trên GitHub

Workflow `.github/workflows/release.yml` tự động build trên Windows và tạo GitHub Release khi đẩy một tag có dạng `vX.Y.Z`:

```bash
git tag -a v1.0.0 -m "PADOrganizer v1.0.0"
git push origin v1.0.0
```

Workflow cũng có thể chạy thủ công từ tab **Actions** để kiểm tra artefact mà không tạo GitHub Release. Mỗi lần phát hành cần dùng một số phiên bản và tag mới.

## Cấu trúc dự án

```text
PADOrganizer/
├── main.py                 # Giao diện và luồng ứng dụng
├── modules/
│   ├── classifier.py       # Di chuyển tệp và hoàn tác
│   ├── config_manager.py   # Quy tắc phân loại và đường dẫn dữ liệu
│   ├── deduplicator.py     # Phát hiện tệp trùng lặp
│   ├── logger.py           # Nhật ký hoạt động
│   └── theme.py            # Hệ thống giao diện và hiệu ứng
├── PADOrganizer.spec       # Cấu hình PyInstaller
├── build.bat               # Script đóng gói cho Windows
├── build_installer.bat     # Tạo installer từ tệp đã đóng gói
├── build_release.bat       # Tạo toàn bộ artefact phát hành
├── installer/
│   └── PADOrganizer.iss    # Cấu hình Inno Setup
├── scripts/
│   └── New-Checksums.ps1   # Sinh mã kiểm tra SHA-256
├── .github/workflows/
│   └── release.yml         # Tự động build và phát hành theo tag
├── requirements.txt
├── requirements-dev.txt    # Công cụ chỉ dùng để đóng gói
└── logo.ico
```

`config.json`, `logs/` và `PADOrganizer_Trash/` được tạo khi chạy ứng dụng và không được đưa vào Git.

## Lưu ý an toàn

- Hãy kiểm tra kỹ danh sách tệp trước khi chọn xóa vĩnh viễn.
- PADOrganizer chỉ quét các tệp nằm trực tiếp trong thư mục đã chọn khi tìm bản trùng lặp.
- Chức năng hoàn tác chỉ áp dụng cho các thao tác trong phiên đang chạy.

## Giấy phép

Repository hiện chưa khai báo giấy phép sử dụng. Mọi quyền được bảo lưu cho chủ sở hữu repository.
