from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


LIGHT_STYLE = """
    * {
        font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;
        outline: none;
    }
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody, QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #edf1f7;
        color: #171a28;
    }
    QWidget#AppRoot {
        border: 1px solid #c8cfdd;
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
    QFrame#PreferenceCard {
        background-color: #181c2c;
        border: 1px solid #292e43;
        border-radius: 12px;
    }
    QPushButton#PreferenceButton {
        min-height: 34px;
        color: #d9dce7;
        background-color: #23283a;
        border: 1px solid #343a50;
        border-radius: 8px;
        padding: 0 10px;
        text-align: left;
        font-size: 10px;
        font-weight: 700;
    }
    QPushButton#PreferenceButton:hover {
        color: #ffffff;
        background-color: #2d3349;
        border-color: #4b5270;
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
        font-size: 20px;
        font-weight: 800;
    }
    QLabel#HeroMetricValueDark {
        color: #202512;
        font-size: 20px;
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
        border: 1px solid #d8deea;
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
        background-color: #f3f5f9;
        border: 1px solid #dfe4ed;
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
        background-color: #f3f5f9;
        border: 1px solid #dce2ec;
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
    QDialog#AppMessageDialog {
        background-color: transparent;
    }
    QFrame#MessageCard {
        background-color: #ffffff;
        border: 1px solid #e2e5ed;
        border-radius: 20px;
    }
    QFrame#MessageCard[variant="danger"] {
        border-color: #f0d7d4;
    }
    QFrame#MessageCard[variant="success"] {
        border-color: #dce9c5;
    }
    QFrame#MessageIcon {
        background-color: #efecff;
        border: 1px solid #ddd6ff;
        border-radius: 15px;
    }
    QFrame#MessageIcon[variant="danger"] {
        background-color: #fff0ee;
        border-color: #f5d4d0;
    }
    QFrame#MessageIcon[variant="success"] {
        background-color: #edf8d7;
        border-color: #d8ebae;
    }
    QLabel#MessageIconText {
        color: #654fde;
        font-size: 22px;
        font-weight: 850;
    }
    QLabel#MessageIconText[variant="danger"] {
        color: #c64f4f;
    }
    QLabel#MessageIconText[variant="success"] {
        color: #537b14;
    }
    QLabel#MessageKicker {
        color: #6853dc;
        font-size: 9px;
        font-weight: 850;
    }
    QLabel#MessageKicker[variant="danger"] {
        color: #b84b4b;
    }
    QLabel#MessageKicker[variant="success"] {
        color: #587d1d;
    }
    QLabel#MessageTitle {
        color: #1c1f2d;
        font-size: 20px;
        font-weight: 780;
    }
    QLabel#MessageText {
        color: #6f7484;
        font-size: 11px;
    }
    QFrame#MessageDivider {
        background-color: #eceef3;
        border: none;
    }
    QPushButton#MessageClose {
        color: #9297a5;
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 0;
        font-size: 18px;
        font-weight: 500;
    }
    QPushButton#MessageClose:hover {
        color: #2d303d;
        background-color: #f0f1f5;
    }
    QPushButton#MessagePrimary,
    QPushButton#MessageDanger,
    QPushButton#MessageSecondary {
        min-width: 112px;
        min-height: 40px;
        border-radius: 10px;
        padding: 0 18px;
        font-size: 12px;
        font-weight: 750;
    }
    QPushButton#MessagePrimary {
        color: #ffffff;
        background-color: #6852df;
        border: 1px solid #6852df;
    }
    QPushButton#MessagePrimary:hover {
        background-color: #5943cd;
        border-color: #5943cd;
    }
    QPushButton#MessageDanger {
        color: #ffffff;
        background-color: #cf5656;
        border: 1px solid #cf5656;
    }
    QPushButton#MessageDanger:hover {
        background-color: #ba454b;
        border-color: #ba454b;
    }
    QPushButton#MessageSecondary {
        color: #4b4f5d;
        background-color: #ffffff;
        border: 1px solid #dfe2ea;
    }
    QPushButton#MessageSecondary:hover {
        color: #5c47d3;
        background-color: #f3f0ff;
        border-color: #c8bff2;
    }
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


MODERN_LIGHT_OVERRIDES = """
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody,
    QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #f5f6fa;
        color: #181b25;
    }
    QWidget#AppRoot { border-color: #dfe2ea; }

    QFrame#TitleBar {
        background-color: #ffffff;
        border-bottom: 1px solid #e8eaf0;
    }
    QFrame#TitleBrandMark, QFrame#BrandMark, QFrame#FolderMark {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6558e8, stop:1 #8272f3);
    }
    QLabel#WindowTitle { color: #222531; }
    QLabel#WindowTitleSeparator { color: #c7cad4; }
    QLabel#WindowCaption { color: #8a8f9e; }
    QPushButton#WindowControl, QPushButton#CloseControl { color: #656b78; }
    QPushButton#WindowControl:hover { color: #262a35; background-color: #f0f1f5; }

    QFrame#Sidebar {
        background-color: #fbfbfd;
        border-right: 1px solid #e6e8ee;
    }
    QLabel#BrandTitle { color: #20232d; }
    QLabel#BrandCaption, QLabel#SidebarSection { color: #979baa; }
    QPushButton#SidebarButton, QPushButton#SidebarActive, QPushButton#SidebarDanger {
        min-height: 38px;
        border-radius: 9px;
        padding: 0 11px;
    }
    QPushButton#SidebarButton { color: #5f6471; background-color: transparent; }
    QPushButton#SidebarButton:hover { color: #302b72; background-color: #f1f0ff; }
    QPushButton#SidebarActive {
        color: #5444cf;
        background-color: #eeecff;
        border: 1px solid #ded9ff;
    }
    QPushButton#SidebarDanger { color: #d45a65; background-color: transparent; }
    QPushButton#SidebarDanger:hover { color: #b9424e; background-color: #fff0f1; }
    QPushButton#SidebarButton:disabled, QPushButton#SidebarDanger:disabled {
        color: #bec1ca; background-color: transparent;
    }
    QFrame#PreferenceCard {
        background-color: #f1f2f6;
        border: 1px solid #e2e4eb;
        border-radius: 11px;
    }
    QPushButton#PreferenceButton {
        min-height: 30px;
        color: #555b68;
        background-color: #ffffff;
        border: 1px solid #e0e2e9;
        border-radius: 7px;
        padding: 0 8px;
        text-align: center;
        font-size: 10px;
    }
    QPushButton#PreferenceButton:hover {
        color: #5848d5;
        background-color: #f2f0ff;
        border-color: #d4ceff;
    }
    QFrame#PrivacyCard {
        background-color: #eefaf7;
        border: 1px solid #d6eee8;
        border-radius: 11px;
    }
    QLabel#PrivacyDot { color: #20a58f; }
    QLabel#PrivacyTitle { color: #23665b; }
    QLabel#PrivacyText { color: #689087; }
    QLabel#VersionLabel { color: #a1a5b1; }

    QLabel#PageEyebrow { color: #6757e7; }
    QLabel#PageTitle { color: #1b1e28; font-size: 27px; }
    QLabel#PageSubtitle { color: #777c89; }
    QLabel#StatusPill {
        color: #167b6c;
        background-color: #e7f8f4;
        border-color: #c9ece4;
    }
    QLabel#StatusPill[state="busy"] {
        color: #5645cf; background-color: #efedff; border-color: #dcd7ff;
    }
    QLabel#StatusPill[state="warning"] {
        color: #bd4f58; background-color: #fff0f1; border-color: #f5d5d8;
    }

    QFrame#HeroCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5146d8, stop:0.56 #6f5ee7, stop:1 #258f9e);
        border-radius: 18px;
    }
    QLabel#HeroKicker { color: #d8d4ff; }
    QLabel#HeroText { color: #e1e2ef; }
    QFrame#HeroMetric {
        background-color: rgba(255, 255, 255, 24);
        border-color: rgba(255, 255, 255, 44);
    }
    QFrame#HeroMetricAccent { background-color: #72ead1; }
    QLabel#HeroMetricLabelDark { color: #285b52; }
    QLabel#HeroMetricValueDark { color: #123d36; }

    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #ffffff;
        border: 1px solid #e3e6ed;
        border-radius: 15px;
    }
    QLabel#StepBadge { color: #5d4bd7; background-color: #efedff; }
    QFrame#DropZone { background-color: #faf9ff; border-color: #b9b0f4; }
    QFrame#DropZone:hover { background-color: #f3f1ff; border-color: #6d5de7; }
    QFrame#DropZone[selected="true"] { background-color: #f0eeff; border-color: #6d5de7; }
    QLabel#DropPath { color: #6656dc; }
    QFrame#MiniStat, QFrame#OptionRow {
        background-color: #f7f8fb;
        border-color: #e6e8ef;
    }
    QLabel#OptionBadge { color: #ba5260; background-color: #fff0f2; }

    QFrame#ActionDock {
        background-color: #ffffff;
        border: 1px solid #e2e5ec;
        border-radius: 15px;
    }
    QLabel#ActionTitle { color: #222530; }
    QLabel#ActionStatus, QLabel#PercentText { color: #5e4ddd; }
    QProgressBar { background-color: #eceef3; }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6656e6, stop:1 #32b8a7);
    }
    QPushButton#PrimaryButton {
        color: #ffffff;
        background-color: #6252df;
        border: 1px solid #6252df;
    }
    QPushButton#PrimaryButton:hover { background-color: #5545cf; border-color: #5545cf; }
    QPushButton#PrimaryButton:pressed { background-color: #493abd; border-color: #493abd; }
    QPushButton#PrimaryButton:disabled {
        color: #a4a8b2; background-color: #eceef2; border-color: #e3e5ea;
    }
    QPushButton#DarkButton {
        color: #535966;
        background-color: #f7f8fa;
        border: 1px solid #dfe2e9;
    }
    QPushButton#DarkButton:hover {
        color: #5142c8; background-color: #efedff; border-color: #d2ccff;
    }
    QPushButton#DarkButton:disabled {
        color: #b7bac3; background-color: #f5f6f8; border-color: #e9ebef;
    }
