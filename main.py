import os
import shutil
import sys
from copy import deepcopy
from pathlib import Path

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    Qt,
    QThread,
    QUrl,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QDesktopServices,
    QFont,
    QIcon,
    QKeySequence,
    QPainter,
    QShortcut,
)
from PyQt6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QBoxLayout,
    QDialog,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizeGrip,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from modules import ConfigManager, Deduplicator, FileMover, PADLogger
from modules.config_manager import BASE_DIR, DEFAULT_CONFIG, PAD_TRASH_DIR
from modules.theme import APP_STYLE, add_shadow
from modules.updater import (
    UpdateError,
    download_installer,
    fetch_latest_release,
    is_installed_build,
    is_newer_version,
    launch_installer,
)
from version import APP_VERSION


APP_NAME = "PADOrganizer"
APP_FULL_NAME = "PADOrganizer: Personal Archive Directory Organizer"


def get_resource_path(relative_path):
    """Return an absolute resource path in development and PyInstaller builds."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def format_bytes(size):
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def refresh_style(widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


class ToggleSwitch(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(46, 25)
        self._handle_position = 3.0
        self._animation = QPropertyAnimation(self, b"handlePosition", self)
        self._animation.setDuration(170)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.toggled.connect(self._animate)

    def _animate(self, checked):
        self._animation.stop()
        self._animation.setStartValue(self._handle_position)
        self._animation.setEndValue(24.0 if checked else 3.0)
        self._animation.start()

    def get_handle_position(self):
        return self._handle_position

    def set_handle_position(self, value):
        self._handle_position = value
        self.update()

    handlePosition = pyqtProperty(float, get_handle_position, set_handle_position)

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#735cf4") if self.isChecked() else QColor("#d4d8e2"))
        painter.drawRoundedRect(QRectF(0, 0, 46, 25), 12.5, 12.5)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRectF(self._handle_position, 3, 19, 19))


class WorkerThread(QThread):
    progress = pyqtSignal(int, int, str)
    completed = pyqtSignal(int, int)
    failed = pyqtSignal(str)

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
        try:
            all_files = [
                path
                for path in self.watch_path.iterdir()
                if path.is_file() and path.name not in {"activity.log", "config.json"}
            ]
        except Exception as exc:
            self.failed.emit(f"Không thể đọc thư mục đã chọn: {exc}")
            return

        success_count = 0
        error_count = 0
        total = len(all_files)

        for index, file_path in enumerate(all_files):
            try:
                category = self.get_category(file_path.suffix)
                destination = self.watch_path / category
                new_path = self.mover.move_file(file_path, destination, self.sort_by_date)
                self.logger.log(
                    f"SUCCESS: {file_path.name} -> {new_path.relative_to(self.watch_path)}"
                )
                success_count += 1
            except Exception as exc:
                self.logger.log(f"ERROR: {file_path.name} - {exc}")
                error_count += 1
            self.progress.emit(index + 1, total, file_path.name)

        self.mover.end_batch()
        self.completed.emit(success_count, error_count)


class DedupeThread(QThread):
    progress = pyqtSignal(int, int, str)
    completed = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = Path(target_dir)
        self.deduplicator = Deduplicator()

    def run(self):
        try:
            duplicates = self.deduplicator.find_duplicates(
                self.target_dir,
                lambda current, total, name: self.progress.emit(current, total, name),
            )
            self.completed.emit(duplicates)
        except Exception as exc:
            self.failed.emit(f"Không thể quét tệp trùng lặp: {exc}")


class UpdateCheckThread(QThread):
    completed = pyqtSignal(object)
    failed = pyqtSignal(str)

    def run(self):
        try:
            self.completed.emit(fetch_latest_release())
        except UpdateError as exc:
            self.failed.emit(str(exc))
        except Exception:
            self.failed.emit("Không thể kiểm tra cập nhật vào lúc này.")


class UpdateDownloadThread(QThread):
    progress = pyqtSignal(int, int)
    completed = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, release):
        super().__init__()
        self.release = release

    def run(self):
        try:
            path = download_installer(
                self.release,
                lambda current, total: self.progress.emit(current, total),
            )
            self.completed.emit(str(path))
        except UpdateError as exc:
            self.failed.emit(str(exc))
        except Exception:
            self.failed.emit("Không thể tải bản cập nhật vào lúc này.")


class AppMessageDialog(QDialog):
    ICONS = {
        "info": "i",
        "success": "✓",
        "danger": "!",
    }

    def __init__(
        self,
        kicker,
        title,
        message,
        primary_text,
        secondary_text=None,
        variant="info",
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setObjectName("AppMessageDialog")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(570)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(18, 18, 18, 18)

        card = QFrame()
        card.setObjectName("MessageCard")
        card.setProperty("variant", variant)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 20)
        card_layout.setSpacing(18)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        icon_frame = QFrame()
        icon_frame.setObjectName("MessageIcon")
        icon_frame.setProperty("variant", variant)
        icon_frame.setFixedSize(48, 48)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_label = QLabel(self.ICONS.get(variant, "i"))
        icon_label.setObjectName("MessageIconText")
        icon_label.setProperty("variant", variant)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        top_layout.addWidget(icon_frame, 0, Qt.AlignmentFlag.AlignTop)

        copy_layout = QVBoxLayout()
        copy_layout.setSpacing(5)
        kicker_label = QLabel(kicker.upper())
        kicker_label.setObjectName("MessageKicker")
        kicker_label.setProperty("variant", variant)
        title_label = QLabel(title)
        title_label.setObjectName("MessageTitle")
        title_label.setWordWrap(True)
        message_label = QLabel(message)
        message_label.setObjectName("MessageText")
        message_label.setWordWrap(True)
        copy_layout.addWidget(kicker_label)
        copy_layout.addWidget(title_label)
        copy_layout.addWidget(message_label)
        top_layout.addLayout(copy_layout, 1)

        close_button = QPushButton("×")
        close_button.setObjectName("MessageClose")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setToolTip("Đóng")
        close_button.setFixedSize(32, 32)
        close_button.clicked.connect(self.reject)
        top_layout.addWidget(close_button, 0, Qt.AlignmentFlag.AlignTop)
        card_layout.addLayout(top_layout)

        divider = QFrame()
        divider.setObjectName("MessageDivider")
        divider.setFixedHeight(1)
        card_layout.addWidget(divider)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addStretch()
        self.secondary_button = None
        if secondary_text:
            self.secondary_button = QPushButton(secondary_text)
            self.secondary_button.setObjectName("MessageSecondary")
            self.secondary_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.secondary_button.clicked.connect(self.reject)
            actions.addWidget(self.secondary_button)

        self.primary_button = QPushButton(primary_text)
        self.primary_button.setObjectName(
            "MessageDanger" if variant == "danger" else "MessagePrimary"
        )
        self.primary_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.primary_button.clicked.connect(self.accept)
        self.primary_button.setDefault(True)
        actions.addWidget(self.primary_button)
        card_layout.addLayout(actions)

        outer_layout.addWidget(card)
        add_shadow(card, 40, 9, 38)

    def showEvent(self, event):
        super().showEvent(event)
        parent = self.parentWidget()
        if parent is not None:
            parent_center = parent.frameGeometry().center()
            self.move(parent_center - self.rect().center())


class UpdateDialog(QDialog):
    def __init__(self, release, installed_build, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cập nhật PADOrganizer")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.resize(560, 480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(14)

        eyebrow = QLabel("CẬP NHẬT MỚI")
        eyebrow.setObjectName("DialogEyebrow")
        title = QLabel(f"PADOrganizer v{release.version} đã sẵn sàng")
        title.setObjectName("DialogTitle")
        subtitle = QLabel(
            f"Bạn đang dùng v{APP_VERSION}. Hãy xem nội dung thay đổi trước khi quyết định."
        )
        subtitle.setObjectName("DialogSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        version_card = QFrame()
        version_card.setObjectName("UpdateSummary")
        version_layout = QHBoxLayout(version_card)
        version_layout.setContentsMargins(16, 13, 16, 13)
        current_label = QLabel(f"Hiện tại  ·  v{APP_VERSION}")
        current_label.setObjectName("UpdateVersionMuted")
        arrow = QLabel("→")
        arrow.setObjectName("UpdateArrow")
        latest_label = QLabel(f"Mới nhất  ·  v{release.version}")
        latest_label.setObjectName("UpdateVersionNew")
        version_layout.addWidget(current_label)
        version_layout.addStretch()
        version_layout.addWidget(arrow)
        version_layout.addStretch()
        version_layout.addWidget(latest_label)
        layout.addWidget(version_card)

        notes_title = QLabel("Có gì mới")
        notes_title.setObjectName("OptionTitle")
        layout.addWidget(notes_title)
        notes = QTextBrowser()
        notes.setObjectName("ReleaseNotes")
        notes.setPlainText(release.notes[:6000])
        notes.setOpenExternalLinks(True)
        notes.setMinimumHeight(150)
        layout.addWidget(notes, 1)

        if installed_build:
            hint_text = (
                "Installer sẽ được tải và xác minh SHA-256. "
                "Ứng dụng chỉ đóng sau khi bạn xác nhận cài đặt."
            )
            action_text = "Tải và cập nhật"
        else:
            hint_text = (
                "Bạn đang dùng bản portable hoặc chạy từ mã nguồn. "
                "Trang Release sẽ được mở để bạn chọn bản phù hợp."
            )
            action_text = "Mở trang tải xuống"
        hint = QLabel(hint_text)
        hint.setObjectName("UpdateHint")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton("Để sau")
        cancel_button.setObjectName("DialogButton")
        cancel_button.clicked.connect(self.reject)
        action_button = QPushButton(action_text)
        action_button.setObjectName("PrimaryButton")
        action_button.clicked.connect(self.accept)
        actions.addWidget(cancel_button)
        actions.addWidget(action_button)
        layout.addLayout(actions)


class CategoryEditorDialog(QDialog):
    def __init__(self, category="", extensions=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin quy tắc")
        self.setModal(True)
        self.setFixedWidth(460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(14)

        eyebrow = QLabel("QUY TẮC PHÂN LOẠI")
        eyebrow.setObjectName("DialogEyebrow")
        title = QLabel("Thiết lập nhóm tệp")
        title.setObjectName("DialogTitle")
        hint = QLabel("Đặt tên thư mục đích và nhập các phần mở rộng, cách nhau bằng dấu phẩy.")
        hint.setObjectName("DialogSubtitle")
        hint.setWordWrap(True)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(hint)

        name_label = QLabel("Tên thư mục")
        name_label.setObjectName("OptionTitle")
        self.name_input = QLineEdit(category)
        self.name_input.setPlaceholderText("Ví dụ: Documents")
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        extension_label = QLabel("Phần mở rộng")
        extension_label.setObjectName("OptionTitle")
        self.extension_input = QLineEdit(", ".join(extensions or []))
        self.extension_input.setPlaceholderText(".pdf, .docx, .txt")
        layout.addWidget(extension_label)
        layout.addWidget(self.extension_input)

        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton("Hủy")
        cancel_button.setObjectName("DialogButton")
        cancel_button.clicked.connect(self.reject)
        save_button = QPushButton("Xác nhận")
        save_button.setObjectName("PrimaryButton")
        save_button.clicked.connect(self.validate_and_accept)
        actions.addWidget(cancel_button)
        actions.addWidget(save_button)
        layout.addLayout(actions)

    def validate_and_accept(self):
        category = self.name_input.text().strip()
        extensions = self.normalized_extensions()
        if not category:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập tên thư mục đích.")
            self.name_input.setFocus()
            return
        if not extensions:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập ít nhất một phần mở rộng.")
            self.extension_input.setFocus()
            return
        self.accept()

    def normalized_extensions(self):
        normalized = []
        for raw_value in self.extension_input.text().split(","):
            value = raw_value.strip().lower()
            if not value:
                continue
            if not value.startswith("."):
                value = f".{value}"
            if value not in normalized:
                normalized.append(value)
        return normalized

    def values(self):
        return self.name_input.text().strip(), self.normalized_extensions()


class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.file_map = deepcopy(self.config_manager.get_file_map())
        self.setWindowTitle("Quy tắc phân loại")
        self.setModal(True)
        self.resize(760, 610)
        self.setMinimumSize(650, 520)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 26)
        layout.setSpacing(18)

        eyebrow = QLabel("CÁ NHÂN HÓA")
        eyebrow.setObjectName("DialogEyebrow")
        title = QLabel("Quy tắc phân loại")
        title.setObjectName("DialogTitle")
        subtitle = QLabel(
            "Mỗi phần mở rộng chỉ nên thuộc một nhóm. Nhấp đúp vào một hàng để chỉnh sửa nhanh."
        )
        subtitle.setObjectName("DialogSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["THƯ MỤC ĐÍCH", "PHẦN MỞ RỘNG"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(300)
        self.table.doubleClicked.connect(self.edit_category)
        layout.addWidget(self.table, 1)
        self.populate_table()

        toolbar = QHBoxLayout()
        add_button = QPushButton("+  Thêm nhóm")
        add_button.setObjectName("LinkButton")
        add_button.clicked.connect(self.add_category)
        edit_button = QPushButton("Chỉnh sửa")
        edit_button.setObjectName("SecondaryButton")
        edit_button.clicked.connect(self.edit_category)
        remove_button = QPushButton("Xóa nhóm")
        remove_button.setObjectName("GhostDanger")
        remove_button.clicked.connect(self.remove_category)
        reset_button = QPushButton("Khôi phục mặc định")
        reset_button.setObjectName("SecondaryButton")
        reset_button.clicked.connect(self.reset_defaults)
        toolbar.addWidget(add_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(remove_button)
        toolbar.addStretch()
        toolbar.addWidget(reset_button)
        layout.addLayout(toolbar)

        footer = QHBoxLayout()
        self.rule_count_label = QLabel()
        self.rule_count_label.setObjectName("MutedText")
        footer.addWidget(self.rule_count_label)
        footer.addStretch()
        cancel_button = QPushButton("Hủy thay đổi")
        cancel_button.setObjectName("DialogButton")
        cancel_button.clicked.connect(self.reject)
        save_button = QPushButton("Lưu quy tắc")
        save_button.setObjectName("PrimaryButton")
        save_button.clicked.connect(self.save_settings)
        footer.addWidget(cancel_button)
        footer.addWidget(save_button)
        layout.addLayout(footer)
        self.update_rule_count()

    def populate_table(self):
        self.table.setRowCount(0)
        for category, extensions in self.file_map.items():
            self.append_row(category, extensions)

    def append_row(self, category, extensions):
        row = self.table.rowCount()
        self.table.insertRow(row)
        category_item = QTableWidgetItem(category)
        category_item.setData(Qt.ItemDataRole.UserRole, list(extensions))
        extension_item = QTableWidgetItem(", ".join(extensions))
        self.table.setItem(row, 0, category_item)
        self.table.setItem(row, 1, extension_item)
        self.table.setRowHeight(row, 45)

    def add_category(self):
        dialog = CategoryEditorDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category, extensions = dialog.values()
            existing = [self.table.item(row, 0).text().casefold() for row in range(self.table.rowCount())]
            if category.casefold() in existing:
                QMessageBox.warning(self, "Tên đã tồn tại", "Đã có một nhóm với tên này.")
                return
            self.append_row(category, extensions)
            self.table.selectRow(self.table.rowCount() - 1)
            self.update_rule_count()

    def edit_category(self, _index=None):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Chọn một nhóm", "Hãy chọn nhóm bạn muốn chỉnh sửa.")
            return
        old_name = self.table.item(row, 0).text()
        extensions = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        dialog = CategoryEditorDialog(old_name, extensions, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category, new_extensions = dialog.values()
            duplicates = [
                self.table.item(index, 0).text().casefold()
                for index in range(self.table.rowCount())
                if index != row
            ]
            if category.casefold() in duplicates:
                QMessageBox.warning(self, "Tên đã tồn tại", "Đã có một nhóm với tên này.")
                return
            self.table.item(row, 0).setText(category)
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, new_extensions)
            self.table.item(row, 1).setText(", ".join(new_extensions))
            self.update_rule_count()

    def remove_category(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Chọn một nhóm", "Hãy chọn nhóm bạn muốn xóa.")
            return
        category = self.table.item(row, 0).text()
        reply = QMessageBox.question(
            self,
            "Xóa quy tắc",
            f"Xóa nhóm “{category}” khỏi danh sách phân loại?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            self.update_rule_count()

    def reset_defaults(self):
        reply = QMessageBox.question(
            self,
            "Khôi phục mặc định",
            "Thay toàn bộ danh sách hiện tại bằng bộ quy tắc mặc định?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.file_map = deepcopy(DEFAULT_CONFIG["file_map"])
            self.populate_table()
            self.update_rule_count()

    def update_rule_count(self):
        extension_count = sum(
            len(self.table.item(row, 0).data(Qt.ItemDataRole.UserRole) or [])
            for row in range(self.table.rowCount())
        )
        self.rule_count_label.setText(f"{self.table.rowCount()} nhóm · {extension_count} phần mở rộng")

    def save_settings(self):
        file_map = {}
        seen_extensions = {}
        conflicts = []
        for row in range(self.table.rowCount()):
            category = self.table.item(row, 0).text().strip()
            extensions = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole) or []
            file_map[category] = list(extensions)
            for extension in extensions:
                if extension in seen_extensions:
                    conflicts.append(f"{extension} ({seen_extensions[extension]} / {category})")
                else:
                    seen_extensions[extension] = category

        if not file_map:
            QMessageBox.warning(self, "Danh sách trống", "Cần giữ lại ít nhất một nhóm phân loại.")
            return
        if conflicts:
            preview = ", ".join(conflicts[:5])
            QMessageBox.warning(
                self,
                "Phần mở rộng bị trùng",
                f"Mỗi phần mở rộng chỉ nên thuộc một nhóm:\n{preview}",
            )
            return
        self.config_manager.set_file_map(file_map)
        self.accept()


class DedupeDialog(QDialog):
    def __init__(self, duplicates, logger, mover, parent=None):
        super().__init__(parent)
        self.duplicates = duplicates
        self.logger = logger
        self.mover = mover
        self.group_buttons = []
        self.setWindowTitle("Xử lý tệp trùng lặp")
        self.setModal(True)
        self.resize(820, 680)
        self.setMinimumSize(700, 560)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 26)
        layout.setSpacing(16)

        eyebrow = QLabel("DỌN DẸP AN TOÀN")
        eyebrow.setObjectName("DialogEyebrow")
        title = QLabel("Chọn bản cần giữ lại")
        title.setObjectName("DialogTitle")
        duplicate_files = sum(len(group) for group in self.duplicates)
        subtitle = QLabel(
            f"Phát hiện {len(self.duplicates)} nhóm với {duplicate_files} tệp. "
            "PADOrganizer đã chọn sẵn tên tệp ngắn gọn nhất; bạn có thể đổi lựa chọn hoặc bỏ qua từng nhóm."
        )
        subtitle.setObjectName("DialogSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(2, 2, 8, 2)
        content_layout.setSpacing(12)

        for index, group in enumerate(self.duplicates):
            sorted_group = sorted(group, key=lambda path: (len(path.name), path.name.lower()))
            group_box = QGroupBox(f"NHÓM {index + 1}  ·  {len(group)} TỆP GIỐNG NHAU")
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(6)

            button_group = QButtonGroup(self)
            skip_button = QRadioButton("Bỏ qua nhóm này — không tác động tệp nào")
            skip_button.file_path = None
            button_group.addButton(skip_button)
            group_layout.addWidget(skip_button)

            for file_index, file_path in enumerate(sorted_group):
                try:
                    size_text = format_bytes(file_path.stat().st_size)
                except OSError:
                    size_text = "Không rõ dung lượng"
                radio = QRadioButton(f"Giữ lại  {file_path.name}   ·   {size_text}")
                radio.file_path = file_path
                radio.setToolTip(str(file_path))
                if file_index == 0:
                    radio.setChecked(True)
                button_group.addButton(radio)
                group_layout.addWidget(radio)

            button_group.buttonToggled.connect(self.update_selection_summary)
            self.group_buttons.append(button_group)
            content_layout.addWidget(group_box)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        footer = QHBoxLayout()
        self.selection_summary = QLabel()
        self.selection_summary.setObjectName("MutedText")
        footer.addWidget(self.selection_summary)
        footer.addStretch()
        cancel_button = QPushButton("Để sau")
        cancel_button.setObjectName("DialogButton")
        cancel_button.clicked.connect(self.reject)
        trash_button = QPushButton("Chuyển vào thùng rác")
        trash_button.setObjectName("SecondaryButton")
        trash_button.clicked.connect(lambda: self.process_deletion(permanent=False))
        delete_button = QPushButton("Xóa vĩnh viễn")
        delete_button.setObjectName("DangerButton")
        delete_button.clicked.connect(lambda: self.process_deletion(permanent=True))
        footer.addWidget(cancel_button)
        footer.addWidget(trash_button)
        footer.addWidget(delete_button)
        layout.addLayout(footer)
        self.update_selection_summary()

    def selected_files_to_remove(self):
        selected = []
        for group, button_group in zip(self.duplicates, self.group_buttons):
            checked = button_group.checkedButton()
            if checked is None or checked.file_path is None:
                continue
            selected.extend(path for path in group if path != checked.file_path)
        return selected

    def update_selection_summary(self, *_args):
        selected = self.selected_files_to_remove()
        reclaimable = 0
        for path in selected:
            try:
                reclaimable += path.stat().st_size
            except OSError:
                pass
        self.selection_summary.setText(
            f"Sẽ xử lý {len(selected)} tệp · có thể giải phóng {format_bytes(reclaimable)}"
        )

    def process_deletion(self, permanent=False):
        files_to_remove = self.selected_files_to_remove()
        if not files_to_remove:
            QMessageBox.information(self, "Không có thay đổi", "Bạn đang bỏ qua tất cả các nhóm.")
            return

        if permanent:
            reply = QMessageBox.warning(
                self,
                "Xóa vĩnh viễn",
                f"Xóa vĩnh viễn {len(files_to_remove)} tệp? Thao tác này không thể hoàn tác.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
        else:
            reply = QMessageBox.question(
                self,
                "Chuyển vào thùng rác",
                f"Chuyển {len(files_to_remove)} tệp vào PADOrganizer_Trash? Bạn có thể lấy lại chúng sau.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
        if reply != QMessageBox.StandardButton.Yes:
            return

        success = 0
        errors = 0
        if permanent:
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    self.logger.log(f"PERMANENT DELETED: {file_path.name}")
                    success += 1
                except Exception as exc:
                    self.logger.log(f"PERM DELETE ERROR: {file_path.name} - {exc}")
                    errors += 1
        else:
            PAD_TRASH_DIR.mkdir(parents=True, exist_ok=True)
            self.mover.start_batch()
            for file_path in files_to_remove:
                try:
                    new_path = self.mover.move_file(file_path, PAD_TRASH_DIR, sort_by_date=False)
                    self.logger.log(f"TRASHED: {file_path.name} -> {new_path.name}")
                    success += 1
                except Exception as exc:
                    self.logger.log(f"TRASH ERROR: {file_path.name} - {exc}")
                    errors += 1
            self.mover.end_batch()

        QMessageBox.information(
            self,
            "Đã xử lý xong",
            f"Thành công: {success}\nLỗi: {errors}",
        )
        self.accept()


class TitleBar(QFrame):
    def __init__(self, window):
        super().__init__(window)
        self.host_window = window
        self.setObjectName("TitleBar")
        self.setFixedHeight(46)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 0, 0)
        layout.setSpacing(9)

        mark = QFrame()
        mark.setObjectName("TitleBrandMark")
        mark.setFixedSize(24, 24)
        mark_layout = QVBoxLayout(mark)
        mark_layout.setContentsMargins(0, 0, 0, 0)
        mark_text = QLabel("P")
        mark_text.setObjectName("TitleBrandLetter")
        mark_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark_text.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        mark_layout.addWidget(mark_text)
        layout.addWidget(mark)

        title = QLabel(APP_NAME)
        title.setObjectName("WindowTitle")
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(title)

        separator = QLabel("/")
        separator.setObjectName("WindowTitleSeparator")
        separator.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(separator)

        caption = QLabel("Personal Archive Directory Organizer")
        caption.setObjectName("WindowCaption")
        caption.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(caption)
        layout.addStretch()

        self.minimize_button = self.make_control("−", "Thu nhỏ")
        self.maximize_button = self.make_control("□", "Phóng to")
        self.close_button = self.make_control("×", "Đóng", close_button=True)
        self.minimize_button.clicked.connect(window.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximized)
        self.close_button.clicked.connect(window.close)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def make_control(self, text, tooltip, close_button=False):
        button = QPushButton(text)
        button.setObjectName("CloseControl" if close_button else "WindowControl")
        button.setFixedSize(48, 46)
        button.setToolTip(tooltip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def toggle_maximized(self):
        if self.host_window.isMaximized():
            self.host_window.showNormal()
        else:
            self.host_window.showMaximized()
        self.update_maximize_button()

    def update_maximize_button(self):
        maximized = self.host_window.isMaximized()
        self.maximize_button.setText("❐" if maximized else "□")
        self.maximize_button.setToolTip("Khôi phục" if maximized else "Phóng to")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            window_handle = self.host_window.windowHandle()
            if window_handle is not None:
                window_handle.startSystemMove()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximized()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.logger = PADLogger()
        self.mover = FileMover()
        self.target_dir = ""
        self.is_busy = False
        self.shortcuts = []
        self.update_check_worker = None
        self.update_download_worker = None
        self.pending_update_release = None
        self.init_ui()
        self.install_shortcuts()
        self.refresh_rule_summary()
        self.refresh_directory_summary()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(APP_FULL_NAME)
        self.setMinimumSize(980, 700)
        self.resize(1220, 820)
        self.setAcceptDrops(True)

        icon_path = get_resource_path("logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        root = QWidget()
        root.setObjectName("AppRoot")
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        root_layout.addWidget(self.title_bar)

        body = QWidget()
        body.setObjectName("WindowBody")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        self.build_sidebar(body_layout)
        self.build_content(body_layout)
        root_layout.addWidget(body, 1)

        self.resize_grip = QSizeGrip(root)
        self.resize_grip.setObjectName("ResizeGrip")
        self.resize_grip.setFixedSize(18, 18)
        self.resize_grip.raise_()

    def build_sidebar(self, root_layout):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(238)
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(22, 24, 22, 22)
        side_layout.setSpacing(8)

        brand = QHBoxLayout()
        brand.setSpacing(11)
        mark = QFrame()
        mark.setObjectName("BrandMark")
        mark.setFixedSize(43, 43)
        mark_layout = QVBoxLayout(mark)
        mark_layout.setContentsMargins(0, 0, 0, 0)
        mark_letter = QLabel("P")
        mark_letter.setObjectName("BrandLetter")
        mark_letter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark_layout.addWidget(mark_letter)
        brand_text = QVBoxLayout()
        brand_text.setSpacing(0)
        brand_title = QLabel(APP_NAME)
        brand_title.setObjectName("BrandTitle")
        brand_caption = QLabel("PERSONAL ARCHIVE")
        brand_caption.setObjectName("BrandCaption")
        brand_text.addWidget(brand_title)
        brand_text.addWidget(brand_caption)
        brand.addWidget(mark)
        brand.addLayout(brand_text)
        brand.addStretch()
        side_layout.addLayout(brand)
        side_layout.addSpacing(30)

        section = QLabel("KHÔNG GIAN LÀM VIỆC")
        section.setObjectName("SidebarSection")
        side_layout.addWidget(section)

        dashboard_button = QPushButton("Tổng quan")
        dashboard_button.setObjectName("SidebarActive")
        dashboard_button.setCursor(Qt.CursorShape.PointingHandCursor)
        side_layout.addWidget(dashboard_button)

        self.side_rules_button = QPushButton("Quy tắc phân loại")
        self.side_rules_button.setObjectName("SidebarButton")
        self.side_rules_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.side_rules_button.clicked.connect(self.open_settings)
        side_layout.addWidget(self.side_rules_button)

        self.btn_open_trash = QPushButton("Mở thùng rác")
        self.btn_open_trash.setObjectName("SidebarButton")
        self.btn_open_trash.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_trash.clicked.connect(self.open_trash)
        side_layout.addWidget(self.btn_open_trash)

        side_layout.addSpacing(14)
        maintenance_section = QLabel("BẢO TRÌ")
        maintenance_section.setObjectName("SidebarSection")
        side_layout.addWidget(maintenance_section)

        self.btn_check_updates = QPushButton("Kiểm tra cập nhật")
        self.btn_check_updates.setObjectName("SidebarButton")
        self.btn_check_updates.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check_updates.setToolTip("Chỉ kết nối GitHub khi bạn chủ động kiểm tra")
        self.btn_check_updates.clicked.connect(self.check_for_updates)
        side_layout.addWidget(self.btn_check_updates)

        self.btn_empty_trash = QPushButton("Dọn sạch thùng rác")
        self.btn_empty_trash.setObjectName("SidebarDanger")
        self.btn_empty_trash.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_empty_trash.clicked.connect(self.empty_trash)
        side_layout.addWidget(self.btn_empty_trash)

        self.btn_clear_logs = QPushButton("Xóa nhật ký")
        self.btn_clear_logs.setObjectName("SidebarButton")
        self.btn_clear_logs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear_logs.setToolTip("Xóa toàn bộ nhật ký hoạt động đang lưu trên máy")
        self.btn_clear_logs.clicked.connect(self.clear_logs)
        side_layout.addWidget(self.btn_clear_logs)

        side_layout.addStretch()
        version_label = QLabel(f"PADOrganizer  ·  v{APP_VERSION}")
        version_label.setObjectName("VersionLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(version_label)
        side_layout.addSpacing(4)
        privacy = QFrame()
        privacy.setObjectName("PrivacyCard")
        privacy_layout = QVBoxLayout(privacy)
        privacy_layout.setContentsMargins(15, 14, 15, 14)
        privacy_layout.setSpacing(6)
        privacy_header = QHBoxLayout()
        privacy_header.setSpacing(8)
        privacy_dot = QLabel("•")
        privacy_dot.setObjectName("PrivacyDot")
        privacy_title = QLabel("Riêng tư tuyệt đối")
        privacy_title.setObjectName("PrivacyTitle")
        privacy_header.addWidget(privacy_dot)
        privacy_header.addWidget(privacy_title)
        privacy_header.addStretch()
        privacy_hint = QLabel(
            "Tệp cá nhân luôn ở trên thiết bị.\nChỉ kết nối GitHub khi bạn kiểm tra cập nhật."
        )
        privacy_hint.setObjectName("PrivacyText")
        privacy_hint.setWordWrap(True)
        privacy_layout.addLayout(privacy_header)
        privacy_layout.addWidget(privacy_hint)
        side_layout.addWidget(privacy)
        root_layout.addWidget(self.sidebar)

    def build_content(self, root_layout):
        scroll = QScrollArea()
        scroll.setObjectName("MainScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("ScrollContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(34, 28, 34, 32)
        layout.setSpacing(20)

        header = QHBoxLayout()
        heading = QVBoxLayout()
        heading.setSpacing(3)
        eyebrow = QLabel("TRUNG TÂM SẮP XẾP")
        eyebrow.setObjectName("PageEyebrow")
        title = QLabel("Không gian của bạn, ngăn nắp hơn.")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Một luồng làm việc rõ ràng để phân loại, tìm bản trùng và khôi phục khi cần.")
        subtitle.setObjectName("PageSubtitle")
        heading.addWidget(eyebrow)
        heading.addWidget(title)
        heading.addWidget(subtitle)
        header.addLayout(heading)
        header.addStretch()
        self.status_pill = QLabel("Sẵn sàng")
        self.status_pill.setObjectName("StatusPill")
        self.status_pill.setProperty("state", "ready")
        header.addWidget(self.status_pill, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(header)

        hero = QFrame()
        hero.setObjectName("HeroCard")
        self.hero_layout = QHBoxLayout(hero)
        self.hero_layout.setContentsMargins(28, 25, 28, 25)
        self.hero_layout.setSpacing(24)
        hero_copy = QVBoxLayout()
        hero_copy.setSpacing(7)
        hero_kicker = QLabel("PADORGANIZER · LOCAL FIRST")
        hero_kicker.setObjectName("HeroKicker")
        hero_title = QLabel("Dọn một lần. Nhẹ đầu cả ngày.")
        hero_title.setObjectName("HeroTitle")
        hero_text = QLabel(
            "Chọn một thư mục, xem nhanh quy mô và để PADOrganizer đưa từng tệp về đúng chỗ."
        )
        hero_text.setObjectName("HeroText")
        hero_text.setWordWrap(True)
        hero_copy.addWidget(hero_kicker)
        hero_copy.addWidget(hero_title)
        hero_copy.addWidget(hero_text)
        hero_copy.addStretch()
        self.hero_layout.addLayout(hero_copy, 1)

        metrics = QHBoxLayout()
        metrics.setSpacing(10)
        folder_metric, self.hero_folder_value = self.make_hero_metric(
            "THƯ MỤC", "Chưa chọn", width=166
        )
        rules_metric, self.hero_rules_value = self.make_hero_metric("NHÓM QUY TẮC", "0")
        files_metric, self.hero_files_value = self.make_hero_metric("TỆP SẴN SÀNG", "—", accent=True)
        metrics.addWidget(folder_metric, 0, Qt.AlignmentFlag.AlignVCenter)
        metrics.addWidget(rules_metric, 0, Qt.AlignmentFlag.AlignVCenter)
        metrics.addWidget(files_metric, 0, Qt.AlignmentFlag.AlignVCenter)
        metrics.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hero_layout.addLayout(metrics)
        add_shadow(hero, 40, 12, 42)
        layout.addWidget(hero)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(18)
        source_card = self.build_source_card()
        tool_card = self.build_tool_card()
        self.cards_layout.addWidget(source_card, 5)
        self.cards_layout.addWidget(tool_card, 3)
        layout.addLayout(self.cards_layout)

        action_dock = self.build_action_dock()
        layout.addWidget(action_dock)
        layout.addStretch()

        scroll.setWidget(content)
        root_layout.addWidget(scroll, 1)
        self.apply_responsive_layout()

    def make_hero_metric(self, label_text, value_text, accent=False, width=132):
        frame = QFrame()
        frame.setObjectName("HeroMetricAccent" if accent else "HeroMetric")
        frame.setFixedSize(width, 96)
        metric_layout = QVBoxLayout(frame)
        metric_layout.setContentsMargins(14, 11, 14, 11)
        metric_layout.setSpacing(4)
        metric_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        value = QLabel(value_text)
        value.setObjectName("HeroMetricValueDark" if accent else "HeroMetricValue")
        value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label = QLabel(label_text)
        label.setObjectName("HeroMetricLabelDark" if accent else "HeroMetricLabel")
        metric_layout.addWidget(value)
        metric_layout.addWidget(label)
        return frame, value

    def build_source_card(self):
        card = QFrame()
        card.setObjectName("SourceCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 20, 22, 20)
        card_layout.setSpacing(14)

        heading = QHBoxLayout()
        text = QVBoxLayout()
        text.setSpacing(3)
        badge = QLabel("BƯỚC 01")
        badge.setObjectName("StepBadge")
        badge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        title = QLabel("Chọn không gian cần sắp xếp")
        title.setObjectName("CardTitle")
        description = QLabel("Chỉ các tệp nằm trực tiếp trong thư mục được xử lý.")
        description.setObjectName("CardText")
        text.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
        text.addWidget(title)
        text.addWidget(description)
        heading.addLayout(text)
        heading.addStretch()
        card_layout.addLayout(heading)

        self.dropzone = QFrame()
        self.dropzone.setObjectName("DropZone")
        self.dropzone.setProperty("selected", False)
        self.dropzone.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dropzone.mousePressEvent = self.on_dropzone_click
        drop_layout = QHBoxLayout(self.dropzone)
        drop_layout.setContentsMargins(16, 15, 16, 15)
        drop_layout.setSpacing(13)

        folder_mark = QFrame()
        folder_mark.setObjectName("FolderMark")
        folder_mark.setFixedSize(46, 46)
        folder_mark_layout = QVBoxLayout(folder_mark)
        folder_mark_layout.setContentsMargins(0, 0, 0, 0)
        folder_letter = QLabel("D")
        folder_letter.setObjectName("FolderMarkText")
        folder_letter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        folder_mark_layout.addWidget(folder_letter)
        drop_layout.addWidget(folder_mark)

        drop_copy = QVBoxLayout()
        drop_copy.setSpacing(2)
        self.folder_title_label = QLabel("Kéo thả thư mục vào đây")
        self.folder_title_label.setObjectName("DropTitle")
        self.folder_path_label = QLabel("hoặc chọn từ máy tính của bạn")
        self.folder_path_label.setObjectName("DropPath")
        self.folder_path_label.setWordWrap(True)
        drop_copy.addWidget(self.folder_title_label)
        drop_copy.addWidget(self.folder_path_label)
        drop_layout.addLayout(drop_copy, 1)

        self.btn_select = QPushButton("Chọn thư mục")
        self.btn_select.setObjectName("SecondaryButton")
        self.btn_select.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select.clicked.connect(self.select_directory)
        drop_layout.addWidget(self.btn_select)
        card_layout.addWidget(self.dropzone)

        stats = QHBoxLayout()
        stats.setSpacing(10)
        file_stat, self.file_count_label = self.make_mini_stat("TỆP TRỰC TIẾP")
        size_stat, self.total_size_label = self.make_mini_stat("TỔNG DUNG LƯỢNG")
        stats.addWidget(file_stat)
        stats.addWidget(size_stat)
        card_layout.addLayout(stats)
        add_shadow(card, 30, 8, 25)
        return card

    def make_mini_stat(self, label_text):
        frame = QFrame()
        frame.setObjectName("MiniStat")
        stat_layout = QVBoxLayout(frame)
        stat_layout.setContentsMargins(13, 10, 13, 10)
        stat_layout.setSpacing(1)
        value = QLabel("—")
        value.setObjectName("MiniStatValue")
        label = QLabel(label_text)
        label.setObjectName("MiniStatLabel")
        stat_layout.addWidget(value)
        stat_layout.addWidget(label)
        return frame, value

    def build_tool_card(self):
        card = QFrame()
        card.setObjectName("ToolCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(12)

        badge = QLabel("BƯỚC 02")
        badge.setObjectName("StepBadge")
        badge.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        title = QLabel("Tinh chỉnh cách tổ chức")
        title.setObjectName("CardTitle")
        description = QLabel("Mặc định an toàn, đủ linh hoạt khi bạn cần.")
        description.setObjectName("CardText")
        layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)
        layout.addWidget(description)

        date_row = QFrame()
        date_row.setObjectName("OptionRow")
        date_layout = QHBoxLayout(date_row)
        date_layout.setContentsMargins(13, 11, 13, 11)
        date_copy = QVBoxLayout()
        date_copy.setSpacing(1)
        date_title = QLabel("Chia theo Năm–Tháng")
        date_title.setObjectName("OptionTitle")
        date_text = QLabel("Tạo thêm tầng 2026-08 trong mỗi nhóm")
        date_text.setObjectName("OptionText")
        date_copy.addWidget(date_title)
        date_copy.addWidget(date_text)
        self.date_toggle = ToggleSwitch()
        self.date_toggle.setChecked(self.config_manager.is_sort_by_date_enabled())
        self.date_toggle.toggled.connect(self.save_date_setting)
        date_layout.addLayout(date_copy, 1)
        date_layout.addWidget(self.date_toggle)
        layout.addWidget(date_row)

        rules_row = QFrame()
        rules_row.setObjectName("OptionRow")
        rules_layout = QHBoxLayout(rules_row)
        rules_layout.setContentsMargins(13, 11, 13, 11)
        rules_copy = QVBoxLayout()
        rules_copy.setSpacing(1)
        rules_title = QLabel("Bộ quy tắc hiện tại")
        rules_title.setObjectName("OptionTitle")
        self.rules_summary_label = QLabel("Đang tải...")
        self.rules_summary_label.setObjectName("OptionText")
        rules_copy.addWidget(rules_title)
        rules_copy.addWidget(self.rules_summary_label)
        self.quick_rules_button = QPushButton("Quản lý")
        self.quick_rules_button.setObjectName("LinkButton")
        self.quick_rules_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quick_rules_button.clicked.connect(self.open_settings)
        rules_layout.addLayout(rules_copy, 1)
        rules_layout.addWidget(self.quick_rules_button)
        layout.addWidget(rules_row)

        trash_row = QFrame()
        trash_row.setObjectName("OptionRow")
        trash_layout = QHBoxLayout(trash_row)
        trash_layout.setContentsMargins(13, 11, 13, 11)
        trash_copy = QVBoxLayout()
        trash_copy.setSpacing(1)
        trash_title = QLabel("Thùng rác nội bộ")
        trash_title.setObjectName("OptionTitle")
        self.trash_summary_label = QLabel("Đang kiểm tra...")
        self.trash_summary_label.setObjectName("OptionText")
        trash_copy.addWidget(trash_title)
        trash_copy.addWidget(self.trash_summary_label)
        self.trash_badge = QLabel("TRỐNG")
        self.trash_badge.setObjectName("OptionBadge")
        trash_layout.addLayout(trash_copy, 1)
        trash_layout.addWidget(self.trash_badge)
        layout.addWidget(trash_row)
        layout.addStretch()
        add_shadow(card, 30, 8, 25)
        return card

    def build_action_dock(self):
        dock = QFrame()
        dock.setObjectName("ActionDock")
        layout = QHBoxLayout(dock)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(18)

        status_area = QVBoxLayout()
        status_area.setSpacing(6)
        self.action_title_label = QLabel("Sẵn sàng khi bạn sẵn sàng")
        self.action_title_label.setObjectName("ActionTitle")
        self.status_label = QLabel("Chọn một thư mục để bắt đầu")
        self.status_label.setObjectName("ActionStatus")
        progress_header = QHBoxLayout()
        progress_header.addWidget(self.status_label)
        progress_header.addStretch()
        self.percent_label = QLabel("0%")
        self.percent_label.setObjectName("PercentText")
        progress_header.addWidget(self.percent_label)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        status_area.addWidget(self.action_title_label)
        status_area.addLayout(progress_header)
        status_area.addWidget(self.progress)
        layout.addLayout(status_area, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(9)
        self.btn_undo = QPushButton("Hoàn tác")
        self.btn_undo.setObjectName("DarkButton")
        self.btn_undo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_undo.clicked.connect(self.undo_action)
        self.btn_dedupe = QPushButton("Tìm bản trùng")
        self.btn_dedupe.setObjectName("DarkButton")
        self.btn_dedupe.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_dedupe.clicked.connect(self.run_dedupe)
        self.btn_run = QPushButton("Tổ chức ngay")
        self.btn_run.setObjectName("PrimaryButton")
        self.btn_run.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_run.clicked.connect(self.run_organizer)
        buttons.addWidget(self.btn_undo)
        buttons.addWidget(self.btn_dedupe)
        buttons.addWidget(self.btn_run)
        layout.addLayout(buttons)
        add_shadow(dock, 38, 10, 38)
        return dock

    def install_shortcuts(self):
        shortcut_map = {
            "Ctrl+O": self.select_directory,
            "Ctrl+Return": self.run_organizer,
            "Ctrl+D": self.run_dedupe,
            "Ctrl+Z": self.undo_action,
            "Ctrl+,": self.open_settings,
        }
        for sequence, callback in shortcut_map.items():
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(callback)
            self.shortcuts.append(shortcut)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "cards_layout"):
            self.apply_responsive_layout()
        if hasattr(self, "title_bar"):
            self.title_bar.update_maximize_button()
        if hasattr(self, "resize_grip"):
            self.resize_grip.move(self.width() - 18, self.height() - 18)
            self.resize_grip.setVisible(not self.isMaximized())

    def apply_responsive_layout(self):
        compact = self.width() < 1200
        direction = (
            QBoxLayout.Direction.TopToBottom
            if compact
            else QBoxLayout.Direction.LeftToRight
        )
        self.hero_layout.setDirection(direction)
        self.cards_layout.setDirection(direction)
        self.hero_layout.setSpacing(16 if compact else 24)
        self.cards_layout.setSpacing(14 if compact else 18)
        self.sidebar.setFixedWidth(238)

    def on_dropzone_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_busy:
            self.select_directory()

    def dragEnterEvent(self, event):
        if self.is_busy:
            event.ignore()
            return
        urls = event.mimeData().urls()
        if any(Path(url.toLocalFile()).is_dir() for url in urls):
            event.acceptProposedAction()
            self.dropzone.setProperty("selected", True)
            refresh_style(self.dropzone)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.dropzone.setProperty("selected", bool(self.target_dir))
        refresh_style(self.dropzone)
        event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_dir():
                self.set_target_directory(path)
                event.acceptProposedAction()
                return
        event.ignore()

    def set_target_directory(self, folder):
        path = Path(folder).resolve()
        if not path.is_dir():
            QMessageBox.warning(self, "Thư mục không hợp lệ", "Không thể truy cập thư mục đã chọn.")
            return
        if path == BASE_DIR.resolve():
            QMessageBox.warning(
                self,
                "Không thể chọn thư mục ứng dụng",
                "Để bảo vệ chương trình và dữ liệu cấu hình, hãy chọn một thư mục khác.",
            )
            return
        self.target_dir = str(path)
        self.refresh_directory_summary()
        self.set_status_pill("Đã chọn thư mục", "ready")
        self.action_title_label.setText("Thư mục đã sẵn sàng")
        self.status_label.setText("Chọn “Tổ chức ngay” hoặc kiểm tra các tệp trùng lặp")

    def refresh_directory_summary(self):
        if not self.target_dir:
            self.folder_title_label.setText("Kéo thả thư mục vào đây")
            self.folder_path_label.setText("hoặc chọn từ máy tính của bạn")
            self.folder_path_label.setToolTip("")
            self.file_count_label.setText("—")
            self.total_size_label.setText("—")
            self.hero_folder_value.setText("Chưa chọn")
            self.hero_folder_value.setToolTip("")
            self.hero_files_value.setText("—")
            self.dropzone.setProperty("selected", False)
            refresh_style(self.dropzone)
            self.set_ui_enabled(True)
            self.check_trash_exists()
            return

        path = Path(self.target_dir)
        try:
            files = [item for item in path.iterdir() if item.is_file()]
            total_size = sum(item.stat().st_size for item in files)
        except OSError as exc:
            QMessageBox.critical(self, "Không thể đọc thư mục", str(exc))
            self.target_dir = ""
            self.refresh_directory_summary()
            return

        display_name = path.name or str(path)
        self.folder_title_label.setText(display_name)
        self.folder_path_label.setText(str(path))
        self.folder_path_label.setToolTip(str(path))
        self.file_count_label.setText(f"{len(files):,}")
        self.total_size_label.setText(format_bytes(total_size))
        self.hero_folder_value.setText(display_name[:12] + ("…" if len(display_name) > 12 else ""))
        self.hero_folder_value.setToolTip(str(path))
        self.hero_files_value.setText(f"{len(files):,}")
        self.dropzone.setProperty("selected", True)
        refresh_style(self.dropzone)
        self.set_ui_enabled(True)
        self.check_trash_exists()

    def refresh_rule_summary(self):
        file_map = self.config_manager.get_file_map()
        rule_count = len(file_map)
        extension_count = sum(len(extensions) for extensions in file_map.values())
        self.hero_rules_value.setText(str(rule_count))
        self.rules_summary_label.setText(f"{rule_count} nhóm · {extension_count} phần mở rộng")

    def set_status_pill(self, text, state="ready"):
        self.status_pill.setText(text)
        self.status_pill.setProperty("state", state)
        refresh_style(self.status_pill)

    def save_date_setting(self, checked):
        self.config_manager.set_sort_by_date(bool(checked))

    def select_directory(self):
        if self.is_busy:
            return
        start_path = self.target_dir or str(Path.home())
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục cần sắp xếp", start_path)
        if folder:
            self.set_target_directory(folder)

    def check_trash_exists(self):
        has_content = False
        file_count = 0
        if PAD_TRASH_DIR.exists():
            try:
                entries = list(PAD_TRASH_DIR.iterdir())
                has_content = bool(entries)
                file_count = sum(1 for entry in entries if entry.is_file())
            except OSError:
                has_content = False
        self.trash_badge.setText("CÓ TỆP" if has_content else "TRỐNG")
        self.trash_summary_label.setText(
            f"{file_count} tệp đang chờ xử lý" if has_content else "Không có tệp đang lưu tạm"
        )
        self.btn_empty_trash.setEnabled(has_content and not self.is_busy)

    def check_logs_exist(self):
        self.btn_clear_logs.setEnabled(not self.is_busy and self.logger.has_logs())

    def open_trash(self):
        PAD_TRASH_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(PAD_TRASH_DIR))
        except AttributeError:
            import subprocess

            subprocess.call(["explorer", str(PAD_TRASH_DIR)])
        except OSError as exc:
            QMessageBox.critical(self, "Không thể mở thùng rác", str(exc))

    def open_settings(self):
        if self.is_busy:
            return
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_rule_summary()
            self.set_status_pill("Đã lưu quy tắc", "ready")

    def set_ui_enabled(self, enabled):
        self.is_busy = not enabled
        has_target = bool(self.target_dir)
        self.btn_run.setEnabled(enabled and has_target)
        self.btn_dedupe.setEnabled(enabled and has_target)
        self.btn_undo.setEnabled(enabled and self.mover.has_history())
        self.btn_select.setEnabled(enabled)
        self.date_toggle.setEnabled(enabled)
        self.quick_rules_button.setEnabled(enabled)
        self.side_rules_button.setEnabled(enabled)
        self.btn_open_trash.setEnabled(enabled)
        self.btn_check_updates.setEnabled(enabled)
        self.check_trash_exists()
        self.check_logs_exist()

    def begin_operation(self, title, status):
        self.set_ui_enabled(False)
        self.set_status_pill("Đang xử lý", "busy")
        self.action_title_label.setText(title)
        self.status_label.setText(status)
        self.progress.setValue(0)
        self.percent_label.setText("0%")

    def run_organizer(self):
        if self.is_busy:
            return
        if not self.target_dir:
            QMessageBox.information(self, "Chọn thư mục", "Hãy chọn thư mục bạn muốn tổ chức trước.")
            return
        self.begin_operation("Đang tổ chức thư mục", "Chuẩn bị phân loại tệp...")
        self.mover.start_batch()
        self.worker = WorkerThread(
            self.target_dir,
            self.config_manager.get_file_map(),
            self.mover,
            self.logger,
            self.date_toggle.isChecked(),
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.completed.connect(self.organize_finished)
        self.worker.failed.connect(self.operation_failed)
        self.worker.start()

    def update_progress(self, current, total, name):
        percent = int((current / total) * 100) if total else 100
        self.progress.setValue(percent)
        self.percent_label.setText(f"{percent}%")
        self.status_label.setText(f"Đang xử lý: {name}")

    def organize_finished(self, success, errors):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        self.percent_label.setText("100%")
        self.refresh_directory_summary()
        if success == 0 and errors == 0:
            self.action_title_label.setText("Thư mục đã gọn sẵn")
            self.status_label.setText("Không có tệp trực tiếp nào cần phân loại")
            self.set_status_pill("Không có thay đổi", "ready")
            QMessageBox.information(self, "Không có tệp cần xử lý", "Thư mục này đã sẵn sàng.")
            return
        self.action_title_label.setText("Tổ chức hoàn tất")
        self.status_label.setText(f"Đã di chuyển {success} tệp · {errors} lỗi")
        self.set_status_pill("Hoàn tất", "ready" if errors == 0 else "warning")
        QMessageBox.information(
            self,
            "Đã tổ chức xong",
            f"Di chuyển thành công: {success}\nLỗi: {errors}\n\nBạn có thể hoàn tác ngay trong phiên này.",
        )

    def operation_failed(self, message):
        self.set_ui_enabled(True)
        self.progress.setValue(0)
        self.percent_label.setText("0%")
        self.action_title_label.setText("Không thể hoàn thành")
        self.status_label.setText(message)
        self.set_status_pill("Cần kiểm tra", "warning")
        QMessageBox.critical(self, "Thao tác thất bại", message)

    def undo_action(self):
        if self.is_busy or not self.mover.has_history():
            return
        reply = QMessageBox.question(
            self,
            "Hoàn tác lần gần nhất",
            "Đưa các tệp của lần xử lý gần nhất trở về vị trí cũ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self.logger.log("--- BẮT ĐẦU HOÀN TÁC ---")
        success, errors = self.mover.undo_last_operation(self.logger)
        self.logger.log("--- KẾT THÚC HOÀN TÁC ---")
        self.refresh_directory_summary()
        self.set_ui_enabled(True)
        self.action_title_label.setText("Đã hoàn tác")
        self.status_label.setText(f"Khôi phục {success} tệp · {errors} lỗi")
        self.set_status_pill("Đã khôi phục", "ready" if errors == 0 else "warning")
        QMessageBox.information(self, "Hoàn tác hoàn tất", f"Khôi phục: {success}\nLỗi: {errors}")

    def empty_trash(self):
        if self.is_busy or not PAD_TRASH_DIR.exists():
            return
        try:
            has_content = any(PAD_TRASH_DIR.iterdir())
        except OSError:
            has_content = False
        if not has_content:
            self.check_trash_exists()
            return
        reply = QMessageBox.warning(
            self,
            "Dọn sạch thùng rác",
            "Xóa vĩnh viễn toàn bộ nội dung trong PADOrganizer_Trash? Thao tác này không thể hoàn tác.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            shutil.rmtree(PAD_TRASH_DIR)
            self.logger.log("EMPTY TRASH: Đã xóa vĩnh viễn thùng rác.")
            self.check_trash_exists()
            self.set_status_pill("Đã dọn thùng rác", "ready")
            QMessageBox.information(self, "Thùng rác đã trống", "Toàn bộ nội dung đã được xóa.")
        except Exception as exc:
            QMessageBox.critical(self, "Không thể dọn thùng rác", str(exc))

    def clear_logs(self):
        if self.is_busy:
            return
        if not self.logger.has_logs():
            self.check_logs_exist()
            AppMessageDialog(
                "Bảo trì",
                "Nhật ký đang trống",
                "Không có nhật ký hoạt động nào cần dọn dẹp vào lúc này.",
                "Đã hiểu",
                variant="info",
                parent=self,
            ).exec()
            return

        dialog = AppMessageDialog(
            "Bảo trì dữ liệu",
            "Xóa toàn bộ nhật ký hoạt động?",
            "Nhật ký đang lưu trên máy sẽ được dọn sạch. Tệp cá nhân và cấu hình phân loại của bạn không bị ảnh hưởng.",
            "Xóa nhật ký",
            "Giữ lại",
            variant="danger",
            parent=self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            self.logger.clear_logs()
            self.check_logs_exist()
            self.set_status_pill("Đã xóa nhật ký", "ready")
            AppMessageDialog(
                "Hoàn tất",
                "Nhật ký đã được dọn sạch",
                "PADOrganizer đã xóa nhật ký hoạt động. Tệp và cấu hình của bạn vẫn được giữ nguyên.",
                "Đã hiểu",
                variant="success",
                parent=self,
            ).exec()
        except OSError as exc:
            QMessageBox.critical(self, "Không thể xóa nhật ký", str(exc))

    def check_for_updates(self):
        if self.is_busy:
            return
        self.begin_operation("Đang kiểm tra cập nhật", "Kết nối GitHub theo yêu cầu của bạn...")
        self.progress.setValue(15)
        self.percent_label.setText("…")
        self.update_check_worker = UpdateCheckThread()
        self.update_check_worker.completed.connect(self.update_check_finished)
        self.update_check_worker.failed.connect(self.update_operation_failed)
        self.update_check_worker.finished.connect(self.update_check_worker.deleteLater)
        self.update_check_worker.start()

    def update_check_finished(self, release):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        self.percent_label.setText("100%")
        if not is_newer_version(release.version, APP_VERSION):
            self.action_title_label.setText("Không có bản phát hành mới hơn")
            self.status_label.setText(f"Phiên bản đang sử dụng · v{APP_VERSION}")
            self.set_status_pill("Mới nhất", "ready")
            self.logger.log(f"UPDATE CHECK: Không có bản mới hơn v{APP_VERSION}.")
            AppMessageDialog(
                "Cập nhật",
                "Bạn đang dùng phiên bản mới nhất",
                f"PADOrganizer v{APP_VERSION} hiện đã là bản phát hành mới nhất trên GitHub.",
                "Đã hiểu",
                variant="success",
                parent=self,
            ).exec()
            return

        self.pending_update_release = release
        self.action_title_label.setText(f"Đã có PADOrganizer v{release.version}")
        self.status_label.setText("Xem nội dung thay đổi và cập nhật khi bạn sẵn sàng")
        self.set_status_pill("Có bản mới", "warning")
        self.logger.log(f"UPDATE AVAILABLE: v{APP_VERSION} -> v{release.version}")

        installed_build = is_installed_build()
        dialog = UpdateDialog(release, installed_build, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        if not installed_build:
            if not QDesktopServices.openUrl(QUrl(release.page_url)):
                QMessageBox.warning(
                    self,
                    "Không thể mở trình duyệt",
                    f"Hãy mở trang sau để tải bản mới:\n{release.page_url}",
                )
            return
        self.download_update(release)

    def download_update(self, release):
        self.begin_operation(
            f"Đang tải PADOrganizer v{release.version}",
            "Chuẩn bị tải Installer từ GitHub...",
        )
        self.pending_update_release = release
        self.update_download_worker = UpdateDownloadThread(release)
        self.update_download_worker.progress.connect(self.update_download_progress)
        self.update_download_worker.completed.connect(self.update_download_finished)
        self.update_download_worker.failed.connect(self.update_operation_failed)
        self.update_download_worker.finished.connect(self.update_download_worker.deleteLater)
        self.update_download_worker.start()

    def update_download_progress(self, current, total):
        percent = int((current / total) * 100) if total else 0
        self.progress.setValue(percent)
        self.percent_label.setText(f"{percent}%" if total else "…")
        if total:
            self.status_label.setText(f"Đã tải {format_bytes(current)} / {format_bytes(total)}")
        else:
            self.status_label.setText(f"Đã tải {format_bytes(current)}")

    def update_download_finished(self, installer_path):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        self.percent_label.setText("100%")
        self.action_title_label.setText("Bản cập nhật đã sẵn sàng")
        self.status_label.setText("Installer đã tải xong và khớp mã SHA-256")
        self.set_status_pill("Đã xác minh", "ready")

        release = self.pending_update_release
        version_text = release.version if release else "mới"
        reply = QMessageBox.question(
            self,
            "Cài đặt bản cập nhật",
            f"PADOrganizer v{version_text} đã được tải và xác minh thành công.\n\n"
            "Cài đặt ngay bây giờ? PADOrganizer sẽ đóng và mở trình cài đặt.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply != QMessageBox.StandardButton.Yes:
            try:
                Path(installer_path).unlink()
            except OSError:
                pass
            self.status_label.setText("Bạn có thể kiểm tra và tải lại bất cứ lúc nào")
            self.set_status_pill("Để sau", "ready")
            return

        try:
            launch_installer(installer_path)
        except UpdateError as exc:
            self.update_operation_failed(str(exc))
            return

        self.logger.log(f"UPDATE INSTALL: Đã mở Installer v{version_text}.")
        self.is_busy = False
        QApplication.instance().quit()

    def update_operation_failed(self, message):
        self.set_ui_enabled(True)
        self.progress.setValue(0)
        self.percent_label.setText("0%")
        self.action_title_label.setText("Không thể cập nhật")
        self.status_label.setText(message)
        self.set_status_pill("Thử lại sau", "warning")
        self.logger.log(f"UPDATE ERROR: {message}")
        QMessageBox.warning(self, "Không thể cập nhật", message)

    def run_dedupe(self):
        if self.is_busy:
            return
        if not self.target_dir:
            QMessageBox.information(self, "Chọn thư mục", "Hãy chọn thư mục cần kiểm tra trước.")
            return
        self.begin_operation("Đang tìm các bản trùng", "Đọc và đối chiếu nội dung tệp...")
        self.dedupe_worker = DedupeThread(self.target_dir)
        self.dedupe_worker.progress.connect(self.update_progress)
        self.dedupe_worker.completed.connect(self.dedupe_finished)
        self.dedupe_worker.failed.connect(self.operation_failed)
        self.dedupe_worker.start()

    def dedupe_finished(self, duplicates):
        self.set_ui_enabled(True)
        self.progress.setValue(100)
        self.percent_label.setText("100%")
        if not duplicates:
            self.action_title_label.setText("Không phát hiện bản trùng")
            self.status_label.setText("Các tệp trực tiếp trong thư mục đều khác nhau")
            self.set_status_pill("Sạch sẽ", "ready")
            QMessageBox.information(self, "Không có tệp trùng", "Thư mục này đang rất gọn gàng.")
            return
        self.action_title_label.setText("Đã tìm thấy bản trùng")
        self.status_label.setText(f"{len(duplicates)} nhóm cần bạn quyết định")
        self.set_status_pill("Cần xem lại", "warning")
        dialog = DedupeDialog(duplicates, self.logger, self.mover, self)
        dialog.exec()
        self.refresh_directory_summary()
        self.set_ui_enabled(True)

    def closeEvent(self, event):
        if self.is_busy:
            QMessageBox.information(
                self,
                "Đang thực hiện thao tác",
                "PADOrganizer đang làm việc. Vui lòng chờ thao tác hiện tại hoàn tất trước khi đóng.",
            )
            event.ignore()
            return
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_FULL_NAME)
    app.setOrganizationName("padduwcs")
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI Variable Text", 10))
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
