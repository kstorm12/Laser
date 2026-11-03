@echo off
rem Double-click to pull the latest settings and job files from GitHub.
rem Fast-forward only: refuses to merge if this PC has unsaved commits (see windows-pc.md).
cd /d "%~dp0"
git pull --ff-only
if errorlevel 1 (
  echo.
  echo Update FAILED. See "If update fails" in windows-pc.md.
  pause
  exit /b 1
)
echo.
echo Up to date.
pause
