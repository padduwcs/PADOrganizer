@echo off
setlocal

echo ==============================================
echo   CAI DAT VA DONG GOI PADORGANIZER
echo ==============================================
echo.

echo [1/2] Cai dat thu vien...
python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [2/2] Dang tien hanh dong goi bang PyInstaller...
python -m PyInstaller --clean PADOrganizer.spec
if errorlevel 1 goto :error

echo.
echo ==============================================
echo Hoan tat! File thuc thi nam trong thu muc dist/
echo ==============================================
pause
exit /b 0

:error
echo.
echo Dong goi that bai. Vui long kiem tra loi o tren.
pause
exit /b 1
