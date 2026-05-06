# main.py
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QProgressBar, QCheckBox,
                             QInputDialog, QListWidget, QDialog, QScrollArea,
                             QGroupBox, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from modules import FileMover, SmartLogger, ConfigManager, Deduplicator
from modules.config_manager import GLOBAL_TRASH_DIR

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class WorkerThread(QThread):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(int, int)

    def __init__(self, watch_path, file_map, mover, logger, sort_by_date):
        super().__init__()
        self.watch_path = Path(watch_path)
        self.file_map = file_map
        self.mover = mover
        self.logger = logger
        self.sort_by_date = sort_by_date

    def get_category(self, extension):
        ext_lower = extension.lower()
        for category, extensions in self.file_map.items():
            if ext_lower in extensions:
                return category
        return "Others"

    def run(self):
        success_count = 0
        error_count = 0
        
        all_files = [f for f in self.watch_path.iterdir() if f.is_file() and f.name != "activity.log" and f.name != "config.json"]
        total = len(all_files)
        
        for i, file_path in enumerate(all_files):
            try:
                category = self.get_category(file_path.suffix)
                dest_folder = self.watch_path / category
                
                new_path = self.mover.move_file(file_path, dest_folder, self.sort_by_date)
                self.logger.log(f"SUCCESS: {file_path.name} -> {new_path.relative_to(self.watch_path)}")
                success_count += 1
            except Exception as e:
                self.logger.log(f"ERROR: {file_path.name} - {e}")
                error_count += 1
                
            self.progress.emit(i + 1, total, file_path.name)
            
        self.mover.end_batch()
        self.finished.emit(success_count, error_count)

class DedupeThread(QThread):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(list)

    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = Path(target_dir)
        self.deduplicator = Deduplicator()

    def run(self):
        def callback(current, total, name):
            self.progress.emit(current, total, name)
            
        duplicates = self.deduplicator.find_duplicates(self.target_dir, callback)
        self.finished.emit(duplicates)

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.file_map = self.config_manager.get_file_map()
        self.setWindowTitle("Cài đặt phân loại")
        self.resize(400, 300)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        
        for category, extensions in self.file_map.items():
            ext_str = ", ".join(extensions)
            self.list_widget.addItem(f"{category}: {ext_str}")
            
        layout.addWidget(QLabel("Danh sách phân loại (Tên Thư Mục: .ext1, .ext2):"))
        layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm")
        add_btn.clicked.connect(self.add_category)
        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(self.save_settings)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def add_category(self):
        text, ok = QInputDialog.getText(self, "Thêm loại", "Nhập theo định dạng 'Tên: .ext1, .ext2'")
        if ok and text:
            self.list_widget.addItem(text)
            
    def save_settings(self):
        new_map = {}
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i).text()
            if ":" in item:
                cat, exts = item.split(":", 1)
                ext_list = [e.strip() for e in exts.split(",") if e.strip().startswith(".")]
                new_map[cat.strip()] = ext_list
        self.config_manager.set_file_map(new_map)
        self.accept()

