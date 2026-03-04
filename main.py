# main.py
import time
from pathlib import Path
from tkinter import Tk, filedialog  
from config import FILE_MAP
from modules import FileMover, SmartLogger

class OrganizerApp:
    def __init__(self, watch_path):
        self.watch_path = Path(watch_path)
        self.mover = FileMover()
        self.logger = SmartLogger()

    def get_category(self, extension):
        for category, extensions in FILE_MAP.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def run(self):
        if not self.watch_path.exists():
            print("❌ Thư mục không tồn tại!")
            return

        print(f"🚀 Đang theo dõi: {self.watch_path}")
        try:
            # while True:
            for file_path in self.watch_path.iterdir():
                if file_path.is_file() and file_path.name != "activity.log":
                    category = self.get_category(file_path.suffix)
                    dest_folder = self.watch_path / category
                    
                    new_path = self.mover.move_file(file_path, dest_folder)
                    self.logger.log(f"Moved: {file_path.name} -> {category}/{new_path.name}")
                    print(f"✔ Đã dọn dẹp: {file_path.name}")
                
                # time.sleep(10)
        except KeyboardInterrupt:
            print("\n👋 Đã dừng chương trình.")

def select_folder():
    """Hàm này sẽ mở cửa sổ để người dùng chọn thư mục"""
    root = Tk()
    root.withdraw() # Ẩn cửa sổ chính của tkinter đi
    root.attributes('-topmost', True) # Đưa cửa sổ chọn folder lên trên cùng các cửa sổ khác
    
    # Mở hộp thoại chọn thư mục
    folder_selected = filedialog.askdirectory(title="Chọn thư mục bạn muốn tự động hóa dọn dẹp")
    
    root.destroy() # Đóng hoàn toàn tkinter sau khi chọn xong
    return folder_selected

if __name__ == "__main__":
    print("--- CHƯƠNG TRÌNH PHÂN LOẠI FILE THÔNG MINH ---")
    
    # Gọi hàm mở cửa sổ chọn folder
    target_path = select_folder()
    
    if target_path: # Nếu người dùng có chọn folder (không nhấn Cancel)
        app = OrganizerApp(target_path)
        app.run()
    else:
        print("⚠ Bạn chưa chọn thư mục nào. Chương trình kết thúc.")