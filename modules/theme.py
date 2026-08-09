from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


APP_STYLE = """
    * {
        font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;
        outline: none;
    }
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody, QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #f4f6fb;
        color: #171a28;
    }
    QWidget#AppRoot {
        border: 1px solid #252a3b;
    }

    /* Custom title bar */
    QFrame#TitleBar {
        background-color: #0d101a;
        border: none;
        border-bottom: 1px solid #24293a;
    }
    QFrame#TitleBrandMark {
        background-color: #735cf4;
        border-radius: 7px;
    }
    QLabel#TitleBrandLetter {
        color: #ffffff;
        font-size: 12px;
        font-weight: 850;
    }
    QLabel#WindowTitle {
        color: #f4f5fa;
        font-size: 12px;
        font-weight: 750;
    }
    QLabel#WindowTitleSeparator {
        color: #474d62;
        font-size: 11px;
    }
    QLabel#WindowCaption {
        color: #858b9f;
        font-size: 10px;
        font-weight: 550;
    }
    QPushButton#WindowControl, QPushButton#CloseControl {
        color: #aeb3c3;
        background-color: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        font-family: "Segoe UI Symbol", "Segoe UI", sans-serif;
        font-size: 15px;
        font-weight: 500;
    }
    QPushButton#WindowControl:hover {
        color: #ffffff;
        background-color: #24293a;
    }
    QPushButton#CloseControl:hover {
        color: #ffffff;
        background-color: #d9434e;
    }
    QSizeGrip#ResizeGrip {
        width: 18px;
        height: 18px;
        background-color: transparent;
    }
    QToolTip {
        color: #ffffff;
        background-color: #191d2d;
        border: 1px solid #30354a;
        border-radius: 7px;
        padding: 7px 9px;
    }

    /* Sidebar */
    QFrame#Sidebar {
        background-color: #101321;
        border: none;
    }
    QFrame#BrandMark {
        background-color: #735cf4;
        border-radius: 12px;
    }
    QLabel#BrandLetter {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
    }
    QLabel#BrandTitle {
        color: #ffffff;
        font-size: 17px;
        font-weight: 750;
    }
    QLabel#BrandCaption, QLabel#SidebarSection {
        color: #74798f;
        font-size: 10px;
        font-weight: 700;
    }
    QPushButton#SidebarButton, QPushButton#SidebarActive, QPushButton#SidebarDanger {
        min-height: 42px;
        border: none;
        border-radius: 10px;
        padding: 0 13px;
        text-align: left;
        font-size: 13px;
        font-weight: 650;
    }
    QPushButton#SidebarButton {
        color: #a8adbf;
        background-color: transparent;
    }
    QPushButton#SidebarButton:hover {
        color: #ffffff;
        background-color: #1a1e30;
    }
    QPushButton#SidebarActive {
        color: #ffffff;
        background-color: #272b42;
        border: 1px solid #363b56;
    }
    QPushButton#SidebarDanger {
        color: #f2a6a2;
        background-color: transparent;
    }
    QPushButton#SidebarDanger:hover {
        color: #ffd4d1;
        background-color: #2a1e2b;
    }
    QPushButton#SidebarButton:disabled, QPushButton#SidebarDanger:disabled {
        color: #4c5060;
        background-color: transparent;
    }
    QFrame#PrivacyCard {
        background-color: #181c2c;
        border: 1px solid #292e43;
        border-radius: 14px;
    }
    QLabel#PrivacyDot {
        color: #c9f36a;
        font-size: 17px;
        font-weight: 900;
    }
    QLabel#PrivacyTitle {
        color: #eff1f8;
        font-size: 13px;
        font-weight: 750;
    }
    QLabel#PrivacyText {
        color: #a2a7b8;
        font-size: 11px;
    }
    QLabel#VersionLabel {
        color: #696f84;
        font-size: 10px;
        font-weight: 650;
        padding: 3px 0;
    }

    /* Top bar and hero */
    QLabel#PageEyebrow {
        color: #735cf4;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#PageTitle {
        color: #171a28;
        font-size: 28px;
        font-weight: 780;
    }
    QLabel#PageSubtitle {
        color: #74798a;
        font-size: 12px;
    }
    QLabel#StatusPill {
        color: #426600;
        background-color: #e9f8c8;
        border: 1px solid #d3ec9d;
        border-radius: 11px;
        padding: 6px 11px;
        font-size: 11px;
        font-weight: 750;
    }
    QLabel#StatusPill[state="busy"] {
        color: #4e3abb;
        background-color: #eeeaff;
        border-color: #d9d0ff;
    }
    QLabel#StatusPill[state="warning"] {
        color: #a4493b;
        background-color: #fff0ea;
        border-color: #f7d5cc;
    }
    QFrame#HeroCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #171a2b, stop:0.52 #28234d, stop:1 #694cbb);
        border: none;
        border-radius: 20px;
    }
    QLabel#HeroKicker {
        color: #cfc7ff;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#HeroTitle {
        color: #ffffff;
        font-size: 28px;
        font-weight: 780;
    }
    QLabel#HeroText {
        color: #c4c5d3;
        font-size: 12px;
    }
    QFrame#HeroMetric {
        background-color: rgba(255, 255, 255, 28);
        border: 1px solid rgba(255, 255, 255, 48);
        border-radius: 13px;
    }
    QFrame#HeroMetricAccent {
        background-color: #c9f36a;
        border: none;
        border-radius: 13px;
    }
    QLabel#HeroMetricValue {
        color: #ffffff;
        font-size: 23px;
        font-weight: 800;
    }
    QLabel#HeroMetricValueDark {
        color: #202512;
        font-size: 23px;
        font-weight: 800;
    }
    QLabel#HeroMetricLabel {
        color: #c6c4d4;
        font-size: 10px;
        font-weight: 750;
    }
    QLabel#HeroMetricLabelDark {
        color: #4d572b;
        font-size: 10px;
        font-weight: 750;
    }

    /* Cards */
    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #ffffff;
        border: 1px solid #e5e8f0;
        border-radius: 17px;
    }
    QLabel#StepBadge {
        color: #5e47da;
        background-color: #efecff;
        border-radius: 7px;
        padding: 4px 7px;
        font-size: 9px;
        font-weight: 800;
    }
    QLabel#CardTitle {
        color: #1b1e2c;
        font-size: 18px;
        font-weight: 750;
    }
    QLabel#CardText, QLabel#MutedText {
        color: #7a7f90;
        font-size: 11px;
    }
    QFrame#DropZone {
        background-color: #f8f7ff;
        border: 1px dashed #aca0ed;
        border-radius: 14px;
    }
    QFrame#DropZone:hover {
        background-color: #f1eeff;
        border-color: #735cf4;
    }
    QFrame#DropZone[selected="true"] {
        background-color: #f0edff;
        border: 1px solid #8d7cf0;
    }
    QFrame#FolderMark {
        background-color: #735cf4;
        border-radius: 12px;
    }
    QLabel#FolderMarkText {
        color: #ffffff;
        font-size: 18px;
        font-weight: 800;
    }
    QLabel#DropTitle {
        color: #252838;
        font-size: 14px;
        font-weight: 750;
    }
    QLabel#DropPath {
        color: #6652d5;
        font-size: 10px;
    }
    QFrame#MiniStat {
        background-color: #f7f8fb;
        border: 1px solid #eceef4;
        border-radius: 10px;
    }
    QLabel#MiniStatValue {
        color: #232634;
        font-size: 15px;
        font-weight: 780;
    }
    QLabel#MiniStatLabel {
        color: #898e9e;
        font-size: 9px;
        font-weight: 650;
    }
    QFrame#OptionRow {
        background-color: #f8f9fc;
        border: 1px solid #e9ebf2;
        border-radius: 12px;
    }
    QLabel#OptionTitle {
        color: #242735;
        font-size: 13px;
        font-weight: 730;
    }
    QLabel#OptionText {
        color: #858a99;
        font-size: 10px;
    }
    QLabel#OptionBadge {
        color: #a54b39;
        background-color: #fff0e9;
        border-radius: 7px;
        padding: 4px 7px;
        font-size: 9px;
        font-weight: 750;
    }

    /* Action dock */
    QFrame#ActionDock {
        background-color: #171a29;
        border: none;
        border-radius: 17px;
    }
    QLabel#ActionTitle {
        color: #ffffff;
        font-size: 17px;
        font-weight: 760;
    }
    QLabel#ActionText {
        color: #9da2b4;
        font-size: 10px;
    }
    QLabel#ActionStatus {
        color: #c9f36a;
        font-size: 10px;
        font-weight: 700;
    }
    QLabel#PercentText {
        color: #c9f36a;
        font-size: 11px;
        font-weight: 800;
    }
    QProgressBar {
        min-height: 7px;
        max-height: 7px;
        border: none;
        border-radius: 3px;
        color: transparent;
        background-color: #34384b;
    }
    QProgressBar::chunk {
        background-color: #c9f36a;
        border-radius: 3px;
    }

    /* Buttons */
    QPushButton {
        font-size: 12px;
        font-weight: 700;
        border-radius: 10px;
        padding: 10px 15px;
    }
    QPushButton#PrimaryButton {
        color: #202511;
        background-color: #c9f36a;
        border: none;
        padding: 13px 20px;
        font-size: 14px;
        font-weight: 800;
    }
    QPushButton#PrimaryButton:hover { background-color: #d7ff7e; }
    QPushButton#PrimaryButton:pressed { background-color: #b9e454; }
    QPushButton#PrimaryButton:disabled {
        color: #676b76;
        background-color: #323647;
    }
    QPushButton#DarkButton {
        color: #f4f5f8;
        background-color: #292d40;
        border: 1px solid #3b4056;
        padding: 12px 17px;
    }
    QPushButton#DarkButton:hover {
        color: #ffffff;
        background-color: #353a50;
        border-color: #545a74;
    }
    QPushButton#DarkButton:disabled {
        color: #5c6170;
        background-color: #222535;
        border-color: #303445;
    }
    QPushButton#SecondaryButton, QPushButton#DialogButton {
        color: #353847;
        background-color: #ffffff;
        border: 1px solid #dfe2ea;
    }
    QPushButton#SecondaryButton:hover, QPushButton#DialogButton:hover {
        color: #5f49d8;
        background-color: #f4f1ff;
        border-color: #bdb3ef;
    }
    QPushButton#SecondaryButton:disabled {
        color: #a3a7b2;
        background-color: #f0f1f4;
        border-color: #e4e6eb;
    }
    QPushButton#DangerButton {
        color: #ffffff;
        background-color: #d95656;
        border: none;
    }
    QPushButton#DangerButton:hover { background-color: #bf4147; }
    QPushButton#GhostDanger {
        color: #c94e4e;
        background-color: #ffffff;
        border: 1px solid #efcece;
    }
    QPushButton#GhostDanger:hover { background-color: #fff1f1; }
    QPushButton#LinkButton {
        color: #654fde;
        background-color: #f0edff;
        border: 1px solid #dfd9ff;
        text-align: left;
    }
    QPushButton#LinkButton:hover {
        color: #4d37c5;
        background-color: #e7e2ff;
    }

    /* Dialogs and inputs */
    QDialog { background-color: #f6f7fb; color: #1a1d2a; }
    QLabel#DialogEyebrow {
        color: #6b54e7;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#DialogTitle {
        color: #191c29;
        font-size: 25px;
        font-weight: 780;
    }
    QLabel#DialogSubtitle {
        color: #7a7f8e;
        font-size: 11px;
    }
    QFrame#UpdateSummary {
        background-color: #eeebff;
        border: 1px solid #dcd5ff;
        border-radius: 12px;
    }
    QLabel#UpdateVersionMuted {
        color: #74798a;
        font-size: 11px;
        font-weight: 700;
    }
    QLabel#UpdateArrow {
        color: #8b78ed;
        font-size: 16px;
        font-weight: 800;
    }
    QLabel#UpdateVersionNew {
        color: #533ccc;
        font-size: 12px;
        font-weight: 800;
    }
    QLabel#UpdateHint {
        color: #6f7484;
        background-color: #f0f2f7;
        border: 1px solid #e1e4eb;
        border-radius: 9px;
        padding: 10px 12px;
        font-size: 10px;
    }
    QTextBrowser#ReleaseNotes {
        color: #343744;
        background-color: #ffffff;
        border: 1px solid #e0e3eb;
        border-radius: 10px;
        padding: 10px;
        font-size: 11px;
        selection-background-color: #dcd5ff;
    }
    QLineEdit {
        min-height: 22px;
        color: #252836;
        background-color: #ffffff;
        border: 1px solid #dfe2e9;
        border-radius: 9px;
        padding: 9px 11px;
        selection-background-color: #dcd5ff;
    }
    QLineEdit:focus { border: 2px solid #7963ed; }
    QTableWidget {
        color: #2c2f3c;
        background-color: #ffffff;
        alternate-background-color: #fafbfc;
        border: 1px solid #e1e4eb;
        border-radius: 12px;
        gridline-color: #eef0f4;
        selection-background-color: #ece8ff;
        selection-color: #4d39bd;
    }
    QHeaderView::section {
        color: #777c8b;
        background-color: #f5f6f9;
        border: none;
        border-bottom: 1px solid #e4e6ec;
        padding: 10px;
        font-size: 10px;
        font-weight: 750;
    }
    QRadioButton {
        color: #3b3e4b;
        spacing: 9px;
        padding: 5px;
        font-size: 11px;
    }
    QRadioButton::indicator {
        width: 17px;
        height: 17px;
        border-radius: 9px;
        background-color: #ffffff;
        border: 1px solid #b8bdc8;
    }
    QRadioButton::indicator:checked {
        background-color: #735cf4;
        border: 4px solid #e6e1ff;
    }
    QRadioButton:checked { color: #252735; font-weight: 700; }
    QScrollArea { border: none; background-color: transparent; }
    QScrollArea > QWidget > QWidget { background-color: transparent; }
    QScrollBar:vertical { width: 9px; background: transparent; margin: 2px; }
    QScrollBar::handle:vertical {
        min-height: 30px;
        background-color: #c7cad4;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover { background-color: #a8acb8; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    QGroupBox {
        color: #252836;
        background-color: #ffffff;
        border: 1px solid #e1e4eb;
        border-radius: 12px;
        margin-top: 18px;
        padding: 20px 14px 14px 14px;
        font-size: 12px;
        font-weight: 750;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        color: #5e48d7;
        background-color: #efecff;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QMessageBox { background-color: #f7f8fb; }
    QMessageBox QLabel { color: #2a2d3a; min-width: 320px; }
    QMessageBox QPushButton {
        min-width: 90px;
        color: #353847;
        background-color: #ffffff;
        border: 1px solid #dfe2ea;
    }
    QMessageBox QPushButton:hover {
        color: #5f49d8;
        background-color: #f0edff;
        border-color: #bdb3ef;
    }
"""


def add_shadow(widget, blur_radius=34, y_offset=9, opacity=32):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setOffset(0, y_offset)
    shadow.setColor(QColor(21, 24, 40, opacity))
    widget.setGraphicsEffect(shadow)
    return shadow
