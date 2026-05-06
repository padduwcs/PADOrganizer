# Smart File Organizer 🚀

Ứng dụng dọn dẹp và sắp xếp file tự động bằng Python, với giao diện hiện đại sử dụng **PyQt6**.

![Smart Organizer Logo](logo.ico)

## 🌟 Tính năng nổi bật

- **Tự động phân loại**: Gom các file lộn xộn vào đúng thư mục (Images, Documents, Videos...) theo quy tắc tùy chỉnh.
- **Phân loại theo thời gian**: Tự động tạo thư mục theo `Năm-Tháng` (ví dụ: `Images/2026-05`).
- **Giao diện hiện đại (GUI)**: Trải nghiệm sử dụng mượt mà với PyQt6, hiển thị tiến trình rõ ràng.
- **Hoàn tác (Undo) Thông minh** ↩️: Khôi phục lại trạng thái file theo từng đợt thao tác (hỗ trợ dọn dẹp rỗng).
- **Tìm và Xóa file trùng lặp an toàn** 🗑️: 
  - Chỉ quét trong thư mục hiện tại để không làm hỏng cấu trúc thư mục con.
  - Tự động nhận diện và ưu tiên giữ lại file gốc.
  - Hỗ trợ thùng rác trung tâm (`Smart_Trash`), cho phép khôi phục lại bất kỳ lúc nào ngay cả khi đã tắt phần mềm.
  - Hỗ trợ tùy chọn giữ lại bộ file không muốn can thiệp.
- **Tùy biến quy tắc**: Cho phép người dùng thêm/bớt các định dạng file thông qua giao diện `Cài đặt` (Settings).

## 🛠️ Cài đặt & Sử dụng
1. Clone mã nguồn về máy:
   ```bash
   git clone https://github.com/Ten-Cua-Ban/smart-file-organizer.git
   cd smart-file-organizer
   ```

2. Cài đặt các thư viện (Khuyến nghị dùng môi trường ảo hoặc Conda):
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy file trực tiếp:
   ```bash
   python main.py
   ```

## 📦 Đóng gói thành ứng dụng (.exe)

Dự án đã có sẵn file cấu hình `SmartOrganizer.spec`. Để đóng gói thành file `.exe` chạy độc lập (không cần cài python/conda), bạn chỉ cần chạy:
```bash
build.bat
```
Hoặc chạy lệnh thủ công: `pyinstaller SmartOrganizer.spec`.
File ứng dụng sẽ xuất hiện trong thư mục `dist/`.

## 📜 Cấu trúc thư mục
- `main.py`: Chứa giao diện PyQt6 và luồng chạy chính.
- `modules/`: Chứa các module xử lý logic.
  - `classifier.py`: Di chuyển file và lưu lịch sử (Undo).
  - `deduplicator.py`: Thuật toán băm và quét file trùng lặp.
  - `config_manager.py`: Lưu và đọc cài đặt từ `config.json`.
  - `logger.py`: Ghi lại nhật ký vào thư mục `logs/`.
- `requirements.txt`: Danh sách các thư viện Python.
- `build.bat`: Script đóng gói ứng dụng nhanh cho Windows.
- `config.json` (tự động tạo): Lưu quy tắc phân loại của bạn.