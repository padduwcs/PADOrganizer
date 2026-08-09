@echo off
setlocal

set "NO_PAUSE="
if /I "%~1"=="--no-pause" set "NO_PAUSE=1"

set "PYTHON_CMD="
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=.venv\Scripts\python.exe"
if not defined PYTHON_CMD if exist "venv\Scripts\python.exe" set "PYTHON_CMD=venv\Scripts\python.exe"
if not defined PYTHON_CMD where py.exe >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD where python.exe >nul 2>nul
if not defined PYTHON_CMD if not errorlevel 1 set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
    echo Khong tim thay Python 3. Hay tao .venv hoac cai Python truoc khi build.
    goto :error
)

echo ==============================================
echo   CAI DAT VA DONG GOI PADORGANIZER
echo ==============================================
echo.

echo [1/2] Cai dat thu vien...
%PYTHON_CMD% -m pip install -r requirements-dev.txt
if errorlevel 1 goto :error

echo.
echo [2/2] Dang tien hanh dong goi bang PyInstaller...
%PYTHON_CMD% -m PyInstaller --clean PADOrganizer.spec
if errorlevel 1 goto :error

echo.
echo ==============================================
echo Hoan tat! File thuc thi nam trong thu muc dist/
echo ==============================================
if not defined NO_PAUSE pause
exit /b 0

:error
echo.
echo Dong goi that bai. Vui long kiem tra loi o tren.
if not defined NO_PAUSE pause
exit /b 1
