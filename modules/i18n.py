"""Small, dependency-free runtime localization helpers for the Qt interface."""

from PyQt6.QtCore import QObject, QTranslator
from PyQt6.QtWidgets import (
    QFileDialog as QtFileDialog,
    QDialog as QtDialog,
    QGroupBox as QtGroupBox,
    QLabel as QtLabel,
    QLineEdit as QtLineEdit,
    QMainWindow as QtMainWindow,
    QMessageBox as QtMessageBox,
    QPushButton as QtPushButton,
    QRadioButton as QtRadioButton,
    QTableWidget as QtTableWidget,
)


_language = "vi"


TRANSLATIONS = {
    "Đóng": "Close",
    "Cập nhật PADOrganizer": "Update PADOrganizer",
    "CẬP NHẬT MỚI": "NEW UPDATE",
    "Có gì mới": "What's new",
    "Installer sẽ được tải và xác minh SHA-256. Ứng dụng chỉ đóng sau khi bạn xác nhận cài đặt.": "The installer will be downloaded and SHA-256 verified. The app closes only after you confirm installation.",
    "Tải và cập nhật": "Download and update",
    "Bạn đang dùng bản portable hoặc chạy từ mã nguồn. Trang Release sẽ được mở để bạn chọn bản phù hợp.": "You are using a portable or source build. The Releases page will open so you can choose the right package.",
    "Mở trang tải xuống": "Open download page",
    "Để sau": "Later",
    "Thông tin quy tắc": "Rule details",
    "QUY TẮC PHÂN LOẠI": "ORGANIZATION RULE",
    "Thiết lập nhóm tệp": "Set up a file group",
    "Đặt tên thư mục đích và nhập các phần mở rộng, cách nhau bằng dấu phẩy.": "Name the destination folder and enter extensions separated by commas.",
    "Tên thư mục": "Folder name",
    "Ví dụ: Documents": "Example: Documents",
    "Phần mở rộng": "Extensions",
    "Hủy": "Cancel",
    "Xác nhận": "Confirm",
    "Thiếu thông tin": "Missing information",
    "Vui lòng nhập tên thư mục đích.": "Enter a destination folder name.",
    "Vui lòng nhập ít nhất một phần mở rộng.": "Enter at least one file extension.",
    "Quy tắc phân loại": "Organization rules",
    "CÁ NHÂN HÓA": "CUSTOMIZE",
    "Mỗi phần mở rộng chỉ nên thuộc một nhóm. Nhấp đúp vào một hàng để chỉnh sửa nhanh.": "Each extension should belong to one group. Double-click a row to edit it quickly.",
    "THƯ MỤC ĐÍCH": "DESTINATION FOLDER",
    "PHẦN MỞ RỘNG": "EXTENSIONS",
    "+  Thêm nhóm": "+  Add group",
    "Chỉnh sửa": "Edit",
    "Xóa nhóm": "Remove group",
    "Khôi phục mặc định": "Restore defaults",
    "Hủy thay đổi": "Discard changes",
    "Lưu quy tắc": "Save rules",
    "Tên đã tồn tại": "Name already exists",
    "Đã có một nhóm với tên này.": "A group with this name already exists.",
    "Chọn một nhóm": "Select a group",
    "Hãy chọn nhóm bạn muốn chỉnh sửa.": "Select the group you want to edit.",
    "Hãy chọn nhóm bạn muốn xóa.": "Select the group you want to remove.",
    "Xóa quy tắc": "Remove rule",
    "Thay toàn bộ danh sách hiện tại bằng bộ quy tắc mặc định?": "Replace the current list with the default rules?",
    "Danh sách trống": "Empty list",
    "Cần giữ lại ít nhất một nhóm phân loại.": "Keep at least one organization group.",
    "Phần mở rộng bị trùng": "Duplicate extension",
    "Xử lý tệp trùng lặp": "Manage duplicate files",
    "DỌN DẸP AN TOÀN": "SAFE CLEANUP",
    "Chọn bản cần giữ lại": "Choose the copy to keep",
    "Bỏ qua nhóm này — không tác động tệp nào": "Skip this group — leave every file untouched",
    "Không rõ dung lượng": "Unknown size",
    "Chuyển vào thùng rác": "Move to trash",
    "Xóa vĩnh viễn": "Delete permanently",
    "Không có thay đổi": "No changes",
    "Bạn đang bỏ qua tất cả các nhóm.": "You are skipping every group.",
    "Đã xử lý xong": "Processing complete",
    "Thu nhỏ": "Minimize",
    "Phóng to": "Maximize",
    "Khôi phục": "Restore",
    "PERSONAL ARCHIVE": "PERSONAL ARCHIVE",
    "KHÔNG GIAN LÀM VIỆC": "WORKSPACE",
    "LÀM VIỆC": "WORKSPACE",
    "Tổng quan": "Overview",
    "Mở thùng rác": "Open trash",
    "BẢO TRÌ": "MAINTENANCE",
    "Kiểm tra cập nhật": "Check for updates",
    "Chỉ kết nối GitHub khi bạn chủ động kiểm tra": "Connects to GitHub only when you check manually",
    "Dọn sạch thùng rác": "Empty trash",
    "Xóa nhật ký": "Clear activity log",
    "Xóa toàn bộ nhật ký hoạt động đang lưu trên máy": "Clear the activity log stored on this device",
    "GIAO DIỆN": "APPEARANCE",
    "☾  Chế độ tối": "☾  Dark mode",
    "☀  Chế độ sáng": "☀  Light mode",
    "☾  Tối": "☾  Dark",
    "☀  Sáng": "☀  Light",
    "Chuyển sang chế độ tối": "Switch to dark mode",
    "Chuyển sang chế độ sáng": "Switch to light mode",
    "Chuyển sang tiếng Anh": "Switch to English",
    "Chuyển sang tiếng Việt": "Switch to Vietnamese",
    "EN  ·  English": "EN  ·  English",
    "VI  ·  Tiếng Việt": "VI  ·  Tiếng Việt",
    "Riêng tư tuyệt đối": "Private by design",
    "Riêng tư": "Private",
    "Tệp cá nhân không được tải lên dịch vụ đám mây.": "Personal files are never uploaded to a cloud service.",
    "Dữ liệu luôn riêng tư": "Your data stays private",
    "Xử lý 100% trên thiết bị": "100% on-device processing",
    "Xử lý trên thiết bị": "Processed on device",
    "Tệp cá nhân luôn ở trên thiết bị.\nChỉ kết nối GitHub khi bạn kiểm tra cập nhật.": "Personal files always stay on your device.\nGitHub is contacted only when you check for updates.",
    "TRUNG TÂM SẮP XẾP": "ORGANIZATION HUB",
    "Sắp xếp tệp, nhẹ nhàng hơn.": "A simpler way to organize files.",
    "Sắp xếp tệp.": "Organize files.",
    "Phân loại, tìm tệp trùng và khôi phục tệp ngay trên thiết bị.": "Organize, find duplicates, and restore files directly on your device.",
    "Không gian của bạn, ngăn nắp hơn.": "A calmer, more organized space.",
    "Một luồng làm việc rõ ràng để phân loại, tìm bản trùng và khôi phục khi cần.": "A clear workflow to organize, find duplicates, and restore files when needed.",
    "Sẵn sàng": "Ready",
    "PADORGANIZER · LOCAL FIRST": "PADORGANIZER · LOCAL FIRST",
    "Mọi thứ về đúng chỗ.": "Everything in its place.",
    "Gọn đúng chỗ.": "Neatly organized.",
    "Chọn thư mục và để PADOrganizer xử lý phần còn lại.": "Choose a folder and let PADOrganizer handle the rest.",
    "Dọn một lần. Nhẹ đầu cả ngày.": "Organize once. Stay focused all day.",
    "Chọn một thư mục, xem nhanh quy mô và để PADOrganizer đưa từng tệp về đúng chỗ.": "Choose a folder, review it at a glance, and let PADOrganizer put every file in its place.",
    "THƯ MỤC": "FOLDER",
    "Chưa chọn": "Not selected",
    "NHÓM QUY TẮC": "RULE GROUPS",
    "QUY TẮC": "RULES",
    "TỆP SẴN SÀNG": "FILES READY",
    "TỆP": "FILES",
    "BƯỚC 01": "STEP 01",
    "Chọn không gian cần sắp xếp": "Choose a folder to organize",
    "Chỉ các tệp nằm trực tiếp trong thư mục được xử lý.": "Only files directly inside the folder are processed.",
    "Kéo thả thư mục vào đây": "Drag and drop a folder here",
    "Thả thư mục vào đây": "Drop a folder here",
    "Kéo một thư mục từ File Explorer và thả vào khu vực này.": "Drag a folder from File Explorer and drop it here.",
    "hoặc chọn từ máy tính của bạn": "or choose one from your computer",
    "Chọn thư mục": "Choose folder",
    "Duyệt...": "Browse...",
    "Mở hộp thoại chọn thư mục · Ctrl+O": "Open the folder picker · Ctrl+O",
    "TỆP TRỰC TIẾP": "DIRECT FILES",
    "TỔNG DUNG LƯỢNG": "TOTAL SIZE",
    "BƯỚC 02": "STEP 02",
    "Tinh chỉnh cách tổ chức": "Fine-tune organization",
    "Tùy chọn sắp xếp": "Organization options",
    "Điều chỉnh cấu trúc thư mục và quy tắc phân loại.": "Adjust folder structure and organization rules.",
    "Mặc định an toàn, đủ linh hoạt khi bạn cần.": "Safe defaults with flexibility when you need it.",
    "Chia theo Năm–Tháng": "Group by Year–Month",
    "Tạo thêm tầng 2026-08 trong mỗi nhóm": "Add a 2026-08 level inside each group",
    "Tạo thêm thư mục Năm–Tháng, ví dụ 2026-08, trong mỗi nhóm.": "Add a Year–Month folder, such as 2026-08, inside each group.",
    "Bộ quy tắc hiện tại": "Current rule set",
    "Xem và chỉnh sửa nhóm thư mục cùng các phần mở rộng tương ứng.": "View and edit folder groups and their associated extensions.",
    "Đang tải...": "Loading...",
    "Quản lý": "Manage",
    "Mở trình quản lý quy tắc · Ctrl+,": "Open the rule manager · Ctrl+,",
    "Thùng rác nội bộ": "Internal trash",
    "Nơi giữ tạm các tệp đã loại bỏ để bạn có thể khôi phục.": "Temporarily stores removed files so they can be restored.",
    "Đang kiểm tra...": "Checking...",
    "TRỐNG": "EMPTY",
    "CÓ TỆP": "HAS FILES",
    "Sẵn sàng khi bạn sẵn sàng": "Ready when you are",
    "Chọn một thư mục để bắt đầu": "Choose a folder to get started",
    "Hoàn tác": "Undo",
    "Hoàn tác lần sắp xếp gần nhất · Ctrl+Z": "Undo the latest organization run · Ctrl+Z",
    "Tìm bản trùng": "Find duplicates",
    "Tìm các tệp có nội dung giống nhau · Ctrl+D": "Find files with identical contents · Ctrl+D",
    "Tổ chức ngay": "Organize now",
    "Bắt đầu sắp xếp thư mục đã chọn · Ctrl+Enter": "Organize the selected folder · Ctrl+Enter",
    "Quản lý nhóm tệp và phần mở rộng · Ctrl+,": "Manage file groups and extensions · Ctrl+,",
    "Mở PADOrganizer_Trash trong File Explorer": "Open PADOrganizer_Trash in File Explorer",
    "Xóa vĩnh viễn toàn bộ nội dung trong thùng rác nội bộ": "Permanently delete everything in the internal trash",
    "Thư mục không hợp lệ": "Invalid folder",
    "Không thể truy cập thư mục đã chọn.": "The selected folder cannot be accessed.",
    "Không thể chọn thư mục ứng dụng": "The app folder cannot be selected",
    "Để bảo vệ chương trình và dữ liệu cấu hình, hãy chọn một thư mục khác.": "Choose another folder to protect the app and its configuration data.",
    "Đã chọn thư mục": "Folder selected",
    "Thư mục đã sẵn sàng": "Folder ready",
    "Chọn “Tổ chức ngay” hoặc kiểm tra các tệp trùng lặp": "Choose “Organize now” or scan for duplicate files",
    "Không thể đọc thư mục": "Cannot read folder",
    "Chọn thư mục cần sắp xếp": "Choose a folder to organize",
    "Không có tệp đang lưu tạm": "No files are being held temporarily",
    "Không thể mở thùng rác": "Cannot open trash",
    "Đã lưu quy tắc": "Rules saved",
    "Đang xử lý": "Working",
    "Hãy chọn thư mục bạn muốn tổ chức trước.": "Choose the folder you want to organize first.",
    "Đang tổ chức thư mục": "Organizing folder",
    "Chuẩn bị phân loại tệp...": "Preparing to organize files...",
    "Thư mục đã gọn sẵn": "Folder is already organized",
    "Không có tệp trực tiếp nào cần phân loại": "There are no direct files to organize",
    "Không có tệp cần xử lý": "No files to process",
    "Thư mục này đã sẵn sàng.": "This folder is all set.",
    "Tổ chức hoàn tất": "Organization complete",
    "Hoàn tất": "Complete",
    "Đã tổ chức xong": "Folder organized",
    "Không thể hoàn thành": "Unable to complete",
    "Cần kiểm tra": "Needs attention",
    "Thao tác thất bại": "Operation failed",
    "Hoàn tác lần gần nhất": "Undo last operation",
    "Đưa các tệp của lần xử lý gần nhất trở về vị trí cũ?": "Return files from the latest operation to their original locations?",
    "Đã hoàn tác": "Undo complete",
    "Đã khôi phục": "Restored",
    "Hoàn tác hoàn tất": "Undo complete",
    "Xóa vĩnh viễn toàn bộ nội dung trong PADOrganizer_Trash? Thao tác này không thể hoàn tác.": "Permanently delete everything in PADOrganizer_Trash? This action cannot be undone.",
    "Đã dọn thùng rác": "Trash emptied",
    "Thùng rác đã trống": "Trash is empty",
    "Toàn bộ nội dung đã được xóa.": "All contents have been deleted.",
    "Không thể dọn thùng rác": "Cannot empty trash",
    "Bảo trì": "Maintenance",
    "Nhật ký đang trống": "Activity log is empty",
    "Không có nhật ký hoạt động nào cần dọn dẹp vào lúc này.": "There are no activity log entries to clear.",
    "Đã hiểu": "Got it",
    "Bảo trì dữ liệu": "Data maintenance",
    "Xóa toàn bộ nhật ký hoạt động?": "Clear the entire activity log?",
    "Nhật ký đang lưu trên máy sẽ được dọn sạch. Tệp cá nhân và cấu hình phân loại của bạn không bị ảnh hưởng.": "The local activity log will be cleared. Your personal files and organization rules are unaffected.",
    "Giữ lại": "Keep it",
    "Đã xóa nhật ký": "Activity log cleared",
    "Nhật ký đã được dọn sạch": "Activity log has been cleared",
    "PADOrganizer đã xóa nhật ký hoạt động. Tệp và cấu hình của bạn vẫn được giữ nguyên.": "PADOrganizer cleared the activity log. Your files and configuration remain unchanged.",
    "Không thể xóa nhật ký": "Cannot clear activity log",
    "Đang kiểm tra cập nhật": "Checking for updates",
    "Kết nối GitHub theo yêu cầu của bạn...": "Connecting to GitHub at your request...",
    "Không có bản phát hành mới hơn": "No newer release found",
    "Mới nhất": "Up to date",
    "Cập nhật": "Update",
    "Bạn đang dùng phiên bản mới nhất": "You are using the latest version",
    "Xem nội dung thay đổi và cập nhật khi bạn sẵn sàng": "Review the changes and update when you are ready",
    "Có bản mới": "Update available",
    "Không thể mở trình duyệt": "Cannot open browser",
    "Chuẩn bị tải Installer từ GitHub...": "Preparing to download the installer from GitHub...",
    "Bản cập nhật đã sẵn sàng": "Update is ready",
    "Installer đã tải xong và khớp mã SHA-256": "The installer is downloaded and its SHA-256 matches",
    "Đã xác minh": "Verified",
    "mới": "new",
    "Cài đặt bản cập nhật": "Install update",
    "Bạn có thể kiểm tra và tải lại bất cứ lúc nào": "You can check and download it again at any time",
    "Không thể cập nhật": "Unable to update",
    "Thử lại sau": "Try again later",
    "Hãy chọn thư mục cần kiểm tra trước.": "Choose a folder to scan first.",
    "Đang tìm các bản trùng": "Finding duplicates",
    "Đọc và đối chiếu nội dung tệp...": "Reading and comparing file contents...",
    "Không phát hiện bản trùng": "No duplicates found",
    "Các tệp trực tiếp trong thư mục đều khác nhau": "All direct files in the folder are unique",
    "Sạch sẽ": "All clear",
    "Không có tệp trùng": "No duplicate files",
    "Thư mục này đang rất gọn gàng.": "This folder is already nicely organized.",
    "Đã tìm thấy bản trùng": "Duplicates found",
    "Cần xem lại": "Review needed",
    "Đang thực hiện thao tác": "Operation in progress",
    "PADOrganizer đang làm việc. Vui lòng chờ thao tác hiện tại hoàn tất trước khi đóng.": "PADOrganizer is working. Wait for the current operation to finish before closing.",
    "Không thể kiểm tra cập nhật vào lúc này.": "Unable to check for updates right now.",
    "Không thể tải bản cập nhật vào lúc này.": "Unable to download the update right now.",
    "GitHub trả về một đường dẫn tải xuống không hợp lệ.": "GitHub returned an invalid download URL.",
    "GitHub đang giới hạn yêu cầu. Vui lòng thử lại sau.": "GitHub is rate-limiting requests. Try again later.",
    "Chưa tìm thấy bản phát hành công khai trên GitHub.": "No public GitHub release was found.",
    "Không thể kết nối GitHub. Hãy kiểm tra Internet và thử lại.": "Unable to connect to GitHub. Check your internet connection and try again.",
    "Kết nối GitHub quá thời gian chờ. Vui lòng thử lại.": "The GitHub connection timed out. Try again.",
    "Không thể hoàn tất kết nối cập nhật.": "Unable to complete the update connection.",
    "GitHub trả về dữ liệu phiên bản không hợp lệ.": "GitHub returned invalid release data.",
    "Bản phát hành mới nhất không có số phiên bản hợp lệ.": "The latest release does not have a valid version number.",
    "Không tìm thấy mã SHA-256 để xác minh Installer.": "No SHA-256 checksum was found to verify the installer.",
    "Không có ghi chú cho phiên bản này.": "No release notes are available for this version.",
    "Không thể lưu Installer vào thư mục tạm của Windows.": "Unable to save the installer in the Windows temporary folder.",
    "Installer tải xuống không khớp mã SHA-256 và đã bị loại bỏ.": "The downloaded installer failed SHA-256 verification and was removed.",
    "Không thể hoàn tất file Installer đã tải.": "Unable to finalize the downloaded installer.",
    "Không thể mở Installer đã tải trên thiết bị này.": "The downloaded installer cannot be opened on this device.",
    "Windows không thể khởi chạy Installer đã tải.": "Windows could not launch the downloaded installer.",
}


