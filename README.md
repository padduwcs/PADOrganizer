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
- Mọi thao tác diễn ra cục bộ; dữ liệu cá nhân không được tải lên mạng.

Phím tắt:

| Phím | Thao tác |
|---|---|
| `Ctrl+O` | Chọn thư mục |
| `Ctrl+Enter` | Tổ chức thư mục |
| `Ctrl+D` | Tìm tệp trùng |
| `Ctrl+Z` | Hoàn tác |
| `Ctrl+,` | Mở quy tắc phân loại |

## Cài đặt và chạy

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

Chạy:

```bat
build.bat
```

Hoặc đóng gói thủ công:

```bash
pyinstaller PADOrganizer.spec
```

Tệp thực thi được tạo tại `dist/PADOrganizer.exe`.

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
├── requirements.txt
└── logo.ico
```

`config.json`, `logs/` và `PADOrganizer_Trash/` được tạo khi chạy ứng dụng và không được đưa vào Git.

## Lưu ý an toàn

- Hãy kiểm tra kỹ danh sách tệp trước khi chọn xóa vĩnh viễn.
- PADOrganizer chỉ quét các tệp nằm trực tiếp trong thư mục đã chọn khi tìm bản trùng lặp.
- Chức năng hoàn tác chỉ áp dụng cho các thao tác trong phiên đang chạy.

## Giấy phép

Repository hiện chưa khai báo giấy phép sử dụng. Mọi quyền được bảo lưu cho chủ sở hữu repository.
