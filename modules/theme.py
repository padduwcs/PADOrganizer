from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


LIGHT_STYLE = """
    * {
        font-family: "Segoe UI Variable Text", "Segoe UI", sans-serif;
        outline: none;
    }
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody, QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #f3f0ed;
        color: #1e1a16;
    }
    QWidget#AppRoot {
        border: 1px solid #d4cec7;
    }

    /* Custom title bar */
    QFrame#TitleBar {
        background-color: #13100d;
        border: none;
        border-bottom: 1px solid #2e2923;
    }
    QLabel#WindowTitle {
        color: #f7f5f3;
        font-size: 12px;
        font-weight: 750;
    }
    QLabel#WindowTitleSeparator {
        color: #534d46;
        font-size: 11px;
    }
    QLabel#WindowCaption {
        color: #928a82;
        font-size: 10px;
        font-weight: 550;
    }
    QPushButton#WindowControl, QPushButton#CloseControl {
        color: #b8b2ac;
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
        background-color: #2e2923;
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
        background-color: #211d18;
        border: 1px solid #3b352e;
        border-radius: 7px;
        padding: 7px 9px;
    }

    /* Sidebar */
    QFrame#Sidebar {
        background-color: #17130f;
        border: none;
    }
    QLabel#BrandTitle {
        color: #ffffff;
        font-size: 17px;
        font-weight: 750;
    }
    QLabel#BrandCaption, QLabel#SidebarSection {
        color: #7f7971;
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
        color: #b3aca5;
        background-color: transparent;
    }
    QPushButton#SidebarButton:hover {
        color: #ffffff;
        background-color: #231e19;
    }
    QPushButton#SidebarActive {
        color: #ffffff;
        background-color: #312b25;
        border: 1px solid #423b34;
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
        color: #55504a;
        background-color: transparent;
    }
    QFrame#PrivacyCard {
        background-color: #201c17;
        border: 1px solid #342e28;
        border-radius: 14px;
    }
    QLabel#PrivacyDot {
        color: #d7eacc;
        font-size: 17px;
        font-weight: 900;
    }
    QLabel#PrivacyTitle {
        color: #f4f1ed;
        font-size: 13px;
        font-weight: 750;
    }
    QLabel#PrivacyText {
        color: #ada69f;
        font-size: 11px;
    }
    QLabel#VersionLabel {
        color: #756f67;
        font-size: 10px;
        font-weight: 650;
        padding: 3px 0;
    }
    QFrame#PreferenceCard {
        background-color: #201c17;
        border: 1px solid #342e28;
        border-radius: 12px;
    }
    QPushButton#PreferenceButton {
        min-height: 34px;
        color: #e0dcd7;
        background-color: #2d2822;
        border: 1px solid #403a33;
        border-radius: 8px;
        padding: 0 10px;
        text-align: left;
        font-size: 10px;
        font-weight: 700;
    }
    QPushButton#PreferenceButton:hover {
        color: #ffffff;
        background-color: #39332c;
        border-color: #5a5249;
    }

    /* Top bar and hero */
    QLabel#PageEyebrow {
        color: #b95a23;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#PageTitle {
        color: #1e1a16;
        font-size: 28px;
        font-weight: 780;
    }
    QLabel#PageSubtitle {
        color: #7e7972;
        font-size: 12px;
    }
    QLabel#StatusPill {
        color: #406629;
        background-color: #ecf4e7;
        border: 1px solid #d8e7cf;
        border-radius: 11px;
        padding: 6px 11px;
        font-size: 11px;
        font-weight: 750;
    }
    QLabel#StatusPill[state="busy"] {
        color: #71472f;
        background-color: #f6ebdf;
        border-color: #f4cfb9;
    }
    QLabel#StatusPill[state="warning"] {
        color: #a4493b;
        background-color: #fff0ea;
        border-color: #f7d5cc;
    }
    QFrame#HeroCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #211915, stop:0.52 #35261d, stop:1 #81573e);
        border: none;
        border-radius: 20px;
    }
    QLabel#HeroKicker {
        color: #f1c4aa;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#HeroTitle {
        color: #ffffff;
        font-size: 28px;
        font-weight: 780;
    }
    QLabel#HeroText {
        color: #cac5c0;
        font-size: 12px;
    }
    QFrame#HeroMetric {
        background-color: rgba(255, 255, 255, 28);
        border: 1px solid rgba(255, 255, 255, 48);
        border-radius: 13px;
    }
    QFrame#HeroMetricAccent {
        background-color: #d7eacc;
        border: none;
        border-radius: 13px;
    }
    QLabel#HeroMetricValue {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
    }
    QLabel#HeroMetricValueDark {
        color: #1e251a;
        font-size: 20px;
        font-weight: 800;
    }
    QLabel#HeroMetricLabel {
        color: #cac5c0;
        font-size: 10px;
        font-weight: 750;
    }
    QLabel#HeroMetricLabelDark {
        color: #47573e;
        font-size: 10px;
        font-weight: 750;
    }

    /* Cards */
    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #ffffff;
        border: 1px solid #e2ddd7;
        border-radius: 17px;
    }
    QLabel#StepBadge {
        color: #8f512d;
        background-color: #f6ede2;
        border-radius: 7px;
        padding: 4px 7px;
        font-size: 9px;
        font-weight: 800;
    }
    QLabel#CardTitle {
        color: #221e1a;
        font-size: 18px;
        font-weight: 750;
    }
    QLabel#CardText, QLabel#MutedText {
        color: #847e78;
        font-size: 11px;
    }
    QFrame#DropZone {
        background-color: #fbf7f3;
        border: 1px dashed #d79d7c;
        border-radius: 14px;
    }
    QFrame#DropZone:hover {
        background-color: #f7efe5;
        border-color: #b95a23;
    }
    QFrame#DropZone[selected="true"] {
        background-color: #f7eee3;
        border: 1px solid #d2743d;
    }
    QFrame#FolderMark {
        background-color: #b95a23;
        border-radius: 12px;
    }
    QLabel#FolderMarkText {
        color: #ffffff;
        font-size: 18px;
        font-weight: 800;
    }
    QLabel#DropTitle {
        color: #2c2823;
        font-size: 14px;
        font-weight: 750;
    }
    QLabel#DropPath {
        color: #955835;
        font-size: 10px;
    }
    QFrame#MiniStat {
        background-color: #f6f5f3;
        border: 1px solid #e7e3de;
        border-radius: 10px;
    }
    QLabel#MiniStatValue {
        color: #2a2622;
        font-size: 15px;
        font-weight: 780;
    }
    QLabel#MiniStatLabel {
        color: #938d87;
        font-size: 9px;
        font-weight: 650;
    }
    QFrame#OptionRow {
        background-color: #f6f5f3;
        border: 1px solid #e6e1dc;
        border-radius: 12px;
    }
    QLabel#OptionTitle {
        color: #2b2723;
        font-size: 13px;
        font-weight: 730;
    }
    QLabel#OptionText {
        color: #8f8983;
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
        background-color: #1e1a16;
        border: none;
        border-radius: 17px;
    }
    QLabel#ActionTitle {
        color: #ffffff;
        font-size: 17px;
        font-weight: 760;
    }
    QLabel#ActionText {
        color: #a8a19a;
        font-size: 10px;
    }
    QLabel#ActionStatus {
        color: #d7eacc;
        font-size: 10px;
        font-weight: 700;
    }
    QLabel#PercentText {
        color: #d7eacc;
        font-size: 11px;
        font-weight: 800;
    }
    QProgressBar {
        min-height: 7px;
        max-height: 7px;
        border: none;
        border-radius: 3px;
        color: transparent;
        background-color: #3d3832;
    }
    QProgressBar::chunk {
        background-color: #d7eacc;
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
        color: #1e2519;
        background-color: #d7eacc;
        border: none;
        padding: 13px 20px;
        font-size: 14px;
        font-weight: 800;
    }
    QPushButton#PrimaryButton:hover { background-color: #e9f4e3; }
    QPushButton#PrimaryButton:pressed { background-color: #c3dcb5; }
    QPushButton#PrimaryButton:disabled {
        color: #6e6b66;
        background-color: #3b3630;
    }
    QPushButton#DarkButton {
        color: #f6f5f4;
        background-color: #322d27;
        border: 1px solid #464039;
        padding: 12px 17px;
    }
    QPushButton#DarkButton:hover {
        color: #ffffff;
        background-color: #403a33;
        border-color: #615a52;
    }
    QPushButton#DarkButton:disabled {
        color: #65605b;
        background-color: #292520;
        border-color: #39342f;
    }
    QPushButton#SecondaryButton, QPushButton#DialogButton {
        color: #3c3833;
        background-color: #ffffff;
        border: 1px solid #e5e2de;
    }
    QPushButton#SecondaryButton:hover, QPushButton#DialogButton:hover {
        color: #8f522f;
        background-color: #f9f2ea;
        border-color: #ddb198;
    }
    QPushButton#SecondaryButton:disabled {
        color: #aaa6a2;
        background-color: #f2f1f0;
        border-color: #e8e6e3;
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
        color: #99562f;
        background-color: #f7eee3;
        border: 1px solid #f6d8c6;
        text-align: left;
    }
    QPushButton#LinkButton:hover {
        color: #73472d;
        background-color: #f2e3d2;
    }

    /* Dialogs and inputs */
    QDialog { background-color: #f8f7f5; color: #211d19; }
    QDialog#AppMessageDialog {
        background-color: transparent;
    }
    QFrame#MessageCard {
        background-color: #ffffff;
        border: 1px solid #e8e5e1;
        border-radius: 20px;
    }
    QFrame#MessageCard[variant="danger"] {
        border-color: #f0d7d4;
    }
    QFrame#MessageCard[variant="success"] {
        border-color: #dee7d9;
    }
    QFrame#MessageIcon {
        background-color: #f6ede2;
        border: 1px solid #f5d5c2;
        border-radius: 15px;
    }
    QFrame#MessageIcon[variant="danger"] {
        background-color: #fff0ee;
        border-color: #f5d4d0;
    }
    QFrame#MessageIcon[variant="success"] {
        background-color: #eff6eb;
        border-color: #dae7d3;
    }
    QLabel#MessageIconText {
        color: #99562f;
        font-size: 22px;
        font-weight: 850;
    }
    QLabel#MessageIconText[variant="danger"] {
        color: #c64f4f;
    }
    QLabel#MessageIconText[variant="success"] {
        color: #517a3a;
    }
    QLabel#MessageKicker {
        color: #9c5832;
        font-size: 9px;
        font-weight: 850;
    }
    QLabel#MessageKicker[variant="danger"] {
        color: #b84b4b;
    }
    QLabel#MessageKicker[variant="success"] {
        color: #577c41;
    }
    QLabel#MessageTitle {
        color: #231f1b;
        font-size: 20px;
        font-weight: 780;
    }
    QLabel#MessageText {
        color: #79746e;
        font-size: 11px;
    }
    QFrame#MessageDivider {
        background-color: #f0eeeb;
        border: none;
    }
    QPushButton#MessageClose {
        color: #9b9690;
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 0;
        font-size: 18px;
        font-weight: 500;
    }
    QPushButton#MessageClose:hover {
        color: #34302c;
        background-color: #f2f1ef;
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
        background-color: #9d582f;
        border: 1px solid #9d582f;
    }
    QPushButton#MessagePrimary:hover {
        background-color: #824f31;
        border-color: #824f31;
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
        color: #534f4a;
        background-color: #ffffff;
        border: 1px solid #e5e2de;
    }
    QPushButton#MessageSecondary:hover {
        color: #8a5130;
        background-color: #f8f1e8;
        border-color: #e3bea8;
    }
    QLabel#DialogEyebrow {
        color: #a6582b;
        font-size: 10px;
        font-weight: 800;
    }
    QLabel#DialogTitle {
        color: #1f1c18;
        font-size: 25px;
        font-weight: 780;
    }
    QLabel#DialogSubtitle {
        color: #847e78;
        font-size: 11px;
    }
    QFrame#UpdateSummary {
        background-color: #f6ece0;
        border: 1px solid #f5d3c0;
        border-radius: 12px;
    }
    QLabel#UpdateVersionMuted {
        color: #7e7972;
        font-size: 11px;
        font-weight: 700;
    }
    QLabel#UpdateArrow {
        color: #cd703b;
        font-size: 16px;
        font-weight: 800;
    }
    QLabel#UpdateVersionNew {
        color: #7c4b2e;
        font-size: 12px;
        font-weight: 800;
    }
    QLabel#UpdateHint {
        color: #79746e;
        background-color: #f4f2ef;
        border: 1px solid #e6e4e0;
        border-radius: 9px;
        padding: 10px 12px;
        font-size: 10px;
    }
    QTextBrowser#ReleaseNotes {
        color: #3b3733;
        background-color: #ffffff;
        border: 1px solid #e6e3df;
        border-radius: 10px;
        padding: 10px;
        font-size: 11px;
        selection-background-color: #f5d3c0;
    }
    QLineEdit {
        min-height: 22px;
        color: #2c2824;
        background-color: #ffffff;
        border: 1px solid #e4e2de;
        border-radius: 9px;
        padding: 9px 11px;
        selection-background-color: #f5d3c0;
    }
    QLineEdit:focus { border: 2px solid #bb602c; }
    QTableWidget {
        color: #332f2b;
        background-color: #ffffff;
        alternate-background-color: #fbfbfa;
        border: 1px solid #e6e4e0;
        border-radius: 12px;
        gridline-color: #f1f0ee;
        selection-background-color: #f5e9dc;
        selection-color: #71472e;
    }
    QHeaderView::section {
        color: #807b76;
        background-color: #f7f6f4;
        border: none;
        border-bottom: 1px solid #e8e6e3;
        padding: 10px;
        font-size: 10px;
        font-weight: 750;
    }
    QRadioButton {
        color: #423e3a;
        spacing: 9px;
        padding: 5px;
        font-size: 11px;
    }
    QRadioButton::indicator {
        width: 17px;
        height: 17px;
        border-radius: 9px;
        background-color: #ffffff;
        border: 1px solid #c1bcb7;
    }
    QRadioButton::indicator:checked {
        background-color: #b95a23;
        border: 4px solid #f2e2d1;
    }
    QRadioButton:checked { color: #2b2723; font-weight: 700; }
    QScrollArea { border: none; background-color: transparent; }
    QScrollArea > QWidget > QWidget { background-color: transparent; }
    QScrollBar:vertical { width: 9px; background: transparent; margin: 2px; }
    QScrollBar::handle:vertical {
        min-height: 30px;
        background-color: #cdcac6;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover { background-color: #b0aba7; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    QGroupBox {
        color: #2c2824;
        background-color: #ffffff;
        border: 1px solid #e6e4e0;
        border-radius: 12px;
        margin-top: 18px;
        padding: 20px 14px 14px 14px;
        font-size: 12px;
        font-weight: 750;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        color: #8e522f;
        background-color: #f6ede2;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QMessageBox { background-color: #f9f8f6; }
    QMessageBox QLabel { color: #312d29; min-width: 320px; }
    QMessageBox QPushButton {
        min-width: 90px;
        color: #3c3833;
        background-color: #ffffff;
        border: 1px solid #e5e2de;
    }
    QMessageBox QPushButton:hover {
        color: #8f522f;
        background-color: #f7eee3;
        border-color: #ddb198;
    }
"""