"""


DARK_OVERRIDES = """
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody, QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #0f121b;
        color: #eef1f7;
    }
    QWidget#AppRoot { border-color: #343a4b; }
    QToolTip { color: #f8f9fc; background-color: #252a39; border-color: #464d61; }

    QLabel#PageTitle { color: #f5f7fb; }
    QLabel#PageSubtitle { color: #aeb5c5; }
    QLabel#PageEyebrow { color: #a998ff; }
    QLabel#StatusPill {
        color: #d9ff86; background-color: #243019; border-color: #435d24;
    }
    QLabel#StatusPill[state="busy"] {
        color: #c8bdff; background-color: #292442; border-color: #4a4172;
    }
    QLabel#StatusPill[state="warning"] {
        color: #ffb4a8; background-color: #3b2524; border-color: #68403b;
    }

    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #191d28; border-color: #303646;
    }
    QLabel#StepBadge { color: #c1b5ff; background-color: #302a4b; }
    QLabel#CardTitle, QLabel#DropTitle, QLabel#MiniStatValue,
    QLabel#OptionTitle { color: #f0f2f7; }
    QLabel#CardText, QLabel#MutedText, QLabel#MiniStatLabel,
    QLabel#OptionText { color: #a7adbc; }
    QFrame#DropZone { background-color: #222232; border-color: #7569b9; }
    QFrame#DropZone:hover { background-color: #29263d; border-color: #a391ff; }
    QFrame#DropZone[selected="true"] { background-color: #2c2844; border-color: #a391ff; }
    QLabel#DropPath { color: #b6a8ff; }
    QFrame#MiniStat, QFrame#OptionRow { background-color: #222631; border-color: #353b49; }
    QLabel#OptionBadge { color: #ffc0b2; background-color: #432925; }

    QPushButton#SecondaryButton, QPushButton#DialogButton,
    QPushButton#GhostDanger, QPushButton#MessageSecondary {
        color: #e4e7ee; background-color: #252a36; border-color: #414858;
    }
    QPushButton#SecondaryButton:hover, QPushButton#DialogButton:hover,
    QPushButton#MessageSecondary:hover {
        color: #ffffff; background-color: #302b49; border-color: #7769b7;
    }
    QPushButton#SecondaryButton:disabled {
        color: #686e7d; background-color: #1c202a; border-color: #2c313d;
    }
    QPushButton#GhostDanger { color: #ffaaa7; border-color: #60403f; }
    QPushButton#GhostDanger:hover { background-color: #3c2527; }
    QPushButton#LinkButton { color: #c6bbff; background-color: #302b49; border-color: #4a426c; }
    QPushButton#LinkButton:hover { color: #ffffff; background-color: #3a3457; }

    QDialog, QMessageBox { background-color: #11151f; color: #eef1f7; }
    QDialog#AppMessageDialog { background-color: transparent; }
    QFrame#MessageCard { background-color: #1b1f2b; border-color: #373d4c; }
    QFrame#MessageCard[variant="danger"] { border-color: #64403e; }
    QFrame#MessageCard[variant="success"] { border-color: #485c31; }
    QFrame#MessageIcon { background-color: #302a4b; border-color: #4a4170; }
    QFrame#MessageIcon[variant="danger"] { background-color: #402625; border-color: #653e3b; }
    QFrame#MessageIcon[variant="success"] { background-color: #29351d; border-color: #475d2d; }
    QLabel#MessageIconText, QLabel#MessageKicker, QLabel#DialogEyebrow { color: #b9abff; }
    QLabel#MessageIconText[variant="danger"], QLabel#MessageKicker[variant="danger"] { color: #ffaaa5; }
    QLabel#MessageIconText[variant="success"], QLabel#MessageKicker[variant="success"] { color: #c9f36a; }
    QLabel#MessageTitle, QLabel#DialogTitle { color: #f5f7fb; }
    QLabel#MessageText, QLabel#DialogSubtitle { color: #adb3c2; }
    QFrame#MessageDivider { background-color: #343947; }
    QPushButton#MessageClose { color: #a8adbb; }
    QPushButton#MessageClose:hover { color: #ffffff; background-color: #292e3a; }

    QFrame#UpdateSummary { background-color: #2b2742; border-color: #49416b; }
    QLabel#UpdateVersionMuted { color: #acb1c0; }
    QLabel#UpdateArrow { color: #aa9cff; }
    QLabel#UpdateVersionNew { color: #c2b7ff; }
    QLabel#UpdateHint { color: #b8bdc9; background-color: #20242e; border-color: #353b48; }
    QTextBrowser#ReleaseNotes, QLineEdit, QTableWidget, QGroupBox {
        color: #e3e6ed; background-color: #1b1f29; border-color: #373d4a;
    }
    QTextBrowser#ReleaseNotes, QLineEdit, QTableWidget {
        selection-background-color: #4a3e78; selection-color: #ffffff;
    }
    QLineEdit:focus { border: 2px solid #9b89ff; }
    QTableWidget { alternate-background-color: #202530; gridline-color: #303642; }
    QHeaderView::section {
        color: #b9beca; background-color: #252a35; border-bottom-color: #3a404d;
    }
    QRadioButton { color: #d5d9e2; }
    QRadioButton::indicator { background-color: #242934; border-color: #707789; }
    QRadioButton::indicator:checked { background-color: #8c78f4; border-color: #322b51; }
    QRadioButton:checked { color: #ffffff; }
    QScrollBar::handle:vertical { background-color: #505666; }
    QScrollBar::handle:vertical:hover { background-color: #6b7284; }
    QGroupBox::title { color: #c0b4ff; background-color: #302b49; }
    QMessageBox QLabel { color: #e7eaf1; }
    QMessageBox QPushButton { color: #e4e7ee; background-color: #252a36; border-color: #414858; }
    QMessageBox QPushButton:hover { color: #ffffff; background-color: #302b49; border-color: #7769b7; }

    QFrame#TitleBar {
        background-color: #151820;
        border-bottom: 1px solid #292e39;
    }
    QLabel#WindowTitle { color: #f1f3f7; }
    QLabel#WindowTitleSeparator { color: #484e5c; }
    QLabel#WindowCaption { color: #858b99; }
    QPushButton#WindowControl, QPushButton#CloseControl { color: #a8adba; }
    QPushButton#WindowControl:hover { color: #ffffff; background-color: #292e39; }

    QFrame#Sidebar {
        background-color: #171a22;
        border-right: 1px solid #292e39;
    }
    QLabel#BrandTitle { color: #f2f4f8; }
    QLabel#BrandCaption, QLabel#SidebarSection { color: #747b8c; }
    QPushButton#SidebarButton { color: #aeb3c0; background-color: transparent; }
    QPushButton#SidebarButton:hover { color: #ffffff; background-color: #252836; }
    QPushButton#SidebarActive {
        color: #d8d2ff; background-color: #2c2944; border-color: #423d61;
    }
    QPushButton#SidebarDanger { color: #f09299; background-color: transparent; }
    QPushButton#SidebarDanger:hover { color: #ffb4ba; background-color: #342326; }
    QPushButton#SidebarButton:disabled, QPushButton#SidebarDanger:disabled {
        color: #555b68; background-color: transparent;
    }
    QFrame#PreferenceCard {
        background-color: #20242e; border-color: #303641;
    }
    QPushButton#PreferenceButton {
        color: #c8ccd5; background-color: #292e39; border-color: #383e4b;
    }
    QPushButton#PreferenceButton:hover {
        color: #ffffff; background-color: #35304e; border-color: #554d79;
    }
    QFrame#PrivacyCard { background-color: #1c2b2a; border-color: #29413e; }
    QLabel#PrivacyDot { color: #55d4bd; }
    QLabel#PrivacyTitle { color: #b8e9df; }
    QLabel#PrivacyText { color: #779e97; }
    QLabel#VersionLabel { color: #666d7c; }

    QLabel#StatusPill {
        color: #7ce5d1; background-color: #19302d; border-color: #2c514b;
    }
    QFrame#HeroMetricAccent { background-color: #62dbc4; }
    QFrame#ActionDock { background-color: #1b1f29; border-color: #303642; }
    QLabel#ActionTitle { color: #f2f4f8; }
    QLabel#ActionStatus, QLabel#PercentText { color: #8f80f4; }
    QProgressBar { background-color: #303541; }
    QPushButton#DarkButton {
        color: #e2e5eb; background-color: #252a35; border-color: #3b424f;
    }
    QPushButton#DarkButton:hover {
        color: #ffffff; background-color: #312d49; border-color: #5c527f;
    }
    QPushButton#DarkButton:disabled {
        color: #606674; background-color: #20242d; border-color: #2c313c;
    }
    QPushButton#PrimaryButton:disabled {
        color: #686e7a; background-color: #292e38; border-color: #303641;
    }
"""


APP_STYLE = LIGHT_STYLE + MODERN_LIGHT_OVERRIDES


def get_app_style(theme="light"):
    style = LIGHT_STYLE + MODERN_LIGHT_OVERRIDES
    return style + (DARK_OVERRIDES if theme == "dark" else "")


def add_shadow(widget, blur_radius=34, y_offset=9, opacity=32):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setOffset(0, y_offset)
    shadow.setColor(QColor(22, 25, 38, opacity))
    widget.setGraphicsEffect(shadow)
    return shadow
