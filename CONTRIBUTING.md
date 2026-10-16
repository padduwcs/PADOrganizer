# Đóng góp cho PADOrganizer

Cảm ơn bạn đã quan tâm! Mọi đóng góp — báo lỗi, đề xuất tính năng, cải thiện bản dịch hay gửi mã — đều được hoan nghênh.

## Báo lỗi và đề xuất

- Tìm trong [Issues](https://github.com/padduwcs/PADOrganizer/issues) trước để tránh trùng lặp.
- Dùng mẫu **Báo lỗi** hoặc **Đề xuất tính năng** khi tạo issue mới.
- Với lỗi, hãy ghi rõ phiên bản (hiển thị ở góc dưới thanh bên), hệ điều hành, cách tái hiện và đính kèm đoạn nhật ký liên quan nếu có. Nhớ xóa đường dẫn hoặc tên tệp nhạy cảm trước khi gửi.
- Lỗ hổng bảo mật vui lòng **không** đăng công khai; xem [SECURITY.md](SECURITY.md).

## Gửi Pull Request

1. Fork repository và tạo nhánh từ `main`, ví dụ `fix/undo-empty-folder`.
2. Cài môi trường phát triển theo [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).
3. Viết test cho thay đổi của bạn, nhất là khi thay đổi động tới tệp của người dùng.
4. Đảm bảo các lệnh sau chạy sạch:

   ```bash
   python -m ruff check .
   python -m unittest discover -s tests -v
   ```

5. Thêm mô tả thay đổi vào mục mới nhất của [CHANGELOG.md](CHANGELOG.md) nếu người dùng có thể nhận thấy nó.
6. Mở Pull Request và điền mẫu mô tả. CI sẽ chạy lint và test trên Windows lẫn Linux.

## Nguyên tắc

- **An toàn dữ liệu là ưu tiên số một.** Mọi thao tác với tệp phải dùng `modules/safety.py` để lấy danh sách tệp, có thể hoàn tác hoặc yêu cầu xác nhận rõ ràng.
- **Không kết nối mạng ngầm.** Ứng dụng chỉ truy cập Internet khi người dùng bấm *Kiểm tra cập nhật*.
- **Song ngữ.** Chuỗi hiển thị viết bằng tiếng Việt và cần có bản dịch tương ứng trong `modules/i18n.py`.
- Giữ phong cách mã sẵn có; commit message viết bằng tiếng Anh, dạng mệnh lệnh ngắn gọn (ví dụ `Add duplicate preview`).

Khi gửi đóng góp, bạn đồng ý để đóng góp đó được phát hành theo [Giấy phép Apache 2.0](LICENSE) của dự án.
