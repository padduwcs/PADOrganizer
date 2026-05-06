@echo off
echo ==============================================
echo   CAI DAT VA DONG GOI SMART FILE ORGANIZER
echo ==============================================
echo.

echo [1/2] Cai dat thu vien...
pip install PyQt6 pyinstaller

echo.
echo [2/2] Dang tien hanh dong goi bang PyInstaller...
pyinstaller SmartOrganizer.spec

echo.
echo ==============================================
echo Hoan tat! File thuc thi nam trong thu muc dist/
echo ==============================================
pause
