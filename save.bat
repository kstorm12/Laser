@echo off
rem Double-click to commit everything new on this PC (job files, photos) and push to GitHub.
rem Pulls first so Omarchy's edits come down before yours go up.
cd /d "%~dp0"
git pull --ff-only || goto fail
git status --short
echo.
set "msg="
set /p msg=What changed (blank cancels): 
if "%msg%"=="" (echo Cancelled. & pause & exit /b 0)
git add -A || goto fail
git commit -m "Laser PC: %msg%" || goto fail
git push || goto fail
echo.
echo Saved and pushed.
pause
exit /b 0
:fail
echo.
echo Save FAILED. See "If update fails" in windows-pc.md.
pause
exit /b 1
