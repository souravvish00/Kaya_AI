@echo off
setlocal

set "ROOT=%~dp0"
set "FRONTEND=%ROOT%frontend"

title KAYA Launcher
echo.   
echo ==============================
echo Starting KAYA local workspace
echo ==============================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11+ and try again.
  pause
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo npm was not found. Install Node.js LTS and try again.
  pause
  exit /b 1
)

cd /d "%ROOT%"
echo Running the one-command KAYA launcher...
npm run kaya

echo.
echo KAYA stopped. Press any key to close this window.
pause