MODERN_LIGHT_OVERRIDES = """
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody,
    QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #f7f6f4;
        color: #1e1b17;
    }
    QWidget#AppRoot { border-color: #e5e2de; }

    QFrame#TitleBar {
        background-color: #ffffff;
        border-bottom: 1px solid #eceae7;
    }
    QFrame#FolderMark {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #a8592b, stop:1 #cf672b);
    }
    QLabel#WindowTitle { color: #282521; }
    QLabel#WindowTitleSeparator { color: #cdcac6; }
    QLabel#WindowCaption { color: #948e88; }
    QPushButton#WindowControl, QPushButton#CloseControl { color: #6f6a65; }
    QPushButton#WindowControl:hover { color: #2d2a26; background-color: #f2f1ef; }

    QFrame#Sidebar {
        background-color: #fbfbfd;
        border-right: 1px solid #eae8e5;
    }
    QLabel#BrandTitle { color: #26231f; }
    QLabel#BrandCaption, QLabel#SidebarSection { color: #a09b95; }
    QPushButton#SidebarButton, QPushButton#SidebarActive, QPushButton#SidebarDanger {
        min-height: 38px;
        border-radius: 9px;
        padding: 0 11px;
    }
    QPushButton#SidebarButton { color: #68635e; background-color: transparent; }
    QPushButton#SidebarButton:hover { color: #473022; background-color: #f8f0e7; }
    QPushButton#SidebarActive {
        color: #834e30;
        background-color: #f6ede1;
        border: 1px solid #f6d7c6;
    }
    QPushButton#SidebarDanger { color: #d45a65; background-color: transparent; }
    QPushButton#SidebarDanger:hover { color: #b9424e; background-color: #fff0f1; }
    QPushButton#SidebarButton:disabled, QPushButton#SidebarDanger:disabled {
        color: #c4c1bd; background-color: transparent;
    }
    QFrame#PreferenceCard {
        background-color: #f3f2f0;
        border: 1px solid #e6e4e1;
        border-radius: 11px;
    }
    QPushButton#PreferenceButton {
        min-height: 30px;
        color: #5f5a55;
        background-color: #ffffff;
        border: 1px solid #e4e2df;
        border-radius: 7px;
        padding: 0 8px;
        text-align: center;
        font-size: 10px;
    }
    QPushButton#PreferenceButton:hover {
        color: #8a5130;
        background-color: #f8f0e8;
        border-color: #f3ccb5;
    }
    QFrame#PrivacyCard {
        background-color: #f5f8f3;
        border: 1px solid #e4ebe0;
        border-radius: 11px;
    }
    QLabel#PrivacyDot { color: #6da150; }
    QLabel#PrivacyTitle { color: #4a633c; }
    QLabel#PrivacyText { color: #7f8c78; }
    QLabel#VersionLabel { color: #a9a4a0; }

    QLabel#PageEyebrow { color: #a7592c; }
    QLabel#PageTitle { color: #211e1a; font-size: 27px; }
    QLabel#PageSubtitle { color: #807b76; }
    QLabel#StatusPill {
        color: #51783a;
        background-color: #f1f6ef;
        border-color: #dee8d9;
    }
    QLabel#StatusPill[state="busy"] {
        color: #844f31; background-color: #f7eee3; border-color: #f5d5c3;
    }
    QLabel#StatusPill[state="warning"] {
        color: #bd4f58; background-color: #fff0f1; border-color: #f5d5d8;
    }

    QFrame#HeroCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7a3f22, stop:0.56 #a8552a, stop:1 #cf7a3f);
        border-radius: 18px;
    }
    QLabel#HeroKicker { color: #f4d2be; }
    QLabel#HeroText { color: #eae1dc; }
    QFrame#HeroMetric {
        background-color: rgba(255, 255, 255, 24);
        border-color: rgba(255, 255, 255, 44);
    }
    QFrame#HeroMetricAccent { background-color: #c4ddb6; }
    QLabel#HeroMetricLabelDark { color: #46583b; }
    QLabel#HeroMetricValueDark { color: #2b3b22; }

    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #ffffff;
        border: 1px solid #e8e6e2;
        border-radius: 15px;
    }
    QLabel#StepBadge { color: #8f5330; background-color: #f7eee3; }
    QFrame#DropZone { background-color: #faf9ff; border-color: #e2ad8e; }
    QFrame#DropZone:hover { background-color: #f9f1e9; border-color: #ad5d2e; }
    QFrame#DropZone[selected="true"] { background-color: #f7eee4; border-color: #ad5d2e; }
    QLabel#DropPath { color: #9d5a33; }
    QFrame#MiniStat, QFrame#OptionRow {
        background-color: #f9f8f6;
        border-color: #eae8e5;
    }
    QLabel#OptionBadge { color: #ba5260; background-color: #fff0f2; }

    QFrame#ActionDock {
        background-color: #ffffff;
        border: 1px solid #e7e5e1;
        border-radius: 15px;
    }
    QLabel#ActionTitle { color: #282521; }
    QLabel#ActionStatus, QLabel#PercentText { color: #95542e; }
    QProgressBar { background-color: #f0eeeb; }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a5582c, stop:1 #89b172);
    }
    QPushButton#PrimaryButton {
        color: #ffffff;
        background-color: #9b572f;
        border: 1px solid #9b572f;
    }
    QPushButton#PrimaryButton:hover { background-color: #844f31; border-color: #844f31; }
    QPushButton#PrimaryButton:pressed { background-color: #70472f; border-color: #70472f; }
    QPushButton#PrimaryButton:disabled {
        color: #aba7a3; background-color: #efeeec; border-color: #e7e5e2;
    }
    QPushButton#DarkButton {
        color: #5d5853;
        background-color: #f9f8f7;
        border: 1px solid #e4e2de;
    }
    QPushButton#DarkButton:hover {
        color: #7c4d32; background-color: #f7eee3; border-color: #f2c9b2;
    }
    QPushButton#DarkButton:disabled {
        color: #bdbab6; background-color: #f7f6f5; border-color: #ecebe9;
    }
"""