_PHRASES = (
    ("Không thể đọc thư mục đã chọn: ", "Unable to read the selected folder: "),
    ("Không thể quét tệp trùng lặp: ", "Unable to scan for duplicate files: "),
    ("Phiên bản không hợp lệ: ", "Invalid version: "),
    ("GitHub phản hồi lỗi HTTP ", "GitHub returned HTTP error "),
    ("Bản phát hành v", "Release v"),
    (" chưa có file Installer phù hợp.", " does not include a compatible installer."),
    (" đã sẵn sàng", " is ready"),
    ("Bạn đang dùng v", "You are using v"),
    (". Hãy xem nội dung thay đổi trước khi quyết định.", ". Review the changes before deciding."),
    ("Hiện tại  ·  v", "Current  ·  v"),
    ("Mới nhất  ·  v", "Latest  ·  v"),
    ("Xóa nhóm “", "Remove group “"),
    ("” khỏi danh sách phân loại?", "” from the organization rules?"),
    (" nhóm · ", " groups · "),
    (" phần mở rộng", " extensions"),
    ("Mỗi phần mở rộng chỉ nên thuộc một nhóm:\n", "Each extension should belong to only one group:\n"),
    ("Phát hiện ", "Found "),
    (" nhóm với ", " groups containing "),
    (" tệp. PADOrganizer đã chọn sẵn tên tệp ngắn gọn nhất; bạn có thể đổi lựa chọn hoặc bỏ qua từng nhóm.", " files. PADOrganizer preselected the shortest filename; you can change the choice or skip any group."),
    ("NHÓM ", "GROUP "),
    (" TỆP GIỐNG NHAU", " IDENTICAL FILES"),
    ("Giữ lại  ", "Keep  "),
    ("Không rõ dung lượng", "Unknown size"),
    ("Sẽ xử lý ", "Will process "),
    (" tệp · có thể giải phóng ", " files · can reclaim "),
    ("Xóa vĩnh viễn ", "Permanently delete "),
    (" tệp? Thao tác này không thể hoàn tác.", " files? This action cannot be undone."),
    ("Chuyển ", "Move "),
    (" tệp vào PADOrganizer_Trash? Bạn có thể lấy lại chúng sau.", " files to PADOrganizer_Trash? You can restore them later."),
    ("Thành công: ", "Successful: "),
    ("Lỗi: ", "Errors: "),
    (" tệp đang chờ xử lý", " files awaiting review"),
    ("Đang xử lý: ", "Processing: "),
    ("Đã di chuyển ", "Moved "),
    (" tệp · ", " files · "),
    (" lỗi", " errors"),
    ("Di chuyển thành công: ", "Moved successfully: "),
    ("Khôi phục ", "Restored "),
    ("Khôi phục: ", "Restored: "),
    ("Phiên bản đang sử dụng · v", "Current version · v"),
    (" hiện đã là bản phát hành mới nhất trên GitHub.", " is currently the latest GitHub release."),
    ("Đã có PADOrganizer v", "PADOrganizer v"),
    ("Đang tải PADOrganizer v", "Downloading PADOrganizer v"),
    ("Đã tải ", "Downloaded "),
    (" đã được tải và xác minh thành công.\n\nCài đặt ngay bây giờ? PADOrganizer sẽ đóng và mở trình cài đặt.", " was downloaded and verified successfully.\n\nInstall it now? PADOrganizer will close and launch the installer."),
    (" nhóm cần bạn quyết định", " groups need your decision"),
)


