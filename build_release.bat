@echo off
setlocal

set "APP_VERSION=%~1"
if not defined APP_VERSION set "APP_VERSION=1.0.0"

call build.bat --no-pause
if errorlevel 1 exit /b 1

call build_installer.bat %APP_VERSION%
if errorlevel 1 exit /b 1

if not exist "release" mkdir "release"
copy /Y "dist\PADOrganizer.exe" "release\PADOrganizer-portable-v%APP_VERSION%.exe" >nul
if errorlevel 1 exit /b 1

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\New-Checksums.ps1" -Directory "release"
if errorlevel 1 exit /b 1

echo.
echo Hoan tat ban phat hanh v%APP_VERSION%.
echo Cac tep nam trong thu muc release\.
exit /b 0