DARK_OVERRIDES = """
    QMainWindow, QWidget#AppRoot, QWidget#WindowBody, QScrollArea#MainScroll, QWidget#ScrollContent {
        background-color: #14120f;
        color: #f3f0ed;
    }
    QWidget#AppRoot { border-color: #3f3933; }
    QToolTip { color: #faf9f7; background-color: #2e2a24; border-color: #534c45; }

    QLabel#PageTitle { color: #f8f7f4; }
    QLabel#PageSubtitle { color: #bab4ad; }
    QLabel#PageEyebrow { color: #e59262; }
    QLabel#StatusPill {
        color: #eaf4e5; background-color: #272f22; border-color: #465b3a;
    }
    QLabel#StatusPill[state="busy"] {
        color: #efba9c; background-color: #2d2720; border-color: #50463b;
    }
    QLabel#StatusPill[state="warning"] {
        color: #ffb4a8; background-color: #3b2524; border-color: #68403b;
    }

    QFrame#Card, QFrame#SourceCard, QFrame#ToolCard {
        background-color: #201d19; border-color: #3a3530;
    }
    QLabel#StepBadge { color: #edb28f; background-color: #342e26; }
    QLabel#CardTitle, QLabel#DropTitle, QLabel#MiniStatValue,
    QLabel#OptionTitle { color: #f4f2ef; }
    QLabel#CardText, QLabel#MutedText, QLabel#MiniStatLabel,
    QLabel#OptionText { color: #b2aca5; }
    QFrame#DropZone { background-color: #26231f; border-color: #946b53; }
    QFrame#DropZone:hover { background-color: #2d2823; border-color: #e48a56; }
    QFrame#DropZone[selected="true"] { background-color: #302b24; border-color: #e48a56; }
    QLabel#DropPath { color: #e9a37b; }
    QFrame#MiniStat, QFrame#OptionRow { background-color: #292622; border-color: #3f3a35; }
    QLabel#OptionBadge { color: #ffc0b2; background-color: #432925; }

    QPushButton#SecondaryButton, QPushButton#DialogButton,
    QPushButton#GhostDanger, QPushButton#MessageSecondary {
        color: #e9e7e3; background-color: #2d2925; border-color: #4d4741;
    }
    QPushButton#SecondaryButton:hover, QPushButton#DialogButton:hover,
    QPushButton#MessageSecondary:hover {
        color: #ffffff; background-color: #342e27; border-color: #936b54;
    }
    QPushButton#SecondaryButton:disabled {
        color: #726d67; background-color: #23201c; border-color: #34302c;
    }
    QPushButton#GhostDanger { color: #ffaaa7; border-color: #60403f; }
    QPushButton#GhostDanger:hover { background-color: #3c2527; }
    QPushButton#LinkButton { color: #eeb898; background-color: #342e27; border-color: #4f463d; }
    QPushButton#LinkButton:hover { color: #ffffff; background-color: #3f382f; }

    QDialog, QMessageBox { background-color: #181511; color: #f3f0ed; }
    QDialog#AppMessageDialog { background-color: transparent; }
    QFrame#MessageCard { background-color: #221f1b; border-color: #413c37; }
    QFrame#MessageCard[variant="danger"] { border-color: #64403e; }
    QFrame#MessageCard[variant="success"] { border-color: #4b5a42; }
    QFrame#MessageIcon { background-color: #342e26; border-color: #50463b; }
    QFrame#MessageIcon[variant="danger"] { background-color: #402625; border-color: #653e3b; }
    QFrame#MessageIcon[variant="success"] { background-color: #2b3427; border-color: #4a5b40; }
    QLabel#MessageIconText, QLabel#MessageKicker, QLabel#DialogEyebrow { color: #eaa780; }
    QLabel#MessageIconText[variant="danger"], QLabel#MessageKicker[variant="danger"] { color: #ffaaa5; }
    QLabel#MessageIconText[variant="success"], QLabel#MessageKicker[variant="success"] { color: #d7eacc; }
    QLabel#MessageTitle, QLabel#DialogTitle { color: #f8f7f4; }
    QLabel#MessageText, QLabel#DialogSubtitle { color: #b8b2ab; }
    QFrame#MessageDivider { background-color: #3d3933; }
    QPushButton#MessageClose { color: #b2aca6; }
    QPushButton#MessageClose:hover { color: #ffffff; background-color: #312d29; }

    QFrame#UpdateSummary { background-color: #2f2a23; border-color: #4e453c; }
    QLabel#UpdateVersionMuted { color: #b6b0aa; }
    QLabel#UpdateArrow { color: #e69667; }
    QLabel#UpdateVersionNew { color: #edb392; }
    QLabel#UpdateHint { color: #c1bcb7; background-color: #272420; border-color: #3f3a35; }
    QTextBrowser#ReleaseNotes, QLineEdit, QTableWidget, QGroupBox {
        color: #e8e6e2; background-color: #221f1b; border-color: #413c37;
    }
    QTextBrowser#ReleaseNotes, QLineEdit, QTableWidget {
        selection-background-color: #584235; selection-color: #ffffff;
    }
    QLineEdit:focus { border: 2px solid #e18048; }
    QTableWidget { alternate-background-color: #282420; gridline-color: #393530; }
    QHeaderView::section {
        color: #c2bdb8; background-color: #2d2925; border-bottom-color: #443f3a;
    }
    QRadioButton { color: #dcd8d4; }
    QRadioButton::indicator { background-color: #2c2824; border-color: #7c766f; }
    QRadioButton::indicator:checked { background-color: #d56e32; border-color: #3c2d25; }
    QRadioButton:checked { color: #ffffff; }
    QScrollBar::handle:vertical { background-color: #5b554f; }
    QScrollBar::handle:vertical:hover { background-color: #77716a; }
    QGroupBox::title { color: #edb08e; background-color: #342e27; }
    QMessageBox QLabel { color: #ece9e6; }
    QMessageBox QPushButton { color: #e9e7e3; background-color: #2d2925; border-color: #4d4741; }
    QMessageBox QPushButton:hover { color: #ffffff; background-color: #342e27; border-color: #936b54; }

    QFrame#TitleBar {
        background-color: #1a1815;
        border-bottom: 1px solid #312d29;
    }
    QLabel#WindowTitle { color: #f4f3f1; }
    QLabel#WindowTitleSeparator { color: #524d48; }
    QLabel#WindowCaption { color: #8f8a84; }
    QPushButton#WindowControl, QPushButton#CloseControl { color: #b1aca7; }
    QPushButton#WindowControl:hover { color: #ffffff; background-color: #312d29; }

    QFrame#Sidebar {
        background-color: #1c1a17;
        border-right: 1px solid #312d29;
    }
    QLabel#BrandTitle { color: #f5f4f2; }
    QLabel#BrandCaption, QLabel#SidebarSection { color: #807a73; }
    QPushButton#SidebarButton { color: #b7b2ad; background-color: transparent; }
    QPushButton#SidebarButton:hover { color: #ffffff; background-color: #2c2824; }
    QPushButton#SidebarActive {
        color: #f4d0bb; background-color: #312b25; border-color: #484038;
    }
    QPushButton#SidebarDanger { color: #f09299; background-color: transparent; }
    QPushButton#SidebarDanger:hover { color: #ffb4ba; background-color: #342326; }
    QPushButton#SidebarButton:disabled, QPushButton#SidebarDanger:disabled {
        color: #5f5a55; background-color: transparent;
    }
    QFrame#PreferenceCard {
        background-color: #272420; border-color: #393530;
    }
    QPushButton#PreferenceButton {
        color: #cfcbc7; background-color: #312d29; border-color: #423d38;
    }
    QPushButton#PreferenceButton:hover {
        color: #ffffff; background-color: #39332c; border-color: #5b5147;
    }
    QFrame#PrivacyCard { background-color: #252a22; border-color: #373f32; }
    QLabel#PrivacyDot { color: #abc99b; }
    QLabel#PrivacyTitle { color: #d6e3cf; }
    QLabel#PrivacyText { color: #8e9a87; }
    QLabel#VersionLabel { color: #716c66; }

    QLabel#StatusPill {
        color: #c2dab5; background-color: #262e22; border-color: #414e3a;
    }
    QFrame#HeroMetricAccent { background-color: #b4cfa4; }
    QFrame#ActionDock { background-color: #221f1b; border-color: #393530; }
    QLabel#ActionTitle { color: #f5f4f2; }
    QLabel#ActionStatus, QLabel#PercentText { color: #d7763e; }
    QProgressBar { background-color: #383430; }
    QPushButton#DarkButton {
        color: #e7e4e2; background-color: #2d2925; border-color: #46413b;
    }
    QPushButton#DarkButton:hover {
        color: #ffffff; background-color: #353029; border-color: #60574c;
    }
    QPushButton#DarkButton:disabled {
        color: #6a6560; background-color: #272320; border-color: #34302c;
    }
    QPushButton#PrimaryButton:disabled {
        color: #726d68; background-color: #312d29; border-color: #393530;
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
