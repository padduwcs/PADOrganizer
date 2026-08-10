<div align="center">
  <img src="logo.ico" alt="PADOrganizer" width="96">
  <h1>PADOrganizer</h1>
  <p><strong>Personal Archive Directory Organizer</strong></p>
  <p>Sắp xếp thư mục, tìm tệp trùng và dọn dẹp an toàn ngay trên máy tính của bạn.</p>
  <p><a href="https://github.com/padduwcs/PADOrganizer/releases/latest"><strong>Tải phiên bản mới nhất</strong></a></p>
</div>

## PADOrganizer giúp bạn làm gì?

- Phân loại tệp tự động vào `Images`, `Documents`, `Videos`, `Audio` và các nhóm khác.
- Tùy chỉnh tên nhóm và phần mở rộng theo nhu cầu riêng.
- Chia tệp theo `Năm–Tháng` khi cần lưu trữ lâu dài.
- Tìm tệp trùng theo nội dung trước khi quyết định giữ hoặc xóa.
- Hoàn tác lần sắp xếp gần nhất trong phiên đang mở.
- Giữ tệp cần dọn trong thùng rác nội bộ trước khi xóa vĩnh viễn.
- Chủ động kiểm tra, tải và xác minh phiên bản mới từ GitHub khi bạn yêu cầu.
- Chuyển đổi tức thời giữa giao diện sáng/tối và ngôn ngữ Tiếng Việt/English.

Mọi thao tác với tệp đều diễn ra cục bộ. PADOrganizer không tải tệp hoặc dữ liệu cá nhân của bạn lên mạng; ứng dụng chỉ kết nối GitHub khi bạn bấm **Kiểm tra cập nhật**.

## Cài đặt trên Windows

1. Mở trang [Releases](https://github.com/padduwcs/PADOrganizer/releases/latest).
2. Tải `PADOrganizer-Setup-vX.Y.Z.exe` trong phần **Assets**.
3. Mở tệp vừa tải và làm theo hướng dẫn cài đặt.
4. Khởi động PADOrganizer từ Start Menu hoặc shortcut ngoài Desktop.

Bạn không cần cài Python hay thư viện bổ sung. Nếu không muốn cài đặt, hãy tải bản `PADOrganizer-portable-vX.Y.Z.exe` và đặt nó trong một thư mục riêng trước khi chạy.

> Windows SmartScreen có thể cảnh báo vì ứng dụng hiện chưa có chữ ký số. Chỉ tiếp tục khi tệp được tải từ repository chính thức này; bạn có thể đối chiếu với `SHA256SUMS.txt` trong cùng bản phát hành.

## Bắt đầu sử dụng

1. Kéo thả thư mục vào ứng dụng hoặc chọn **Duyệt...**.
2. Bật **Chia theo Năm–Tháng** hoặc mở **Quy tắc phân loại** nếu muốn tùy chỉnh.
3. Chọn **Tổ chức ngay** và theo dõi kết quả trên màn hình.
4. Dùng **Hoàn tác** nếu muốn khôi phục lần sắp xếp vừa thực hiện.

Để dọn tệp trùng, chọn **Tìm bản trùng**, đánh dấu bản muốn giữ rồi chuyển các bản còn lại vào thùng rác nội bộ. Hãy kiểm tra kỹ trước khi chọn **Xóa vĩnh viễn**.

## Cập nhật phiên bản

Chọn **Kiểm tra cập nhật** trong mục **Bảo trì**. PADOrganizer không tự kiểm tra trong nền.

- Bản cài đặt: ứng dụng có thể tải Installer, xác minh SHA-256 và hỏi lại trước khi mở trình cài đặt.
- Bản portable hoặc chạy từ mã nguồn: ứng dụng mở trang Release để bạn chọn file phù hợp.

Quá trình cập nhật giữ nguyên quy tắc, nhật ký và các tệp trong thùng rác nội bộ.

## Dữ liệu và quyền riêng tư

PADOrganizer lưu dữ liệu ngay trên thiết bị:

- `config.json`: quy tắc và tùy chọn của bạn.
- `logs/`: nhật ký hoạt động; có thể xóa từ mục **Bảo trì**.
- `PADOrganizer_Trash/`: các tệp đã chuyển vào thùng rác nội bộ.

Cài bản mới vào cùng vị trí sẽ giữ nguyên các dữ liệu này. Khi gỡ ứng dụng từ **Windows Settings → Apps**, dữ liệu cá nhân không bị tự động xóa; nếu muốn dọn hoàn toàn, hãy xóa thư mục `%LOCALAPPDATA%\Programs\PADOrganizer` sau khi gỡ cài đặt.

## Phím tắt

| Phím | Thao tác |
|---|---|
| `Ctrl+O` | Chọn thư mục |
| `Ctrl+Enter` | Tổ chức thư mục |
| `Ctrl+D` | Tìm tệp trùng |
| `Ctrl+Z` | Hoàn tác |
| `Ctrl+,` | Mở quy tắc phân loại |

## Lưu ý

- PADOrganizer chỉ xử lý các tệp nằm trực tiếp trong thư mục đã chọn, không tự ý quét toàn bộ máy tính.
- Hoàn tác chỉ áp dụng cho lần sắp xếp gần nhất trong phiên đang mở.
- Tệp trong thùng rác nội bộ vẫn chiếm dung lượng cho đến khi bạn dọn sạch.

Bạn muốn chạy từ mã nguồn hoặc đóng góp cho dự án? Xem [Hướng dẫn phát triển](docs/DEVELOPMENT.md).

## Giấy phép

Repository hiện chưa khai báo giấy phép sử dụng. Mọi quyền được bảo lưu cho chủ sở hữu repository.
