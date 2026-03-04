# main.py
import sys
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

# Import từ các module bạn đã viết
from config import FILE_MAP
from modules import FileMover, SmartLogger

class OrganizerApp:
    def __init__(self, watch_path):
        """Khởi tạo App với đường dẫn cần dọn dẹp"""
        self.watch_path = Path(watch_path)
        self.mover = FileMover()
        self.logger = SmartLogger()
        self.success_count = 0
        self.error_count = 0

    def get_category(self, extension):
        """Xác định thư mục đích dựa trên đuôi file"""
        ext_lower = extension.lower()
        for category, extensions in FILE_MAP.items():
            if ext_lower in extensions:
                return category
        return "Others"

    def run(self):
        """Thực thi dọn dẹp một lần duy nhất"""
        # Kiểm tra tính hợp lệ của thư mục
        if not self.watch_path.exists() or not self.watch_path.is_dir():
            messagebox.showerror("Lỗi", "Thư mục không tồn tại hoặc không hợp lệ!")
            return

        # Quét toàn bộ file trong thư mục
        for file_path in self.watch_path.iterdir():
            # Chỉ xử lý file, bỏ qua thư mục con và file log
            if file_path.is_file() and file_path.name != "activity.log":
                try:
                    category = self.get_category(file_path.suffix)
                    dest_folder = self.watch_path / category
                    
                    # Thực hiện di chuyển và xử lý trùng tên
                    new_path = self.mover.move_file(file_path, dest_folder)
                    
                    # Ghi log
                    self.logger.log(f"SUCCESS: {file_path.name} -> {category}/{new_path.name}")
                    self.success_count += 1
                except Exception as e:
                    self.logger.log(f"ERROR: Không thể di chuyển {file_path.name}. Lỗi: {e}")
                    self.error_count += 1

        # Hiển thị báo cáo cuối cùng
        self.show_report()

    def show_report(self):
        """Hiện bảng thông báo kết quả cho người dùng"""
        msg = f"Quá trình dọn dẹp hoàn tất!\n\n"
        msg += f"✅ Thành công: {self.success_count} file\n"
        if self.error_count > 0:
            msg += f"❌ Lỗi: {self.error_count} file (Xem chi tiết tại activity.log)"
        
        messagebox.showinfo("Smart File Organizer", msg)

def select_folder_via_gui():
    """Mở cửa sổ chuẩn của hệ điều hành để chọn thư mục"""
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính của tkinter
    root.attributes('-topmost', True)  # Đưa cửa sổ chọn folder lên trên cùng
    
    selected_path = filedialog.askdirectory(title="Chọn thư mục bạn muốn dọn dẹp")
    
    root.destroy()
    return selected_path

if __name__ == "__main__":
    # 1. Yêu cầu người dùng chọn thư mục
    target_dir = select_folder_via_gui()
    
    # 2. Nếu người dùng chọn thư mục (không nhấn Cancel)
    if target_dir:
        app = OrganizerApp(target_dir)
        app.run()
    else:
        print("Chương trình đã được hủy bỏ bởi người dùng.")
        sys.exit()