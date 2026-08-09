@echo off
setlocal

set "APP_VERSION=%~1"
if not defined APP_VERSION set "APP_VERSION=1.0.0"

if not exist "dist\PADOrganizer.exe" (
    echo Khong tim thay dist\PADOrganizer.exe.
    echo Hay chay build.bat truoc khi tao installer.
    exit /b 1
)

set "ISCC_EXE="
where ISCC.exe >nul 2>nul
if not errorlevel 1 set "ISCC_EXE=ISCC.exe"

if not defined ISCC_EXE if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_EXE=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_EXE=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE if exist "%LocalAppData%\Programs\Inno Setup 6\ISCC.exe" set "ISCC_EXE=%LocalAppData%\Programs\Inno Setup 6\ISCC.exe"

if not defined ISCC_EXE (
    echo Khong tim thay Inno Setup 6.
    echo Tai tai https://jrsoftware.org/isdl.php roi chay lai script nay.
    exit /b 1
)

echo Dang tao PADOrganizer Installer v%APP_VERSION%...
"%ISCC_EXE%" /DMyAppVersion=%APP_VERSION% "installer\PADOrganizer.iss"
if errorlevel 1 exit /b 1

echo Installer da duoc tao trong thu muc release\.
exit /b 0
