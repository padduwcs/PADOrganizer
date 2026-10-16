# Nhật ký thay đổi

Mọi thay đổi đáng chú ý của PADOrganizer được ghi lại tại đây. Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/) và dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

Nội dung của mỗi phiên bản cũng được dùng làm ghi chú phát hành trên GitHub và hiển thị trong hộp thoại **Có gì mới** của ứng dụng.

## [1.3.0] - 2026-10-17

### Thêm mới
- Logo và bộ nhận diện mới cho PADOrganizer; giao diện sáng/tối chuyển sang tông nâu, cam và xanh rêu của logo.
- Gói Linux: bản `.deb` cho Ubuntu/Debian và AppImage cho các bản phân phối khác, kèm icon độ phân giải cao.
- Giấy phép Apache-2.0.

### Thay đổi
- Tìm tệp trùng nhanh hơn rõ rệt: chỉ đọc nội dung những tệp có cùng kích thước.
- Chuyển bản trùng vào thùng rác hoặc xóa vĩnh viễn chạy nền, kèm thanh tiến độ, giao diện không còn bị đứng.
- Phần mở rộng không còn phân biệt chữ hoa/thường (`.JPG` và `.jpg` cùng một nhóm).

### An toàn
- Không bao giờ di chuyển tệp ẩn, tệp hệ thống (`.bashrc`, `desktop.ini`…) và liên kết tượng trưng.
- Không cho chọn thư mục gốc ổ đĩa, thư mục Home và thư mục hệ thống như `C:\Windows`, `Program Files`, `/usr`.
- Tệp rỗng (0 byte) không còn bị coi là bản trùng.
- Cấu hình được ghi an toàn; nếu `config.json` bị hỏng, ứng dụng giữ lại bản sao `config.json.broken` thay vì âm thầm mất quy tắc tùy chỉnh.

## [1.2.0] - 2026-08-10

### Thêm mới
- Giao diện tối và nút chuyển đổi sáng/tối tức thời.
- Giao diện tiếng Anh; chuyển đổi Tiếng Việt/English ngay trong ứng dụng.

## [1.1.1] - 2026-08-09

### Thay đổi
- Tinh chỉnh hộp thoại bảo trì và cập nhật.

## [1.1.0] - 2026-08-09

### Thêm mới
- Kiểm tra cập nhật theo yêu cầu: tải Installer, xác minh SHA-256 và hỏi lại trước khi cài.
- Tài liệu hướng dẫn dành cho người dùng cuối.

## [1.0.0] - 2026-08-09

### Thêm mới
- Phát hành đầu tiên với tên PADOrganizer: phân loại tệp theo quy tắc, chia theo Năm–Tháng, hoàn tác trong phiên, tìm tệp trùng và thùng rác nội bộ.
- Installer Windows và bản portable.
- Dọn nhật ký hoạt động từ mục Bảo trì.

[1.3.0]: https://github.com/padduwcs/PADOrganizer/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/padduwcs/PADOrganizer/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/padduwcs/PADOrganizer/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/padduwcs/PADOrganizer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/padduwcs/PADOrganizer/releases/tag/v1.0.0