def set_language(language):
    global _language
    _language = "en" if language == "en" else "vi"


def get_language():
    return _language


def translate(text):
    if not isinstance(text, str) or _language == "vi":
        return text
    translated = TRANSLATIONS.get(text)
    if translated is not None:
        return translated
    result = text
    for vietnamese, english in _PHRASES:
        result = result.replace(vietnamese, english)
    return result


class _LocalizedTextMixin:
    def setText(self, text):
        self._source_text = text
        super().setText(translate(text))

    def setToolTip(self, text):
        self._source_tooltip = text
        super().setToolTip(translate(text))

    def retranslate(self):
        if hasattr(self, "_source_text"):
            super().setText(translate(self._source_text))
        if hasattr(self, "_source_tooltip"):
            super().setToolTip(translate(self._source_tooltip))


class LocalizedLabel(_LocalizedTextMixin, QtLabel):
    def __init__(self, text="", parent=None):
        super().__init__("", parent)
        self.setText(text)


class LocalizedPushButton(_LocalizedTextMixin, QtPushButton):
    def __init__(self, text="", parent=None):
        super().__init__("", parent)
        self.setText(text)


class LocalizedRadioButton(_LocalizedTextMixin, QtRadioButton):
    def __init__(self, text="", parent=None):
        super().__init__("", parent)
        self.setText(text)