class DedupeDialog(QDialog):
    def __init__(self, duplicates, logger, mover, target_dir, parent=None):
        super().__init__(parent)
        self.duplicates = duplicates
        self.logger = logger
        self.mover = mover
        self.target_dir = Path(target_dir)
        self.to_delete = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Xóa File Trùng Lặp")
        self.resize(550, 450)
        
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel("Chọn file bạn muốn GIỮ LẠI trong mỗi nhóm.\nBạn có thể chuyển file không chọn vào Thùng Rác hoặc Xóa Vĩnh Viễn.")
        info_label.setStyleSheet("color: #dc3545; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(info_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        self.group_buttons = []
        
        for i, group in enumerate(self.duplicates):
            group_box = QGroupBox(f"Nhóm trùng lặp {i+1} ({len(group)} files)")
            group_layout = QVBoxLayout()
            
            # Sắp xếp để file có tên gốc, ngắn gọn nhất được ưu tiên (thứ tự chiều dài tên trước, từ điển sau)
            sorted_group = sorted(group, key=lambda f: (len(f.name), f.name.lower(), str(f).lower()))
            
            btn_group = QButtonGroup(self)
            
            rb_skip = QRadioButton("⏭️ Bỏ qua nhóm này (Không xóa file nào)")
            rb_skip.file_path = None
            rb_skip.setStyleSheet("""
                QRadioButton { color: #6c757d; font-style: italic; }
                QRadioButton:checked { color: #dc3545; font-weight: bold; font-style: normal; }
            """)
            btn_group.addButton(rb_skip)
            group_layout.addWidget(rb_skip)
            
            for j, f in enumerate(sorted_group):
                size_kb = f.stat().st_size / 1024
                # Hiển thị tên file và thư mục chứa nó
                rb = QRadioButton(f"{f.name} ({f.parent.name}) - {size_kb:.1f} KB")
                rb.file_path = f
                
                # Mặc định giữ file có tên nhỏ nhất (phần tử đầu tiên)
                if j == 0:
                    rb.setChecked(True)
                
                btn_group.addButton(rb)
                group_layout.addWidget(rb)
                
            self.group_buttons.append(btn_group)
            group_box.setLayout(group_layout)
            content_layout.addWidget(group_box)
            
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        btn_trash = QPushButton("🗑️ Chuyển vào Thùng rác")
        btn_trash.setStyleSheet("""
            QPushButton { background-color: #ffc107; color: #212529; }
            QPushButton:hover { background-color: #e0a800; }
        """)
        btn_trash.clicked.connect(lambda: self.process_deletion(permanent=False))
        
        btn_delete = QPushButton("💥 Xóa Vĩnh Viễn")
        btn_delete.setStyleSheet("""
            QPushButton { background-color: #dc3545; color: white; }
            QPushButton:hover { background-color: #c82333; }
        """)
        btn_delete.clicked.connect(lambda: self.process_deletion(permanent=True))
        
        btn_cancel = QPushButton("Hủy")
        btn_cancel.setStyleSheet("""
            QPushButton { background-color: #6c757d; color: white; }
            QPushButton:hover { background-color: #5a6268; }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_trash)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def process_deletion(self, permanent=False):
        self.to_delete.clear()
        # Tìm các file không được checked
        for i, group in enumerate(self.duplicates):
            btn_group = self.group_buttons[i]
            checked_btn = btn_group.checkedButton()
            
            if checked_btn is None or checked_btn.file_path is None:
                continue
                
            for f in group:
                if f != checked_btn.file_path:
                    self.to_delete.append(f)
                    
        if not self.to_delete:
            QMessageBox.information(self, "Thông báo", "Không có file nào bị xóa.")
            self.reject()
            return
            
        if permanent:
            reply = QMessageBox.question(self, "Cảnh báo Xóa Vĩnh Viễn", f"Bạn có chắc muốn XÓA VĨNH VIỄN {len(self.to_delete)} file?\n(KHÔNG THỂ KHÔI PHỤC)", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                deleted_count = 0
                for f in self.to_delete:
                    try:
                        f.unlink()
                        deleted_count += 1
                        self.logger.log(f"PERMANENT DELETED: {f.name}")
                    except Exception as e:
                        self.logger.log(f"PERM DELETE ERROR: Không thể xóa {f.name} - {e}")
                QMessageBox.information(self, "Thành công", f"Đã xóa vĩnh viễn {deleted_count} file rác.")
                self.accept()
        else:
            reply = QMessageBox.question(self, "Chuyển vào Thùng rác", f"Bạn có chắc muốn chuyển {len(self.to_delete)} file vào Smart_Trash không?\n(Bạn có thể mở Smart_Trash để lấy lại sau)", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if not GLOBAL_TRASH_DIR.exists():
                    GLOBAL_TRASH_DIR.mkdir(parents=True)
                
                self.mover.start_batch()
                deleted_count = 0
                for f in self.to_delete:
                    try:
                        f_name = f.name
                        new_path = self.mover.move_file(f, GLOBAL_TRASH_DIR, sort_by_date=False)
                        self.logger.log(f"TRASHED: {f_name} -> {new_path.name}")
                        deleted_count += 1
                    except Exception as e:
                        self.logger.log(f"TRASH ERROR: Không thể chuyển {f.name} - {e}")
                self.mover.end_batch()
                        
                QMessageBox.information(self, "Thành công", f"Đã chuyển {deleted_count} file trùng lặp vào Smart_Trash.")
                if self.parent() and hasattr(self.parent(), 'btn_undo'):
                    self.parent().btn_undo.setEnabled(True)
                    if hasattr(self.parent(), 'check_trash_exists'):
                        self.parent().check_trash_exists()
                self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.logger = SmartLogger()
        self.mover = FileMover()
        self.target_dir = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Smart File Organizer")
        self.resize(600, 400)
        
        icon_path = get_resource_path('logo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Sửa màu sắc để dễ nhìn hơn, tương phản cao, hiện đại
        self.setStyleSheet("""
            QMainWindow, QDialog { background-color: #ffffff; color: #111111; }
            QLabel { color: #111111; font-size: 14px; }
            QCheckBox { color: #111111; font-size: 14px; }
            QRadioButton { color: #555555; font-size: 13px; }
            QRadioButton:checked { color: #28a745; font-weight: bold; }
            QGroupBox { font-weight: bold; color: #0056b3; border: 1px solid #cccccc; border-radius: 5px; margin-top: 15px; padding-top: 15px;}
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
            QPushButton { 
                background-color: #007bff; color: white; 
                border-radius: 6px; padding: 8px 16px; font-weight: bold; border: none;
            }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:disabled { background-color: #e0e0e0; color: #888888; }
            QProgressBar { text-align: center; border-radius: 5px; color: black; font-weight: bold; border: 1px solid #ccc; background-color: #f8f9fa;}
            QProgressBar::chunk { background-color: #28a745; border-radius: 4px; }
            QListWidget { background-color: #f8f9fa; color: #111111; border: 1px solid #ccc; border-radius: 5px; }
            QScrollArea { border: none; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        title = QLabel("Smart File Organizer")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0056b3; margin-bottom: 10px;")
        main_layout.addWidget(title)

        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Chưa chọn thư mục")
        self.dir_label.setStyleSheet("color: #333333; background: #f8f9fa; padding: 8px; border: 1px solid #ced4da; border-radius: 5px; font-weight: bold;")
        btn_select = QPushButton("Mở Thư Mục")
        btn_select.setStyleSheet("background-color: #6c757d;")
        btn_select.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.dir_label, 1)
        dir_layout.addWidget(btn_select)
        main_layout.addLayout(dir_layout)

        opt_layout = QHBoxLayout()
        self.chk_date = QCheckBox("Tạo thư mục theo Năm-Tháng")
        self.chk_date.setChecked(self.config_manager.is_sort_by_date_enabled())
        self.chk_date.stateChanged.connect(self.save_date_setting)
        btn_settings = QPushButton("⚙️ Cài Đặt Quy Tắc")
        btn_settings.setStyleSheet("""
            QPushButton { background-color: #6c757d; color: white; }
            QPushButton:hover { background-color: #5a6268; }
        """)
        btn_settings.clicked.connect(self.open_settings)
        opt_layout.addWidget(self.chk_date)
        opt_layout.addStretch()
        opt_layout.addWidget(btn_settings)
        main_layout.addLayout(opt_layout)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(25)
        main_layout.addWidget(self.progress)
        
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-style: italic; color: #555555;")
        main_layout.addWidget(self.status_label)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        
        self.btn_run = QPushButton("🚀 Bắt Đầu Dọn Dẹp")
        self.btn_run.clicked.connect(self.run_organizer)
        self.btn_run.setMinimumHeight(45)
        
        self.btn_undo = QPushButton("↩️ Hoàn Tác")
        self.btn_undo.setStyleSheet("""
            QPushButton { background-color: #ffc107; color: #212529; border-radius: 6px; padding: 8px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #e0a800; }
            QPushButton:disabled { background-color: #e0e0e0; color: #888888; }
        """)
        self.btn_undo.clicked.connect(self.undo_action)
        self.btn_undo.setEnabled(False)
        self.btn_undo.setMinimumHeight(45)
        
        self.btn_dedupe = QPushButton("🗑️ Dọn File Trùng")
        self.btn_dedupe.setStyleSheet("""
            QPushButton { background-color: #17a2b8; color: white; border-radius: 6px; padding: 8px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #138496; }
            QPushButton:disabled { background-color: #e0e0e0; color: #888888; }
        """)
        self.btn_dedupe.clicked.connect(self.run_dedupe)
        self.btn_dedupe.setMinimumHeight(45)

        trash_layout = QVBoxLayout()
        trash_layout.setSpacing(5)
        self.btn_open_trash = QPushButton("📂 Mở Thùng Rác")
        self.btn_open_trash.setStyleSheet("""
            QPushButton { background-color: #17a2b8; color: white; padding: 4px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #138496; }
        """)
        self.btn_open_trash.clicked.connect(self.open_trash)
        self.btn_open_trash.setEnabled(True)
        
        self.btn_empty_trash = QPushButton("🔥 Dọn Rác")
        self.btn_empty_trash.setStyleSheet("""
            QPushButton { background-color: #dc3545; color: white; padding: 4px; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #c82333; }
            QPushButton:disabled { background-color: #e0e0e0; color: #888888; }
        """)
        self.btn_empty_trash.clicked.connect(self.empty_trash)
        self.btn_empty_trash.setEnabled(False)
        
        trash_layout.addWidget(self.btn_open_trash)
        trash_layout.addWidget(self.btn_empty_trash)

        action_layout.addWidget(self.btn_run, 3) 
        action_layout.addWidget(self.btn_undo, 2)
        action_layout.addWidget(self.btn_dedupe, 2)
        action_layout.addLayout(trash_layout, 2)
        main_layout.addLayout(action_layout)

    def save_date_setting(self, state):
        self.config_manager.set_sort_by_date(state == Qt.CheckState.Checked.value)

    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục")
        if folder:
            self.target_dir = folder
            self.dir_label.setText(folder)
            self.check_trash_exists()

    def check_trash_exists(self):
        if GLOBAL_TRASH_DIR.exists() and any(GLOBAL_TRASH_DIR.iterdir()):
            self.btn_empty_trash.setEnabled(True)
        else:
            self.btn_empty_trash.setEnabled(False)

    def open_trash(self):
        if not GLOBAL_TRASH_DIR.exists():
            GLOBAL_TRASH_DIR.mkdir(parents=True)
        import subprocess
        try:
            os.startfile(str(GLOBAL_TRASH_DIR))
        except AttributeError:
            subprocess.call(['explorer', str(GLOBAL_TRASH_DIR)])

    def open_settings(self):
        dlg = SettingsDialog(self.config_manager, self)
        dlg.exec()

    def set_ui_enabled(self, enabled):
        self.btn_run.setEnabled(enabled)
        self.btn_dedupe.setEnabled(enabled)
        if enabled:
            self.check_trash_exists()
        else:
            self.btn_empty_trash.setEnabled(False)

    def run_organizer(self):
        if not self.target_dir:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục trước!")
            return
            
        self.set_ui_enabled(False)
        self.status_label.setText("Đang dọn dẹp...")
        self.progress.setValue(0)
        
        self.mover.start_batch()
        self.worker = WorkerThread(
            self.target_dir, 
            self.config_manager.get_file_map(),
            self.mover,
            self.logger,
            self.chk_date.isChecked()
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.organize_finished)
        self.worker.start()

    def update_progress(self, current, total, name):
        percent = int((current / total) * 100) if total > 0 else 100
        self.progress.setValue(percent)
        self.status_label.setText(f"Đang xử lý: {name}")

    def organize_finished(self, success, error):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        self.status_label.setText("Hoàn tất!")
        self.btn_undo.setEnabled(True)
        
        msg = f"Dọn dẹp xong!\nThành công: {success}\nLỗi: {error}"
        QMessageBox.information(self, "Kết quả", msg)

    def undo_action(self):
        reply = QMessageBox.question(
            self, "Xác nhận", 
            "Bạn có chắc muốn hoàn tác bước dọn dẹp vừa rồi?\n(Các file sẽ trở về vị trí cũ)", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logger.log("--- BẮT ĐẦU HOÀN TÁC (UNDO) ---")
            success, error = self.mover.undo_last_operation(self.logger)
            self.logger.log("--- KẾT THÚC HOÀN TÁC ---")
            QMessageBox.information(self, "Hoàn tác", f"Đã khôi phục {success} file. Lỗi: {error}\n(Chi tiết xem trong logs/activity.log)")
            self.btn_undo.setEnabled(self.mover.has_history())
            self.check_trash_exists()

    def empty_trash(self):
        if not GLOBAL_TRASH_DIR.exists():
            return
            
        reply = QMessageBox.question(
            self, "Dọn Sạch Thùng Rác", 
            "Bạn có chắc muốn XÓA VĨNH VIỄN tất cả các file trong thùng rác Smart_Trash không?\n(Hành động này KHÔNG THỂ hoàn tác)", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            import shutil
            try:
                shutil.rmtree(str(GLOBAL_TRASH_DIR))
                QMessageBox.information(self, "Thành công", "Đã dọn sạch thùng rác!")
                self.check_trash_exists()
                self.logger.log("EMPTY TRASH: Đã xóa vĩnh viễn thùng rác.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa thùng rác: {e}")

    def run_dedupe(self):
        if not self.target_dir:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục trước!")
            return
            
        self.set_ui_enabled(False)
        self.status_label.setText("Đang quét file trùng lặp (có thể mất vài phút)...")
        self.progress.setValue(0)
        
        self.dedupe_worker = DedupeThread(self.target_dir)
        self.dedupe_worker.progress.connect(self.update_progress)
        self.dedupe_worker.finished.connect(self.dedupe_finished)
        self.dedupe_worker.start()

    def dedupe_finished(self, duplicates):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        
        if not duplicates:
            self.status_label.setText("Tuyệt vời! Không tìm thấy file trùng lặp.")
            QMessageBox.information(self, "Kết quả", "Thư mục sạch sẽ, không có file trùng lặp!")
            return
            
        self.status_label.setText(f"Phát hiện {len(duplicates)} nhóm trùng lặp.")
        
        # Hiển thị giao diện chọn và xóa file
        dlg = DedupeDialog(duplicates, self.logger, self.mover, self.target_dir, self)
        dlg.exec()

def main():
    app = QApplication(sys.argv)
    
    if not os.path.exists(get_resource_path('logo.ico')):
        pass
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()