class LocalizedGroupBox(QtGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__("", parent)
        self.setTitle(title)

    def setTitle(self, title):
        self._source_title = title
        super().setTitle(translate(title))

    def retranslate(self):
        super().setTitle(translate(self._source_title))


class LocalizedDialog(QtDialog):
    def setWindowTitle(self, title):
        self._source_window_title = title
        super().setWindowTitle(translate(title))

    def retranslate(self):
        if hasattr(self, "_source_window_title"):
            super().setWindowTitle(translate(self._source_window_title))


class LocalizedMainWindow(QtMainWindow):
    def setWindowTitle(self, title):
        self._source_window_title = title
        super().setWindowTitle(translate(title))

    def retranslate(self):
        if hasattr(self, "_source_window_title"):
            super().setWindowTitle(translate(self._source_window_title))


class LocalizedLineEdit(QtLineEdit):
    def setPlaceholderText(self, text):
        self._source_placeholder = text
        super().setPlaceholderText(translate(text))

    def retranslate(self):
        if hasattr(self, "_source_placeholder"):
            super().setPlaceholderText(translate(self._source_placeholder))


class LocalizedTableWidget(QtTableWidget):
    def setHorizontalHeaderLabels(self, labels):
        self._source_header_labels = list(labels)
        super().setHorizontalHeaderLabels([translate(label) for label in labels])

    def retranslate(self):
        if hasattr(self, "_source_header_labels"):
            super().setHorizontalHeaderLabels(
                [translate(label) for label in self._source_header_labels]
            )


class LocalizedFileDialog(QtFileDialog):
    @staticmethod
    def getExistingDirectory(parent=None, caption="", directory="", options=None):
        if options is None:
            return QtFileDialog.getExistingDirectory(parent, translate(caption), directory)
        return QtFileDialog.getExistingDirectory(parent, translate(caption), directory, options)


class LocalizedMessageBox(QtMessageBox):
    @staticmethod
    def information(parent, title, text, buttons=QtMessageBox.StandardButton.Ok, defaultButton=QtMessageBox.StandardButton.NoButton):
        return QtMessageBox.information(parent, translate(title), translate(text), buttons, defaultButton)

    @staticmethod
    def warning(parent, title, text, buttons=QtMessageBox.StandardButton.Ok, defaultButton=QtMessageBox.StandardButton.NoButton):
        return QtMessageBox.warning(parent, translate(title), translate(text), buttons, defaultButton)

    @staticmethod
    def critical(parent, title, text, buttons=QtMessageBox.StandardButton.Ok, defaultButton=QtMessageBox.StandardButton.NoButton):
        return QtMessageBox.critical(parent, translate(title), translate(text), buttons, defaultButton)

    @staticmethod
    def question(parent, title, text, buttons=QtMessageBox.StandardButton.Yes | QtMessageBox.StandardButton.No, defaultButton=QtMessageBox.StandardButton.NoButton):
        return QtMessageBox.question(parent, translate(title), translate(text), buttons, defaultButton)


class StandardButtonTranslator(QTranslator):
    _VI = {
        "&Yes": "&Có",
        "Yes": "Có",
        "&No": "&Không",
        "No": "Không",
        "OK": "Đồng ý",
        "Cancel": "Hủy",
        "Close": "Đóng",
    }

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        del context, disambiguation, n
        if _language == "vi":
            return self._VI.get(sourceText, "")
        return ""


def retranslate_tree(root):
    widgets = [root, *root.findChildren(QObject)]
    for widget in widgets:
        retranslate = getattr(widget, "retranslate", None)
        if callable(retranslate):
            retranslate()
